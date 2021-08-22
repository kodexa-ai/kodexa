# kodexa.client.ProjectsApi

All URIs are relative to *https://lehua.kodexa.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**activate_assistant**](ProjectsApi.md#activate_assistant) | **PUT** /api/projects/{id}/assistants/{assistantId}/activate | 
[**add_assistant**](ProjectsApi.md#add_assistant) | **POST** /api/projects/{id}/assistants | 
[**create_project**](ProjectsApi.md#create_project) | **POST** /api/projects | 
[**deactivate_assistant**](ProjectsApi.md#deactivate_assistant) | **PUT** /api/projects/{id}/assistants/{assistantId}/deactivate | 
[**delete_assistant**](ProjectsApi.md#delete_assistant) | **DELETE** /api/projects/{id}/assistants/{assistantId} | 
[**delete_project**](ProjectsApi.md#delete_project) | **DELETE** /api/projects/{id} | 
[**get_assistants**](ProjectsApi.md#get_assistants) | **GET** /api/projects/{id}/assistants | 
[**get_classification_taxonomies**](ProjectsApi.md#get_classification_taxonomies) | **GET** /api/projects/{id}/classificationTaxonomies | 
[**get_content_taxonomies**](ProjectsApi.md#get_content_taxonomies) | **GET** /api/projects/{id}/contentTaxonomies | 
[**get_dashboards**](ProjectsApi.md#get_dashboards) | **GET** /api/projects/{id}/dashboards | 
[**get_data_stores**](ProjectsApi.md#get_data_stores) | **GET** /api/projects/{id}/dataStores | 
[**get_document_stores**](ProjectsApi.md#get_document_stores) | **GET** /api/projects/{id}/documentStores | 
[**get_model_stores**](ProjectsApi.md#get_model_stores) | **GET** /api/projects/{id}/modelStores | 
[**get_project**](ProjectsApi.md#get_project) | **GET** /api/projects/{id} | 
[**list_project**](ProjectsApi.md#list_project) | **GET** /api/projects | 
[**process_document**](ProjectsApi.md#process_document) | **POST** /api/projects/{id}/assistants/{assistantId}/execute | 
[**reindex_project**](ProjectsApi.md#reindex_project) | **PUT** /api/projects/_reindex | 
[**update_assistant**](ProjectsApi.md#update_assistant) | **PUT** /api/projects/{id}/assistants | 
[**update_project**](ProjectsApi.md#update_project) | **PUT** /api/projects/{id} | 


# **activate_assistant**
> activate_assistant(id, assistant_id)



Activate the assistant (ensuring it gets content events)

### Example

```python
import time
import kodexa.client
from kodexa.client.api import projects_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = projects_api.ProjectsApi(api_client)
    id = "id_example" # str | 
    assistant_id = "assistantId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.activate_assistant(id, assistant_id)
    except kodexa.client.ApiException as e:
        print("Exception when calling ProjectsApi->activate_assistant: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **assistant_id** | **str**|  |

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

# **add_assistant**
> Assistant add_assistant(id, assistant)



Create and add assistant to project

### Example

```python
import time
import kodexa.client
from kodexa.client.api import projects_api
from kodexa.client.model.assistant import Assistant
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = projects_api.ProjectsApi(api_client)
    id = "id_example" # str | 
    assistant = Assistant(
        id="id_example",
        name="name_example",
        description="description_example",
        assistant_definition_ref="assistant_definition_ref_example",
        definition=AssistantDefinition(
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
        ),
        active=True,
        run_on_existing_content=True,
        stores=[
            "stores_example",
        ],
        store_mapping={
            "key": "key_example",
        },
        options={
            "key": {},
        },
        subscriptions=[
            AssistantSubscription(),
        ],
        schedules=[
            AssistantSchedule(
                type="type_example",
                cron_expression="cron_expression_example",
                last_event=dateutil_parser('1970-01-01T00:00:00.00Z'),
                next_event=dateutil_parser('1970-01-01T00:00:00.00Z'),
            ),
        ],
        validation_errors=[
            ValidationError(
                message="message_example",
                option="option_example",
                description="description_example",
            ),
        ],
    ) # Assistant | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.add_assistant(id, assistant)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ProjectsApi->add_assistant: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **assistant** | [**Assistant**](Assistant.md)|  |

### Return type

[**Assistant**](Assistant.md)

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

# **create_project**
> ProjectMetadata create_project(project_metadata)



Create a new instance of the resource

### Example

```python
import time
import kodexa.client
from kodexa.client.api import projects_api
from kodexa.client.model.project_metadata import ProjectMetadata
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = projects_api.ProjectsApi(api_client)
    project_metadata = ProjectMetadata(
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
        metadata=Project(
            description="description_example",
            project_template_ref="project_template_ref_example",
            data_store_refs=[
                "data_store_refs_example",
            ],
            document_store_refs=[
                "document_store_refs_example",
            ],
            model_store_refs=[
                "model_store_refs_example",
            ],
            content_taxonomy_refs=[
                "content_taxonomy_refs_example",
            ],
            classification_taxonomy_refs=[
                "classification_taxonomy_refs_example",
            ],
            dashboard_refs=[
                "dashboard_refs_example",
            ],
            labels=[
                Label(
                    id="id_example",
                    color="color_example",
                    label="label_example",
                    name="name_example",
                ),
            ],
            statuses=[
                DocumentStatus(
                    id="id_example",
                    color="color_example",
                    status="status_example",
                    status_type="UNRESOLVED",
                ),
            ],
        ),
        name="name_example",
        stores=[
            StoreMetadata(
                projects=[
                    ProjectMetadata(),
                ],
                id="id_example",
                uuid="uuid_example",
                version="version_example",
                created_on=dateutil_parser('1970-01-01T00:00:00.00Z'),
                updated_on=dateutil_parser('1970-01-01T00:00:00.00Z'),
                created_by="created_by_example",
                updated_by="updated_by_example",
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
                slug="slug_example",
                metadata=Store(
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
                    store_type="DOCUMENT",
                    searchable=True,
                    store_purpose="OPERATIONAL",
                    metadata=,
                    view_options=StoreViewOptions(
                        last_event=True,
                        show_extension=True,
                        show_created=True,
                        show_modfied=True,
                    ),
                    saved_filters=[
                        SavedFilter(
                            id="id_example",
                            name="name_example",
                            filter={},
                        ),
                    ],
                ),
                extension_pack_ref="extension_pack_ref_example",
            ),
        ],
        taxonomies=[
            TaxonomyMetadata(
                projects=[
                    ProjectMetadata(),
                ],
                id="id_example",
                version="version_example",
                uuid="uuid_example",
                created_on=dateutil_parser('1970-01-01T00:00:00.00Z'),
                updated_on=dateutil_parser('1970-01-01T00:00:00.00Z'),
                created_by="created_by_example",
                updated_by="updated_by_example",
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
                slug="slug_example",
                metadata=Taxonomy(
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
                    taxonomy_type="CONTENT",
                    enabled=True,
                    taxons=[
                        Taxon(
                            id="id_example",
                            label="label_example",
                            generate_name=True,
                            group=True,
                            name="name_example",
                            value_path="VALUE_OR_ALL_CONTENT",
                            metadata_value="FILENAME",
                            data_path="data_path_example",
                            expression="expression_example",
                            description="description_example",
                            enabled=True,
                            color="color_example",
                            children=[
                                Taxon(),
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
                            node_types=[
                                "node_types_example",
                            ],
                            taxon_type="STRING",
                            type_features={
                                "key": {},
                            },
                        ),
                    ],
                    total_taxons=1,
                ),
                extension_pack_ref="extension_pack_ref_example",
            ),
        ],
        channel=ChannelMetadata(
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
        ),
    ) # ProjectMetadata | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_project(project_metadata)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ProjectsApi->create_project: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_metadata** | [**ProjectMetadata**](ProjectMetadata.md)|  |

### Return type

[**ProjectMetadata**](ProjectMetadata.md)

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

# **deactivate_assistant**
> deactivate_assistant(id, assistant_id)



Deactivate the assistant (stopping it from getting content events)

### Example

```python
import time
import kodexa.client
from kodexa.client.api import projects_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = projects_api.ProjectsApi(api_client)
    id = "id_example" # str | 
    assistant_id = "assistantId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.deactivate_assistant(id, assistant_id)
    except kodexa.client.ApiException as e:
        print("Exception when calling ProjectsApi->deactivate_assistant: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **assistant_id** | **str**|  |

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

# **delete_assistant**
> delete_assistant(id, assistant_id)



Delete specified assistant

### Example

```python
import time
import kodexa.client
from kodexa.client.api import projects_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = projects_api.ProjectsApi(api_client)
    id = "id_example" # str | 
    assistant_id = "assistantId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_assistant(id, assistant_id)
    except kodexa.client.ApiException as e:
        print("Exception when calling ProjectsApi->delete_assistant: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **assistant_id** | **str**|  |

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

# **delete_project**
> delete_project(id, delete_associated)



Delete the project with the provided ID and its associated resources

### Example

```python
import time
import kodexa.client
from kodexa.client.api import projects_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = projects_api.ProjectsApi(api_client)
    id = "id_example" # str | 
    delete_associated = "deleteAssociated_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_project(id, delete_associated)
    except kodexa.client.ApiException as e:
        print("Exception when calling ProjectsApi->delete_project: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **delete_associated** | **str**|  |

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
**401** | You are not authorized to view the resource |  -  |
**200** | Successfully deleted the resource |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_assistants**
> PageAssistant get_assistants(id, query_context)



Paginated list of assistants that have been added to this project

### Example

```python
import time
import kodexa.client
from kodexa.client.api import projects_api
from kodexa.client.model.page_assistant import PageAssistant
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
    api_instance = projects_api.ProjectsApi(api_client)
    id = "id_example" # str | 
    query_context = QueryContext(
        page_size__default_20=1,
        page_number__default_1=1,
        sorts_to_apply="sorts_to_apply_example",
        simple_filter_to_apply="simple_filter_to_apply_example",
    ) # QueryContext | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_assistants(id, query_context)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ProjectsApi->get_assistants: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **query_context** | **QueryContext**|  |

### Return type

[**PageAssistant**](PageAssistant.md)

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

# **get_classification_taxonomies**
> [Taxonomy] get_classification_taxonomies(id)



Get a list of the taxonomies (type classification) associated with this project

### Example

```python
import time
import kodexa.client
from kodexa.client.api import projects_api
from kodexa.client.model.taxonomy import Taxonomy
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = projects_api.ProjectsApi(api_client)
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_classification_taxonomies(id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ProjectsApi->get_classification_taxonomies: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |

### Return type

[**[Taxonomy]**](Taxonomy.md)

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

# **get_content_taxonomies**
> [Taxonomy] get_content_taxonomies(id)



Get a list of the taxonomies (type content) associated with this project

### Example

```python
import time
import kodexa.client
from kodexa.client.api import projects_api
from kodexa.client.model.taxonomy import Taxonomy
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = projects_api.ProjectsApi(api_client)
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_content_taxonomies(id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ProjectsApi->get_content_taxonomies: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |

### Return type

[**[Taxonomy]**](Taxonomy.md)

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

# **get_dashboards**
> [Dashboard] get_dashboards(id)



Get a list of the dashboards associated with this project

### Example

```python
import time
import kodexa.client
from kodexa.client.api import projects_api
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
    api_instance = projects_api.ProjectsApi(api_client)
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_dashboards(id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ProjectsApi->get_dashboards: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |

### Return type

[**[Dashboard]**](Dashboard.md)

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

# **get_data_stores**
> [Store] get_data_stores(id)



Get a list of the stores (type data) associated with this project

### Example

```python
import time
import kodexa.client
from kodexa.client.api import projects_api
from kodexa.client.model.store import Store
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = projects_api.ProjectsApi(api_client)
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_data_stores(id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ProjectsApi->get_data_stores: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |

### Return type

[**[Store]**](Store.md)

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

# **get_document_stores**
> [Store] get_document_stores(id)



Get a list of the stores (type document) associated with this project

### Example

```python
import time
import kodexa.client
from kodexa.client.api import projects_api
from kodexa.client.model.store import Store
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = projects_api.ProjectsApi(api_client)
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_document_stores(id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ProjectsApi->get_document_stores: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |

### Return type

[**[Store]**](Store.md)

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

# **get_model_stores**
> [Store] get_model_stores(id)



Get a list of the stores (type document) associated with this project

### Example

```python
import time
import kodexa.client
from kodexa.client.api import projects_api
from kodexa.client.model.store import Store
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = projects_api.ProjectsApi(api_client)
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_model_stores(id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ProjectsApi->get_model_stores: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |

### Return type

[**[Store]**](Store.md)

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

# **get_project**
> ProjectMetadata get_project(id)



Get a resource with the provided ID

### Example

```python
import time
import kodexa.client
from kodexa.client.api import projects_api
from kodexa.client.model.project_metadata import ProjectMetadata
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = projects_api.ProjectsApi(api_client)
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_project(id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ProjectsApi->get_project: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |

### Return type

[**ProjectMetadata**](ProjectMetadata.md)

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

# **list_project**
> PageProjectMetadata list_project(query_context)



List a page of the resources

### Example

```python
import time
import kodexa.client
from kodexa.client.api import projects_api
from kodexa.client.model.page_project_metadata import PageProjectMetadata
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
    api_instance = projects_api.ProjectsApi(api_client)
    query_context = QueryContext(
        page_size__default_20=1,
        page_number__default_1=1,
        sorts_to_apply="sorts_to_apply_example",
        simple_filter_to_apply="simple_filter_to_apply_example",
    ) # QueryContext | 
    query = "*" # str |  (optional) if omitted the server will use the default value of "*"

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.list_project(query_context)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ProjectsApi->list_project: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.list_project(query_context, query=query)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ProjectsApi->list_project: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query_context** | **QueryContext**|  |
 **query** | **str**|  | [optional] if omitted the server will use the default value of "*"

### Return type

[**PageProjectMetadata**](PageProjectMetadata.md)

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

# **process_document**
> CloudExecutionEvent process_document(id, assistant_id)



Send a document to upload and send as an event to an assistant

### Example

```python
import time
import kodexa.client
from kodexa.client.api import projects_api
from kodexa.client.model.cloud_execution_event import CloudExecutionEvent
from kodexa.client.model.inline_object3 import InlineObject3
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = projects_api.ProjectsApi(api_client)
    id = "id_example" # str | 
    assistant_id = "assistantId_example" # str | 
    event_type = "eventType_example" # str |  (optional)
    options = "options_example" # str |  (optional)
    inline_object3 = InlineObject3(
        document=open('/path/to/file', 'rb'),
    ) # InlineObject3 |  (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.process_document(id, assistant_id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ProjectsApi->process_document: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.process_document(id, assistant_id, event_type=event_type, options=options, inline_object3=inline_object3)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ProjectsApi->process_document: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **assistant_id** | **str**|  |
 **event_type** | **str**|  | [optional]
 **options** | **str**|  | [optional]
 **inline_object3** | [**InlineObject3**](InlineObject3.md)|  | [optional]

### Return type

[**CloudExecutionEvent**](CloudExecutionEvent.md)

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

# **reindex_project**
> reindex_project()



Re-index the resource

### Example

```python
import time
import kodexa.client
from kodexa.client.api import projects_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = projects_api.ProjectsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        api_instance.reindex_project()
    except kodexa.client.ApiException as e:
        print("Exception when calling ProjectsApi->reindex_project: %s\n" % e)
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

# **update_assistant**
> Assistant update_assistant(id, assistant)



Update the assistant in the given project

### Example

```python
import time
import kodexa.client
from kodexa.client.api import projects_api
from kodexa.client.model.assistant import Assistant
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = projects_api.ProjectsApi(api_client)
    id = "id_example" # str | 
    assistant = Assistant(
        id="id_example",
        name="name_example",
        description="description_example",
        assistant_definition_ref="assistant_definition_ref_example",
        definition=AssistantDefinition(
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
        ),
        active=True,
        run_on_existing_content=True,
        stores=[
            "stores_example",
        ],
        store_mapping={
            "key": "key_example",
        },
        options={
            "key": {},
        },
        subscriptions=[
            AssistantSubscription(),
        ],
        schedules=[
            AssistantSchedule(
                type="type_example",
                cron_expression="cron_expression_example",
                last_event=dateutil_parser('1970-01-01T00:00:00.00Z'),
                next_event=dateutil_parser('1970-01-01T00:00:00.00Z'),
            ),
        ],
        validation_errors=[
            ValidationError(
                message="message_example",
                option="option_example",
                description="description_example",
            ),
        ],
    ) # Assistant | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_assistant(id, assistant)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ProjectsApi->update_assistant: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **assistant** | [**Assistant**](Assistant.md)|  |

### Return type

[**Assistant**](Assistant.md)

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

# **update_project**
> ProjectMetadata update_project(id, project_metadata)



Update the given instance

### Example

```python
import time
import kodexa.client
from kodexa.client.api import projects_api
from kodexa.client.model.project_metadata import ProjectMetadata
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = projects_api.ProjectsApi(api_client)
    id = "id_example" # str | 
    project_metadata = ProjectMetadata(
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
        metadata=Project(
            description="description_example",
            project_template_ref="project_template_ref_example",
            data_store_refs=[
                "data_store_refs_example",
            ],
            document_store_refs=[
                "document_store_refs_example",
            ],
            model_store_refs=[
                "model_store_refs_example",
            ],
            content_taxonomy_refs=[
                "content_taxonomy_refs_example",
            ],
            classification_taxonomy_refs=[
                "classification_taxonomy_refs_example",
            ],
            dashboard_refs=[
                "dashboard_refs_example",
            ],
            labels=[
                Label(
                    id="id_example",
                    color="color_example",
                    label="label_example",
                    name="name_example",
                ),
            ],
            statuses=[
                DocumentStatus(
                    id="id_example",
                    color="color_example",
                    status="status_example",
                    status_type="UNRESOLVED",
                ),
            ],
        ),
        name="name_example",
        stores=[
            StoreMetadata(
                projects=[
                    ProjectMetadata(),
                ],
                id="id_example",
                uuid="uuid_example",
                version="version_example",
                created_on=dateutil_parser('1970-01-01T00:00:00.00Z'),
                updated_on=dateutil_parser('1970-01-01T00:00:00.00Z'),
                created_by="created_by_example",
                updated_by="updated_by_example",
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
                slug="slug_example",
                metadata=Store(
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
                    store_type="DOCUMENT",
                    searchable=True,
                    store_purpose="OPERATIONAL",
                    metadata=,
                    view_options=StoreViewOptions(
                        last_event=True,
                        show_extension=True,
                        show_created=True,
                        show_modfied=True,
                    ),
                    saved_filters=[
                        SavedFilter(
                            id="id_example",
                            name="name_example",
                            filter={},
                        ),
                    ],
                ),
                extension_pack_ref="extension_pack_ref_example",
            ),
        ],
        taxonomies=[
            TaxonomyMetadata(
                projects=[
                    ProjectMetadata(),
                ],
                id="id_example",
                version="version_example",
                uuid="uuid_example",
                created_on=dateutil_parser('1970-01-01T00:00:00.00Z'),
                updated_on=dateutil_parser('1970-01-01T00:00:00.00Z'),
                created_by="created_by_example",
                updated_by="updated_by_example",
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
                slug="slug_example",
                metadata=Taxonomy(
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
                    taxonomy_type="CONTENT",
                    enabled=True,
                    taxons=[
                        Taxon(
                            id="id_example",
                            label="label_example",
                            generate_name=True,
                            group=True,
                            name="name_example",
                            value_path="VALUE_OR_ALL_CONTENT",
                            metadata_value="FILENAME",
                            data_path="data_path_example",
                            expression="expression_example",
                            description="description_example",
                            enabled=True,
                            color="color_example",
                            children=[
                                Taxon(),
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
                            node_types=[
                                "node_types_example",
                            ],
                            taxon_type="STRING",
                            type_features={
                                "key": {},
                            },
                        ),
                    ],
                    total_taxons=1,
                ),
                extension_pack_ref="extension_pack_ref_example",
            ),
        ],
        channel=ChannelMetadata(
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
        ),
    ) # ProjectMetadata | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_project(id, project_metadata)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling ProjectsApi->update_project: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **project_metadata** | [**ProjectMetadata**](ProjectMetadata.md)|  |

### Return type

[**ProjectMetadata**](ProjectMetadata.md)

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

