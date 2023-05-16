from flask import Blueprint, redirect, url_for, Response, request
from flask_login import login_required, logout_user, current_user

from src.decorators import check_content_type
from src.views import login_manager, db_adapter

auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    return db_adapter.get_user(int(user_id))


@auth.route('/login', methods=['POST'])
@check_content_type
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if db_adapter.login_user(username, password):
        user_id = current_user.get_id()
        return Response(status=200, response=f'Successful login! User ID: {user_id}')
    else:
        return Response(status=400, response='Invalid credentials. Please try again.')


@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('root'))
