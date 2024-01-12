import unittest
from datetime import datetime

from m3_python_sdk.resources.billing.billing import BillingResource
from m3_python_sdk.resources.consumption.adjustment import AdjustmentResource
from m3_python_sdk.resources.consumption.consumption import ConsumptionResource
from m3_python_sdk.utils.constants import SdkCloud
from tests.services.s3_service import S3Client
from tests.strategies.contract_strategy import ContractStrategy


class TestConsumptionResource(unittest.TestCase):

    def setUp(self) -> None:
        contract_strategy = ContractStrategy()
        self.consumption = ConsumptionResource(client=contract_strategy)
        self.adjustment = AdjustmentResource(client=contract_strategy)

        s3_client = S3Client()
        self.billing = BillingResource(
            client=contract_strategy
        )

        now = datetime.now()

        self.current_year = now.year
        self.current_month = now.month

    def test_add_consumption_project(self):
        self.consumption.add_consumption(
            source_project='EPM-CIT2',
            target_project='EPM-TAR',
            target_region='AZURE-PAAS',
            year=self.current_year,
            month=self.current_month,
            value=0.01,
            description='Added by autotest for EPM-CIT2 tenant for AZURE-PAAS'
        )

    def test_add_consumption_account(self):
        self.consumption.add_consumption(
            source_account_number='9d6cfeed-c793-4190-90cc-5ec066a3b4e6',
            target_account_number='EPM-TAR',
            service_name='AmazonS3',
            target_region='AZURE-PAAS',
            year=self.current_year,
            month=self.current_month,
            value=0.01,
            description='Added by autotest for EPM-CIT2 tenant for AZURE-PAAS'
        )

    def test_get_consumption_project(self):

        self.consumption.get_consumption(
            source_project='EPM-CIT2',
            target_project='EPM-TAR',
            target_region='AZURE-PAAS',
            year=self.current_year,
            month=self.current_month,
            description='Added by autotest for EPM-CIT2 tenant for AZURE-PAAS'
        )

    def test_get_consumption_account(self):

        self.consumption.get_consumption(
            source_account_number='9d6cfeed-c793-4190-90cc-5ec066a3b4e6',
            target_account_number='EPM-TAR',
            service_name='AmazonS3',
            target_region='AZURE-PAAS',
            year=self.current_year,
            month=self.current_month,
            description='Added by autotest for EPM-CIT2 tenant for AZURE-PAAS'
        )

    def test_delete_consumption_project(self):

        self.consumption.delete_consumption(
            source_project='EPM-CIT2',
            target_project='EPM-TAR',
            target_region='AZURE-PAAS',
            year=self.current_year,
            month=self.current_month,
            description='Added by autotest for EPM-CIT2 tenant for AZURE-PAAS'
        )

    def test_delete_consumption_account(self):

        self.consumption.delete_consumption(
            source_account_number='9d6cfeed-c793-4190-90cc-5ec066a3b4e6',
            target_account_number='EPM-TAR',
            service_name='AmazonS3',
            target_region='AZURE-PAAS',
            year=self.current_year,
            month=self.current_month,
            description='Added by autotest for EPM-CIT2 tenant for AZURE-PAAS'
        )

    def test_add_consumption_details_project_region(self):

        self.consumption.add_consumption_details(
            target_project='EPM-CIT2',
            target_region='AWS-EUCENTRAL',
            day=1,
            year=self.current_year,
            month=self.current_month,
            product_name='maestro_diagnostics_test_kpi',
            kpi_name='Device Plan',
            amount=15,
            price=4,
            price_unit='plan-month',
            cost=100
        )

    def test_add_consumption_details_account_cloud(self):

        self.consumption.add_consumption_details(
            target_account_number='9d6cfeed-c793-4190-90cc-5ec066a3b4e6',
            target_cloud=SdkCloud.AZURE,
            day=1,
            year=self.current_year,
            month=self.current_month,
            product_name='maestro_diagnostics_test_kpi',
            kpi_name='Device Plan',
            amount=15,
            price=4,
            price_unit='plan-month',
            cost=100
        )

    def test_get_consumption_details_project_region(self):

        self.consumption.get_consumption_details(
            target_project='EPM-CIT2',
            target_region='AWS-EUCENTRAL',
            day=1,
            year=self.current_year,
            month=self.current_month
        )

    def test_get_consumption_details_account_cloud(self):

        self.consumption.get_consumption_details(
            target_account_number='9d6cfeed-c793-4190-90cc-5ec066a3b4e6',
            target_cloud=SdkCloud.AZURE,
            day=1,
            year=self.current_year,
            month=self.current_month
        )

    def test_delete_consumption_details_project_region(self):

        self.consumption.delete_consumption_details(
            target_project='EPM-CIT2',
            target_region='AWS-EUCENTRAL',
            day=1,
            year=self.current_year,
            month=self.current_month
        )

    def test_delete_consumption_details_account_cloud(self):

        self.consumption.delete_consumption_details(
            target_account_number='9d6cfeed-c793-4190-90cc-5ec066a3b4e6',
            target_cloud=SdkCloud.AZURE,
            day=1,
            year=self.current_year,
            month=self.current_month
        )

    def test_check_tenant_status(self):

        self.consumption.check_tenant_status(
            tenant_name='EPM-CIT2',
            region='AZURE-PASS',
            force_activate=True
        )

    def test_add_adjustment_project_region(self):

        self.adjustment.add_adjustment(
            target_project='EPM-CIT2',
            target_region='AWS-EUCENTRAL',
            year=self.current_year,
            month=self.current_month,
            description='Adjustment added by autotest for EPM-CIT2 tenant with'
                        ' PREPAYMENT type for AWS-EUCENTRAL',
            credit_type='PREPAYMENT',
            currency_native=False,
            value=-0.01
        )

    def test_add_adjustment_account_number_cloud(self):

        self.adjustment.add_adjustment(
            target_account_number='9d6cfeed-c793-4190-90cc-5ec066a3b4e6',
            target_cloud=SdkCloud.AZURE,
            year=self.current_year,
            month=self.current_month,
            description='Adjustment added by autotest for EPM-CIT2 tenant'
                        ' with PREPAYMENT type for AZURE',
            credit_type='PREPAYMENT',
            currency_native=False,
            value=-0.01
        )

    def test_get_adjustment_project_region(self):

        self.adjustment.get_adjustment(
            target_project='EPM-CIT2',
            target_region='AWS-EUCENTRAL',
            year=self.current_year,
            month=self.current_month,
            description='Adjustment added by autotest for EPM-CIT2 tenant with'
                        ' PREPAYMENT type for AWS-EUCENTRAL',
            credit_type='PREPAYMENT'
        )

    def test_get_adjustment_account_number_cloud(self):

        self.adjustment.get_adjustment(
            target_account_number='9d6cfeed-c793-4190-90cc-5ec066a3b4e6',
            target_cloud=SdkCloud.AZURE,
            year=self.current_year,
            month=self.current_month,
            description='Adjustment added by autotest for EPM-CIT2 tenant with'
                        ' PREPAYMENT type for AZURE',
            credit_type='PREPAYMENT'
        )

    def test_delete_adjustment_project_region(self):

        self.adjustment.delete_adjustment(
            target_project='EPM-CIT2',
            target_region='AWS-EUCENTRAL',
            year=self.current_year,
            month=self.current_month,
            description='Adjustment added by autotest for EPM-CIT2 tenant with'
                        ' PREPAYMENT type for AWS-EUCENTRAL',
            credit_type='PREPAYMENT'
        )

    def test_delete_adjustment_account_cloud(self):

        self.adjustment.delete_adjustment(
            target_account_number='9d6cfeed-c793-4190-90cc-5ec066a3b4e6',
            target_cloud=SdkCloud.AZURE,
            year=self.current_year,
            month=self.current_month,
            description='Adjustment added by autotest for EPM-CIT2 tenant with'
                        ' PREPAYMENT type for AZURE',
            credit_type='PREPAYMENT'
        )

    def test_total_report_tenant_cloud(self):

        self.adjustment.total_report(
            from_date=1698796800000,
            to_date=1701388800000,
            tenant='EPM-CIT2',
            cloud=[SdkCloud.AZURE, SdkCloud.AWS,
                   SdkCloud.OPEN_STACK, SdkCloud.GOOGLE],
            tag='autotest:checkQuotas',
        )

    def test_total_report_tenant_group_region(self):

        self.adjustment.total_report(
            from_date=1698796800000,
            to_date=1701388800000,
            tenant_group='EPM-CIT2',
            region='AWS-EUCENTRAL',
            report=False,
            grand_total=False
        )
