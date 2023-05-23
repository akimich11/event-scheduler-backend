import functools
from flask import request, Response


def check_content_type(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        if request.headers.get('Content-Type') == 'application/json':
            return func(*args, **kwargs)
        return Response(status=400, response='Send request with Content-Type=application/json to login')
    return wrapped
