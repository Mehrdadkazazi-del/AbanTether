from sqlalchemy import Column, Integer, String

from app.utils.database import Base


class Currency(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    code = Column(String)
