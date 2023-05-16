from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
)


Base = declarative_base()


class User(UserMixin, Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True)
    password = Column(String(128))

    def get_id(self):
        return str(self.id)


class Plan(Base):
    __tablename__ = "plan"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    participants = Column(String(255))
    user_id = Column(Integer, ForeignKey("user.id"))
    category_id = Column(Integer, ForeignKey("category.id"))
    status_id = Column(Integer, ForeignKey("status.id"))
    repeat_interval_id = Column(Integer, ForeignKey("repeat_interval.id"))

    user = relationship("User", foreign_keys="Plan.user_id", backref="plans")
    category = relationship("Category", foreign_keys="Plan.category_id", backref="plans")
    status = relationship("Status", foreign_keys="Plan.status_id", backref="plans")
    repeat_interval = relationship("RepeatInterval", foreign_keys="Plan.repeat_interval_id", backref="plans")

    def to_json(self) -> dict:
        intervals = [event.to_interval() for event in self.events]
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category.name,
            'participants': self.participants,
            'status': self.status.name if self.status else None,
            'intervals': intervals
        }


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    plan_id = Column(Integer, ForeignKey("plan.id"))

    plan = relationship("Plan", foreign_keys="Event.plan_id", backref="events")

    def to_interval(self) -> dict:
        return [
            self.start_date.astimezone().isoformat(),
            self.end_date.astimezone().isoformat() if self.end_date else None
        ]


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))


class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))


class RepeatInterval(Base):
    __tablename__ = "repeat_interval"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
