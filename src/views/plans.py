import json
from datetime import datetime

from flask import Blueprint, Response, request
from flask_login import login_required, current_user
from jsonschema.exceptions import ValidationError

from src.errors.object_not_found_error import ObjectNotFoundError
from src.decorators import check_content_type
from src.validators import validate_event_data_request_body
from src.views import db_adapter

plans = Blueprint('plans', __name__)


@plans.route('/events', methods=['POST'])
@check_content_type
@login_required
def create_event():
    body = request.json
    try:
        validate_event_data_request_body(body)
        start_date = datetime.fromisoformat(body['startDate'])
        end_date = datetime.fromisoformat(body['endDate']) if 'endDate' in body else None
        plan = db_adapter.create_plan(user_id=current_user.get_id(),
                                      name=body['name'],
                                      start_date=start_date,
                                      end_date=end_date,
                                      repeat_interval=body['repeat'],
                                      category_name=body['category'],
                                      participants=body['participants'])
    except (ValidationError, ObjectNotFoundError) as err:
        return Response(status=400, response=str(err))
    return Response(status=200, response=json.dumps(plan.to_json()))
