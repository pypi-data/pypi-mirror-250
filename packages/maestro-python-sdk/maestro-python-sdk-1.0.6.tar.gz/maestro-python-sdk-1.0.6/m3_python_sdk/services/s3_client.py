# import io
# import os
#
# import boto3
#
# from m3_python_sdk.utils.logger import get_logger
#
# _LOG = get_logger('s3_service')
#
#
# class S3Client:
#
#     def __init__(self):
#
#         self.region = os.getenv('REGION', None)
#         self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID', None)
#         self.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY', None)
#         self.aws_session_token = os.getenv('AWS_SESSION_TOKEN', None)
#
#         if not self.aws_access_key_id and not self.aws_secret_access_key:
#             raise ValueError('AWS access key and secret key'
#                              ' should be provided')
#         self._client = None
#
#     def _init_client(self):
#         self._client = boto3.client(
#             's3',
#             region_name=self.region,
#             aws_access_key_id=self.aws_access_key_id,
#             aws_secret_access_key=self.aws_secret_access_key,
#             aws_session_token=self.aws_session_token
#         )
#
#     @property
#     def client(self):
#         if not self._client:
#             self._init_client()
#         return self._client
#
#     def create_and_get_presigned_url(self, bucket_name: str, file_name: str,
#                                      content: bytes,
#                                      client_method='get_object',
#                                      http_method='GET',
#                                      expires_in_sec=3600):
#         self.client.upload_fileobj(
#             io.BytesIO(content), bucket_name, file_name)
#         url = self.client.generate_presigned_url(
#             ClientMethod=client_method,
#             Params={
#                 'Bucket': bucket_name,
#                 'Key': file_name,
#             },
#             ExpiresIn=expires_in_sec,
#             HttpMethod=http_method
#         )
#
#         return url
#
#     def get_presigned_url(self, file_name, content, bucket):
#         _LOG.debug('Retrieving presigned url')
#         return self.create_and_get_presigned_url(
#             file_name=file_name,
#             content=content,
#             bucket_name=bucket
#         )
