# kodexa.client.MembershipsApi

All URIs are relative to *https://lehua.kodexa.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_membership**](MembershipsApi.md#create_membership) | **POST** /api/memberships | 
[**delete_membership**](MembershipsApi.md#delete_membership) | **DELETE** /api/memberships/{id} | 
[**get_membership**](MembershipsApi.md#get_membership) | **GET** /api/memberships/{id} | 
[**list_membership**](MembershipsApi.md#list_membership) | **GET** /api/memberships | 
[**reindex_membership**](MembershipsApi.md#reindex_membership) | **PUT** /api/memberships/_reindex | 
[**update_membership**](MembershipsApi.md#update_membership) | **PUT** /api/memberships/{id} | 


# **create_membership**
> Membership create_membership(membership)



Create a new instance of the resource

### Example

```python
import time
import kodexa.client
from kodexa.client.api import memberships_api
from kodexa.client.model.membership import Membership
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = memberships_api.MembershipsApi(api_client)
    membership = Membership(
        id="id_example",
        uuid="uuid_example",
        created_on=dateutil_parser('1970-01-01T00:00:00.00Z'),
        updated_on=dateutil_parser('1970-01-01T00:00:00.00Z'),
        created_by="created_by_example",
        updated_by="updated_by_example",
        role="OWNER",
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
        user=User(
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
        ),
    ) # Membership | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_membership(membership)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling MembershipsApi->create_membership: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **membership** | [**Membership**](Membership.md)|  |

### Return type

[**Membership**](Membership.md)

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

# **delete_membership**
> delete_membership(id)



Delete the resource with the provided ID

### Example

```python
import time
import kodexa.client
from kodexa.client.api import memberships_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = memberships_api.MembershipsApi(api_client)
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_membership(id)
    except kodexa.client.ApiException as e:
        print("Exception when calling MembershipsApi->delete_membership: %s\n" % e)
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

# **get_membership**
> Membership get_membership(id)



Get a resource with the provided ID

### Example

```python
import time
import kodexa.client
from kodexa.client.api import memberships_api
from kodexa.client.model.membership import Membership
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = memberships_api.MembershipsApi(api_client)
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_membership(id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling MembershipsApi->get_membership: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |

### Return type

[**Membership**](Membership.md)

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

# **list_membership**
> PageMembership list_membership(query_context)



List a page of the resources

### Example

```python
import time
import kodexa.client
from kodexa.client.api import memberships_api
from kodexa.client.model.page_membership import PageMembership
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
    api_instance = memberships_api.MembershipsApi(api_client)
    query_context = QueryContext(
        page_size__default_20=1,
        page_number__default_1=1,
        sorts_to_apply="sorts_to_apply_example",
        simple_filter_to_apply="simple_filter_to_apply_example",
    ) # QueryContext | 
    query = "*" # str |  (optional) if omitted the server will use the default value of "*"

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.list_membership(query_context)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling MembershipsApi->list_membership: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.list_membership(query_context, query=query)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling MembershipsApi->list_membership: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query_context** | **QueryContext**|  |
 **query** | **str**|  | [optional] if omitted the server will use the default value of "*"

### Return type

[**PageMembership**](PageMembership.md)

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

# **reindex_membership**
> reindex_membership()



Re-index the resource

### Example

```python
import time
import kodexa.client
from kodexa.client.api import memberships_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = memberships_api.MembershipsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        api_instance.reindex_membership()
    except kodexa.client.ApiException as e:
        print("Exception when calling MembershipsApi->reindex_membership: %s\n" % e)
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

# **update_membership**
> Membership update_membership(id, membership)



Update the given instance

### Example

```python
import time
import kodexa.client
from kodexa.client.api import memberships_api
from kodexa.client.model.membership import Membership
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = memberships_api.MembershipsApi(api_client)
    id = "id_example" # str | 
    membership = Membership(
        id="id_example",
        uuid="uuid_example",
        created_on=dateutil_parser('1970-01-01T00:00:00.00Z'),
        updated_on=dateutil_parser('1970-01-01T00:00:00.00Z'),
        created_by="created_by_example",
        updated_by="updated_by_example",
        role="OWNER",
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
        user=User(
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
        ),
    ) # Membership | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_membership(id, membership)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling MembershipsApi->update_membership: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **membership** | [**Membership**](Membership.md)|  |

### Return type

[**Membership**](Membership.md)

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

