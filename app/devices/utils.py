from datetime import datetime
from sqlalchemy.exc import IntegrityError

from lib.factory import db
from lib.utils import setattrs

from .models import Device, Contact, ContactException


def save_device(instance=None, **kwargs):
    """
    Creates or updates existing device
    :param instance: Instance of device to update
    :param kwargs:
    :return: Device
    """
    if instance:
        setattrs(instance, **kwargs, updated_at=datetime.utcnow(), ignore_nulls=True)
    else:
        instance = Device(**kwargs)

    db.session.add(instance)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        if 'uid_token' in kwargs:
            device = Device.query.filter_by(uid_token=kwargs['uid_token']).one_or_none()
            if device:
                return save_device(device, **kwargs)
        raise
    return instance


def save_contact(instance=None, **kwargs):
    """
    Creates or updates contact
    :param instance: Instance of contact to update
    :param kwargs:
    :return: Contact
    """
    if instance:
        setattrs(instance, **kwargs, updated_at=datetime.utcnow(), ignore_nulls=True)
    else:
        instance = Contact(**kwargs)

    db.session.add(instance)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ContactException('Duplicate contact')
    return instance


def check_token(token):
    return bool(token)


def get_device_by_token(token):
    device_id, token = token.split(':')
    # Add some extra logic here
    return Device.query.get(device_id)
