import logging
import os

logging.basicConfig(
    level=logging.WARN,
    format='%(asctime)s | %(name)s > %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S'
)


logger = logging.getLogger('indoor')
logger.setLevel(os.environ.get('LOG_LEVEL', logging.DEBUG))
