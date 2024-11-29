from sqlalchemy import Column, Integer, String, ForeignKey

from app.utils.database import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, index=True)
    total_amount = Column(Integer)
    user_id = Column('f_user_id', Integer, ForeignKey("users.id"))
