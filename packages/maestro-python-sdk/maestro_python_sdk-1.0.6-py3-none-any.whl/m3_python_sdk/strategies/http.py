import os
from urllib.parse import urljoin

import requests

from m3_python_sdk.strategies.abstract_strategy import AbstractStrategy
from m3_python_sdk.utils.exeption import raise_application_exception
from m3_python_sdk.utils.logger import get_logger

_LOG = get_logger('HttpService')


class HttpStrategy(AbstractStrategy):

    def __init__(self, sdk_access_key: str = None, sdk_secret_key: str = None,
                 maestro_user: str = None, api_link: str = None):

        """
        This init method allow the creation of basic sdk HTTP strategy to use
        different maestro billing tools through Http protocol

        >>> client = HttpStrategy()

        By default, it takes all params from env variables, so you need to
         configure them first
        :param sdk_access_key: maestro sdk access key. REQUIRED
        :param sdk_secret_key: maestro sdk secret key. REQUIRED
        :param maestro_user: maestro sdk user. REQUIRED
        :param api_link: api link from maestro server, REQUIRED
        """
        self._api_link = api_link if api_link else os.getenv('API_LINK', None)

        self._sdk_access_key = sdk_access_key if sdk_access_key \
            else os.getenv("SDK_ACCESS_KEY", None)

        self._sdk_secret_key = sdk_secret_key if sdk_secret_key \
            else os.getenv("SDK_SECRET_KEY", None)

        self._maestro_user = maestro_user if maestro_user \
            else os.getenv("MAESTRO_USER", None)

        if (not self._sdk_access_key or not self._sdk_secret_key
                or not self._maestro_user or not self._api_link):
            raise ValueError("Missing required sdk credential variables")

    @classmethod
    def build(cls, host: str, port: int = None, https: bool = None,
              stage: str = '',
              sdk_access_key: str = None, sdk_secret_key: str = None,
              maestro_user: str = None) -> 'HttpStrategy':
        """
        # >>> host = 'm3.cloud.com'
        # >>> port = '8000'
        # >>> https = True
        # >>> stage = 'maestro/api/v3'
        # >>> sdk_access_key = 'secret'
        # >>> sdk_secret_key = 'secret'
        # >>> maestro_user = 'user'
        # >>> http = HttpStrategy.build(host, port, https, stage,
         sdk_access_key,
        # >>> sdk_secret_key, maestro_user)
        # >>> client._api_link
        https://m3.cloud.com:8000/maestro/api/v3


        This class method allows the creation of a HttpStrategy object with
        the specified parameters, including the host and authentication
        credentials.
        :param host: domain, optionally with schema and port, but without path
        :param port: optional port, will override one in host
        :param https: flag whether it's https protocol. If None,
        will be resolved from port
        :param stage: path stage
        :param sdk_access_key: maestro sdk access key. REQUIRED
        :param sdk_secret_key: maestro sdk secret key. REQUIRED
        :param maestro_user: maestro sdk user. REQUIRED
        :return:
        """
        pair = host.split('://', maxsplit=1)
        scheme = None
        host = pair[-1]
        if len(pair) == 2:
            scheme = pair[0]
        pair = host.rsplit(':', maxsplit=1)
        host = pair[0]
        if len(pair) == 2 and not port:
            port = int(pair[-1])

        if not scheme and https is None:  # resolving schema
            # we should resolve schema from port only if
            # - it's not provided
            # - https == None
            https = not port or port == 443
            scheme = 'https' if https else 'http'
        elif isinstance(https, bool):
            scheme = 'https' if https else 'http'
        # https is None and schema
        assert scheme in ('https', 'http')
        link = f'{scheme}://{host}'
        if port:
            link += f':{port}'
        if stage:
            link = urljoin(link, stage)
        return cls(
            api_link=link,
            sdk_secret_key=sdk_secret_key,
            sdk_access_key=sdk_access_key,
            maestro_user=maestro_user
        )

    @property
    def api_link(self):
        return self._api_link

    @api_link.setter
    def api_link(self, value):
        self._api_link = value

    @staticmethod
    def _verify_response(response):
        status_code = response.status_code
        if status_code == 404:
            raise raise_application_exception(
                code=status_code,
                content=f'Requested resource not found, {response.raw.reason}'
            )
        if status_code == 401:
            raise raise_application_exception(
                code=401,
                content='You have been provided Bad Credentials,'
                        ' or resource is not found'
            )
        if status_code == 413:
            message = response.json().get('message', 'Payload Too Large')
            raise raise_application_exception(
                code=413, content=message
            )
        if status_code == 500:
            raise raise_application_exception(
                code=500,
                content=f'Error during executing request.{response.raw.reason}'
            )
        if not status_code:
            raise raise_application_exception(
                code=204,
                content=f'Empty response received.{response.raw.reason}'
            )
        if status_code != 200:
            raise raise_application_exception(
                code=status_code,
                content=f'Message: {response.text}'
            )
        return response.content.decode()

    def _pre_process_request(self, request_data: dict, command_name):

        _LOG.debug('Generating request_id')
        request_id = super()._generate_id()

        _LOG.debug('Signing HTTP headers')
        headers = super()._get_signed_headers(
            access_key=self._sdk_access_key,
            secret_key=self._sdk_secret_key,
            user=self._maestro_user,
            async_request=False,
            http=True
        )

        _LOG.debug('Encrypting HTTP body')

        body = [{
            'id': request_id,
            'type': command_name,
            'params': request_data
        }]

        _LOG.debug(f'Request Body: {body}')

        encrypted_body = super()._encrypt(secret_key=self._sdk_secret_key,
                                          data=body)
        encrypted_body = encrypted_body.decode('utf-8')

        return request_id, headers, encrypted_body

    def make_request(self, request_data: dict, command_name: str):

        request_id, headers, encrypted_body = \
            self._pre_process_request(request_data=request_data,
                                      command_name=command_name)

        _LOG.debug(f'Going to send post request to maestro server with'
                   f' request_id: {request_id},'
                   f' encrypted_body: {encrypted_body}')

        response = requests.post(url=self._api_link, headers=headers,
                                 data=encrypted_body)

        _LOG.debug('Going to verify and process server response')
        response = self._verify_response(response)
        return super().post_process_request(response=response,
                                            secret_key=self._sdk_secret_key)

    def execute(self, command_name: str, request_data: dict, **kwargs):

        return self.make_request(
            command_name=command_name,
            request_data=request_data,
        )
