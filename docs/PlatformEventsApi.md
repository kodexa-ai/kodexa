# kodexa.client.PlatformEventsApi

All URIs are relative to *https://lehua.kodexa.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_event**](PlatformEventsApi.md#get_event) | **GET** /api/events/{organizationSlug}/{id} | 
[**list_platform_event**](PlatformEventsApi.md#list_platform_event) | **GET** /api/events/{organizationSlug} | 
[**reindex_platform_event**](PlatformEventsApi.md#reindex_platform_event) | **POST** /api/events/{organizationSlug}/_reindex | 


# **get_event**
> PlatformEvent get_event(organization_slug, id)



Get event with specified ID in organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import platform_events_api
from kodexa.client.model.platform_event import PlatformEvent
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = platform_events_api.PlatformEventsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_event(organization_slug, id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling PlatformEventsApi->get_event: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **id** | **str**|  |

### Return type

[**PlatformEvent**](PlatformEvent.md)

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

# **list_platform_event**
> PagePlatformEvent list_platform_event(organization_slug, query_context)



Get paginated list of the events in a specific organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import platform_events_api
from kodexa.client.model.page_platform_event import PagePlatformEvent
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
    api_instance = platform_events_api.PlatformEventsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    query_context = QueryContext(
        page_size__default_20=1,
        page_number__default_1=1,
        sorts_to_apply="sorts_to_apply_example",
        simple_filter_to_apply="simple_filter_to_apply_example",
    ) # QueryContext | 
    query = "*" # str |  (optional) if omitted the server will use the default value of "*"

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.list_platform_event(organization_slug, query_context)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling PlatformEventsApi->list_platform_event: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.list_platform_event(organization_slug, query_context, query=query)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling PlatformEventsApi->list_platform_event: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **query_context** | **QueryContext**|  |
 **query** | **str**|  | [optional] if omitted the server will use the default value of "*"

### Return type

[**PagePlatformEvent**](PagePlatformEvent.md)

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

# **reindex_platform_event**
> reindex_platform_event(organization_slug)



### Example

```python
import time
import kodexa.client
from kodexa.client.api import platform_events_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = platform_events_api.PlatformEventsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.reindex_platform_event(organization_slug)
    except kodexa.client.ApiException as e:
        print("Exception when calling PlatformEventsApi->reindex_platform_event: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |

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

