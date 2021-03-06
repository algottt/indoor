import pytest

from lib.utils import get_random_str

from app.users.constants import ROLE_ADMIN, ROLE_USER
from app.locations.models import City

endpoint = 'locations.add_city_view'


@pytest.mark.parametrize("name", [
    '12345',
    '     ',
    '\n\n\n\n\n',
    '!@#$%^&*',
    get_random_str(255),
    get_random_str(2),
])
def test_default(client, add_user, name):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    resp = client.post(
        endpoint=endpoint,
        data=dict(
            name=name,
        )
    )
    assert 'id' in resp
    city = City.query.get(resp['id'])
    assert city

    assert 'name' in resp
    assert resp['name'] == city.name == name


def test_not_admin_failure(client, add_user):
    _ = add_user(role=ROLE_USER, log_him_in=True)

    resp = client.post(
        endpoint=endpoint,
        data=dict(
            name=get_random_str(),
        ),
        check_status=403
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1


@pytest.mark.parametrize("name", [
    None,
    '',
    get_random_str(1),
    get_random_str(256),
])
def test_malformed_params_failure(client, add_user, name):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    resp = client.post(
        endpoint=endpoint,
        data=dict(
            name=name,
        ),
        check_status=400
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1
