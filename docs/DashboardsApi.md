# kodexa.client.DashboardsApi

All URIs are relative to *https://lehua.kodexa.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_connector**](DashboardsApi.md#create_connector) | **POST** /api/dashboards/{organizationSlug} | 
[**delete_connector**](DashboardsApi.md#delete_connector) | **DELETE** /api/dashboards/{organizationSlug}/{slug} | 
[**delete_version_connector**](DashboardsApi.md#delete_version_connector) | **DELETE** /api/dashboards/{organizationSlug}/{slug}/{version} | 
[**get_connector**](DashboardsApi.md#get_connector) | **GET** /api/dashboards/{organizationSlug}/{slug} | 
[**get_version_connector**](DashboardsApi.md#get_version_connector) | **GET** /api/dashboards/{organizationSlug}/{slug}/{version} | 
[**list_connector**](DashboardsApi.md#list_connector) | **GET** /api/dashboards/{organizationSlug} | 
[**update_connector**](DashboardsApi.md#update_connector) | **PUT** /api/dashboards/{organizationSlug}/{slug} | 
[**update_version_connector**](DashboardsApi.md#update_version_connector) | **PUT** /api/dashboards/{organizationSlug}/{slug}/{version} | 


# **create_connector**
> Dashboard create_connector(organization_slug, dashboard)



Create a new instance of the object in the organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import dashboards_api
from kodexa.client.model.dashboard import Dashboard
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = dashboards_api.DashboardsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    dashboard = Dashboard() # Dashboard | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_connector(organization_slug, dashboard)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling DashboardsApi->create_connector: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **dashboard** | [**Dashboard**](Dashboard.md)|  |

### Return type

[**Dashboard**](Dashboard.md)

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

# **delete_connector**
> bool delete_connector(organization_slug, slug)



Delete the current version of the given object

### Example

```python
import time
import kodexa.client
from kodexa.client.api import dashboards_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = dashboards_api.DashboardsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.delete_connector(organization_slug, slug)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling DashboardsApi->delete_connector: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |

### Return type

**bool**

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

# **delete_version_connector**
> bool delete_version_connector(organization_slug, slug, version)



Delete the specified version of the given object

### Example

```python
import time
import kodexa.client
from kodexa.client.api import dashboards_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = dashboards_api.DashboardsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.delete_version_connector(organization_slug, slug, version)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling DashboardsApi->delete_version_connector: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |

### Return type

**bool**

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

# **get_connector**
> Dashboard get_connector(organization_slug, slug)



Get the current version of the object with given slug

### Example

```python
import time
import kodexa.client
from kodexa.client.api import dashboards_api
from kodexa.client.model.dashboard import Dashboard
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = dashboards_api.DashboardsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_connector(organization_slug, slug)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling DashboardsApi->get_connector: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |

### Return type

[**Dashboard**](Dashboard.md)

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

# **get_version_connector**
> Dashboard get_version_connector(organization_slug, slug, version)



Get the specific version of the object with given slug

### Example

```python
import time
import kodexa.client
from kodexa.client.api import dashboards_api
from kodexa.client.model.dashboard import Dashboard
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = dashboards_api.DashboardsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_version_connector(organization_slug, slug, version)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling DashboardsApi->get_version_connector: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |

### Return type

[**Dashboard**](Dashboard.md)

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

# **list_connector**
> PageDashboard list_connector(organization_slug)



Get a paginated list of the objects for an organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import dashboards_api
from kodexa.client.model.page_dashboard import PageDashboard
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = dashboards_api.DashboardsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    query = "*" # str |  (optional) if omitted the server will use the default value of "*"
    include_public = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.list_connector(organization_slug)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling DashboardsApi->list_connector: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.list_connector(organization_slug, query=query, include_public=include_public)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling DashboardsApi->list_connector: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **query** | **str**|  | [optional] if omitted the server will use the default value of "*"
 **include_public** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**PageDashboard**](PageDashboard.md)

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

# **update_connector**
> Dashboard update_connector(organization_slug, slug, dashboard)



Update the current version object with given slug in the organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import dashboards_api
from kodexa.client.model.dashboard import Dashboard
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = dashboards_api.DashboardsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    dashboard = Dashboard() # Dashboard | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_connector(organization_slug, slug, dashboard)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling DashboardsApi->update_connector: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |
 **dashboard** | [**Dashboard**](Dashboard.md)|  |

### Return type

[**Dashboard**](Dashboard.md)

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

# **update_version_connector**
> Dashboard update_version_connector(organization_slug, slug, version, dashboard)



Update the object with given slug and version in the organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import dashboards_api
from kodexa.client.model.dashboard import Dashboard
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = dashboards_api.DashboardsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    dashboard = Dashboard() # Dashboard | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_version_connector(organization_slug, slug, version, dashboard)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling DashboardsApi->update_version_connector: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **dashboard** | [**Dashboard**](Dashboard.md)|  |

### Return type

[**Dashboard**](Dashboard.md)

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

