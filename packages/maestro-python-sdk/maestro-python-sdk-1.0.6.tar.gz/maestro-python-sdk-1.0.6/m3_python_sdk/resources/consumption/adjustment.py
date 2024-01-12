import re
import datetime as dt
from datetime import datetime

from m3_python_sdk.strategies.http import HttpStrategy
from m3_python_sdk.strategies.rabbitmq import RabbitMqStrategy
from m3_python_sdk.utils.constants import ADD_ADJUSTMENT, GET_ADJUSTMENT, \
    DELETE_ADJUSTMENT, GET_TOTAL_BILLING_REPORT, SdkCloud, StatusCodes
from m3_python_sdk.utils.logger import get_logger
from m3_python_sdk.utils.exeption import raise_application_exception

_LOG = get_logger('Adjustment')


class AdjustmentResource:

    def __init__(self, client: 'RabbitMqStrategy' or 'HttpStrategy'):
        self._client = client

    def add_adjustment(self,
                       month: int,
                       year: int,
                       credit_type: str,
                       value: float,
                       description: str = None,
                       target_project: str = None,
                       target_account_number: str = None,
                       currency_native: bool = False,
                       target_region: str = None,
                       target_cloud: SdkCloud = None,
                       sync: bool = True, secure_parameters=None,
                       is_flat_request=None, compressed: bool = False
                       ) -> [dict, None]:
        params = {
            'year': year,
            'month': month,
            'value': value,
            'credit_type': credit_type,
            'description': description,
            'currency_native': currency_native
        }

        if target_project:
            params.update({'target_project': target_project})
        if target_account_number:
            params.update({'target_account_number': target_account_number})

        if target_region:
            params.update({'target_region': target_region})
        if target_cloud:
            params.update({'target_cloud': target_cloud})

        _LOG.info(f'Parameters to set: {params}')
        if value == 0:
            _LOG.warning('The value is equal to 0; Skipping')
            return

        res = self._client.execute(
            command_name=ADD_ADJUSTMENT,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        return res

    def get_adjustment(self,
                       month: int,
                       year: int,
                       description: str,
                       credit_type: str,
                       target_project: str = None,
                       target_account_number: str = None,
                       target_region: str = None,
                       target_cloud: SdkCloud = None,

                       sync: bool = True, secure_parameters=None,
                       is_flat_request=None, compressed: bool = False
                       ) -> dict:
        params = {
            'year': year,
            'month': month,
            'credit_type': credit_type,
            'description': description,
        }

        if target_project:
            params.update({'target_project': target_project})
        if target_account_number:
            params.update({'target_account_number': target_account_number})

        if target_region:
            params.update({'target_region': target_region})
        if target_cloud:
            params.update({'target_cloud': target_cloud})

        res = self._client.execute(
            command_name=GET_ADJUSTMENT,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed)

        return res

    def delete_adjustment(self,
                          month: int,
                          year: int,
                          description: str,
                          credit_type: str,
                          target_project: str = None,
                          target_account_number: str = None,
                          target_region: str = None,
                          target_cloud: SdkCloud = None,

                          sync: bool = True, secure_parameters=None,
                          is_flat_request=None, compressed: bool = False
                          ) -> dict:
        params = {
            'year': year,
            'month': month,
            'credit_type': credit_type,
            'description': description,
        }

        if target_project:
            params.update({'target_project': target_project})
        if target_account_number:
            params.update({'target_account_number': target_account_number})

        if target_region:
            params.update({'target_region': target_region})
        if target_cloud:
            params.update({'target_cloud': target_cloud})

        res = self._client.execute(
            command_name=DELETE_ADJUSTMENT,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed)

        return res

    def total_report(self, from_date: [str, int, float],
                     to_date: [str, int, float],
                     tenant_group: str = None,
                     tenant: str = None, region: str = None,
                     cloud: [SdkCloud, list, str] = None, tag: str = None,
                     report: bool = False, grand_total: bool = True,
                     sync: bool = True, secure_parameters=None,
                     is_flat_request=None, compressed: bool = False
                     ) -> [dict, ValueError]:

        if tenant and tenant_group:
            return ValueError('You cannot pass tenant and tenant_group'
                              ' simultaneously ')

        if not tenant and not tenant_group:
            return ValueError('Missing parameters, please provide tenant'
                              ' or tenant_group')

        date_format = '%d.%m.%Y'

        if tenant:
            target = {
                'tenant': tenant.upper(),
                'reportUnit': 'TENANT',
                'onlyGrandTotal': grand_total
            }
        else:
            target = {
                'tenantGroup': tenant_group.upper(),
                'reportUnit': 'TENANT_GROUP',
                'onlyGrandTotal': grand_total
            }

        if not isinstance(report, bool):
            raise ValueError('Report should be of type bool')

        if not isinstance(from_date, int) and not isinstance(from_date, float):
            try:
                from_date = datetime.strptime(from_date, date_format)
                from_date = from_date.replace(
                    tzinfo=dt.timezone.utc).timestamp() * 1000
            except:
                raise_application_exception(
                    code=StatusCodes.BAD_REQUEST_400,
                    content={
                        'error': 'Cannot transform from date to timestamp'
                    }
                )

        if not isinstance(to_date, int) and not isinstance(to_date, float):
            try:
                to_date = datetime.strptime(to_date, date_format)
                to_date = to_date.replace(
                    tzinfo=dt.timezone.utc).timestamp() * 1000
            except:
                raise_application_exception(
                    code=StatusCodes.BAD_REQUEST_400,
                    content={
                        'error': 'Cannot transform from date to timestamp'
                    }
                )

        request_object = {
            'from': from_date,
            'to': to_date,
            'reportFormat': 'JSON',
            'target': target
        }

        if tag:
            if not re.match(r'^[A-Za-z0-9_.:/+-@.]+:[A-Za-z0-90-9_.:/+-@.]*$',
                            tag):
                raise_application_exception(
                    code=StatusCodes.BAD_REQUEST_400,
                    content={
                        'error': 'tag should correspond to pattern tag:value'
                    }
                )
            request_object.update({'tag': tag.replace(':', '=')})

        if report:
            request_object.update({'reportFormat': 'EMAIL'})

        if cloud:
            request_object['target'].update(
                {
                    'clouds': [cloud] if type(cloud) is str else cloud,
                    'reportUnit': 'TENANT_GROUP_AND_CLOUD' if tenant_group \
                        else 'TENANT_AND_CLOUD'
                }
            )
        elif region:
            request_object['target'].update(
                {'region': region.upper()}
            )

        res = self._client.execute(
            command_name=GET_TOTAL_BILLING_REPORT,
            request_data=request_object,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        return res
