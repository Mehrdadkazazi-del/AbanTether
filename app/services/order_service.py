import json
import logging

from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.common.OrderStatus import OrderStatus
from app.config.app_settings import LIMIT_FOR_EXCHANGE, JOBS_ENABLED
from app.exception.exception_handler import UserNotFoundException, InsufficientBalanceException
from app.models.Order import Order
from app.repositories.account_repository import AccountRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.user_repository import UserRepository
from app.utils import redis_connection
from app.utils.db_connection import DataBaseConnection
from app.vo.order_vo import order_vo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OrderService:
    def __init__(self, db: Session):
        self.db = db
        self.account_repository = AccountRepository(db)
        self.user_repository = UserRepository(db)
        self.order_repository = OrderRepository(db)

    def create_order(self, user_id: int, crypto_name: str, amount: float, price_per_unit: float) -> Order:
        try:
            user = self.user_repository.load_user(user_id)
            if not user:
                raise UserNotFoundException()

            total_price = amount * price_per_unit
            user_account = user.accounts[0]
            total_amount = float(user_account.total_amount)

            if total_amount < total_price:
                raise InsufficientBalanceException()

            total_amount -= total_price
            self.account_repository.update_user_account(user_account)

            order = Order(
                user_id=user_id,
                crypto_name=crypto_name,
                amount=amount,
                total_price=total_price,
                is_settled=OrderStatus.PENDING.value,
            )
            self.order_repository.create_order(order)
            self.db.commit()
            self.db.refresh(order)

            if total_price >= LIMIT_FOR_EXCHANGE:
                self.buy_from_exchange(order)
                order.is_settled = OrderStatus.SETTLED.value
                self.order_repository.update_order(order)
            else:
                logger.info("Order added to pending batch for later settlement.")
                if JOBS_ENABLED is not True:
                    self.add_to_redis(order)

            return order
        except (SQLAlchemyError, UserNotFoundException, InsufficientBalanceException) as e:
            logger.error(f"Transaction failed: {str(e)}")
            self.db.rollback()
            raise ValueError(f"Error processing the order: {str(e)}")

    def add_to_redis(self, order: Order):
        redis_connection.REDIS.rpush("pending_orders", json.dumps({
            "id": order.id,
            "crypto_name": order.crypto_name,
            "amount": order.amount,
            "total_price": order.total_price,
        }))
        redis_connection.REDIS.incrbyfloat("pending_total_price", order.total_price)

        current_total = float(redis_connection.REDIS.get("pending_total_price") or 0)
        if current_total >= LIMIT_FOR_EXCHANGE:
            self.process_redis_orders()

    def process_redis_orders(self):
        orders = redis_connection.REDIS.lrange("pending_orders", 0, -1)
        redis_connection.REDIS.delete("pending_orders")
        redis_connection.REDIS.delete("pending_total_price")

        batch_orders = [json.loads(order) for order in orders]
        total_amount = sum(order["amount"] for order in batch_orders)

        batch_order_vo = order_vo(
            crypto_name=batch_orders[0]["crypto_name"],
            amount=total_amount
        )
        self.buy_from_exchange(batch_order_vo)

        for order in batch_orders:
            db_order = self.order_repository.load_order(order["id"])
            db_order.is_settled = OrderStatus.SETTLED.value
            self.order_repository.update_order(db_order)

        logger.info(f"Processed batch orders with total amount: {total_amount}")

    @staticmethod
    def buy_from_exchange(order: order_vo):
        logger.info(f"Settling order for {order.amount} of {order.crypto_name} with external exchange.")


def get_order_service(db: Session = Depends(DataBaseConnection().get_db)):
    return OrderService(db)
