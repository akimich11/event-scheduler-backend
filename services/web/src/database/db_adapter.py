from datetime import datetime
from typing import Optional

from flask_login import login_user
from sqlalchemy.orm import sessionmaker
from ..database.models import User, Category, RepeatInterval, Event
from ..errors.object_not_found_error import CategoryNotFoundError, IntervalNotFoundError


class DBAdapter:
    def __init__(self, engine):
        Session = sessionmaker(engine)
        self.session = Session()

    def login_user(self, username: str, password: str) -> bool:
        user = self.session.query(User).filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return True
        return False

    def get_user(self, user_id: int) -> User:
        return self.session.query(User).filter_by(id=user_id).first()

    def create_plan(self,
                    user_id: int,
                    name: str,
                    category_name: str,
                    start_date: datetime,
                    end_date: Optional[datetime] = None,
                    repeat_interval: Optional[str] = None,
                    participants: Optional[str] = None) -> Event:
        user = self.get_user(user_id)
        category = self.session.query(Category).filter_by(name=category_name).first()
        if not category:
            raise CategoryNotFoundError(f'Category "{category_name}" was not found in database')
        interval = self.session.query(RepeatInterval).filter_by(name=repeat_interval).first()
        if not interval:
            raise IntervalNotFoundError(f'Repeat interval "{repeat_interval}" was not found in database')

        plan = Event(name=name,
                     user=user,
                     category=category,
                     repeat_interval=interval,
                     participants=participants)
        self.session.add_all(plan)
        self.session.commit()
        return plan
