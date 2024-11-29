from sqlalchemy.orm import Session

from app.models.User import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: User):
        self.db.add(user)
        return user

    def load_user(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def load_user_with_first_name(self, first_name: str):
        return self.db.query(User).filter(User.first_name == first_name).first()
