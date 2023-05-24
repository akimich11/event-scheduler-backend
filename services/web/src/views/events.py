import json
from flask import Blueprint, Response, request
from jsonschema.exceptions import ValidationError

from .utils import (
    create_event,
    get_events,
    update_event,
    delete_event,
)
from ..errors.object_not_found_error import ObjectNotFoundError
from ..decorators import check_content_type

events_api = Blueprint('events', __name__)


@events_api.route("/")
def hello_world():
    return f'This is the API root'


@events_api.route('/events', methods=['GET', 'POST', 'PATCH', 'DELETE'])
@check_content_type
def handle_event():
    body = request.json
    try:
        if request.method == 'POST':
            events = create_event(body)
        elif request.method == 'GET':
            events = get_events(body)
        elif request.method == 'PATCH':
            events = update_event(body)
        else:
            delete_event(body)
            return Response(status=204, response=None)

    except (ValidationError, ObjectNotFoundError) as err:
        return Response(status=400, response=str(err))
    return Response(status=200, response=json.dumps([event.to_json() for event in events]))
