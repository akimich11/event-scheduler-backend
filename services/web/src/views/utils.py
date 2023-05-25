from datetime import datetime

from src import db_adapter
from src.validators import (
    validate_get_events_request_body,
    validate_create_event_request_body,
    validate_update_events_request_body,
)


def create_event(body):
    validate_create_event_request_body(body)
    return db_adapter.create_event(user_id=1,
                                   name=body['name'],
                                   start_date=datetime.fromisoformat(body['startDate']),
                                   end_date=datetime.fromisoformat(
                                       body['endDate']) if 'endDate' in body else None,
                                   repeat_interval=body['repeat'],
                                   category_name=body['category'],
                                   participants=body['participants'])


def get_events(body):
    validate_get_events_request_body(body)
    end_date = None
    if 'endDate' in body and body['endDate'] is not None:
        end_date = datetime.fromisoformat(body['endDate'])
    return db_adapter.get_events(user_id=1,
                                 event_name=body['name'],
                                 start_date=datetime.fromisoformat(body['startDate']),
                                 end_date=end_date)


def update_event(body):
    validate_update_events_request_body(body)
    return db_adapter.update_event(user_id=1,
                                   event_name=body['name'],
                                   start_date=datetime.fromisoformat(body['startDate']),
                                   end_date=datetime.fromisoformat(
                                       body['endDate']) if 'endDate' in body else None,
                                   new_data=body)


def delete_event(body):
    validate_get_events_request_body(body)
    db_adapter.delete_events(user_id=1,
                             event_name=body['name'],
                             start_date=datetime.fromisoformat(body['startDate']),
                             end_date=datetime.fromisoformat(
                                 body['endDate']) if 'endDate' in body else None)
