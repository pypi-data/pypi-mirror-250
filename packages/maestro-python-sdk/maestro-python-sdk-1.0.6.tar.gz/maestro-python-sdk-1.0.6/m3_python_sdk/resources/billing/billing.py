from m3_python_sdk.strategies.http import HttpStrategy
from m3_python_sdk.strategies.rabbitmq import RabbitMqStrategy
from m3_python_sdk.utils.constants import BillingApiActions, SdkCloud, \
    StatusCodes
from m3_python_sdk.utils.exeption import raise_application_exception


class BillingResource:

    def __init__(self, client: 'RabbitMqStrategy' or 'HttpStrategy'):
        self._client = client

    def describe_billing_month(self, year: int, month: int,
                               sync: bool = True, secure_parameters=None,
                               is_flat_request=None, compressed: bool = False
                               ) -> dict:
        params = {
            'year': year,
            'month': month
        }

        res = self._client.execute(
            command_name=BillingApiActions.DESCRIBE_BILLING_MONTH,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        return res

    def describe_currency(self, year: int, month: int, cloud: SdkCloud,
                          sync: bool = True, secure_parameters=None,
                          is_flat_request=None, compressed: bool = False
                          ) -> dict:
        params = {
            'year': year,
            'month': month,
            'cloud': cloud
        }

        res = self._client.execute(
            command_name=BillingApiActions.DESCRIBE_CURRENCY,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        return res

    def get_top_account_reports(self, year: int, month: int, number: int = 10,
                                sync: bool = True, secure_parameters=None,
                                is_flat_request=None, compressed: bool = False
                                ) -> dict:
        params = {
            'year': year,
            'month': month,
            'number': number
        }

        res = self._client.execute(
            command_name=BillingApiActions.GET_TOP_ACCOUNTS_REPORT,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        return res

    def add_cost_center(self, regions: list, cost_center: str,
                        rewrite: bool = True,
                        sync: bool = True, secure_parameters=None,
                        is_flat_request=None, compressed: bool = False
                        ):

        params = {
            'zone': list(regions),
            'center': cost_center,
            'rewrite': rewrite
        }

        res = self._client.execute(
            command_name=BillingApiActions.ADD_COST_CENTER,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        return res

    def archive_big_query(self, admin_project_id: str, table_id: str,
                          year: int = None, month: int = None,
                          archivation: str = None,
                          sync: bool = True, secure_parameters=None,
                          is_flat_request=None, compressed: bool = False
                          ):

        if not (year and month) and not archivation:
            raise_application_exception(
                code=StatusCodes.BAD_REQUEST_400,
                content={
                    'error': 'year and month or archivation must be specified'
                }
            )

        params = {
            'adminProjectId': admin_project_id,
            'tableId': table_id
        }
        if archivation:
            archivation = True if archivation == 'enabled' else False
            params.update({'archivationEnabled': archivation})
        if year and month:
            params.update({'year': year, 'month': month})

        res = self._client.execute(
            command_name=BillingApiActions.ARCHIVE_BIG_QUERY,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        return res

    def billing_configure(self, aws_athena_update_schedule: str,
                          aws_cost_explorer_update_schedule: str,
                          aws_cost_column, aws_update_period: str,
                          azure_update_schedule: str, supported_service: str,
                          customize_report_structure: str, describe: str,
                          sync: bool = True, secure_parameters=None,
                          is_flat_request=None, compressed: bool = False):

        aws_update_period = aws_update_period.upper()
        if aws_update_period not in ['DAYS', 'TWO_DAYS', 'THREE_DAYS',
                                     'WEEK', 'MONTH']:
            raise_application_exception(
                code=400,
                content={'error': 'aws_update_period value not allowed'}
            )
        if aws_cost_column not in ['BlendedCost', 'UnBlendedCost']:
            raise_application_exception(
                code=400,
                content={'error': 'aws_cost_column value not allowed'}
            )

        params = {
            'describe': describe,
            'awsAthenaUpdateSchedule': aws_athena_update_schedule,
            'awsCostExplorerUpdateSchedule': aws_cost_explorer_update_schedule,
            'awsCostColumnName': aws_cost_column,
            'awsUpdatePeriod': aws_update_period,
            'azureUpdateSchedule': azure_update_schedule,
            'customizeReportStructure': customize_report_structure,
            'supportedServices': supported_service,
        }

        res = self._client.execute(
            command_name=BillingApiActions.BILLING_CONFIGURE,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        return res
