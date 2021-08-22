# kodexa.client.ExtensionPacksApi

All URIs are relative to *https://lehua.kodexa.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_extension_pack**](ExtensionPacksApi.md#create_extension_pack) | **POST** /api/extensionPacks/{organizationSlug} | 
[**delete_extension_pack**](ExtensionPacksApi.md#delete_extension_pack) | **DELETE** /api/extensionPacks/{organizationSlug}/{slug} | 
[**delete_version_extension_pack**](ExtensionPacksApi.md#delete_version_extension_pack) | **DELETE** /api/extensionPacks/{organizationSlug}/{slug}/{version} | 
[**deploy**](ExtensionPacksApi.md#deploy) | **PUT** /api/extensionPacks/{organizationSlug}/{slug}/{version}/_deploy | 
[**get_extension_pack**](ExtensionPacksApi.md#get_extension_pack) | **GET** /api/extensionPacks/{organizationSlug}/{slug} | 
[**get_version_extension_pack**](ExtensionPacksApi.md#get_version_extension_pack) | **GET** /api/extensionPacks/{organizationSlug}/{slug}/{version} | 
[**list_extension_pack**](ExtensionPacksApi.md#list_extension_pack) | **GET** /api/extensionPacks/{organizationSlug} | 
[**repack**](ExtensionPacksApi.md#repack) | **PUT** /api/extensionPacks/{organizationSlug}/{slug}/{version}/_repack | 
[**undeploy**](ExtensionPacksApi.md#undeploy) | **PUT** /api/extensionPacks/{organizationSlug}/{slug}/{version}/_undeploy | 
[**update_extension_pack**](ExtensionPacksApi.md#update_extension_pack) | **PUT** /api/extensionPacks/{organizationSlug}/{slug} | 
[**update_version_extension_pack**](ExtensionPacksApi.md#update_version_extension_pack) | **PUT** /api/extensionPacks/{organizationSlug}/{slug}/{version} | 


# **create_extension_pack**
> ExtensionPack create_extension_pack(organization_slug, uri, deployment_options)



Create, buid and deploy extension pack from specific URI

### Example

```python
import time
import kodexa.client
from kodexa.client.api import extension_packs_api
from kodexa.client.model.extension_pack import ExtensionPack
from kodexa.client.model.deployment_options import DeploymentOptions
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = extension_packs_api.ExtensionPacksApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    uri = "uri_example" # str | 
    deployment_options = DeploymentOptions(
        deployment_type="KUBERNETES",
        max_replicas=1,
        min_replicas=1,
        reserved_concurrency=1,
        memory_assigned=1,
        sentry_dsn="sentry_dsn_example",
    ) # DeploymentOptions | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_extension_pack(organization_slug, uri, deployment_options)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ExtensionPacksApi->create_extension_pack: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **uri** | **str**|  |
 **deployment_options** | [**DeploymentOptions**](DeploymentOptions.md)|  |

### Return type

[**ExtensionPack**](ExtensionPack.md)

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

# **delete_extension_pack**
> bool delete_extension_pack(organization_slug, slug)



Delete the current version of the given object

### Example

```python
import time
import kodexa.client
from kodexa.client.api import extension_packs_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = extension_packs_api.ExtensionPacksApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.delete_extension_pack(organization_slug, slug)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ExtensionPacksApi->delete_extension_pack: %s\n" % e)
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

# **delete_version_extension_pack**
> bool delete_version_extension_pack(organization_slug, slug, version)



Delete the specified version of the given object

### Example

```python
import time
import kodexa.client
from kodexa.client.api import extension_packs_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = extension_packs_api.ExtensionPacksApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.delete_version_extension_pack(organization_slug, slug, version)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ExtensionPacksApi->delete_version_extension_pack: %s\n" % e)
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

# **deploy**
> ExtensionPack deploy(organization_slug, slug, version, deployment_options)



Deploy the specified version of the extension pack

### Example

```python
import time
import kodexa.client
from kodexa.client.api import extension_packs_api
from kodexa.client.model.extension_pack import ExtensionPack
from kodexa.client.model.deployment_options import DeploymentOptions
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = extension_packs_api.ExtensionPacksApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    deployment_options = DeploymentOptions(
        deployment_type="KUBERNETES",
        max_replicas=1,
        min_replicas=1,
        reserved_concurrency=1,
        memory_assigned=1,
        sentry_dsn="sentry_dsn_example",
    ) # DeploymentOptions | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.deploy(organization_slug, slug, version, deployment_options)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ExtensionPacksApi->deploy: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **deployment_options** | [**DeploymentOptions**](DeploymentOptions.md)|  |

### Return type

[**ExtensionPack**](ExtensionPack.md)

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

# **get_extension_pack**
> ExtensionPack get_extension_pack(organization_slug, slug)



Get the current version of the object with given slug

### Example

```python
import time
import kodexa.client
from kodexa.client.api import extension_packs_api
from kodexa.client.model.extension_pack import ExtensionPack
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = extension_packs_api.ExtensionPacksApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_extension_pack(organization_slug, slug)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ExtensionPacksApi->get_extension_pack: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |

### Return type

[**ExtensionPack**](ExtensionPack.md)

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

# **get_version_extension_pack**
> ExtensionPack get_version_extension_pack(organization_slug, slug, version)



Get the specific version of the object with given slug

### Example

```python
import time
import kodexa.client
from kodexa.client.api import extension_packs_api
from kodexa.client.model.extension_pack import ExtensionPack
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = extension_packs_api.ExtensionPacksApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_version_extension_pack(organization_slug, slug, version)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ExtensionPacksApi->get_version_extension_pack: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |

### Return type

[**ExtensionPack**](ExtensionPack.md)

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

# **list_extension_pack**
> PageExtensionPack list_extension_pack(organization_slug)



Get a paginated list of the objects for an organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import extension_packs_api
from kodexa.client.model.page_extension_pack import PageExtensionPack
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = extension_packs_api.ExtensionPacksApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    query = "*" # str |  (optional) if omitted the server will use the default value of "*"
    include_public = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.list_extension_pack(organization_slug)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ExtensionPacksApi->list_extension_pack: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.list_extension_pack(organization_slug, query=query, include_public=include_public)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ExtensionPacksApi->list_extension_pack: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **query** | **str**|  | [optional] if omitted the server will use the default value of "*"
 **include_public** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**PageExtensionPack**](PageExtensionPack.md)

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

# **repack**
> ExtensionPack repack(organization_slug, slug, version)



Repack (re-download, build and deploy) the given extension pack

### Example

```python
import time
import kodexa.client
from kodexa.client.api import extension_packs_api
from kodexa.client.model.extension_pack import ExtensionPack
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = extension_packs_api.ExtensionPacksApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.repack(organization_slug, slug, version)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ExtensionPacksApi->repack: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |

### Return type

[**ExtensionPack**](ExtensionPack.md)

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

# **undeploy**
> ExtensionPack undeploy(organization_slug, slug, version)



Undeploy the extension pack

### Example

```python
import time
import kodexa.client
from kodexa.client.api import extension_packs_api
from kodexa.client.model.extension_pack import ExtensionPack
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = extension_packs_api.ExtensionPacksApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.undeploy(organization_slug, slug, version)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ExtensionPacksApi->undeploy: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |

### Return type

[**ExtensionPack**](ExtensionPack.md)

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

# **update_extension_pack**
> ExtensionPack update_extension_pack(organization_slug, slug, extension_pack)



Update the current version object with given slug in the organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import extension_packs_api
from kodexa.client.model.extension_pack import ExtensionPack
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = extension_packs_api.ExtensionPacksApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    extension_pack = ExtensionPack() # ExtensionPack | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_extension_pack(organization_slug, slug, extension_pack)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ExtensionPacksApi->update_extension_pack: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |
 **extension_pack** | [**ExtensionPack**](ExtensionPack.md)|  |

### Return type

[**ExtensionPack**](ExtensionPack.md)

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

# **update_version_extension_pack**
> ExtensionPack update_version_extension_pack(organization_slug, slug, version, extension_pack)



Update the object with given slug and version in the organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import extension_packs_api
from kodexa.client.model.extension_pack import ExtensionPack
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = extension_packs_api.ExtensionPacksApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    extension_pack = ExtensionPack() # ExtensionPack | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_version_extension_pack(organization_slug, slug, version, extension_pack)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ExtensionPacksApi->update_version_extension_pack: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **extension_pack** | [**ExtensionPack**](ExtensionPack.md)|  |

### Return type

[**ExtensionPack**](ExtensionPack.md)

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

