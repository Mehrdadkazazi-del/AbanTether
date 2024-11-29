from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.utils.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String)
    national_code = Column(String, unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    accounts = relationship("Account", backref='user')
    orders = relationship("Order", backref='user_order')
