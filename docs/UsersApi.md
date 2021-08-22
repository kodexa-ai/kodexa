# kodexa.client.UsersApi

All URIs are relative to *https://lehua.kodexa.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**activate**](UsersApi.md#activate) | **PUT** /api/users/{id}/activate | 
[**create**](UsersApi.md#create) | **POST** /api/users | 
[**deactivate**](UsersApi.md#deactivate) | **PUT** /api/users/{id}/deactivate | 
[**delete**](UsersApi.md#delete) | **DELETE** /api/users/{id} | 
[**get**](UsersApi.md#get) | **GET** /api/users/{id} | 
[**list**](UsersApi.md#list) | **GET** /api/users | 
[**reindex**](UsersApi.md#reindex) | **PUT** /api/users/_reindex | 
[**set_password**](UsersApi.md#set_password) | **PUT** /api/users/{id}/password | 
[**update**](UsersApi.md#update) | **PUT** /api/users/{id} | 


# **activate**
> User activate(id)



Activate user (admin only)

### Example

```python
import time
import kodexa.client
from kodexa.client.api import users_api
from kodexa.client.model.user import User
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = users_api.UsersApi(api_client)
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.activate(id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling UsersApi->activate: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create**
> User create(user)



Create a new instance of the resource

### Example

```python
import time
import kodexa.client
from kodexa.client.api import users_api
from kodexa.client.model.user import User
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = users_api.UsersApi(api_client)
    user = User(
        id="id_example",
        uuid="uuid_example",
        created_on=dateutil_parser('1970-01-01T00:00:00.00Z'),
        updated_on=dateutil_parser('1970-01-01T00:00:00.00Z'),
        created_by="created_by_example",
        updated_by="updated_by_example",
        email="email_example",
        first_name="first_name_example",
        last_name="last_name_example",
        activated=True,
        platform_admin=True,
        password_reset_date=dateutil_parser('1970-01-01T00:00:00.00Z'),
        last_connected=dateutil_parser('1970-01-01T00:00:00.00Z'),
        user_storage=UserStorage(
            favorite_links=[
                FavoriteLink(
                    link="link_example",
                ),
            ],
        ),
    ) # User | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create(user)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling UsersApi->create: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | [**User**](User.md)|  |

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**401** | You are not authorized to view the resource |  -  |
**403** | Accessing the resource you were trying to reach forbidden |  -  |
**500** | An internal exception has occurred, check the logs for more information |  -  |
**404** | The resource you were trying to reach not found |  -  |
**200** | Successfully created the new resource |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deactivate**
> User deactivate(id)



De-activate user (admin only)

### Example

```python
import time
import kodexa.client
from kodexa.client.api import users_api
from kodexa.client.model.user import User
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = users_api.UsersApi(api_client)
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.deactivate(id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling UsersApi->deactivate: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete**
> delete(id)



Delete the resource with the provided ID

### Example

```python
import time
import kodexa.client
from kodexa.client.api import users_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = users_api.UsersApi(api_client)
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete(id)
    except kodexa.client.ApiException as e:
        print("Exception when calling UsersApi->delete: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**403** | Accessing the resource you were trying to reach forbidden |  -  |
**500** | An internal exception has occurred, check the logs for more information |  -  |
**404** | The resource you were trying to reach not found |  -  |
**401** | You are not authorized to delete the resource |  -  |
**200** | Successfully deleted the resource |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get**
> User get(id)



Get a resource with the provided ID

### Example

```python
import time
import kodexa.client
from kodexa.client.api import users_api
from kodexa.client.model.user import User
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = users_api.UsersApi(api_client)
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get(id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling UsersApi->get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**403** | Accessing the resource you were trying to reach forbidden |  -  |
**500** | An internal exception has occurred, check the logs for more information |  -  |
**404** | The resource you were trying to reach not found |  -  |
**401** | You are not authorized to get the resource |  -  |
**200** | Successfully got the resource |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list**
> PageUser list(query_context)



List a page of the resources

### Example

```python
import time
import kodexa.client
from kodexa.client.api import users_api
from kodexa.client.model.page_user import PageUser
from kodexa.client.model.query_context import QueryContext
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = users_api.UsersApi(api_client)
    query_context = QueryContext(
        page_size__default_20=1,
        page_number__default_1=1,
        sorts_to_apply="sorts_to_apply_example",
        simple_filter_to_apply="simple_filter_to_apply_example",
    ) # QueryContext | 
    query = "*" # str |  (optional) if omitted the server will use the default value of "*"

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.list(query_context)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling UsersApi->list: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.list(query_context, query=query)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling UsersApi->list: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query_context** | **QueryContext**|  |
 **query** | **str**|  | [optional] if omitted the server will use the default value of "*"

### Return type

[**PageUser**](PageUser.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**403** | Accessing the resource you were trying to reach forbidden |  -  |
**500** | An internal exception has occurred, check the logs for more information |  -  |
**401** | You are not authorized to list the resource |  -  |
**404** | The resource you were trying to reach not found |  -  |
**200** | Successfully listed the resource |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **reindex**
> reindex()



Re-index the resource

### Example

```python
import time
import kodexa.client
from kodexa.client.api import users_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = users_api.UsersApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        api_instance.reindex()
    except kodexa.client.ApiException as e:
        print("Exception when calling UsersApi->reindex: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_password**
> User set_password(id, complete_password_reset)



Update users password (admin only)

### Example

```python
import time
import kodexa.client
from kodexa.client.api import users_api
from kodexa.client.model.complete_password_reset import CompletePasswordReset
from kodexa.client.model.user import User
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = users_api.UsersApi(api_client)
    id = "id_example" # str | 
    complete_password_reset = CompletePasswordReset(
        reset_token="reset_token_example",
        password="password_example",
    ) # CompletePasswordReset | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.set_password(id, complete_password_reset)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling UsersApi->set_password: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **complete_password_reset** | [**CompletePasswordReset**](CompletePasswordReset.md)|  |

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update**
> User update(id, user)



Update the given instance

### Example

```python
import time
import kodexa.client
from kodexa.client.api import users_api
from kodexa.client.model.user import User
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = users_api.UsersApi(api_client)
    id = "id_example" # str | 
    user = User(
        id="id_example",
        uuid="uuid_example",
        created_on=dateutil_parser('1970-01-01T00:00:00.00Z'),
        updated_on=dateutil_parser('1970-01-01T00:00:00.00Z'),
        created_by="created_by_example",
        updated_by="updated_by_example",
        email="email_example",
        first_name="first_name_example",
        last_name="last_name_example",
        activated=True,
        platform_admin=True,
        password_reset_date=dateutil_parser('1970-01-01T00:00:00.00Z'),
        last_connected=dateutil_parser('1970-01-01T00:00:00.00Z'),
        user_storage=UserStorage(
            favorite_links=[
                FavoriteLink(
                    link="link_example",
                ),
            ],
        ),
    ) # User | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update(id, user)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling UsersApi->update: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **user** | [**User**](User.md)|  |

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully updated the resource |  -  |
**403** | Accessing the resource you were trying to reach forbidden |  -  |
**500** | An internal exception has occurred, check the logs for more information |  -  |
**401** | You are not authorized to updated the resource |  -  |
**404** | The resource you were trying to reach not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

