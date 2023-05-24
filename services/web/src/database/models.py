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


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True)
    password = Column(String(128))

    def get_id(self):
        return str(self.id)


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    date = Column(DateTime(timezone=True))
    participants = Column(String(255))
    user_id = Column(Integer, ForeignKey("user.id"))
    category_id = Column(Integer, ForeignKey("category.id"))
    status_id = Column(Integer, ForeignKey("status.id"))
    repeat_interval_id = Column(Integer, ForeignKey("repeat_interval.id"))

    user = relationship("User", foreign_keys="Event.user_id", backref="events")
    category = relationship("Category", foreign_keys="Event.category_id", backref="events")
    status = relationship("Status", foreign_keys="Event.status_id", backref="events")
    repeat_interval = relationship("RepeatInterval", foreign_keys="Event.repeat_interval_id", backref="events")

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date.isoformat(),
            'category': self.category.name,
            'participants': self.participants,
            'status': self.status.name if self.status else None
        }


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
