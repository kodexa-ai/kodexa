# kodexa.client.ChannelsApi

All URIs are relative to *https://lehua.kodexa.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_channel**](ChannelsApi.md#create_channel) | **POST** /api/channels | 
[**delete_channel**](ChannelsApi.md#delete_channel) | **DELETE** /api/channels/{id} | 
[**get_channel**](ChannelsApi.md#get_channel) | **GET** /api/channels/{id} | 
[**list_channel**](ChannelsApi.md#list_channel) | **GET** /api/channels | 
[**reindex_channel**](ChannelsApi.md#reindex_channel) | **PUT** /api/channels/_reindex | 
[**update_channel**](ChannelsApi.md#update_channel) | **PUT** /api/channels/{id} | 


# **create_channel**
> ChannelMetadata create_channel(channel_metadata)



Create a new instance of the resource

### Example

```python
import time
import kodexa.client
from kodexa.client.api import channels_api
from kodexa.client.model.channel_metadata import ChannelMetadata
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = channels_api.ChannelsApi(api_client)
    channel_metadata = ChannelMetadata(
        id="id_example",
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
        metadata=Channel(
            id="id_example",
        ),
    ) # ChannelMetadata | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_channel(channel_metadata)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ChannelsApi->create_channel: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **channel_metadata** | [**ChannelMetadata**](ChannelMetadata.md)|  |

### Return type

[**ChannelMetadata**](ChannelMetadata.md)

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

# **delete_channel**
> delete_channel(id)



Delete the resource with the provided ID

### Example

```python
import time
import kodexa.client
from kodexa.client.api import channels_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = channels_api.ChannelsApi(api_client)
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_channel(id)
    except kodexa.client.ApiException as e:
        print("Exception when calling ChannelsApi->delete_channel: %s\n" % e)
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

# **get_channel**
> ChannelMetadata get_channel(id)



Get a resource with the provided ID

### Example

```python
import time
import kodexa.client
from kodexa.client.api import channels_api
from kodexa.client.model.channel_metadata import ChannelMetadata
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = channels_api.ChannelsApi(api_client)
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_channel(id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ChannelsApi->get_channel: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |

### Return type

[**ChannelMetadata**](ChannelMetadata.md)

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

# **list_channel**
> PageChannelMetadata list_channel(query_context)



List a page of the resources

### Example

```python
import time
import kodexa.client
from kodexa.client.api import channels_api
from kodexa.client.model.page_channel_metadata import PageChannelMetadata
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
    api_instance = channels_api.ChannelsApi(api_client)
    query_context = QueryContext(
        page_size__default_20=1,
        page_number__default_1=1,
        sorts_to_apply="sorts_to_apply_example",
        simple_filter_to_apply="simple_filter_to_apply_example",
    ) # QueryContext | 
    query = "*" # str |  (optional) if omitted the server will use the default value of "*"

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.list_channel(query_context)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ChannelsApi->list_channel: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.list_channel(query_context, query=query)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ChannelsApi->list_channel: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query_context** | **QueryContext**|  |
 **query** | **str**|  | [optional] if omitted the server will use the default value of "*"

### Return type

[**PageChannelMetadata**](PageChannelMetadata.md)

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

# **reindex_channel**
> reindex_channel()



Re-index the resource

### Example

```python
import time
import kodexa.client
from kodexa.client.api import channels_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = channels_api.ChannelsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        api_instance.reindex_channel()
    except kodexa.client.ApiException as e:
        print("Exception when calling ChannelsApi->reindex_channel: %s\n" % e)
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

# **update_channel**
> ChannelMetadata update_channel(id, channel_metadata)



Update the given instance

### Example

```python
import time
import kodexa.client
from kodexa.client.api import channels_api
from kodexa.client.model.channel_metadata import ChannelMetadata
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = channels_api.ChannelsApi(api_client)
    id = "id_example" # str | 
    channel_metadata = ChannelMetadata(
        id="id_example",
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
        metadata=Channel(
            id="id_example",
        ),
    ) # ChannelMetadata | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_channel(id, channel_metadata)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ChannelsApi->update_channel: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **channel_metadata** | [**ChannelMetadata**](ChannelMetadata.md)|  |

### Return type

[**ChannelMetadata**](ChannelMetadata.md)

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

