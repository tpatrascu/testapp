from core import app
from markupsafe import escape
from http import HTTPStatus
from flask import abort, request
from flask.wrappers import Response
from datetime import datetime

from models import db
from models import User


@app.route("/hello/<username>", methods=['GET'])
def get_username(username):
    sanitized_username=escape(username)
    user = User.query.filter_by(username=sanitized_username).first()

    if user is None:
        abort(404)

    if user.days_until_birthday() == 0:
        return {
            "message": f"Hello, {user.username}! Happy birthday!"
        }

    return {
        "message": f"Hello, {user.username}! Your birthday is in {user.days_until_birthday()} day(s)"
    }


@app.route("/hello/<username>", methods=['PUT'])
def put_username(username):
    sanitized_username=escape(username)
    request_data = request.get_json()

    try:
        birth_date_str = request_data['dateOfBirth']
        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
    except (KeyError, ValueError):
        abort(400, 'Invalid message format')

    user = User.query.filter_by(username=sanitized_username).first()

    try:
        if user is None:
            newuser = User(sanitized_username, birth_date)
            db.session.add(newuser)
            db.session.commit()
        else:
            user.birth_date = birth_date
            db.session.commit()
    except ValueError as e:
        abort(400, f'Invalid value: {str(e)}')

    return Response(status=HTTPStatus(204))


@app.route("/health", methods=['GET'])
def health():
    try:
        db.engine.execute('SELECT 1')
    except:
        abort(500, "FAILED: Database connection failed")
    
    return Response(response="OK", status=HTTPStatus(200))

@app.route("/liveness", methods=['GET'])
def liveness():
    return Response(response="OK", status=HTTPStatus(200))
