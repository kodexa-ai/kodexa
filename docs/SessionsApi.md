# kodexa.client.SessionsApi

All URIs are relative to *https://lehua.kodexa.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_pipeline_session_by_pipeline**](SessionsApi.md#create_pipeline_session_by_pipeline) | **POST** /api/sessions | 
[**get_events**](SessionsApi.md#get_events) | **GET** /api/sessions/{sessionId}/events | 
[**get_execution**](SessionsApi.md#get_execution) | **GET** /api/sessions/{id}/executions/{executionId} | 
[**get_execution_store**](SessionsApi.md#get_execution_store) | **GET** /api/sessions/{sessionId}/executions/{executionId}/stores/{storeId} | 
[**get_session**](SessionsApi.md#get_session) | **GET** /api/sessions/{sessionId} | 
[**list_executions**](SessionsApi.md#list_executions) | **GET** /api/sessions/{id}/executions | 
[**list_sessions**](SessionsApi.md#list_sessions) | **GET** /api/sessions | 
[**process_event**](SessionsApi.md#process_event) | **POST** /api/sessions/{sessionId}/events | 
[**update_execution_store**](SessionsApi.md#update_execution_store) | **POST** /api/sessions/{sessionId}/executions/{executionId}/stores/{storeId} | 


# **create_pipeline_session_by_pipeline**
> dict create_pipeline_session_by_pipeline(pipeline, assistant, action, pipeline2)



Create a session for the action by reference

### Example

```python
import time
import kodexa.client
from kodexa.client.api import sessions_api
from kodexa.client.model.pipeline import Pipeline
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = sessions_api.SessionsApi(api_client)
    pipeline = "pipeline_example" # str | 
    assistant = "assistant_example" # str | 
    action = "action_example" # str | 
    pipeline2 = Pipeline() # Pipeline | 
    x_access_token = "x-access-token_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_pipeline_session_by_pipeline(pipeline, assistant, action, pipeline2)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling SessionsApi->create_pipeline_session_by_pipeline: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.create_pipeline_session_by_pipeline(pipeline, assistant, action, pipeline2, x_access_token=x_access_token)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling SessionsApi->create_pipeline_session_by_pipeline: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pipeline** | **str**|  |
 **assistant** | **str**|  |
 **action** | **str**|  |
 **pipeline2** | [**Pipeline**](Pipeline.md)|  |
 **x_access_token** | **str**|  | [optional]

### Return type

**dict**

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

# **get_events**
> PageCloudSessionEvent get_events(session_id)



Get a paginated list of the events for a specific session

### Example

```python
import time
import kodexa.client
from kodexa.client.api import sessions_api
from kodexa.client.model.page_cloud_session_event import PageCloudSessionEvent
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = sessions_api.SessionsApi(api_client)
    session_id = "sessionId_example" # str | 
    x_access_token = "x-access-token_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_events(session_id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling SessionsApi->get_events: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_events(session_id, x_access_token=x_access_token)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling SessionsApi->get_events: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  |
 **x_access_token** | **str**|  | [optional]

### Return type

[**PageCloudSessionEvent**](PageCloudSessionEvent.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_execution**
> CloudExecution get_execution(id, execution_id)



Get the specified execution in the session

### Example

```python
import time
import kodexa.client
from kodexa.client.api import sessions_api
from kodexa.client.model.cloud_execution import CloudExecution
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = sessions_api.SessionsApi(api_client)
    id = "id_example" # str | 
    execution_id = "executionId_example" # str | 
    x_access_token = "x-access-token_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_execution(id, execution_id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling SessionsApi->get_execution: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_execution(id, execution_id, x_access_token=x_access_token)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling SessionsApi->get_execution: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **execution_id** | **str**|  |
 **x_access_token** | **str**|  | [optional]

### Return type

[**CloudExecution**](CloudExecution.md)

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

# **get_execution_store**
> CloudStore get_execution_store(session_id, store_id, execution_id)



Get the data and structure of a session store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import sessions_api
from kodexa.client.model.cloud_store import CloudStore
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = sessions_api.SessionsApi(api_client)
    session_id = "sessionId_example" # str | 
    store_id = "storeId_example" # str | 
    execution_id = "executionId_example" # str | 
    x_access_token = "x-access-token_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_execution_store(session_id, store_id, execution_id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling SessionsApi->get_execution_store: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_execution_store(session_id, store_id, execution_id, x_access_token=x_access_token)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling SessionsApi->get_execution_store: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  |
 **store_id** | **str**|  |
 **execution_id** | **str**|  |
 **x_access_token** | **str**|  | [optional]

### Return type

[**CloudStore**](CloudStore.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_session**
> dict get_session(x_access_token, session_id)



Get the specific session

### Example

```python
import time
import kodexa.client
from kodexa.client.api import sessions_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = sessions_api.SessionsApi(api_client)
    x_access_token = "x-access-token_example" # str | 
    session_id = "sessionId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_session(x_access_token, session_id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling SessionsApi->get_session: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_access_token** | **str**|  |
 **session_id** | **str**|  |

### Return type

**dict**

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

# **list_executions**
> PageCloudExecution list_executions(id)



Gets paginated list of executions in the session

### Example

```python
import time
import kodexa.client
from kodexa.client.api import sessions_api
from kodexa.client.model.page_cloud_execution import PageCloudExecution
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = sessions_api.SessionsApi(api_client)
    id = "id_example" # str | 
    x_access_token = "x-access-token_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.list_executions(id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling SessionsApi->list_executions: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.list_executions(id, x_access_token=x_access_token)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling SessionsApi->list_executions: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **x_access_token** | **str**|  | [optional]

### Return type

[**PageCloudExecution**](PageCloudExecution.md)

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

# **list_sessions**
> PageCloudSession list_sessions()



Get a list of the sessions by access token

### Example

```python
import time
import kodexa.client
from kodexa.client.api import sessions_api
from kodexa.client.model.page_cloud_session import PageCloudSession
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = sessions_api.SessionsApi(api_client)
    x_access_token = "x-access-token_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.list_sessions(x_access_token=x_access_token)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling SessionsApi->list_sessions: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_access_token** | **str**|  | [optional]

### Return type

[**PageCloudSession**](PageCloudSession.md)

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

# **process_event**
> CloudExecution process_event(x_access_token, session_id, cloud_session_event)



Pass, and process, a new event in the session

### Example

```python
import time
import kodexa.client
from kodexa.client.api import sessions_api
from kodexa.client.model.cloud_execution import CloudExecution
from kodexa.client.model.cloud_session_event import CloudSessionEvent
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = sessions_api.SessionsApi(api_client)
    x_access_token = "x-access-token_example" # str | 
    session_id = "sessionId_example" # str | 
    cloud_session_event = CloudSessionEvent(
        id="id_example",
        type="START_EXECUTION",
        execution_id="execution_id_example",
        store_ref="store_ref_example",
        document_family_id="document_family_id_example",
        session_id="session_id_example",
        token="token_example",
        sub_type="sub_type_example",
        step=CloudExecutionStep(
            id="id_example",
            status="PENDING",
            exception_details=ExceptionDetails(
                message="message_example",
                status_code=1,
                error_message="error_message_example",
                error_type="error_type_example",
                executed_version="executed_version_example",
                advice="advice_example",
                description="description_example",
                cause={},
                documentation_url="documentation_url_example",
                stack_trace=[
                    {},
                ],
                help="help_example",
                option_errors={
                    "key": {},
                },
                validation_errors=[
                    ValidationError(
                        message="message_example",
                        option="option_example",
                        description="description_example",
                    ),
                ],
            ),
            name="name_example",
            start=dateutil_parser('1970-01-01T00:00:00.00Z'),
            end=dateutil_parser('1970-01-01T00:00:00.00Z'),
            processing_time=1,
            parameterized=True,
            conditional=True,
            enabled=True,
            condition="condition_example",
            options={
                "key": {},
            },
            option_types={
                "key": "key_example",
            },
            context={
                "key": {},
            },
            content_objects=[
                ContentObject(
                    id="id_example",
                    document_version="document_version_example",
                    labels=[
                        "labels_example",
                    ],
                    classes=[
                        ContentClassification(
                            label="label_example",
                            taxonomy="taxonomy_example",
                            selector="selector_example",
                            confidence=3.14,
                        ),
                    ],
                    metadata={
                        "key": {},
                    },
                    source=SourceMetadata(
                        checksum="checksum_example",
                        created="created_example",
                        connector="connector_example",
                        cid="cid_example",
                        headers={
                            "key": {},
                        },
                        original_filename="original_filename_example",
                        original_path="original_path_example",
                        last_modified="last_modified_example",
                        mime_type="mime_type_example",
                        lineage_document_uuid="lineage_document_uuid_example",
                        document_family_id="document_family_id_example",
                        source_document_uuid="source_document_uuid_example",
                    ),
                    mixins=[
                        "mixins_example",
                    ],
                    content_metadata={
                        "key": {},
                    },
                    overlays=[
                        FeatureOverlay(
                            id="id_example",
                            size=1,
                        ),
                    ],
                    created=dateutil_parser('1970-01-01T00:00:00.00Z'),
                    modified=dateutil_parser('1970-01-01T00:00:00.00Z'),
                    size=1,
                    created_date=dateutil_parser('1970-01-01T00:00:00.00Z'),
                    modified_date=dateutil_parser('1970-01-01T00:00:00.00Z'),
                    content_type="DOCUMENT",
                    store_ref="store_ref_example",
                ),
            ],
            stores=[
                CloudStore(
                    id="id_example",
                    name="name_example",
                    store_type="DOCUMENT",
                    ref="ref_example",
                    data={
                        "key": {},
                    },
                ),
            ],
            input_id="input_id_example",
            output_id="output_id_example",
            ref="ref_example",
            deployment_type="KUBERNETES",
            service_name="service_name_example",
            container_name="container_name_example",
        ),
        connector=CloudConnector(
            ref="ref_example",
            service_name="service_name_example",
            container_name="container_name_example",
            options={
                "key": {},
            },
            status="PENDING",
            exception_details=ExceptionDetails(
                message="message_example",
                status_code=1,
                error_message="error_message_example",
                error_type="error_type_example",
                executed_version="executed_version_example",
                advice="advice_example",
                description="description_example",
                cause={},
                documentation_url="documentation_url_example",
                stack_trace=[
                    {},
                ],
                help="help_example",
                option_errors={
                    "key": {},
                },
                validation_errors=[
                    ValidationError(
                        message="message_example",
                        option="option_example",
                        description="description_example",
                    ),
                ],
            ),
            target="target_example",
            download=True,
            start=dateutil_parser('1970-01-01T00:00:00.00Z'),
            end=dateutil_parser('1970-01-01T00:00:00.00Z'),
            processing_time=1,
        ),
        assistant=CloudAssistant(
            assistant_id="assistant_id_example",
            assistant_name="assistant_name_example",
            ref="ref_example",
            deployment_type="KUBERNETES",
            service_name="service_name_example",
            container_name="container_name_example",
            options={
                "key": {},
            },
            option_types={
                "key": "key_example",
            },
            status="PENDING",
            exception_details=ExceptionDetails(
                message="message_example",
                status_code=1,
                error_message="error_message_example",
                error_type="error_type_example",
                executed_version="executed_version_example",
                advice="advice_example",
                description="description_example",
                cause={},
                documentation_url="documentation_url_example",
                stack_trace=[
                    {},
                ],
                help="help_example",
                option_errors={
                    "key": {},
                },
                validation_errors=[
                    ValidationError(
                        message="message_example",
                        option="option_example",
                        description="description_example",
                    ),
                ],
            ),
            event=,
            response=CloudAssistantResponse(
                text="text_example",
                pipelines=[
                    CloudAssistantPipeline(
                        description="description_example",
                        pipeline=Pipeline(),
                        write_back_to_store=True,
                        data_source_ref="data_source_ref_example",
                        taxonomy_refs=[
                            "taxonomy_refs_example",
                        ],
                    ),
                ],
            ),
            start=dateutil_parser('1970-01-01T00:00:00.00Z'),
            end=dateutil_parser('1970-01-01T00:00:00.00Z'),
            processing_time=1,
        ),
        source={
            "key": {},
        },
        payload={
            "key": {},
        },
        content_objects=[
            ContentObject(
                id="id_example",
                document_version="document_version_example",
                labels=[
                    "labels_example",
                ],
                classes=[
                    ContentClassification(
                        label="label_example",
                        taxonomy="taxonomy_example",
                        selector="selector_example",
                        confidence=3.14,
                    ),
                ],
                metadata={
                    "key": {},
                },
                source=SourceMetadata(
                    checksum="checksum_example",
                    created="created_example",
                    connector="connector_example",
                    cid="cid_example",
                    headers={
                        "key": {},
                    },
                    original_filename="original_filename_example",
                    original_path="original_path_example",
                    last_modified="last_modified_example",
                    mime_type="mime_type_example",
                    lineage_document_uuid="lineage_document_uuid_example",
                    document_family_id="document_family_id_example",
                    source_document_uuid="source_document_uuid_example",
                ),
                mixins=[
                    "mixins_example",
                ],
                content_metadata={
                    "key": {},
                },
                overlays=[
                    FeatureOverlay(
                        id="id_example",
                        size=1,
                    ),
                ],
                created=dateutil_parser('1970-01-01T00:00:00.00Z'),
                modified=dateutil_parser('1970-01-01T00:00:00.00Z'),
                size=1,
                created_date=dateutil_parser('1970-01-01T00:00:00.00Z'),
                modified_date=dateutil_parser('1970-01-01T00:00:00.00Z'),
                content_type="DOCUMENT",
                store_ref="store_ref_example",
            ),
        ],
        input_id="input_id_example",
        target_deployment_type="KUBERNETES",
        target="target_example",
        platform_url="platform_url_example",
        debug=True,
        created=dateutil_parser('1970-01-01T00:00:00.00Z'),
    ) # CloudSessionEvent | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.process_event(x_access_token, session_id, cloud_session_event)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling SessionsApi->process_event: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_access_token** | **str**|  |
 **session_id** | **str**|  |
 **cloud_session_event** | [**CloudSessionEvent**](CloudSessionEvent.md)|  |

### Return type

[**CloudExecution**](CloudExecution.md)

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

# **update_execution_store**
> CloudStore update_execution_store(session_id, store_id, execution_id, cloud_store)



Update a execution-based store content

### Example

```python
import time
import kodexa.client
from kodexa.client.api import sessions_api
from kodexa.client.model.cloud_store import CloudStore
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = sessions_api.SessionsApi(api_client)
    session_id = "sessionId_example" # str | 
    store_id = "storeId_example" # str | 
    execution_id = "executionId_example" # str | 
    cloud_store = CloudStore(
        id="id_example",
        name="name_example",
        store_type="DOCUMENT",
        ref="ref_example",
        data={
            "key": {},
        },
    ) # CloudStore | 
    x_access_token = "x-access-token_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_execution_store(session_id, store_id, execution_id, cloud_store)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling SessionsApi->update_execution_store: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.update_execution_store(session_id, store_id, execution_id, cloud_store, x_access_token=x_access_token)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling SessionsApi->update_execution_store: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  |
 **store_id** | **str**|  |
 **execution_id** | **str**|  |
 **cloud_store** | [**CloudStore**](CloudStore.md)|  |
 **x_access_token** | **str**|  | [optional]

### Return type

[**CloudStore**](CloudStore.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

