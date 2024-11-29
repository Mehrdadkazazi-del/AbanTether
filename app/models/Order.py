from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.common.OrderStatus import OrderStatus
from app.utils.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column('f_user_id', Integer, ForeignKey("users.id"))
    crypto_name = Column(String)
    amount = Column(Float)
    total_price = Column(Float)
    is_settled = Column(String, default=OrderStatus.PENDING.value)
