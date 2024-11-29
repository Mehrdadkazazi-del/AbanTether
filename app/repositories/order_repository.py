from sqlalchemy.orm import Session

from app.exception.exception_handler import OrderNotFoundException
from app.models.Order import Order


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, order: Order):
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def update_order(self, order: Order):
        existing_order = self.db.query(Order).filter(Order.id == order.id).first()

        if existing_order is None:
            raise OrderNotFoundException()

        existing_order.id = order.id
        existing_order.crypto_name = order.crypto_name
        existing_order.amount = order.amount
        existing_order.total_price = order.total_price
        existing_order.is_settled = order.is_settled
        self.db.commit()
        self.db.refresh(existing_order)

        return existing_order

    def load_order(self, order_id: int):
        return self.db.query(Order).filter(Order.id == order_id).first()
