# kodexa.client.AssistantsApi

All URIs are relative to *https://lehua.kodexa.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_assistant_definition**](AssistantsApi.md#create_assistant_definition) | **POST** /api/assistants/{organizationSlug} | 
[**delete_assistant_definition**](AssistantsApi.md#delete_assistant_definition) | **DELETE** /api/assistants/{organizationSlug}/{slug} | 
[**delete_version_assistant_definition**](AssistantsApi.md#delete_version_assistant_definition) | **DELETE** /api/assistants/{organizationSlug}/{slug}/{version} | 
[**get_assistant_definition**](AssistantsApi.md#get_assistant_definition) | **GET** /api/assistants/{organizationSlug}/{slug} | 
[**get_version_assistant_definition**](AssistantsApi.md#get_version_assistant_definition) | **GET** /api/assistants/{organizationSlug}/{slug}/{version} | 
[**list_assistant_definition**](AssistantsApi.md#list_assistant_definition) | **GET** /api/assistants/{organizationSlug} | 
[**update_assistant_definition**](AssistantsApi.md#update_assistant_definition) | **PUT** /api/assistants/{organizationSlug}/{slug} | 
[**update_version_assistant_definition**](AssistantsApi.md#update_version_assistant_definition) | **PUT** /api/assistants/{organizationSlug}/{slug}/{version} | 


# **create_assistant_definition**
> AssistantDefinition create_assistant_definition(organization_slug, assistant_definition)



Create a new instance of the object in the organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import assistants_api
from kodexa.client.model.assistant_definition import AssistantDefinition
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = assistants_api.AssistantsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    assistant_definition = AssistantDefinition(
        schema_version=1,
        org_slug="zBAMDTMv2D2ylmgd10Z3UB6UkJSIS",
        slug="zBAMDTMv2D2ylmgd10Z3UB6UkJSIS",
        type="type_example",
        name="name_example",
        description="description_example",
        version="version_example",
        deployed=dateutil_parser('1970-01-01T00:00:00.00Z'),
        public_access=True,
        ref="ref_example",
        url_of_image_for_assistant="url_of_image_for_assistant_example",
        a_list_of_associated_tags=[
            MetadataTag(
                tag="tag_example",
                image_url="image_url_example",
            ),
        ],
        extension_pack_ref="extension_pack_ref_example",
        the_assistant_can_be_scheduled=True,
        the_assistant_is_reactive_to_content_changes=True,
        the_implementation_of_the_assistant=AssistantImplementation(
            package="package_example",
            _class="_class_example",
        ),
        additional_metadata_for_the_assistant=AssistantMetadata(
            avatar=Avatar(
                icon="icon_example",
                icon_group="icon_group_example",
            ),
            tags=[
                "tags_example",
            ],
            tabs=[
                TabGroup(
                    id="id_example",
                    name="name_example",
                    icon="icon_example",
                    show_if="show_if_example",
                ),
            ],
            options=[
                Option(
                    tab_id="tab_id_example",
                    name="name_example",
                    label="label_example",
                    hint="hint_example",
                    required=True,
                    type="type_example",
                    list_type="list_type_example",
                    default={},
                    description="description_example",
                    show_if="show_if_example",
                    possible_values=[
                        PossibleValue(
                            label="label_example",
                            value={},
                        ),
                    ],
                ),
            ],
        ),
        services_used_by_the_assistant=[
            ,
        ],
        taxonomies_that_the_assistant_uses=[
            AssistantTaxonomy(
                ref="ref_example",
            ),
        ],
        options_for_the_assistant=[
            Option(
                tab_id="tab_id_example",
                name="name_example",
                label="label_example",
                hint="hint_example",
                required=True,
                type="type_example",
                list_type="list_type_example",
                default={},
                description="description_example",
                show_if="show_if_example",
                possible_values=[
                    PossibleValue(
                        label="label_example",
                        value={},
                    ),
                ],
            ),
        ],
        event_types_that_the_assistant_is_able_to_response_to=[
            EventType(
                name="name_example",
                icon="icon_example",
                label="label_example",
                content_object=True,
            ),
        ],
        event_filters=[
            EventFilter(
                event_type="event_type_example",
                path="path_example",
                case_sensitive=True,
            ),
        ],
        the_default_schedules_that_the_assistant_has=[
            AssistantSchedule(
                type="type_example",
                cron_expression="cron_expression_example",
                last_event=dateutil_parser('1970-01-01T00:00:00.00Z'),
                next_event=dateutil_parser('1970-01-01T00:00:00.00Z'),
            ),
        ],
        the_default_subscriptions_that_the_assistant_has=[
            AssistantSubscription(),
        ],
        the_full_description_of_the_assistant="the_full_description_of_the_assistant_example",
        a_help_url_where_you_can_learn_more_about_the_assistant="a_help_url_where_you_can_learn_more_about_the_assistant_example",
        the_category_of_assistant="TASK",
    ) # AssistantDefinition | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_assistant_definition(organization_slug, assistant_definition)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AssistantsApi->create_assistant_definition: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **assistant_definition** | [**AssistantDefinition**](AssistantDefinition.md)|  |

### Return type

[**AssistantDefinition**](AssistantDefinition.md)

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

# **delete_assistant_definition**
> bool delete_assistant_definition(organization_slug, slug)



Delete the current version of the given object

### Example

```python
import time
import kodexa.client
from kodexa.client.api import assistants_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = assistants_api.AssistantsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.delete_assistant_definition(organization_slug, slug)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AssistantsApi->delete_assistant_definition: %s\n" % e)
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

# **delete_version_assistant_definition**
> bool delete_version_assistant_definition(organization_slug, slug, version)



Delete the specified version of the given object

### Example

```python
import time
import kodexa.client
from kodexa.client.api import assistants_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = assistants_api.AssistantsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.delete_version_assistant_definition(organization_slug, slug, version)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AssistantsApi->delete_version_assistant_definition: %s\n" % e)
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

# **get_assistant_definition**
> AssistantDefinition get_assistant_definition(organization_slug, slug)



Get the current version of the object with given slug

### Example

```python
import time
import kodexa.client
from kodexa.client.api import assistants_api
from kodexa.client.model.assistant_definition import AssistantDefinition
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = assistants_api.AssistantsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_assistant_definition(organization_slug, slug)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AssistantsApi->get_assistant_definition: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |

### Return type

[**AssistantDefinition**](AssistantDefinition.md)

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

# **get_version_assistant_definition**
> AssistantDefinition get_version_assistant_definition(organization_slug, slug, version)



Get the specific version of the object with given slug

### Example

```python
import time
import kodexa.client
from kodexa.client.api import assistants_api
from kodexa.client.model.assistant_definition import AssistantDefinition
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = assistants_api.AssistantsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_version_assistant_definition(organization_slug, slug, version)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AssistantsApi->get_version_assistant_definition: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |

### Return type

[**AssistantDefinition**](AssistantDefinition.md)

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

# **list_assistant_definition**
> PageAssistantDefinition list_assistant_definition(organization_slug)



Get a paginated list of the objects for an organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import assistants_api
from kodexa.client.model.page_assistant_definition import PageAssistantDefinition
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = assistants_api.AssistantsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    query = "*" # str |  (optional) if omitted the server will use the default value of "*"
    include_public = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.list_assistant_definition(organization_slug)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AssistantsApi->list_assistant_definition: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.list_assistant_definition(organization_slug, query=query, include_public=include_public)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AssistantsApi->list_assistant_definition: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **query** | **str**|  | [optional] if omitted the server will use the default value of "*"
 **include_public** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**PageAssistantDefinition**](PageAssistantDefinition.md)

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

# **update_assistant_definition**
> AssistantDefinition update_assistant_definition(organization_slug, slug, assistant_definition)



Update the current version object with given slug in the organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import assistants_api
from kodexa.client.model.assistant_definition import AssistantDefinition
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = assistants_api.AssistantsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    assistant_definition = AssistantDefinition(
        schema_version=1,
        org_slug="zBAMDTMv2D2ylmgd10Z3UB6UkJSIS",
        slug="zBAMDTMv2D2ylmgd10Z3UB6UkJSIS",
        type="type_example",
        name="name_example",
        description="description_example",
        version="version_example",
        deployed=dateutil_parser('1970-01-01T00:00:00.00Z'),
        public_access=True,
        ref="ref_example",
        url_of_image_for_assistant="url_of_image_for_assistant_example",
        a_list_of_associated_tags=[
            MetadataTag(
                tag="tag_example",
                image_url="image_url_example",
            ),
        ],
        extension_pack_ref="extension_pack_ref_example",
        the_assistant_can_be_scheduled=True,
        the_assistant_is_reactive_to_content_changes=True,
        the_implementation_of_the_assistant=AssistantImplementation(
            package="package_example",
            _class="_class_example",
        ),
        additional_metadata_for_the_assistant=AssistantMetadata(
            avatar=Avatar(
                icon="icon_example",
                icon_group="icon_group_example",
            ),
            tags=[
                "tags_example",
            ],
            tabs=[
                TabGroup(
                    id="id_example",
                    name="name_example",
                    icon="icon_example",
                    show_if="show_if_example",
                ),
            ],
            options=[
                Option(
                    tab_id="tab_id_example",
                    name="name_example",
                    label="label_example",
                    hint="hint_example",
                    required=True,
                    type="type_example",
                    list_type="list_type_example",
                    default={},
                    description="description_example",
                    show_if="show_if_example",
                    possible_values=[
                        PossibleValue(
                            label="label_example",
                            value={},
                        ),
                    ],
                ),
            ],
        ),
        services_used_by_the_assistant=[
            ,
        ],
        taxonomies_that_the_assistant_uses=[
            AssistantTaxonomy(
                ref="ref_example",
            ),
        ],
        options_for_the_assistant=[
            Option(
                tab_id="tab_id_example",
                name="name_example",
                label="label_example",
                hint="hint_example",
                required=True,
                type="type_example",
                list_type="list_type_example",
                default={},
                description="description_example",
                show_if="show_if_example",
                possible_values=[
                    PossibleValue(
                        label="label_example",
                        value={},
                    ),
                ],
            ),
        ],
        event_types_that_the_assistant_is_able_to_response_to=[
            EventType(
                name="name_example",
                icon="icon_example",
                label="label_example",
                content_object=True,
            ),
        ],
        event_filters=[
            EventFilter(
                event_type="event_type_example",
                path="path_example",
                case_sensitive=True,
            ),
        ],
        the_default_schedules_that_the_assistant_has=[
            AssistantSchedule(
                type="type_example",
                cron_expression="cron_expression_example",
                last_event=dateutil_parser('1970-01-01T00:00:00.00Z'),
                next_event=dateutil_parser('1970-01-01T00:00:00.00Z'),
            ),
        ],
        the_default_subscriptions_that_the_assistant_has=[
            AssistantSubscription(),
        ],
        the_full_description_of_the_assistant="the_full_description_of_the_assistant_example",
        a_help_url_where_you_can_learn_more_about_the_assistant="a_help_url_where_you_can_learn_more_about_the_assistant_example",
        the_category_of_assistant="TASK",
    ) # AssistantDefinition | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_assistant_definition(organization_slug, slug, assistant_definition)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AssistantsApi->update_assistant_definition: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |
 **assistant_definition** | [**AssistantDefinition**](AssistantDefinition.md)|  |

### Return type

[**AssistantDefinition**](AssistantDefinition.md)

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

# **update_version_assistant_definition**
> AssistantDefinition update_version_assistant_definition(organization_slug, slug, version, assistant_definition)



Update the object with given slug and version in the organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import assistants_api
from kodexa.client.model.assistant_definition import AssistantDefinition
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = assistants_api.AssistantsApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    assistant_definition = AssistantDefinition(
        schema_version=1,
        org_slug="zBAMDTMv2D2ylmgd10Z3UB6UkJSIS",
        slug="zBAMDTMv2D2ylmgd10Z3UB6UkJSIS",
        type="type_example",
        name="name_example",
        description="description_example",
        version="version_example",
        deployed=dateutil_parser('1970-01-01T00:00:00.00Z'),
        public_access=True,
        ref="ref_example",
        url_of_image_for_assistant="url_of_image_for_assistant_example",
        a_list_of_associated_tags=[
            MetadataTag(
                tag="tag_example",
                image_url="image_url_example",
            ),
        ],
        extension_pack_ref="extension_pack_ref_example",
        the_assistant_can_be_scheduled=True,
        the_assistant_is_reactive_to_content_changes=True,
        the_implementation_of_the_assistant=AssistantImplementation(
            package="package_example",
            _class="_class_example",
        ),
        additional_metadata_for_the_assistant=AssistantMetadata(
            avatar=Avatar(
                icon="icon_example",
                icon_group="icon_group_example",
            ),
            tags=[
                "tags_example",
            ],
            tabs=[
                TabGroup(
                    id="id_example",
                    name="name_example",
                    icon="icon_example",
                    show_if="show_if_example",
                ),
            ],
            options=[
                Option(
                    tab_id="tab_id_example",
                    name="name_example",
                    label="label_example",
                    hint="hint_example",
                    required=True,
                    type="type_example",
                    list_type="list_type_example",
                    default={},
                    description="description_example",
                    show_if="show_if_example",
                    possible_values=[
                        PossibleValue(
                            label="label_example",
                            value={},
                        ),
                    ],
                ),
            ],
        ),
        services_used_by_the_assistant=[
            ,
        ],
        taxonomies_that_the_assistant_uses=[
            AssistantTaxonomy(
                ref="ref_example",
            ),
        ],
        options_for_the_assistant=[
            Option(
                tab_id="tab_id_example",
                name="name_example",
                label="label_example",
                hint="hint_example",
                required=True,
                type="type_example",
                list_type="list_type_example",
                default={},
                description="description_example",
                show_if="show_if_example",
                possible_values=[
                    PossibleValue(
                        label="label_example",
                        value={},
                    ),
                ],
            ),
        ],
        event_types_that_the_assistant_is_able_to_response_to=[
            EventType(
                name="name_example",
                icon="icon_example",
                label="label_example",
                content_object=True,
            ),
        ],
        event_filters=[
            EventFilter(
                event_type="event_type_example",
                path="path_example",
                case_sensitive=True,
            ),
        ],
        the_default_schedules_that_the_assistant_has=[
            AssistantSchedule(
                type="type_example",
                cron_expression="cron_expression_example",
                last_event=dateutil_parser('1970-01-01T00:00:00.00Z'),
                next_event=dateutil_parser('1970-01-01T00:00:00.00Z'),
            ),
        ],
        the_default_subscriptions_that_the_assistant_has=[
            AssistantSubscription(),
        ],
        the_full_description_of_the_assistant="the_full_description_of_the_assistant_example",
        a_help_url_where_you_can_learn_more_about_the_assistant="a_help_url_where_you_can_learn_more_about_the_assistant_example",
        the_category_of_assistant="TASK",
    ) # AssistantDefinition | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_version_assistant_definition(organization_slug, slug, version, assistant_definition)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AssistantsApi->update_version_assistant_definition: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **assistant_definition** | [**AssistantDefinition**](AssistantDefinition.md)|  |

### Return type

[**AssistantDefinition**](AssistantDefinition.md)

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

