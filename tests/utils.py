from contextlib import contextmanager
import simplejson as json
import functools
import logging

from flask import url_for
import pytest

from lib.factory import db
from flask_sqlalchemy import Model


logger = logging.getLogger('indoor')


@contextmanager
def not_raises(e=None, msg=None):
    if e is None:
        exception = ClientException
    try:
        yield None
    except exception as ex:
        pytest.fail(msg=msg or 'Raises %s' % ex)


class Client:
    json_header = 'application/json'

    def __init__(self, app):
        self.app = app

    @staticmethod
    def _check_headers(headers, to_check):
        """
        Checks response headers
        :param werkzeug.datastructures.Headers headers:
        :param dict to_check:
        :return:
        """
        assert isinstance(to_check, dict)
        for key, value in to_check.items():
            current_vals = headers.get_all(key)

            # Check if header is NOT presented
            if not value:
                assert not current_vals

            # Check only the presence of the header
            elif value is True:
                assert current_vals

            # Check key's presence and value
            else:
                assert current_vals
                assert any([v == value for v in current_vals])

    def _check_cookies(self, to_check):
        """
        Checks response cookies
        :param dict to_check:
        :return:
        """
        assert isinstance(to_check, dict)
        cookies = self.get_cookies()
        for key, value in to_check.items():
            # Check if cookie is NOT presented
            if not value:
                assert key not in cookies

            # Check only the presence of the header
            elif value is True:
                assert key in cookies

            # Check key's presence and value
            else:
                assert key in cookies
                assert value == cookies[key].value

    def get_cookies(self, key=None):
        """
        Returns cookies as a dict or a certain cookie
        :param str key: cookie name
        :return: dict | Cookie
        """
        cookies = {c.name: c for c in self.app.client.cookie_jar}
        if key:
            return cookies[key]
        return cookies

    def send(self, endpoint, method, data=None, content_type=None, headers=None,
             check_status=200, check_headers=None, check_cookies=None, **values):
        """
        Sends request to server
        :param str endpoint: endpoint name
        :param str method:
        :param dict data:
        :param str content_type:
        :param dict headers:
        :param int check_status:
        :param dict check_headers:
        :param dict check_cookies:
        :param dict values:
        :return:
        """
        url = url_for(endpoint=endpoint, **values)
        func = getattr(self.app.client, method)

        kwargs = {}
        if data:
            kwargs['data'] = data
        if content_type:
            kwargs['content_type'] = content_type
        if headers:
            kwargs['headers'] = headers

        logger.debug('Request %s %s kwargs:%s', method, url, kwargs)
        resp = func(url, **kwargs)

        if check_status:    
            assert resp.status_code == check_status, resp.data

        if check_cookies:
            self._check_cookies(to_check=check_cookies)

        if check_headers:
            self._check_headers(headers=resp.headers, to_check=check_headers)

        data = resp.data
        if resp.content_type == 'application/json':
            data = json.loads(resp.data)

        return data

    def get(self, **kwargs):
        return self.send(method='get', **kwargs)

    def delete(self, **kwargs):
        return self.send(method='delete', **kwargs)

    def post(self, content_type=None, data=None, **kwargs):
        if not content_type or content_type == self.json_header:
            data = json.dumps(data)
        return self.send(method='post', data=data, content_type=content_type, **kwargs)

    def put(self, content_type=None, data=None, **kwargs):
        if not content_type or content_type == self.json_header:
            data = json.dumps(data)
        return self.send(method='put', data=data, content_type=content_type, **kwargs)


class ClientException(Exception):
    pass


def truncate_all_tables():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        logger.info('Clear table %s' % table)
        db.session.execute(table.delete())  # Truncates table
    db.session.commit()


def clear_data(fn):
    @functools.wraps(fn)
    def decorated(*args, **kwargs):
        result = fn(*args, **kwargs)
        truncate_all_tables()
        return result
    return decorated
