# kodexa.client.ConnectorsApi

All URIs are relative to *https://lehua.kodexa.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_dashboard**](ConnectorsApi.md#create_dashboard) | **POST** /api/connectors/{organizationSlug} | 
[**delete_dashboard**](ConnectorsApi.md#delete_dashboard) | **DELETE** /api/connectors/{organizationSlug}/{slug} | 
[**delete_version_dashboard**](ConnectorsApi.md#delete_version_dashboard) | **DELETE** /api/connectors/{organizationSlug}/{slug}/{version} | 
[**get_dashboard**](ConnectorsApi.md#get_dashboard) | **GET** /api/connectors/{organizationSlug}/{slug} | 
[**get_version_dashboard**](ConnectorsApi.md#get_version_dashboard) | **GET** /api/connectors/{organizationSlug}/{slug}/{version} | 
[**list_dashboard**](ConnectorsApi.md#list_dashboard) | **GET** /api/connectors/{organizationSlug} | 
[**update_dashboard**](ConnectorsApi.md#update_dashboard) | **PUT** /api/connectors/{organizationSlug}/{slug} | 
[**update_version_dashboard**](ConnectorsApi.md#update_version_dashboard) | **PUT** /api/connectors/{organizationSlug}/{slug}/{version} | 


# **create_dashboard**
> Connector create_dashboard(organization_slug, connector)



Create a new instance of the object in the organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import connectors_api
from kodexa.client.model.connector import Connector
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = connectors_api.ConnectorsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    connector = Connector() # Connector | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_dashboard(organization_slug, connector)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ConnectorsApi->create_dashboard: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **connector** | [**Connector**](Connector.md)|  |

### Return type

[**Connector**](Connector.md)

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

# **delete_dashboard**
> bool delete_dashboard(organization_slug, slug)



Delete the current version of the given object

### Example

```python
import time
import kodexa.client
from kodexa.client.api import connectors_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = connectors_api.ConnectorsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.delete_dashboard(organization_slug, slug)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ConnectorsApi->delete_dashboard: %s\n" % e)
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

# **delete_version_dashboard**
> bool delete_version_dashboard(organization_slug, slug, version)



Delete the specified version of the given object

### Example

```python
import time
import kodexa.client
from kodexa.client.api import connectors_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = connectors_api.ConnectorsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.delete_version_dashboard(organization_slug, slug, version)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ConnectorsApi->delete_version_dashboard: %s\n" % e)
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

# **get_dashboard**
> Connector get_dashboard(organization_slug, slug)



Get the current version of the object with given slug

### Example

```python
import time
import kodexa.client
from kodexa.client.api import connectors_api
from kodexa.client.model.connector import Connector
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = connectors_api.ConnectorsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_dashboard(organization_slug, slug)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ConnectorsApi->get_dashboard: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |

### Return type

[**Connector**](Connector.md)

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

# **get_version_dashboard**
> Connector get_version_dashboard(organization_slug, slug, version)



Get the specific version of the object with given slug

### Example

```python
import time
import kodexa.client
from kodexa.client.api import connectors_api
from kodexa.client.model.connector import Connector
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = connectors_api.ConnectorsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_version_dashboard(organization_slug, slug, version)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ConnectorsApi->get_version_dashboard: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |

### Return type

[**Connector**](Connector.md)

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

# **list_dashboard**
> PageConnector list_dashboard(organization_slug)



Get a paginated list of the objects for an organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import connectors_api
from kodexa.client.model.page_connector import PageConnector
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = connectors_api.ConnectorsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    query = "*" # str |  (optional) if omitted the server will use the default value of "*"
    include_public = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.list_dashboard(organization_slug)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ConnectorsApi->list_dashboard: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.list_dashboard(organization_slug, query=query, include_public=include_public)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ConnectorsApi->list_dashboard: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **query** | **str**|  | [optional] if omitted the server will use the default value of "*"
 **include_public** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**PageConnector**](PageConnector.md)

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

# **update_dashboard**
> Connector update_dashboard(organization_slug, slug, connector)



Update the current version object with given slug in the organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import connectors_api
from kodexa.client.model.connector import Connector
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = connectors_api.ConnectorsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    connector = Connector() # Connector | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_dashboard(organization_slug, slug, connector)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ConnectorsApi->update_dashboard: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |
 **connector** | [**Connector**](Connector.md)|  |

### Return type

[**Connector**](Connector.md)

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

# **update_version_dashboard**
> Connector update_version_dashboard(organization_slug, slug, version, connector)



Update the object with given slug and version in the organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import connectors_api
from kodexa.client.model.connector import Connector
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = connectors_api.ConnectorsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    connector = Connector() # Connector | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_version_dashboard(organization_slug, slug, version, connector)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ConnectorsApi->update_version_dashboard: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **connector** | [**Connector**](Connector.md)|  |

### Return type

[**Connector**](Connector.md)

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

