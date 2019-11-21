import uuid

from flask import current_app as app
from sqlalchemy.exc import IntegrityError

from lib.factory import db
from lib.utils import hash_password

from .models import User, UserException


def get_user_by_id(user_id):
    return User.query.get(int(user_id))


def create_user(email, password, name, **kwargs):
    password = hash_password(
        salt=app.config['SECRET_KEY'],
        password=password
    )
    user = User(
        email=email,
        password=password,
        name=name,
        **kwargs
    )
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise UserException('Email is already in use')
    return user


def login_user(email, password):
    password = hash_password(
        salt=app.config['SECRET_KEY'],
        password=password
    )
    user = User.query.filter_by(email=email, password=password).first()
    if not user:
        raise UserException('Password or email is incorrect')
    sid = str(uuid.uuid1())
    app.cache.set_user_id(
        user_id=user.id,
        token=sid
    )
    return user, sid
