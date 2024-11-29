from typing import Type

from sqlalchemy.orm import Session

from app.models.Currency import Currency


def get_currencies(db: Session) -> list[Type[Currency]]:
    return db.query(Currency).all()
