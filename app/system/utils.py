from sqlalchemy.exc import IntegrityError
from flask import current_app as app

from lib.factory import db

from .models import DeviceHealth, DeviceHealthException
from . import constants as COMMANDS


def save_device_health(**kwargs):
    instance = DeviceHealth(**kwargs)

    db.session.add(instance)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise DeviceHealthException('IntegrityError')
    return instance


def save_command(command, device_ids):
    """
    Save command for device_ids on redis storage
    """
    for i in device_ids:
        app.cache.storage.rpush(COMMANDS.REDIS_KEY + COMMANDS.REDIS_KEY_DELIMITER + f'{i}', command)
    return 'ok'


def get_commands(device_id):
    """
    Get commands from redis storage
    """
    commands = [command for command in app.cache.storage.lrange(COMMANDS.REDIS_KEY +
                                                                COMMANDS.REDIS_KEY_DELIMITER + f'{device_id}', 0, -1)]
    app.cache.storage.delete(f'{COMMANDS.REDIS_KEY}{COMMANDS.REDIS_KEY_DELIMITER}{device_id}')
    return commands