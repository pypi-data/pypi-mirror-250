# Maestro-python-sdk

`The 'Maestro Python SDK'` is an SDK created for facilitating  the communication with Maestro for all Pythonic components including: WSBA, SFTA, Consumption Module, Automover BA etc.

Contents
========
    
 * [Requirements](#requirements)
 * [Installation and configuration](#installation)
 * [Usage](#usage)
 * [Examples](#examples)

# Requirements
> Python 3.10 required

# Installation

> First of all you need to install m3-python-sdk to your project, you can use next command to do it:
- `pip install maestro-python-sdk`

> After you installed maestro-python-sdk to your project, you should set ENV variables,
> this step is optional, because you would be able to pass those params while creating instances, but we highly recommend you to do this, because it will make your use more pleasant and flexible, and also such a method is more secure.
 - SDK_ACCESS_KEY,
 - SDK_SECRET_KEY,
 - MAESTRO_USER,
> This is first required variables you should set, the following variables depend on the way you will be using the SDK.
 
### `Rabbit`
 - RABBIT_EXCHANGE, 
 - DEFAULT_MAESTRO_REQUEST_QUEUE, DEFAULT_MAESTRO_RESPONSE_QUEUE, 
 - DEFAULT_ADMIN_REQUEST_QUEUE, DEFAULT_ADMIN_RESPONSE_QUEUE,
 - DEFAULT_KPI_REQUEST_QUEUE, DEFAULT_KPI_RESPONSE_QUEUE  
### `HTTP`
 - API_LINK


# USAGE

To start using Maestro Python SDK you need to create either an HTTP client or a RabbitMQ client. The difference between them is not significant. If you need to send asynchronous requests, use only the RabbitMQ client, as it is the only one that supports such functionality. In other cases, use whichever is more convenient for you.

## RabbiMQ

**There are two ways to create RabbitMQ client:**

+ Create client using ```__init__``` method of a RabbitMqStrategy class:
+ Create client using ```build``` method of a RabbitMqStrategy class:

### ```__init__``` method Example
>Step 1: Create a RabbitMqStrategy object. This step requires the following information: rabbit connection url for maestro server, your personal sdk access and secret keys, maestro user and names of rabbit queues, more information about parameters is described inside RabbitMqStrategy class. Below is an example of how to create a client:
1. ```python 
   from m3_python_sdk.strategies.rabbitmq import RabbitMqStrategy
   rabbit_client = RabbitMqStrategy(
        connection_url='<connection url>',
        request_queue='<request_queue>',
        response_queue='<response_queue>',
        sdk_access_key='<sdk_access_key>',
        sdk_secret_key='<sdk_secret_key>',
        maestro_user='<maestro_user>'
   )
   # For your information, request/response queues, sdk keys and maestro user
   # could be set as ENV varibles, if you dont provide them while creating class,
   # they would be searched in env variables automatically.

>Step 2: If you provided sdk with correct credentials and parameters you are good to go to use SDK. An examples is provided in the "Examples" topic.

### ```BUILD``` method Example
>Step 1: Create a RabbitMqStrategy object. This step requires the following information: host, username and password, stage, amqps and everything that takes basic __init__ method. Below is an example of how to create a client:
1. ```python 
   rabbit_client = RabbitMqStrategy(
        host='<host123.eu.amazon>',
        stage='<mstrdev>',
        username='<username>',
        password='<password>',
        request_queue='<request_queue>',
        response_queue='<response_queue>',
        sdk_access_key='<sdk_access_key>',
        sdk_secret_key='<sdk_secret_key>',
        maestro_user='<maestro_user>'
   )
   
   #as result you will get next rabbit_url:  
    'amqps://username:password@host123.eu.amazon:5671/mstrdev'
   
   # For your information, request/response queues, sdk keys and maestro user'
   # could be set as ENV varibles, if you dont provide them while creating class,
   # they would be searched in env variables automatically.


> Step 2: If you provided sdk with correct credentials and parameters you are good to go to use SDK. An examples is provided in the "Examples" topic.
> Now that you have created the client, you can use it to interact with the SDK. An example is provided in the "Examples" topic.


## HTTP

**There are two ways to create HTTP client:**

+ Create client using ```__init__``` method of a HTTPStrategy class:
+ Create client using ```build``` method of a HTTPStrategy class:

### ```__init__``` method Example
>Step 1: Create a HTTPStrategy object. This step requires the following information: api_link for maestro server, your personal sdk access and secret keys and maestro user, more information about parameters is described inside HTTPStrategy class. Below is an example of how to create a client:
1. ```python 
   from m3_python_sdk.strategies.http import HTTPStrategy
   http_client = HTTPStrategy(
        api_link='<api link>',
        sdk_access_key='<sdk_access_key>',
        sdk_secret_key='<sdk_secret_key>',
        maestro_user='<maestro_user>'
   )
   # For your information, sdk keys and maestro user could be set as ENV varibles,
   # if you dont provide them while creating class,
   # they would be searched in env variables automatically.
   # Namings for ENV variables:

>Step 2: If you provided sdk with correct credentials and parameters you are good to go to use SDK. An examples is provided in the "Examples" topic.

### ```BUILD``` method Example
>Step 1: Create a HTTPStrategy object. This step requires the following information: host, port, stage, htpps, and everything that takes basic __init__ method except api_link. Below is an example of how to create a client:
1. ```python 
   http_client = HTTPStrategy(
        host='<m3.cloud.com>',
        stage='<maestro/api/v3>',
        port='8000',
        https='True',
        sdk_access_key='<sdk_access_key>',
        sdk_secret_key='<sdk_secret_key>',
        maestro_user='<maestro_user>'
   )
   
   #as result you will get next api_link:  
    https://m3.cloud.com:8000/maestro/api/v3
   
   # For your information, request/response queues, sdk keys and maestro user'
   # could be set as ENV varibles, if you dont provide them while creating class,
   # they would be searched in env variables automatically.
   # SDK_ACCESS_KEY, SDK_SECRET_KEY, MAESTRO_USER, API_LINK

> Step 2: If you provided sdk with correct credentials and parameters you are good to go to use SDK. An examples is provided in the "Examples" topic.
> Now that you have created the client, you can use it to interact with the SDK. An example is provided in the "Examples" topic.
> 
## EXAMPLES

> When you create a basic HTTP ot RabbitMQ clients using one of provided ways, you can use it to call some methods.
>
> In general, methods are separated into next categories:
> - Consumptions
>   - add_consumption
>   - get_consumption
>   - delete_consumption
>   - add_consumption_details
>   - get_consumption_details
>   - delete_consumption_details
>   - check_tenant_status
> - Adjustments
>   - add_adjustment
>   - get_adjustment
>   - delete_adjustment
>   - total_report
> - Billing
>   - describe_billing_month
>   - describe_currency
>   - get_top_account_reports
>   - add_cost_center
>   - archive_big_query
>   - billing_configure


> Here are examples of how to call one method from each category.

> 1. ```python
>    # You need to create Http ot Rabbit client, after that create ConsumptionResource class object and pass your client inside init method
>    from m3_python_sdk.strategies.http import HttpStrategy
>    from m3_python_sdk.resources.consumption.consumption import ConsumptionResource
>    http = HttpStrategy(#the example is given above.)
>    consumption = ConsumptionResource(client=http)
>    consumption.get_consumption(
>           source_project='example',
>           target_project='example',
>           target_region='example',
>           year=example,
>           month=example,
>           description='example'
>    )
>    
>    response: {'status_code': status_code, 'status': status, 'message': message}
>    # Remember that response could also have next params: data, items, table_title, warnings, code

> 2. ```python
>    # You need to create Http ot Rabbit client, after that create AdjustmentResource class object and pass your client inside init method
>    from m3_python_sdk.strategies.rabbitmq import RabbitMqStrategy
>    from m3_python_sdk.resources.consumption.adjustment import AdjustmentResource
>    rabbit = RabbitMqStrategy(#the example is given above.)
>    adjustment = AdjustmentResource(client=rabbit)
>    adjustment.get_adjustment(
>           target_project='example',
>           target_account_number='example',
>           target_region='example',
>           #target_cloud='example',
>           month='example',
>           year='example',
>           description='example',
>           credit_type='example',
>           currency_native='example',
>           value='example'
>    )
>    
>    response: {'status_code': status_code, 'status': status, 'message': message}
>    # Remember that response could also have next params: data, items, table_title, warnings, code

> 3. ```python
>    # You need to create Http ot Rabbit client, after that create BillingResource class object and pass your client inside init method
>    ## Also if you already have some strategy created and you used it for consumptions or adjustment, you need to change Queues using properties.
>    from m3_python_sdk.strategies.rabbitmq import RabbitMqStrategy
>    from m3_python_sdk.resources.billing.billing import BillingResource
>    rabbit = RabbitMqStrategy(#the example is given above.)
>    billing = BillingResource(client=rabbit)
>    billing.describe_billing_month(year=2023, month=11)
>    
>    response: {'status_code': status_code, 'status': status, 'message': message}
>    # Remember that response could also have next params: data, items, table_title, warnings, code

##### Remember, the full list of endpoints can be found inside the consumption.py, adjustment.py and billing.py files. Additionally, greater amount of the endpoints can accept additional arguments, which can also be found inside those files.



