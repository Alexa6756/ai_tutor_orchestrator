from src.db import SessionLocal, User
import datetime
from sqlalchemy.exc import NoResultFound

class PostgresStateManager:
    def __init__(self):
        self.db = SessionLocal()

    def get_user(self, user_id: str):
        try:
            user = self.db.query(User).filter(User.user_id == user_id).one()
            return user.user_info
        except NoResultFound:
            return None

    def upsert_user(self, user_info: dict):
        user_id = user_info.get("user_id")
        existing = self.db.query(User).filter(User.user_id == user_id).first()
        if existing:
            existing.user_info = user_info
            existing.last_interaction = datetime.datetime.utcnow()
        else:
            new_user = User(user_id=user_id, user_info=user_info, conversation_history=[])
            self.db.add(new_user)
        self.db.commit()
