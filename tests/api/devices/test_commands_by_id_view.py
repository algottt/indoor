import pytest

from app.devices import constants as DEVICE

from random import randint

device_id = randint(0, 100)
command = DEVICE.COMMANDS[0][1]

endpoint = 'devices.commands_by_id_view'


@pytest.mark.parametrize("command, device_id", [(command, device_id)])
def test_default(client, command_cache, command, device_id):
    create = command_cache(command, device_id)
    assert create == 'ok'

    resp = client.get(
        endpoint=endpoint,
        device_id=device_id,
    )
    assert [command] == resp
