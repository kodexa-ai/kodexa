# kodexa.client.AccessTokensApi

All URIs are relative to *https://lehua.kodexa.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_access_token**](AccessTokensApi.md#create_access_token) | **POST** /api/accessTokens | 
[**delete_access_token**](AccessTokensApi.md#delete_access_token) | **DELETE** /api/accessTokens/{id} | 
[**get_access_token**](AccessTokensApi.md#get_access_token) | **GET** /api/accessTokens/{id} | 
[**list_access_token**](AccessTokensApi.md#list_access_token) | **GET** /api/accessTokens | 
[**reindex_access_token**](AccessTokensApi.md#reindex_access_token) | **PUT** /api/accessTokens/_reindex | 
[**update_access_token**](AccessTokensApi.md#update_access_token) | **PUT** /api/accessTokens/{id} | 


# **create_access_token**
> AccessToken create_access_token(access_token)



Create a new instance of the resource

### Example

```python
import time
import kodexa.client
from kodexa.client.api import access_tokens_api
from kodexa.client.model.access_token import AccessToken
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = access_tokens_api.AccessTokensApi(api_client)
    access_token = AccessToken(
        id="id_example",
        uuid="uuid_example",
        created_on=dateutil_parser('1970-01-01T00:00:00.00Z'),
        updated_on=dateutil_parser('1970-01-01T00:00:00.00Z'),
        created_by="created_by_example",
        updated_by="updated_by_example",
        name="name_example",
        token="token_example",
        organization=Organization(
            id="id_example",
            uuid="uuid_example",
            created_on=dateutil_parser('1970-01-01T00:00:00.00Z'),
            updated_on=dateutil_parser('1970-01-01T00:00:00.00Z'),
            created_by="created_by_example",
            updated_by="updated_by_example",
            name="name_example",
            slug="zBAMDTMv2D2ylmgd10Z3UB6UkJSIS",
            public_access=True,
            description="description_example",
        ),
    ) # AccessToken | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_access_token(access_token)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AccessTokensApi->create_access_token: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **access_token** | [**AccessToken**](AccessToken.md)|  |

### Return type

[**AccessToken**](AccessToken.md)

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

# **delete_access_token**
> delete_access_token(id)



Delete the resource with the provided ID

### Example

```python
import time
import kodexa.client
from kodexa.client.api import access_tokens_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = access_tokens_api.AccessTokensApi(api_client)
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_access_token(id)
    except kodexa.client.ApiException as e:
        print("Exception when calling AccessTokensApi->delete_access_token: %s\n" % e)
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

# **get_access_token**
> AccessToken get_access_token(id)



Get a resource with the provided ID

### Example

```python
import time
import kodexa.client
from kodexa.client.api import access_tokens_api
from kodexa.client.model.access_token import AccessToken
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = access_tokens_api.AccessTokensApi(api_client)
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_access_token(id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AccessTokensApi->get_access_token: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |

### Return type

[**AccessToken**](AccessToken.md)

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

# **list_access_token**
> PageAccessToken list_access_token(query_context)



List a page of the resources

### Example

```python
import time
import kodexa.client
from kodexa.client.api import access_tokens_api
from kodexa.client.model.page_access_token import PageAccessToken
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
    api_instance = access_tokens_api.AccessTokensApi(api_client)
    query_context = QueryContext(
        page_size__default_20=1,
        page_number__default_1=1,
        sorts_to_apply="sorts_to_apply_example",
        simple_filter_to_apply="simple_filter_to_apply_example",
    ) # QueryContext | 
    query = "*" # str |  (optional) if omitted the server will use the default value of "*"

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.list_access_token(query_context)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AccessTokensApi->list_access_token: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.list_access_token(query_context, query=query)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AccessTokensApi->list_access_token: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query_context** | **QueryContext**|  |
 **query** | **str**|  | [optional] if omitted the server will use the default value of "*"

### Return type

[**PageAccessToken**](PageAccessToken.md)

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

# **reindex_access_token**
> reindex_access_token()



Re-index the resource

### Example

```python
import time
import kodexa.client
from kodexa.client.api import access_tokens_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = access_tokens_api.AccessTokensApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        api_instance.reindex_access_token()
    except kodexa.client.ApiException as e:
        print("Exception when calling AccessTokensApi->reindex_access_token: %s\n" % e)
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

# **update_access_token**
> AccessToken update_access_token(id, access_token)



Update the given instance

### Example

```python
import time
import kodexa.client
from kodexa.client.api import access_tokens_api
from kodexa.client.model.access_token import AccessToken
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = access_tokens_api.AccessTokensApi(api_client)
    id = "id_example" # str | 
    access_token = AccessToken(
        id="id_example",
        uuid="uuid_example",
        created_on=dateutil_parser('1970-01-01T00:00:00.00Z'),
        updated_on=dateutil_parser('1970-01-01T00:00:00.00Z'),
        created_by="created_by_example",
        updated_by="updated_by_example",
        name="name_example",
        token="token_example",
        organization=Organization(
            id="id_example",
            uuid="uuid_example",
            created_on=dateutil_parser('1970-01-01T00:00:00.00Z'),
            updated_on=dateutil_parser('1970-01-01T00:00:00.00Z'),
            created_by="created_by_example",
            updated_by="updated_by_example",
            name="name_example",
            slug="zBAMDTMv2D2ylmgd10Z3UB6UkJSIS",
            public_access=True,
            description="description_example",
        ),
    ) # AccessToken | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_access_token(id, access_token)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AccessTokensApi->update_access_token: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **access_token** | [**AccessToken**](AccessToken.md)|  |

### Return type

[**AccessToken**](AccessToken.md)

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

