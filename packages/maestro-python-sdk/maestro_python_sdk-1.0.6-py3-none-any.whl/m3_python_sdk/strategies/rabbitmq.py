import base64
import gzip
import json
import os

import pika
from pika import exceptions

from m3_python_sdk.strategies.abstract_strategy import AbstractStrategy
from m3_python_sdk.utils.constants import PLAIN_CONTENT_TYPE, \
    TIMEOUT_ERROR_MESSAGE, Queues
from m3_python_sdk.utils.constants import RABBIT_DEFAULT_RESPONSE_TIMEOUT
from m3_python_sdk.utils.constants import SYNC_HEADER, \
    CONFIGURATION_ISSUES_ERROR_MESSAGE
from m3_python_sdk.utils.exeption import raise_application_exception
from m3_python_sdk.utils.logger import get_logger

_LOG = get_logger('RabbitMqService')


class RabbitMqStrategy(AbstractStrategy):
    def __init__(self, connection_url: str,
                 request_queue: str = None,
                 response_queue: str = None,
                 rabbit_exchange: str = None, sdk_access_key: str = None,
                 sdk_secret_key: str = None, maestro_user: str = None,
                 timeout: int = None):
        """
        This init method allow the creation of basic sdk HTTP strategy to use
        different maestro billing tools through Http protocol

        # >>> connection_url = 'url'
        # >>> client = RabbitMqStrategy(connection_url=connection_url)
        response

        :param connection_url: your rabbit maestro connection url
        :param request_queue: rabbit request queue, Assigned to the default
         value
        :param response_queue: rabbit response queue, Assigned to the default
         value
        :param rabbit_exchange: rabbit exchange, Assigned to None by default
        :param sdk_access_key: Your sdk key name: by default takes from env
         variables
        :param sdk_secret_key: Password from your sdk access key: by default
         takes from env variables
        :param maestro_user: Your maestro user: by default takes from env
         variables
        :param timeout: rabbit timeout, by default set to 30 sec
        :return RabbitMqClient object
        """

        self.connection_url = connection_url

        if timeout is None or not isinstance(timeout, int):
            self.timeout = RABBIT_DEFAULT_RESPONSE_TIMEOUT
            _LOG.debug('Timeout set to default 30 second')
        else:
            self.timeout = timeout

        self._sdk_access_key = sdk_access_key if sdk_access_key \
            else os.getenv("SDK_ACCESS_KEY", None)

        self._sdk_secret_key = sdk_secret_key if sdk_secret_key \
            else os.getenv("SDK_SECRET_KEY", None)

        self._maestro_user = maestro_user if maestro_user \
            else os.getenv("MAESTRO_USER", None)

        if (not self._sdk_access_key or not self._sdk_secret_key
                or not self._maestro_user):
            raise ValueError("Missing required sdk credential variables")

        self._request_queue = request_queue if request_queue \
            else os.getenv(Queues.DEFAULT_MAESTRO_REQUEST_QUEUE, None)

        self._response_queue = response_queue if response_queue \
            else os.getenv(Queues.DEFAULT_MAESTRO_RESPONSE_QUEUE, None)

        if not self._request_queue:
            raise ValueError('Missing request queue')

        self.rabbit_exchange = rabbit_exchange if rabbit_exchange \
            else os.getenv('RABBIT_EXCHANGE', None)
        self.responses = {}

        _LOG.debug('Initialized rabbit options: '
                   f'request_queue/routing_key: {self._request_queue}, '
                   f'response_queue: {self._response_queue}, '
                   f'exchange: {self.rabbit_exchange}')

    @classmethod
    def build(cls, host: str, port: int = None, amqps: bool = True,
              stage: str = '', username: str = None,
              password: str = None,
              request_queue: str = Queues.DEFAULT_MAESTRO_REQUEST_QUEUE,
              response_queue: str = Queues.DEFAULT_MAESTRO_RESPONSE_QUEUE,
              rabbit_exchange: str = None, sdk_access_key: str = None,
              sdk_secret_key: str = None, maestro_user: str = None,
              timeout: int = RABBIT_DEFAULT_RESPONSE_TIMEOUT
              ) -> 'RabbitMqStrategy':
        """
        Builds a RabbitMQStrategy object with more flexible way to create url.

        :param host: The host of the RabbitMQ server.
        :param port: The port of the RabbitMQ server. Defaults to 5671 if amqps
         is True, otherwise 5672.
        :param amqps: Whether to use AMQPS. Defaults to True.
        :param stage: The stage. Defaults to ''.
        :param username: The username to connect to the RabbitMQ server.
        :param password: The password to connect to the RabbitMQ server.
        :param request_queue: The request queue.
         Defaults to DEFAULT_REQUEST_QUEUE.
        :param response_queue: The response queue.
         Defaults to DEFAULT_RESPONSE_QUEUE.
        :param rabbit_exchange: The RabbitMQ exchange. Defaults to None.
        :param sdk_access_key: The SDK access key. Defaults to None.
        :param sdk_secret_key: The SDK secret key. Defaults to None.
        :param maestro_user: The Maestro user. Defaults to None.
        :param timeout: The timeout. Defaults to
        RABBIT_DEFAULT_RESPONSE_TIMEOUT.
        :return: A RabbitMqStrategy object.

        # >>> host = 'host123.eu.amazon'
        # >>> stage = 'dev'
        # >>> username = 'maestro_username'
        # >>> password = 'maestro_password'
        # >>> rabit = RabbitMqStrategy.build(host=host,
         stage=stage, username=username, password=password)
        # >>> print(rabit.connection_url)
            amqps://maestro_username:maestro_password@host123.eu.amazon:5671/dev
        """

        if not host:
            raise ValueError('RabbitMQ URL cannot be generated without host')

        pair = host.split('://', maxsplit=1)
        scheme = None
        host = pair[-1]
        if len(pair) == 2:
            scheme = pair[0]
        pair = host.split(':', maxsplit=1)
        host = pair[0]
        if len(pair) == 2 and not port:
            port = int(pair[-1])

        if not scheme and amqps is None:
            amqps = not port or port == 5671
            scheme = 'amqps' if amqps else 'amqp'
        elif isinstance(amqps, bool):
            scheme = 'amqps' if amqps else 'amqp'

        assert scheme in ('amqps', 'amqp')
        link = f"{scheme}://{username}:{password}@"
        if host.startswith('@'):
            host = host[1:]
        link += f"{host}"
        if port:
            link += f":{port}"
        if stage:
            link += f"/{stage}"

        return cls(
            connection_url=link,
            request_queue=request_queue,
            response_queue=response_queue,
            rabbit_exchange=rabbit_exchange,
            sdk_access_key=sdk_access_key,
            sdk_secret_key=sdk_secret_key,
            maestro_user=maestro_user,
            timeout=timeout)

    @property
    def request_queue(self):
        return self._request_queue

    @request_queue.setter
    def request_queue(self, value):
        self._request_queue = value

    @property
    def response_queue(self) -> str:
        return self._response_queue

    @response_queue.setter
    def response_queue(self, new_response_queue):
        self._response_queue = new_response_queue

    def _open_channel(self):
        if not self.connection_url:
            _LOG.error('Cannot connect to RabbitMQ, connection_url'
                       ' was not provided')
        try:
            parameters = pika.URLParameters(self.connection_url)
            self.conn = pika.BlockingConnection(parameters)
            _LOG.debug('Channel opened')
            return self.conn.channel()
        except pika.exceptions.AMQPConnectionError:
            raise raise_application_exception(
                code=401,
                content='Connection to RabbitMQ refused. Bad credentials.')

    def _close(self):
        if self.conn.is_open:
            _LOG.debug('going to close channel')
            self.conn.close()

    def publish(self, message, routing_key, exchange='', headers=None,
                content_type=None):

        channel = self._open_channel()
        channel.confirm_delivery()
        response = channel.basic_publish(exchange=exchange,
                                         routing_key=routing_key,
                                         properties=pika.BasicProperties(
                                             headers=headers,
                                             content_type=content_type),
                                         body=message,
                                         mandatory=True)
        self._close()
        if not response:
            _LOG.error(
                'Message event was returned. Check RabbitMQ configuration: '
                'maybe target queue does not exists.')
            raise raise_application_exception(
                code=502,
                content=CONFIGURATION_ISSUES_ERROR_MESSAGE
            )
        _LOG.info('Message pushed')

    def publish_sync(self, message, routing_key, correlation_id,
                     callback_queue, exchange='', headers=None,
                     content_type=None):

        channel = self._open_channel()
        channel.confirm_delivery()
        response = channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            properties=pika.BasicProperties(headers=headers,
                                            reply_to=callback_queue,
                                            correlation_id=correlation_id,
                                            content_type=content_type),
            body=message)
        if not response:
            _LOG.error(
                'Message event was returned. Check RabbitMQ configuration: '
                'maybe target queue does not exists.')
            raise raise_application_exception(
                code=502,
                content=CONFIGURATION_ISSUES_ERROR_MESSAGE
            )

        _LOG.info('Message pushed')

    def consume_sync(self, queue, correlation_id):
        def _consumer_callback(ch, method, props, body):
            self.responses[props.correlation_id] = body
            ch.basic_ack(delivery_tag=method.delivery_tag)
            ch.stop_consuming(props.correlation_id)

        def _close_on_timeout():
            _LOG.warn('Timeout exceeded. Close connection')
            self.conn.close()

        channel = self._open_channel()
        if channel.basic_consume(queue=queue,
                                 on_message_callback=_consumer_callback,
                                 consumer_tag=correlation_id):
            _LOG.debug(f'Waiting for message. Queue: {queue},'
                       f' Correlation id: {correlation_id}')
        else:
            _LOG.error('Failed to consume. Queue: {0}'.format(queue))
            raise raise_application_exception(
                code=502,
                content=TIMEOUT_ERROR_MESSAGE
            )

        self.conn.add_timeout(self.timeout, _close_on_timeout)

        # blocking method
        channel.start_consuming()
        self._close()

        if correlation_id in list(self.responses.keys()):
            response = self.responses.pop(correlation_id)
            _LOG.debug(f'Received response: {response}')
            return response
        else:
            _LOG.error(f'Response was not received. '
                       f'Timeout: {self.timeout} seconds.')
            return None

    def check_queue_exists(self, queue_name):
        channel = self._open_channel()
        try:
            channel.queue_declare(queue=queue_name, durable=True, passive=True)
        except pika.exceptions.ChannelClosedByBroker as e:
            if e.reply_code == 404:
                return False
        self._close()
        return True

    def declare_queue(self, queue_name):
        channel = self._open_channel()
        declare_resp = channel.queue_declare(queue=queue_name, durable=True)
        _LOG.info(f'Queue declaration response: {declare_resp}')

    @staticmethod
    def _build_payload(id, command_name, parameters, is_flat_request):
        if is_flat_request:
            parameters.update({'type': command_name})
            result = [
                {
                    'id': id,
                    'type': None,
                    'params': parameters
                }
            ]
        else:
            result = [
                {
                    'id': id,
                    'type': command_name,
                    'params': parameters
                }
            ]
        return result

    def _build_message(self, id, command_name, parameters,
                       is_flat_request=False, compressed=False):
        if isinstance(parameters, list):
            result = []
            for payload in parameters:
                result.extend(self._build_payload(id, command_name, payload,
                                                  is_flat_request))
        else:
            result = self._build_payload(id, command_name, parameters,
                                         is_flat_request)
        if compressed:
            return base64.b64encode(gzip.compress(
                json.dumps(result).encode('UTF-8'))).decode()
        return result

    def _build_secure_message(self, id, command_name, parameters_to_secure,
                              secure_parameters=None, is_flat_request=False):
        if not secure_parameters:
            secure_parameters = []
        secured_parameters = {k: (v if k not in secure_parameters else '*****')
                              for k, v in parameters_to_secure.items()}
        return self._build_message(
            command_name=command_name,
            parameters=secured_parameters,
            id=id,
            is_flat_request=is_flat_request
        )

    def pre_process_request(self, command_name, parameters, secure_parameters,
                            is_flat_request, async_request, compressed=False):

        request_id = self._generate_id()

        _LOG.debug('Going to pre-process request')
        message = self._build_message(
            command_name=command_name,
            parameters=parameters,
            id=request_id,
            is_flat_request=is_flat_request,
            compressed=compressed
        )
        secure_message = message
        if not compressed:
            secure_message = self._build_secure_message(
                command_name=command_name,
                parameters_to_secure=parameters,
                secure_parameters=secure_parameters,
                id=request_id,
                is_flat_request=is_flat_request
            )
        _LOG.debug(f'Prepared command: {command_name}'
                   f'\nCommand format: {secure_message}')

        encrypted_body = self._encrypt(
            secret_key=self._sdk_secret_key,
            data=message
        )
        _LOG.debug('Message encrypted')
        # sign headers
        headers = self._get_signed_headers(
            access_key=self._sdk_access_key,
            secret_key=self._sdk_secret_key,
            user=self._maestro_user,
            async_request=async_request,
            compressed=compressed
        )
        _LOG.debug('Signed headers prepared')
        return encrypted_body, headers

    def __resolve_rabbit_options(self, exchange, request_queue,
                                 response_queue):
        exchange = exchange or self.rabbit_exchange
        if exchange:
            routing_key = ''
        else:
            routing_key = request_queue or self._request_queue
            exchange = ''

        response_queue = response_queue if response_queue else (
            self._response_queue)
        return routing_key, exchange, response_queue

    def execute_async(self, command_name, parameters, secure_parameters=None,
                      is_flat_request=None, compressed=True):
        _LOG.debug(
            f'Command info:\n command name: {command_name}'
            f'\n parameters: {parameters}')

        message, headers = self.pre_process_request(
            command_name=command_name,
            parameters=parameters,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            async_request=True,
            compressed=compressed
        )
        headers[SYNC_HEADER] = False

        _LOG.debug('Resolved rabbit options: '
                   f'request_queue/routing_key: {self._request_queue}, '
                   f'exchange: {self.rabbit_exchange}')

        _LOG.debug(f'Prepared headers: {headers}')

        _LOG.debug(
            f'Going to execute async command: {command_name}'
            f'\nCommand format: {message}')

        return self.publish(routing_key=self._request_queue,
                            exchange=self.rabbit_exchange,
                            message=message,
                            headers=headers,
                            content_type=PLAIN_CONTENT_TYPE)

    def execute_sync(self, command_name, parameters, secure_parameters=None,
                     is_flat_request=None, compressed=False):

        message, headers = self.pre_process_request(
            command_name=command_name,
            parameters=parameters,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            async_request=False,
            compressed=compressed
        )

        request_queue, exchange, response_queue = \
            self.__resolve_rabbit_options(
                exchange=self.rabbit_exchange if self.rabbit_exchange else None,
                request_queue=self._request_queue if self._request_queue else None,
                response_queue=self._response_queue if self._response_queue else None
            )
        _LOG.debug('Resolved rabbit options: '
                   f'request_queue/routing_key: {request_queue}, '
                   f'response_queue: {response_queue}, '
                   f'exchange: {exchange}')

        _LOG.debug(f'Prepared headers: {headers}')

        request_id = super()._generate_id()

        _LOG.debug(
            f'Going to execute sync command: {command_name}'
            f'\nCommand format: {message}')

        self.publish_sync(routing_key=request_queue,
                          exchange=exchange,
                          callback_queue=response_queue,
                          correlation_id=request_id,
                          message=message,
                          headers=headers,
                          content_type=PLAIN_CONTENT_TYPE)
        try:
            response_item = self.consume_sync(
                queue=response_queue,
                correlation_id=request_id)
        except exceptions.ConnectionWrongStateError as e:
            raise raise_application_exception(content=e)
        if not response_item:
            raise raise_application_exception(
                code=408,
                content=f'Response was not received.'
                        f' Timeout:{self.timeout} seconds.')

        return super().post_process_request(response=response_item,
                                            secret_key=self._sdk_secret_key)

    def execute(self, request_data: dict, command_name: str, **kwargs, ):

        secure_parameters = kwargs.get('secure_parameters', None)
        is_flat_request = kwargs.get('is_flat_request', None)
        compressed = kwargs.get('compressed', None)
        sync = kwargs.get('sync')

        if sync:
            _LOG.debug('Going to execute_sync inside def execute()')
            return self.execute_sync(
                command_name=command_name,
                parameters=request_data,
                compressed=compressed,
                secure_parameters=secure_parameters,
                is_flat_request=is_flat_request
            )
        else:
            _LOG.debug('Going to execute_async inside def execute()')
            return self.execute_async(
                command_name=command_name,
                parameters=request_data,
                compressed=compressed,
                secure_parameters=secure_parameters,
                is_flat_request=is_flat_request
            )
