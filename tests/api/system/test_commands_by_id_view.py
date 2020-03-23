import pytest
from uuid import uuid4

from app.system import constants as COMMANDS
from config import AUTH_TOKEN_HEADER_NAME
from tests.helpers import add_device


endpoint = 'system.commands_view'


@pytest.mark.parametrize("command", [(s[1]) for s in COMMANDS.COMMANDS])
def test_default(client, command_cache, command):
    device = add_device(uid_token=str(uuid4()))
    create = command_cache(command, device.id)
    assert create == 'ok'

    resp = client.get(
        endpoint=endpoint,
        headers={
            AUTH_TOKEN_HEADER_NAME: f'{device.id}:{device.access_token}',
        },
    )
    assert [command] == resp
