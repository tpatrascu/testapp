import json
import os
import tempfile

import pytest

import time_machine
import datetime

from core import app
from models import db

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

    os.close(db_fd)
    os.unlink(db_path)

def test_get_missing_username(client):
    rv = client.get('/hello/missinguser')
    assert rv.status == '404 NOT FOUND'

def test_put_invalid_username_number(client):
    rv = client.put('/hello/myuser1', json={
        "dateOfBirth": "1970-12-02"
    })
    assert rv.status == '400 BAD REQUEST'
    assert b'Invalid username format' in rv.data

def test_put_invalid_username_symbol(client):
    rv = client.put('/hello/what@', json={
        "dateOfBirth": "1970-12-02"
    })
    assert rv.status == '400 BAD REQUEST'

def test_put_and_get_user(client):
    with time_machine.travel(datetime.date(2020, 1, 10)):
        rv = client.put('/hello/myuser', json={
            "dateOfBirth": "1990-1-20"
        })
        assert rv.status == '204 NO CONTENT'
        rv = client.get('/hello/myuser')
        assert rv.status == '200 OK'
        assert b'Hello, myuser! Your birthday is in 10 day(s)' in rv.data

def test_get_user_birthday(client):
    with time_machine.travel(datetime.date(2020, 1, 10)):
        rv = client.put('/hello/bdayusr', json={
            "dateOfBirth": "1980-1-10"
        })
        assert rv.status == '204 NO CONTENT'
        rv = client.get('/hello/bdayusr')
        assert rv.status == '200 OK'
        assert b'Hello, bdayusr! Happy birthday!' in rv.data

def test_put_update_user(client):
    with time_machine.travel(datetime.date(2020, 1, 10)):
        rv = client.put('/hello/yetanotheruser', json={
            "dateOfBirth": "1990-1-20"
        })
        assert rv.status == '204 NO CONTENT'
        rv = client.put('/hello/yetanotheruser', json={
            "dateOfBirth": "1990-1-21"
        })
        rv = client.get('/hello/yetanotheruser')
        assert rv.status == '200 OK'
        assert b'Hello, yetanotheruser! Your birthday is in 11 day(s)' in rv.data

def test_days_until_birtyday_computation(client):
    with time_machine.travel(datetime.date(2020, 1, 10)):
        rv = client.put('/hello/thisyear', json={
            "dateOfBirth": "1990-4-20"
        })
        assert rv.status == '204 NO CONTENT'
        rv = client.get('/hello/thisyear')
        assert rv.status == '200 OK'
        assert b'Hello, thisyear! Your birthday is in 101 day(s)' in rv.data

        rv = client.put('/hello/nextyear', json={
            "dateOfBirth": "1990-1-9"
        })
        assert rv.status == '204 NO CONTENT'
        rv = client.get('/hello/nextyear')
        assert rv.status == '200 OK'
        assert b'Hello, nextyear! Your birthday is in 365 day(s)' in rv.data

def test_put_invalid_date_future(client):
    with time_machine.travel(datetime.date(2020, 1, 10)):
        rv = client.put('/hello/someuser', json={
            "dateOfBirth": "2020-1-11"
        })
        assert rv.status == '400 BAD REQUEST'
        assert b'Invalid dateOfBirth' in rv.data

def test_put_invalid_date_format(client):
    with time_machine.travel(datetime.date(2020, 1, 10)):
        rv = client.put('/hello/someotheruser', json={
            "dateOfBirth": "1990-13-11"
        })
        assert rv.status == '400 BAD REQUEST'
        assert b'Invalid message format' in rv.data

def test_put_invalid_date_key(client):
    with time_machine.travel(datetime.date(2020, 1, 10)):
        rv = client.put('/hello/someyetanoterotheruser', json={
            "dateOfBirthxxx": "1990-12-11"
        })
        assert rv.status == '400 BAD REQUEST'
        assert b'Invalid message format' in rv.data
        