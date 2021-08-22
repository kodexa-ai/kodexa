# kodexa.client.ActionsApi

All URIs are relative to *https://lehua.kodexa.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_action**](ActionsApi.md#create_action) | **POST** /api/actions/{organizationSlug} | 
[**delete_action**](ActionsApi.md#delete_action) | **DELETE** /api/actions/{organizationSlug}/{slug} | 
[**delete_version_action**](ActionsApi.md#delete_version_action) | **DELETE** /api/actions/{organizationSlug}/{slug}/{version} | 
[**get_action**](ActionsApi.md#get_action) | **GET** /api/actions/{organizationSlug}/{slug} | 
[**get_version_action**](ActionsApi.md#get_version_action) | **GET** /api/actions/{organizationSlug}/{slug}/{version} | 
[**list_action**](ActionsApi.md#list_action) | **GET** /api/actions/{organizationSlug} | 
[**update_action**](ActionsApi.md#update_action) | **PUT** /api/actions/{organizationSlug}/{slug} | 
[**update_version_action**](ActionsApi.md#update_version_action) | **PUT** /api/actions/{organizationSlug}/{slug}/{version} | 


# **create_action**
> Action create_action(organization_slug, action)



Create a new instance of the object in the organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import actions_api
from kodexa.client.model.action import Action
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    action = Action() # Action | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_action(organization_slug, action)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ActionsApi->create_action: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **action** | [**Action**](Action.md)|  |

### Return type

[**Action**](Action.md)

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

# **delete_action**
> bool delete_action(organization_slug, slug)



Delete the current version of the given object

### Example

```python
import time
import kodexa.client
from kodexa.client.api import actions_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.delete_action(organization_slug, slug)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ActionsApi->delete_action: %s\n" % e)
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

# **delete_version_action**
> bool delete_version_action(organization_slug, slug, version)



Delete the specified version of the given object

### Example

```python
import time
import kodexa.client
from kodexa.client.api import actions_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.delete_version_action(organization_slug, slug, version)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ActionsApi->delete_version_action: %s\n" % e)
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

# **get_action**
> Action get_action(organization_slug, slug)



Get the current version of the object with given slug

### Example

```python
import time
import kodexa.client
from kodexa.client.api import actions_api
from kodexa.client.model.action import Action
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_action(organization_slug, slug)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ActionsApi->get_action: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |

### Return type

[**Action**](Action.md)

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

# **get_version_action**
> Action get_version_action(organization_slug, slug, version)



Get the specific version of the object with given slug

### Example

```python
import time
import kodexa.client
from kodexa.client.api import actions_api
from kodexa.client.model.action import Action
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_version_action(organization_slug, slug, version)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ActionsApi->get_version_action: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |

### Return type

[**Action**](Action.md)

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

# **list_action**
> PageAction list_action(organization_slug)



Get a paginated list of the objects for an organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import actions_api
from kodexa.client.model.page_action import PageAction
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    query = "*" # str |  (optional) if omitted the server will use the default value of "*"
    include_public = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.list_action(organization_slug)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ActionsApi->list_action: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.list_action(organization_slug, query=query, include_public=include_public)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ActionsApi->list_action: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **query** | **str**|  | [optional] if omitted the server will use the default value of "*"
 **include_public** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**PageAction**](PageAction.md)

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

# **update_action**
> Action update_action(organization_slug, slug, action)



Update the current version object with given slug in the organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import actions_api
from kodexa.client.model.action import Action
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    action = Action() # Action | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_action(organization_slug, slug, action)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ActionsApi->update_action: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |
 **action** | [**Action**](Action.md)|  |

### Return type

[**Action**](Action.md)

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

# **update_version_action**
> Action update_version_action(organization_slug, slug, version, action)



Update the object with given slug and version in the organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import actions_api
from kodexa.client.model.action import Action
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    action = Action() # Action | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_version_action(organization_slug, slug, version, action)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ActionsApi->update_version_action: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **action** | [**Action**](Action.md)|  |

### Return type

[**Action**](Action.md)

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

