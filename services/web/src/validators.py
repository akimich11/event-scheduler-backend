from datetime import datetime
import jsonschema
from jsonschema.exceptions import ValidationError


def validate_create_event_request_body(request_body: dict) -> None:
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "startDate": {"type": "string"},
            "endDate": {"type": "string"},
            "participants": {"type": "string"},
            "category": {"enum": ["home", "work", "relationships", "education", "health", "sport", "entertainment"]},
            "status": {"enum": [None, "done", "fail"]},
            "repeat": {"enum": [None, "everyday", "weekly", "twice_a_month", "monthly", "yearly"]},
        },
        "required": ["name", "startDate", "category", "participants", "repeat"],
        "additionalProperties": False
    }
    jsonschema.validate(instance=request_body, schema=schema)
    try:
        datetime.fromisoformat(request_body['startDate'])
        if 'endDate' in request_body and request_body['endDate'] is not None:
            datetime.fromisoformat(request_body['endDate'])
    except ValueError as err:
        raise ValidationError(str(err)) from err


def validate_get_events_request_body(request_body: dict) -> None:
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "startDate": {"type": "string"},
            "endDate": {"type": "string"},
        },
        "required": ["name", "startDate"],
        "additionalProperties": False
    }
    jsonschema.validate(instance=request_body, schema=schema)
    try:
        datetime.fromisoformat(request_body['startDate'])
        if 'endDate' in request_body and request_body['endDate'] is not None:
            datetime.fromisoformat(request_body['endDate'])
    except ValueError as err:
        raise ValidationError(str(err)) from err


def validate_update_events_request_body(request_body: dict) -> None:
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "startDate": {"type": "string"},
            "endDate": {"type": "string"},
            "participants": {"type": "string"},
            "category": {"enum": ["home", "work", "relationships", "education", "health", "sport", "entertainment"]},
            "status": {"enum": [None, "done", "fail"]},
            "repeat": {"enum": [None, "everyday", "weekly", "twice_a_month", "monthly", "yearly"]},
        },
        "required": ["name", "startDate"],
        "additionalProperties": False
    }
    jsonschema.validate(instance=request_body, schema=schema)
    try:
        datetime.fromisoformat(request_body['startDate'])
        if 'endDate' in request_body and request_body['endDate'] is not None:
            datetime.fromisoformat(request_body['endDate'])
    except ValueError as err:
        raise ValidationError(str(err)) from err

