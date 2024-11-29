import random

from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.Account import Account
from app.models.User import User
from app.repositories.user_repository import UserRepository
from app.utils.db_connection import DataBaseConnection
from app.utils.hash import Hash


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def create_user_service(self, first_name: str, last_name: str, national_code: str, password: str):
        try:
            with self.db.begin():
                new_user = User(
                    first_name=first_name,
                    last_name=last_name,
                    national_code=national_code,
                    password=Hash.bcrypt(password),
                )
                new_account = Account(
                    account_number=self.generateAccountNumber(national_code),
                    total_amount=5000
                )
                new_user.accounts.append(new_account)

                user_object = self.user_repository.create_user(new_user)
                self.db.commit()
                return user_object
        except SQLAlchemyError as e:
            self.db.rollback()
            raise ValueError(f"Transaction failed: {str(e)}")

    @staticmethod
    def generateAccountNumber(national_code):
        return national_code + "." + str(random.randrange(100, 999))

    def load_user_with_first_name(self, first_name):
        return self.user_repository.load_user_with_first_name(first_name)

    def load_user_by_id(self, user_id):
        return self.user_repository.load_user(user_id)


def get_user_service(db: Session = Depends(DataBaseConnection().get_db)):
    return UserService(db)
