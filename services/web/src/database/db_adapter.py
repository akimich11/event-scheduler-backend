from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import Optional

from flask_login import login_user
from sqlalchemy.orm import sessionmaker
from ..database.models import User, Category, RepeatInterval, Event, Status
from ..errors.object_not_found_error import CategoryNotFoundError, IntervalNotFoundError, StatusNotFoundError


class DBAdapter:
    def __init__(self, engine):
        Session = sessionmaker(engine)
        self.session = Session()

    def create_default_data(self):
        admin = User(username="admin", password="password")
        repeats = [RepeatInterval(name=key) for key in
                   (None, "everyday", "weekly", "twice_a_month", "monthly", "yearly")]
        categories = [Category(name=key) for key in
                      ("home", "work", "relationships", "education", "health", "sport", "entertainment")]
        statuses = [Status(name=key) for key in
                    (None, "done", "fail")]
        self.session.add_all([admin] + repeats + categories + statuses)
        self.session.commit()

    def login_user(self, username: str, password: str) -> bool:
        user = self.session.query(User).filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return True
        return False

    def get_user(self, user_id: int) -> User:
        return self.session.query(User).filter_by(id=user_id).first()

    def create_event(self,
                     user_id: int,
                     name: str,
                     category_name: str,
                     start_date: datetime,
                     end_date: datetime,
                     repeat_interval: Optional[str] = None,
                     participants: Optional[str] = None) -> Event:
        user = self.get_user(user_id)
        category = self.session.query(Category).filter_by(name=category_name).first()
        if not category:
            raise CategoryNotFoundError(f'Category "{category_name}" was not found in database')
        interval = self.session.query(RepeatInterval).filter_by(name=repeat_interval).first()
        if not interval:
            raise IntervalNotFoundError(f'Repeat interval "{repeat_interval}" was not found in database')

        events = []
        current_datetime = start_date
        while current_datetime <= end_date:
            events.append(Event(name=name,
                                user=user,
                                date=start_date,
                                category=category,
                                repeat_interval=interval,
                                participants=participants))
            if interval.name is None:
                break

            elif interval.name == 'everyday':
                current_datetime += timedelta(days=1)
            elif interval.name == 'weekly':
                current_datetime += timedelta(days=7)
            elif interval.name == 'twice_a_month':
                current_datetime += timedelta(days=14)
            elif interval.name == 'monthly':
                current_datetime += relativedelta(months=+1)
            elif interval.name == 'yearly':
                current_datetime += relativedelta(years=+1)

        self.session.add_all(events)
        self.session.commit()
        return events

    def get_events(self,
                   user_id: int,
                   event_name: str,
                   start_date: Optional[datetime] = None,
                   end_date: Optional[datetime] = None) -> list[dict]:
        user = self.get_user(user_id)
        events = self.session.query(Event).filter(
            Event.user == user,
            Event.name == event_name,
            Event.start_date >= start_date,
            Event.end_date <= end_date
        ).all()

        return events

    def delete_events(self, user_id: int,
                      event_name: str,
                      start_date: Optional[datetime] = None,
                      end_date: Optional[datetime] = None) -> None:
        events = self.get_events(user_id, event_name, start_date, end_date)
        for event in events:
            self.session.delete(event)
        self.session.commit()

    def _update_dates(self, events: list[Event], start_date: datetime, end_date: datetime) -> None:
        for event in events:
            if event.date < start_date or (end_date is not None and event.date > end_date):
                self.session.delete(event)
        self.session.commit()

    def update_event(self,
                     user_id: int,
                     event_name: str,
                     new_data: dict,
                     start_date: Optional[datetime] = None,
                     end_date: Optional[datetime] = None,
                     ) -> list[dict]:
        events = self.get_events(user_id, event_name, start_date, end_date)
        for event in events:
            if 'status' in new_data:
                status = self.session.query(Status).filter_by(name=new_data['status']).first()
                if not status:
                    raise StatusNotFoundError(f'Status "{new_data["status"]}" was not found in database')
                event.status = status
            if 'category' in new_data:
                category = self.session.query(Category).filter_by(name=new_data["category"]).first()
                if not category:
                    raise CategoryNotFoundError(f'Category "{new_data["category"]}" was not found in database')
                event.category = category
            if 'interval' in new_data:
                interval = self.session.query(RepeatInterval).filter_by(name=new_data["interval"]).first()
                if not interval:
                    raise IntervalNotFoundError(f'Repeat interval "{new_data["interval"]}" was not found in database')
                event.repeat_interval = interval
            if 'participants' in new_data:
                event.participants = new_data['participants']

        self.session.commit()
        if 'start_date' in new_data:
            start_date = new_data['start_date']
        if 'end_date' in new_data:
            end_date = new_data['end_date']
        self._update_dates(events, start_date, end_date)
        return self.get_events(user_id, event_name, start_date, end_date)
