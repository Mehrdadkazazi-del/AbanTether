from sqlalchemy.orm import Session

from app.models.Account import Account
from app.repositories import account_repository


class AccountService:
    def __init__(self, db: Session):
        self.db = db

    def create_account_service(self, db: Session, account_number: int):
        new_account = Account(account_number=account_number)
        return account_repository.create_account(db, new_account)
