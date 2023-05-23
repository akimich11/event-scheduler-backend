import json
from datetime import datetime

from flask import Blueprint, Response, request
from jsonschema.exceptions import ValidationError

from .. import db_adapter
from ..errors.object_not_found_error import ObjectNotFoundError
from ..decorators import check_content_type
from ..validators import validate_event_data_request_body


events = Blueprint('events', __name__)


@events.route("/")
def hello_world():
    return f'This is the API root'


@events.route('/events', methods=['POST'])
@check_content_type
def create_event():
    body = request.json
    try:
        validate_event_data_request_body(body)
        start_date = datetime.fromisoformat(body['startDate'])
        end_date = datetime.fromisoformat(body['endDate']) if 'endDate' in body else None
        plan = db_adapter.create_plan(user_id=body['user_id'],
                                      name=body['name'],
                                      start_date=start_date,
                                      end_date=end_date,
                                      repeat_interval=body['repeat'],
                                      category_name=body['category'],
                                      participants=body['participants'])
    except (ValidationError, ObjectNotFoundError) as err:
        return Response(status=400, response=str(err))
    return Response(status=200, response=json.dumps(plan.to_json()))


@events.route('/events', methods=['GET'])
def get_events():
    body = request.json
    try:
        start_date = datetime.fromisoformat(request.args['startDate']) if 'startDate' in request.args else None
        end_date = datetime.fromisoformat(request.args['endDate']) if 'endDate' in request.args else None
        plan = db_adapter.create_plan(user_id=body['user_id'],
                                      name=body['name'],
                                      start_date=start_date,
                                      end_date=end_date,
                                      repeat_interval=body['repeat'],
                                      category_name=body['category'],
                                      participants=body['participants'])
    except (ValidationError, ObjectNotFoundError) as err:
        return Response(status=400, response=str(err))
    return Response(status=200, response=json.dumps(plan.to_json()))
