from app.repositories import currency_repository
from app.utils.database import SessionLocal

currency_code_dict = {}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def load_currencies():
    db_session = next(get_db())
    currencies = currency_repository.get_currencies(db_session)

    for currency in currencies:
        currency_code_dict[currency.id] = {
            "name": currency.name,
            "description": currency.description,
            "code": currency.code
        }

    db_session.close()
