import pytest

from app.devices.utils import get_device_by_token, save_command, get_command_log_by_id
from app.users.utils import get_user_by_id, save_user
from app.users.constants import ROLE_MANAGER, ROLE_USER

from app.publishers.utils import save_publisher

from app.system.utils import save_device_health

from lib.auth.manager import AuthManager
from lib.factory import create_app, create_db, create_tables, drop_db, init_app
from lib.utils import get_random_str

from .helpers import add_publisher
from .utils import Client, truncate_all_tables

APP_NAME = 'indoor'


@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    test_app = create_app(name=APP_NAME)
    init_app(test_app)
    AuthManager(
        test_app,
        get_user_func=get_user_by_id,
        get_device_func=get_device_by_token)

    dsn = test_app.config['SQLALCHEMY_DATABASE_URI']
    drop_db(dsn)
    test_app.cache.storage.flushall()
    create_db(dsn)

    # Establish an application context before running the tests.
    ctx = test_app.app_context()
    ctx.push()

    create_tables(test_app)  # Only after context was pushed

    # Add test client
    test_app.client = test_app.test_client()

    def teardown():
        ctx.pop()
        test_app.cache.storage.flushall()

    request.addfinalizer(teardown)
    return test_app


@pytest.fixture
def session(app, request):  #noqa
    """Creates a new database session for a test."""
    connection = app.db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    test_session = app.db.create_scoped_session(options=options)

    app.db.session = test_session

    def teardown():
        transaction.rollback()
        connection.close()
        test_session.remove()

    request.addfinalizer(teardown)
    return test_session


@pytest.fixture(scope='function')
def client(app):  #noqa
    yield Client(app=app)
    truncate_all_tables()


@pytest.fixture(scope='function')
def add_user(client):
    def func(name=None, email=None, password=None, role=ROLE_USER, publisher_id=None, log_him_in=False, **kwargs):
        name = name or f'User_{get_random_str()}'
        email = email or f'{get_random_str()}@email.com'
        password = password or get_random_str()
        publisher_id = publisher_id or add_publisher().id if role == ROLE_MANAGER else None

        user = save_user(
            name=name,
            email=email,
            password=password,
            role=role,
            publisher_id=publisher_id,
            **kwargs
        )

        if log_him_in:
            client.post(
                endpoint='users.login_user_view',
                data=dict(
                    email=email,
                    password=password
                )
            )

        return user
    return func


@pytest.fixture(scope='function')
def login(app, client):
    def func(email, password):
        _ = client.post(
            endpoint='users.login_user_view',
            data=dict(
                email=email,
                password=password
            )
        )
        cookie = client.get_cookies(key=app.config['AUTH_COOKIE_NAME'])
        return cookie.value  # SID
    return func


@pytest.fixture(scope='function')
def command_cache():
    def creator(command, device_id):
        resp = save_command(
            command=command,
            device_ids=[device_id],
        )
        return resp
    return creator


@pytest.fixture(scope='function')
def get_command_record():
    def func(device_id):
        return get_command_log_by_id(device_id)
    return func
