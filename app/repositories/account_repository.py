from sqlalchemy.orm import Session

from app.exception.exception_handler import AccountNotFoundException
from app.models.Account import Account


class AccountRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_account(self, account: Account):
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def update_user_account(self, user_account: Account):
        existing_account = self.db.query(Account).filter(Account.id == user_account.id).first()

        if existing_account is None:
            raise AccountNotFoundException()

        existing_account.id = user_account.id
        existing_account.account_number = user_account.account_number
        existing_account.total_amount = user_account.total_amount
        return existing_account
