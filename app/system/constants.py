WINDOWS = 'windows'
LINUX = 'linux'
OS = (
    WINDOWS,
    LINUX,
)

REDIS_KEY = 'commands'
REDIS_KEY_DELIMITER = '/'

SHOW_INFO = 'info'
RESTART = 'restart'
RESTART_DEVICE = 'restart_device'
SEND_LOGS = 'logs'

COMMANDS = (
    ('Показать информацию', SHOW_INFO),
    ('Перезагрузить программу', RESTART),
    ('Перезапустить устройство', RESTART_DEVICE),
    ('Отправить логи', SEND_LOGS),
)
