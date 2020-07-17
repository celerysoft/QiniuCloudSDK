# -*-coding:utf-8 -*-
import base64
import hashlib
import hmac
import json
from urllib.parse import urlparse

import requests
from qiniu import QiniuMacAuth
from requests.adapters import HTTPAdapter
from urllib3 import Retry

import configs


class BaseSDK(object):
    _ACCESS_KEY = configs.ACCESS_KEY
    _SECRET_KEY = configs.SECRET_KEY

    @staticmethod
    def requests_retry_session(
            retries=3,
            backoff_factor=0.3,
            status_forcelist=(500, 502, 504),
            session=None,
    ):
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session


class BaseQiniuMacSDK(BaseSDK):
    _qiniu_mac_auth = None  # type: QiniuMacAuth

    def __init__(self):
        self._qiniu_mac_auth = QiniuMacAuth(self._ACCESS_KEY, self._SECRET_KEY)

    def __derive_token(self, url: str, method: str,
                       host: str = None, content_type: str = 'application/json', data=None):
        parsed_url = urlparse(url)
        netloc = parsed_url.netloc
        path = parsed_url.path
        query = parsed_url.query

        if not host:
            host = netloc

        sign_data = method.upper() + ' ' + path

        if query is not None and query != '':
            sign_data += '?' + query

        sign_data += '\nHost: ' + host

        if content_type is not None and content_type != '':
            sign_data += '\nContent-Type: ' + content_type

        sign_data += "\n\n"

        if data is not None and content_type is not None and content_type != 'application/octet-stream':
            sign_data += json.dumps(data)

        sign = hmac.new(self._SECRET_KEY.encode(), sign_data.encode(), hashlib.sha1).digest()

        encoded_sign = base64.urlsafe_b64encode(sign)
        token = 'Qiniu ' + self._ACCESS_KEY + ':' + encoded_sign.decode()

        return token
