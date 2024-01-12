from m3_python_sdk.strategies.http import HttpStrategy
from m3_python_sdk.strategies.rabbitmq import RabbitMqStrategy
from m3_python_sdk.utils.constants import ADD_CONSUMPTION, GET_CONSUMPTION, \
    DELETE_CONSUMPTION, ADD_CONSUMPTION_DETAILS, GET_CONSUMPTION_DETAILS, \
    DELETE_CONSUMPTION_DETAILS, CHECK_TENANT_STATUS, SdkCloud


class ConsumptionResource:

    def __init__(self, client: 'RabbitMqStrategy' or 'HttpStrategy'):
        self._client = client

    def get_consumption(self,
                        target_region: str,
                        year: int,
                        month: int,
                        source_project: str = None,
                        target_project: str = None,
                        source_account_number: str = None,
                        target_account_number: str = None,
                        description: str = None, service_name: str = None,
                        sync: bool = True, secure_parameters=None,
                        is_flat_request=None, compressed: bool = False
                        ) -> dict:

        params = {
            'target_region': target_region,
            'year': year,
            'month': month,
            'description': description
        }

        if source_project and target_project:
            params.update({'source_project': source_project,
                           'target_project': target_project})

        if source_account_number and target_account_number and service_name:
            params.update({'source_account_number': source_account_number,
                           'target_account_number': target_account_number,
                           'service_name': service_name})

        res = self._client.execute(
            command_name=GET_CONSUMPTION,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        return res

    def add_consumption(self,
                        target_region: str,
                        year: int,
                        month: int,
                        value: float,
                        source_project: str = None,
                        target_project: str = None,
                        source_account_number: str = None,
                        target_account_number: str = None,
                        description: str = None,
                        service_name: str = None,
                        sync: bool = True, secure_parameters=None,
                        is_flat_request=None, compressed: bool = False
                        ) -> dict:
        params = {
            'target_region': target_region,
            'year': year,
            'month': month,
            'value': value,
            'description': description,
        }

        if source_project and target_project:
            params.update({'source_project': source_project,
                           'target_project': target_project})

        if source_account_number and target_account_number and service_name:
            params.update({'source_account_number': source_account_number,
                           'target_account_number': target_account_number,
                           'service_name': service_name})

        res = self._client.execute(
            command_name=ADD_CONSUMPTION,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        return res

    def delete_consumption(self,
                           target_region: str,
                           year: int,
                           month: int,
                           source_project: str = None,
                           target_project: str = None,
                           source_account_number: str = None,
                           target_account_number: str = None,
                           description: str = None,
                           service_name: str = None,
                           sync: bool = True, secure_parameters=None,
                           is_flat_request=None, compressed: bool = False
                           ) -> dict:
        params = {
            'target_region': target_region,
            'year': year,
            'month': month,
            'description': description
        }

        if source_project and target_project:
            params.update({'source_project': source_project,
                           'target_project': target_project})

        if source_account_number and target_account_number and service_name:
            params.update({'source_account_number': source_account_number,
                           'target_account_number': target_account_number,
                           'service_name': service_name})

        res = self._client.execute(
            command_name=DELETE_CONSUMPTION,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        return res

    def add_consumption_details(self,
                                day: [int, None],
                                month: int,
                                year: int,
                                product_name: str,
                                kpi_name: str,
                                cost: float,
                                amount: float,
                                price: float,
                                price_unit: str,
                                target_project: str = None,
                                target_account_number: str = None,
                                target_region: str = None,
                                target_cloud: SdkCloud = None,
                                sync: bool = True, secure_parameters=None,
                                is_flat_request=None, compressed: bool = False
                                ) -> dict:
        params = {
            'month': month,
            'year': year,
            'records': [
                {
                    "kpi_name": kpi_name,
                    "amount": amount,
                    "price": price,
                    "cost": cost,
                    "product_name": product_name,
                    "price_unit": price_unit,
                }
            ]
        }

        if target_project:
            params.update({'target_project': target_project})
        if target_account_number:
            params.update({'target_account_number': target_account_number})
        if day:
            params.update({'day': day})
        if target_region:
            params.update({'target_region': target_region, })
        if target_cloud:
            params.update({'target_cloud': target_cloud})

        res = self._client.execute(
            command_name=ADD_CONSUMPTION_DETAILS,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        return res

    @staticmethod
    def create_consumption_details_record(product_name: str,
                                          kpi_name: str, cost: float,
                                          amount: float, price: float,
                                          price_unit: str) -> dict:
        record = {
            "kpi_name": kpi_name,
            "amount": amount,
            "price": price,
            "cost": cost,
            "product_name": product_name,
            "price_unit": price_unit,
        }

        return record

    @staticmethod
    def create_consumption_details_data(target_project: str,
                                        day: [int, None],
                                        month: int, year: int,
                                        records: list,
                                        target_region: str = None,
                                        ) -> dict:

        params = {
            'target_project': target_project,
            'target_region': target_region,
            'year': year,
            'month': month,
            'records': records
        }

        if day:
            params.update({'day': day})

        return params

    def add_consumption_details_ready_data(self, params: dict,
                                           sync: bool = False,
                                           secure_parameters=None,
                                           is_flat_request=None,
                                           compressed: bool = False):

        self._client.execute(
            command_name=ADD_CONSUMPTION_DETAILS,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

    def add_consumption_details_ready_record(self, target_project: str,
                                             month: int, year: int,
                                             records: list,
                                             target_region: str = None,
                                             day: int = None,
                                             sync: bool = False,
                                             secure_parameters=None,
                                             is_flat_request=None,
                                             compressed: bool = False
                                             ):

        params = {
            'target_project': target_project,
            'target_region': target_region,
            'year': year,
            'month': month,
            'records': records
        }

        if day:
            params.update({'day': day})

        res = self._client.execute(
            command_name=ADD_CONSUMPTION_DETAILS,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        return res

    def get_consumption_details(self, day: [int, None], month: int, year: int,
                                target_project: str = None,
                                target_account_number: str = None,
                                target_region: str = None,
                                target_cloud: SdkCloud = None,

                                sync: bool = True, secure_parameters=None,
                                is_flat_request=None, compressed: bool = False
                                ) -> dict:
        params = {
            'month': month,
            'year': year
        }

        if target_project:
            params.update({'target_project': target_project})
        if target_account_number:
            params.update({'target_account_number': target_account_number})
        if day:
            params.update({'day': day})
        if target_region:
            params.update({'target_region': target_region, })
        if target_cloud:
            params.update({'target_cloud': target_cloud})

        res = self._client.execute(
            command_name=GET_CONSUMPTION_DETAILS,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        return res

    def delete_consumption_details(self, day: [int, None], month: int,
                                   year: int,
                                   target_project: str = None,
                                   target_account_number: str = None,
                                   target_region: str = None,
                                   target_cloud: SdkCloud = None,
                                   sync: bool = True, secure_parameters=None,
                                   is_flat_request=None,
                                   compressed: bool = False) -> dict:
        params = {
            'month': month,
            'year': year
        }

        if target_project:
            params.update({'target_project': target_project})
        if target_account_number:
            params.update({'target_account_number': target_account_number})
        if day:
            params.update({'day': day})
        if target_region:
            params.update({'target_region': target_region, })
        if target_cloud:
            params.update({'target_cloud': target_cloud})

        res = self._client.execute(
            command_name=DELETE_CONSUMPTION_DETAILS,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        return res

    def check_tenant_status(self, tenant_name: str, region: str,
                            force_activate: bool = None, sync: bool = True,
                            secure_parameters=None, is_flat_request=None,
                            compressed: bool = False) -> dict:
        params = {
            'tenantName': tenant_name,
            'region': region,
        }

        if force_activate:
            params.update({'forceActivate': force_activate})

        res = self._client.execute(
            command_name=CHECK_TENANT_STATUS,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        return res
