import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session

from app.common.OrderStatus import OrderStatus
from app.config.app_settings import CRONE_EXPRESSION, OFFSET, LIMIT, JOBS_ENABLED, LIMIT_FOR_EXCHANGE
from app.models.Order import Order
from app.repositories.order_repository import OrderRepository
from app.services.order_service import OrderService
from app.vo.order_vo import order_vo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BatchJob:
    def __init__(self, db: Session):
        self.db = db
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.process_pending_orders, CronTrigger.from_crontab(CRONE_EXPRESSION))
        self.order_repository = OrderRepository(db)

    def process_pending_orders(self):
        if JOBS_ENABLED is True:
            offset = OFFSET
            limit = LIMIT
            total_amount = 0
            count_of_amount = 0
            while True:
                pending_orders = self.db.query(Order).filter(Order.is_settled == OrderStatus.PENDING.value).offset(offset).limit(limit).all()

                if not pending_orders:
                    break

                total_amount += sum(order.total_price for order in pending_orders)
                count_of_amount += sum(order.amount for order in pending_orders)

                order = pending_orders[0]

                if total_amount >= LIMIT_FOR_EXCHANGE:
                    order_vo.crypto_name = order.crypto_name
                    order_vo.amount = count_of_amount

                    OrderService.buy_from_exchange(order_vo)

                    for order in pending_orders:
                        order.is_settled = OrderStatus.SETTLED.value
                        self.order_repository.update_order(order)

                    logger.info(f"Batch of orders settled with total amount: {total_amount}")
                    break

                offset += limit

            logger.info("Total of pending orders is less than 10. Waiting for more orders.")
        else:
            logger.info("JOB NOT ACTIVATED IN BatchJob .....")

    def start(self):
        self.scheduler.start()
        logger.info("Batch job scheduler started.")

    def shutdown(self):
        self.scheduler.shutdown()
        logger.info("Batch job scheduler shut down.")
