from app.utils.database import SessionLocal


class DataBaseConnection:
    def __init__(self):
        self.db_session = SessionLocal()

    def get_db(self):
        try:
            yield self.db_session
        finally:
            self.db_session.close()
