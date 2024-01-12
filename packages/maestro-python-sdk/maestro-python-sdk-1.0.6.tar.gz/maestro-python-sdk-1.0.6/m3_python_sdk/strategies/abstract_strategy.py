import base64
import binascii
import hashlib
import hmac
import json
import os
import uuid
from abc import ABC, abstractmethod
from datetime import datetime

from m3_python_sdk.utils.constants import SUCCESS_STATUS, ERROR_STATUS
from m3_python_sdk.utils.exeption import raise_application_exception
from m3_python_sdk.utils.logger import get_logger

_LOG = get_logger('AbstractStrategy')


class AbstractStrategy(ABC):

    @abstractmethod
    def execute(self, request_data: dict, command_name: str):
        pass

    @staticmethod
    def _generate_id():
        return str(uuid.uuid1())

    @staticmethod
    def _decrypt(secret_key, data):
        """
        Decode received message from Base64 format, cut initialization
        vector ("iv") from beginning of the message, decrypt message
        """
        from cryptography.hazmat.primitives.ciphers import Cipher, \
            algorithms, modes
        decoded_data = base64.b64decode(data)
        iv = decoded_data[:12]
        encrypted_data = decoded_data[12:]
        cipher = Cipher(
            algorithms.AES(key=secret_key.encode('utf-8')),
            modes.GCM(initialization_vector=iv)
        ).decryptor()
        origin_data_with_iv = cipher.update(encrypted_data)
        # Due to Initialization vector in encrypting method
        # there is need to split useful and useless parts of the
        # server response.
        response = origin_data_with_iv[:-16]
        return response

    @staticmethod
    def _encrypt(secret_key, data):
        """
        Encrypt data, add initialization vector ("iv") at beginning of
         encrypted
        message and encode entire data in Base64 format
        """
        if not secret_key:
            raise ValueError('Cannot detect secret_key. Please add it first')

        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        iv = os.urandom(12)
        plain_text = data if isinstance(data, str) else json.dumps(data)
        data_in_bytes = plain_text.encode('utf-8')
        try:
            cipher = AESGCM(key=secret_key.encode('utf-8'))
        except ValueError as e:
            raise ValueError(str(e).replace(
                'AESGCM key', 'Secret Key'))
        encrypted_data = cipher.encrypt(
            nonce=iv, data=data_in_bytes, associated_data=None)
        encrypted_data_with_iv = bytes(iv) + encrypted_data
        base64_request = base64.b64encode(encrypted_data_with_iv)
        return base64_request

    @staticmethod
    def _get_signed_headers(access_key: str, secret_key: str, user: str,
                            async_request: bool = False,
                            compressed: bool = False, http: bool = False
                            ) -> dict:
        """
        Create and sign necessary headers for interaction with Maestro API
        """
        if not access_key or not user:
            raise ValueError(
                'Cannot detect access_key or user. Please add it first')

        date = int(datetime.now().timestamp()) * 1000
        signature = hmac.new(
            key=bytearray(f'{secret_key}{date}'.encode('utf-8')),
            msg=bytearray(f'M3-POST:{access_key}:{date}:{user}'.encode('utf-8')
                          ),
            digestmod=hashlib.sha256
        ).hexdigest()
        n = 2
        resolved_signature = ''
        for each in [signature[i:i + n] for i in range(0, len(signature), n)]:
            resolved_signature += '1' + each

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "maestro-authentication": resolved_signature,
            "maestro-request-identifier": "api-server",
            "maestro-user-identifier": user,
            "maestro-date": str(date),
            "maestro-accesskey": access_key,
            "maestro-sdk-version": "3.2.80",
            "maestro-sdk-async": 'true' if async_request else 'false',
            # convert compressed to str because of request lib wants it
            "compressed": str(compressed).lower() if http else compressed
        }
        return headers

    def post_process_request(self, response, secret_key: str):
        try:
            response_item = self._decrypt(
                secret_key=secret_key,
                data=response
            )
            _LOG.debug('Message from M3-server successfully decrypted')
        except binascii.Error:
            response_item = response.decode('utf-8')
        try:
            _LOG.debug(f'Raw decrypted message from server: {response_item}')
            response_json = json.loads(response_item).get('results')[0]

            status = response_json.get('status')
            status_code = response_json.get('statusCode', None)
            warnings = response_json.get('warnings', None)

            if status == SUCCESS_STATUS:
                data = response_json.get('data', None)

                try:
                    data = json.loads(data)
                except:
                    data = data

                response = {
                    'status': status,
                    'status_code': status_code,
                }

                if isinstance(data, str):
                    response.update({'message': data})
                if isinstance(data, dict):
                    data = [data]
                if isinstance(data, list):
                    response.update({'items': data})

                items = response_json.get('items', None)
                if items:
                    response.update({'items': items})

                table_title = response_json.get('tableTitle', None)
                if table_title:
                    response.update({'table_title': table_title})

                if warnings:
                    response.update({'warnings': warnings})

                return response

            elif status == ERROR_STATUS:
                error = response_json.get('error', None)

                try:
                    error = json.loads(error)
                except:
                    error = error

                return {
                    'status_code': status_code,
                    'status': status,
                    'message': error
                }
            else:
                data = response_json.get('readableError')

                try:
                    data = json.loads(data)
                except:
                    data = data

                response = {
                    'status_code': status_code,
                    'status': status,
                    'message': data,
                }
                if warnings:
                    response.update({'warnings': warnings})
                return response

        except json.decoder.JSONDecodeError:
            _LOG.error('Response can not be decoded - invalid Json string')
            return raise_application_exception(
                code=500,
                content='Response can not be decoded'
            )
