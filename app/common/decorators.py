from lib.auth.decorators import check_auth, check_device_auth

from app.users.constants import ROLE_ADMIN


def admin_required(fn):
    """
    Shortcut decorator checks that user is logged in and his role is admin
    :param fn:
    :return:
    """
    wrapper = check_auth(roles=[ROLE_ADMIN])
    return wrapper(fn)


def auth_required(fn):
    """
    Shortcut function to check if user is logged in
    :param fn:
    :return:
    """
    wrapper = check_auth()
    return wrapper(fn)


def device_auth_required(fn):
    """
    Shortcut function to check if device token is valid
    :param fn:
    :return:
    """
    wrapper = check_device_auth()
    return wrapper(fn)
