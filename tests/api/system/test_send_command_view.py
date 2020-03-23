import pytest

from app.system import constants as COMMANDS

from lib.utils import get_random_str
from random import randint


endpoint = 'system.send_command_view'


@pytest.mark.parametrize("command,device_ids", [
    (COMMANDS.COMMANDS[0][1], [randint(0, 100)],),
    (COMMANDS.COMMANDS[1][1], [randint(0, 100), randint(0, 100), randint(0, 100)],),
])
def test_default(client, get_command_record, command, device_ids):
    resp = client.post(
        endpoint=endpoint,
        data=dict(
            command=command,
            device_ids=device_ids,
        ),
    )
    assert get_command_record(device_ids[0])[0] == command
    assert 'ok' in resp


@pytest.mark.parametrize("command,device_ids", [
    # Malformed command
    (None, [randint(0, 100)],),
    ('', [randint(0, 100)],),
    ('test', [randint(0, 100)],),
    (get_random_str(), [randint(0, 100)],),

    # Malformed device_ids
    (COMMANDS.COMMANDS[0][1], [''],),
    (COMMANDS.COMMANDS[0][1], ['1a'],),
    (COMMANDS.COMMANDS[0][1], ['abc'],),
    (COMMANDS.COMMANDS[0][1], ['1,2,,3'],),
    (COMMANDS.COMMANDS[0][1], [get_random_str()],),
])
def test_malformed_params_failure(client, command, device_ids):
    resp = client.post(
        endpoint=endpoint,
        data=dict(
            command=command,
            device_ids=device_ids,
        ),
        check_status=400,
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1
