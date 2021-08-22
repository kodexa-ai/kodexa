# kodexa.client.PlatformOverviewApi

All URIs are relative to *https://lehua.kodexa.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_overview**](PlatformOverviewApi.md#get_overview) | **GET** /api | 


# **get_overview**
> PlatformOverview get_overview()



Get platform overview information

### Example

```python
import time
import kodexa.client
from kodexa.client.api import platform_overview_api
from kodexa.client.model.platform_overview import PlatformOverview
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = platform_overview_api.PlatformOverviewApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        api_response = api_instance.get_overview()
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling PlatformOverviewApi->get_overview: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**PlatformOverview**](PlatformOverview.md)

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

