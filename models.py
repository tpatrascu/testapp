from core import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import validates
from datetime import date
import re

db = SQLAlchemy(app)
migrate = Migrate(app, db)

def compute_days_until_birthday(birthday: date, today: date) -> int:
    this_year = (date(today.year, birthday.month, birthday.day) - today).days
    if this_year >= 0:
        return this_year
    next_year = (date(today.year+1, birthday.month, birthday.day) - today).days
    return next_year

class User(db.Model):
    __tablename__ = 'app_users'
    username = db.Column(db.String(256), primary_key=True)
    birth_date = db.Column(db.Date(), nullable=False)

    def __init__(self, username, birth_date):
        self.username = username
        self.birth_date = birth_date

    def days_until_birthday(self):
        return compute_days_until_birthday(self.birth_date, date.today())

    @validates('username')
    def validate_username(self, key, value):
        username_validation_regex = re.compile(r"^[a-zA-Z]+$")
        if username_validation_regex.fullmatch(value):
            return value
        raise ValueError(f'Invalid username format: {value}, can only contain letters.')

    @validates('birth_date')
    def validate_birth_date(self, key, value):
        if value.date() < date.today():
            return value
        raise ValueError(f'Invalid dateOfBirth {value}, dateOfBirth must be in the past.')
