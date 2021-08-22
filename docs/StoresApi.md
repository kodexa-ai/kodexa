# kodexa.client.StoresApi

All URIs are relative to *https://lehua.kodexa.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**bulk_set_lock**](StoresApi.md#bulk_set_lock) | **PUT** /api/stores/{orgSlug}/{slug}/families | 
[**bulk_set_lock_with_version**](StoresApi.md#bulk_set_lock_with_version) | **PUT** /api/stores/{orgSlug}/{slug}/{version}/families | 
[**create_overlay**](StoresApi.md#create_overlay) | **POST** /api/stores/{orgSlug}/{slug}/{version}/families/{id}/objects/{objectId}/overlays | 
[**create_rows**](StoresApi.md#create_rows) | **POST** /api/stores/{orgSlug}/{slug}/rows | 
[**create_rows_for_version**](StoresApi.md#create_rows_for_version) | **POST** /api/stores/{orgSlug}/{slug}/{version}/rows | 
[**create_store**](StoresApi.md#create_store) | **POST** /api/stores/{organizationSlug} | 
[**delete_content_object_with_version**](StoresApi.md#delete_content_object_with_version) | **DELETE** /api/stores/{orgSlug}/{slug}/{version}/families/{documentFamilyId}/objects/{id} | 
[**delete_content_objects_with_version**](StoresApi.md#delete_content_objects_with_version) | **DELETE** /api/stores/{orgSlug}/{slug}/{version}/families | 
[**delete_families**](StoresApi.md#delete_families) | **DELETE** /api/stores/{orgSlug}/{slug}/families | 
[**delete_family_by_id**](StoresApi.md#delete_family_by_id) | **DELETE** /api/stores/{orgSlug}/{slug}/families/{id} | 
[**delete_family_by_path**](StoresApi.md#delete_family_by_path) | **DELETE** /api/stores/{orgSlug}/{slug}/fs/** | 
[**delete_family_by_path_with_version**](StoresApi.md#delete_family_by_path_with_version) | **DELETE** /api/stores/{orgSlug}/{slug}/{version}/fs/** | 
[**delete_family_id_with_version**](StoresApi.md#delete_family_id_with_version) | **DELETE** /api/stores/{orgSlug}/{slug}/{version}/families/{id} | 
[**delete_rows**](StoresApi.md#delete_rows) | **DELETE** /api/stores/{orgSlug}/{slug}/rows | 
[**delete_rows_with_version**](StoresApi.md#delete_rows_with_version) | **DELETE** /api/stores/{orgSlug}/{slug}/{version}/rows | 
[**delete_store**](StoresApi.md#delete_store) | **DELETE** /api/stores/{organizationSlug}/{slug} | 
[**delete_version_store**](StoresApi.md#delete_version_store) | **DELETE** /api/stores/{organizationSlug}/{slug}/{version} | 
[**get_content_object_image**](StoresApi.md#get_content_object_image) | **GET** /api/stores/{orgSlug}/{slug}/families/{documentFamilyId}/preview/{page} | 
[**get_content_object_image_with_version**](StoresApi.md#get_content_object_image_with_version) | **GET** /api/stores/{orgSlug}/{slug}/{version}/families/{documentFamilyId}/preview/{page} | 
[**get_family**](StoresApi.md#get_family) | **GET** /api/stores/{orgSlug}/{slug}/families/{id} | 
[**get_family_by_path**](StoresApi.md#get_family_by_path) | **GET** /api/stores/{orgSlug}/{slug}/fs/** | 
[**get_family_by_path_with_version**](StoresApi.md#get_family_by_path_with_version) | **GET** /api/stores/{orgSlug}/{slug}/{version}/fs/** | 
[**get_family_events**](StoresApi.md#get_family_events) | **GET** /api/stores/{orgSlug}/{slug}/families/{id}/events | 
[**get_family_events_with_version**](StoresApi.md#get_family_events_with_version) | **GET** /api/stores/{orgSlug}/{slug}/{version}/families/{id}/events | 
[**get_family_table_counts**](StoresApi.md#get_family_table_counts) | **GET** /api/stores/{orgSlug}/{slug}/{version}/families/{id}/tableCounts | 
[**get_family_with_version**](StoresApi.md#get_family_with_version) | **GET** /api/stores/{orgSlug}/{slug}/{version}/families/{id} | 
[**get_rows**](StoresApi.md#get_rows) | **GET** /api/stores/{orgSlug}/{slug}/rows | 
[**get_rows_with_version**](StoresApi.md#get_rows_with_version) | **GET** /api/stores/{orgSlug}/{slug}/{version}/rows | 
[**get_store**](StoresApi.md#get_store) | **GET** /api/stores/{organizationSlug}/{slug} | 
[**get_store_metadata**](StoresApi.md#get_store_metadata) | **GET** /api/stores/{orgSlug}/{slug}/metadata | 
[**get_store_metadata_with_version**](StoresApi.md#get_store_metadata_with_version) | **GET** /api/stores/{orgSlug}/{slug}/{version}/metadata | 
[**get_taxonomies**](StoresApi.md#get_taxonomies) | **GET** /api/stores/{orgSlug}/{slug}/taxonomies | 
[**get_taxonomies_by_version**](StoresApi.md#get_taxonomies_by_version) | **GET** /api/stores/{orgSlug}/{slug}/{version}/taxonomies | 
[**get_version_store**](StoresApi.md#get_version_store) | **GET** /api/stores/{organizationSlug}/{slug}/{version} | 
[**list_families**](StoresApi.md#list_families) | **GET** /api/stores/{orgSlug}/{slug}/families | 
[**list_families_with_version**](StoresApi.md#list_families_with_version) | **GET** /api/stores/{orgSlug}/{slug}/{version}/families | 
[**list_store**](StoresApi.md#list_store) | **GET** /api/stores/{organizationSlug} | 
[**lock_family**](StoresApi.md#lock_family) | **PUT** /api/stores/{orgSlug}/{slug}/families/{familyId}/lock | 
[**lock_family_with_version**](StoresApi.md#lock_family_with_version) | **PUT** /api/stores/{orgSlug}/{slug}/{version}/families/{familyId}/lock | 
[**reindex_content_objects**](StoresApi.md#reindex_content_objects) | **POST** /api/stores/{orgSlug}/{slug}/_reindex | 
[**reindex_content_objects_with_version**](StoresApi.md#reindex_content_objects_with_version) | **POST** /api/stores/{orgSlug}/{slug}/{version}/_reindex | 
[**rename_family**](StoresApi.md#rename_family) | **PUT** /api/stores/{orgSlug}/{slug}/fs/** | 
[**rename_family_with_version**](StoresApi.md#rename_family_with_version) | **PUT** /api/stores/{orgSlug}/{slug}/{version}/fs/** | 
[**reprocess_assistants**](StoresApi.md#reprocess_assistants) | **PUT** /api/stores/{orgSlug}/{slug}/reprocessAssistants | 
[**reprocess_assistants_for_family**](StoresApi.md#reprocess_assistants_for_family) | **PUT** /api/stores/{orgSlug}/{slug}/families/{id}/reprocessAssistants | 
[**reprocess_assistants_for_family_with_version**](StoresApi.md#reprocess_assistants_for_family_with_version) | **PUT** /api/stores/{orgSlug}/{slug}/{version}/families/{id}/reprocessAssistants | 
[**reprocess_assistants_with_version**](StoresApi.md#reprocess_assistants_with_version) | **PUT** /api/stores/{orgSlug}/{slug}/{version}/reprocessAssistants | 
[**search_family**](StoresApi.md#search_family) | **GET** /api/stores/{orgSlug}/{slug}/families/{id}/_search | 
[**search_family_with_version**](StoresApi.md#search_family_with_version) | **GET** /api/stores/{orgSlug}/{slug}/{version}/families/{id}/_search | 
[**unlock_family**](StoresApi.md#unlock_family) | **PUT** /api/stores/{orgSlug}/{slug}/families/{familyId}/unlock | 
[**unlock_family_with_version**](StoresApi.md#unlock_family_with_version) | **PUT** /api/stores/{orgSlug}/{slug}/{version}/families/{familyId}/unlock | 
[**update_content_object_in_family**](StoresApi.md#update_content_object_in_family) | **PUT** /api/stores/{orgSlug}/{slug}/{version}/families/{id}/objects/{objectId}/content | 
[**update_family**](StoresApi.md#update_family) | **PUT** /api/stores/{orgSlug}/{slug}/{version}/families/{id} | 
[**update_overlay**](StoresApi.md#update_overlay) | **PUT** /api/stores/{orgSlug}/{slug}/{version}/families/{id}/objects/{objectId}/overlays/{overlayId} | 
[**update_row**](StoresApi.md#update_row) | **PUT** /api/stores/{orgSlug}/{slug}/rows/{rowId} | 
[**update_row_with_version**](StoresApi.md#update_row_with_version) | **PUT** /api/stores/{orgSlug}/{slug}/{version}/rows/{rowId} | 
[**update_store**](StoresApi.md#update_store) | **PUT** /api/stores/{organizationSlug}/{slug} | 
[**update_store_metadata**](StoresApi.md#update_store_metadata) | **PUT** /api/stores/{orgSlug}/{slug}/metadata | 
[**update_store_metadata_with_version**](StoresApi.md#update_store_metadata_with_version) | **PUT** /api/stores/{orgSlug}/{slug}/{version}/metadata | 
[**update_version_store**](StoresApi.md#update_version_store) | **PUT** /api/stores/{organizationSlug}/{slug}/{version} | 


# **bulk_set_lock**
> bulk_set_lock(org_slug, slug, bulk_lock)



Bulk set the lock on a list of document families

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.bulk_lock import BulkLock
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    bulk_lock = BulkLock(
        lock=True,
        document_family_ids=[
            "document_family_ids_example",
        ],
    ) # BulkLock | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.bulk_set_lock(org_slug, slug, bulk_lock)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->bulk_set_lock: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **bulk_lock** | [**BulkLock**](BulkLock.md)|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **bulk_set_lock_with_version**
> bulk_set_lock_with_version(org_slug, slug, version, bulk_lock)



Bulk set the lock on a list of document families

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.bulk_lock import BulkLock
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    bulk_lock = BulkLock(
        lock=True,
        document_family_ids=[
            "document_family_ids_example",
        ],
    ) # BulkLock | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.bulk_set_lock_with_version(org_slug, slug, version, bulk_lock)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->bulk_set_lock_with_version: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **bulk_lock** | [**BulkLock**](BulkLock.md)|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_overlay**
> DocumentFamily create_overlay(org_slug, slug, version, id, object_id)



Create a new overlay on a content object

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.inline_object2 import InlineObject2
from kodexa.client.model.document_family import DocumentFamily
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    id = "id_example" # str | 
    object_id = "objectId_example" # str | 
    inline_object2 = InlineObject2(
        feature_set=open('/path/to/file', 'rb'),
    ) # InlineObject2 |  (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_overlay(org_slug, slug, version, id, object_id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->create_overlay: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.create_overlay(org_slug, slug, version, id, object_id, inline_object2=inline_object2)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->create_overlay: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **id** | **str**|  |
 **object_id** | **str**|  |
 **inline_object2** | [**InlineObject2**](InlineObject2.md)|  | [optional]

### Return type

[**DocumentFamily**](DocumentFamily.md)

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

# **create_rows**
> create_rows(org_slug, slug, stored_row)



Add rows to the the current version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.stored_row import StoredRow
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    stored_row = [
        StoredRow(
            id="id_example",
            org_slug="org_slug_example",
            slug="slug_example",
            version="version_example",
            taxonomy_ref="taxonomy_ref_example",
            path="path_example",
            row_num=1,
            source_ordering="source_ordering_example",
            date_time=dateutil_parser('1970-01-01T00:00:00.00Z'),
            lineage=DataLineage(
                store_ref="store_ref_example",
                document_family_id="document_family_id_example",
                execution_id="execution_id_example",
                content_object_id="content_object_id_example",
            ),
            cells=[
                DataCell(
                    value="value_example",
                    truncated=True,
                    data_type="STRING",
                    tag="tag_example",
                    tag_uuid="tag_uuid_example",
                    date_value="date_value_example",
                    decimal_value=3.14,
                    number_value=1,
                    boolean_value=True,
                    string_value="string_value_example",
                    validation_state="VALID",
                    validation_messages=[
                        CellValidationMessage(
                            message="message_example",
                            validation_features={
                                "key": {},
                            },
                        ),
                    ],
                    data_features={
                        "key": {},
                    },
                    audit_events=[
                        AuditEvent(
                            id="id_example",
                            audit_user="audit_user_example",
                            created=dateutil_parser('1970-01-01T00:00:00.00Z'),
                            cell_override=DataCell(),
                        ),
                    ],
                    label="label_example",
                ),
            ],
            parent_id="parent_id_example",
            table="table_example",
            data={
                "key": "key_example",
            },
        ),
    ] # [StoredRow] | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.create_rows(org_slug, slug, stored_row)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->create_rows: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **stored_row** | [**[StoredRow]**](StoredRow.md)|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_rows_for_version**
> create_rows_for_version(org_slug, slug, version, stored_row)



Add a list of rows to a specific version of the store (import mode)

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.stored_row import StoredRow
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    stored_row = [
        StoredRow(
            id="id_example",
            org_slug="org_slug_example",
            slug="slug_example",
            version="version_example",
            taxonomy_ref="taxonomy_ref_example",
            path="path_example",
            row_num=1,
            source_ordering="source_ordering_example",
            date_time=dateutil_parser('1970-01-01T00:00:00.00Z'),
            lineage=DataLineage(
                store_ref="store_ref_example",
                document_family_id="document_family_id_example",
                execution_id="execution_id_example",
                content_object_id="content_object_id_example",
            ),
            cells=[
                DataCell(
                    value="value_example",
                    truncated=True,
                    data_type="STRING",
                    tag="tag_example",
                    tag_uuid="tag_uuid_example",
                    date_value="date_value_example",
                    decimal_value=3.14,
                    number_value=1,
                    boolean_value=True,
                    string_value="string_value_example",
                    validation_state="VALID",
                    validation_messages=[
                        CellValidationMessage(
                            message="message_example",
                            validation_features={
                                "key": {},
                            },
                        ),
                    ],
                    data_features={
                        "key": {},
                    },
                    audit_events=[
                        AuditEvent(
                            id="id_example",
                            audit_user="audit_user_example",
                            created=dateutil_parser('1970-01-01T00:00:00.00Z'),
                            cell_override=DataCell(),
                        ),
                    ],
                    label="label_example",
                ),
            ],
            parent_id="parent_id_example",
            table="table_example",
            data={
                "key": "key_example",
            },
        ),
    ] # [StoredRow] | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.create_rows_for_version(org_slug, slug, version, stored_row)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->create_rows_for_version: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **stored_row** | [**[StoredRow]**](StoredRow.md)|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_store**
> Store create_store(organization_slug, store)



Create a new instance of the object in the organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
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
    api_instance = stores_api.StoresApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    store = Store(
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
    ) # Store | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_store(organization_slug, store)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->create_store: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **store** | [**Store**](Store.md)|  |

### Return type

[**Store**](Store.md)

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

# **delete_content_object_with_version**
> bool delete_content_object_with_version(org_slug, slug, version, document_family_id, id)



Delete specific content object from document family

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    document_family_id = "documentFamilyId_example" # str | 
    id = "id_example" # str | 
    group_lineage = "false" # str |  (optional) if omitted the server will use the default value of "false"

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.delete_content_object_with_version(org_slug, slug, version, document_family_id, id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->delete_content_object_with_version: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.delete_content_object_with_version(org_slug, slug, version, document_family_id, id, group_lineage=group_lineage)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->delete_content_object_with_version: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **document_family_id** | **str**|  |
 **id** | **str**|  |
 **group_lineage** | **str**|  | [optional] if omitted the server will use the default value of "false"

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

# **delete_content_objects_with_version**
> delete_content_objects_with_version(org_slug, slug, version, bulk_delete)



Bulk delete a set of document families the specified version

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.bulk_delete import BulkDelete
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    bulk_delete = BulkDelete(
        document_family_ids=[
            "document_family_ids_example",
        ],
    ) # BulkDelete | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_content_objects_with_version(org_slug, slug, version, bulk_delete)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->delete_content_objects_with_version: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **bulk_delete** | [**BulkDelete**](BulkDelete.md)|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_families**
> delete_families(org_slug, slug, bulk_delete)



Bulk delete a set of document families in the current version

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.bulk_delete import BulkDelete
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    bulk_delete = BulkDelete(
        document_family_ids=[
            "document_family_ids_example",
        ],
    ) # BulkDelete | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_families(org_slug, slug, bulk_delete)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->delete_families: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **bulk_delete** | [**BulkDelete**](BulkDelete.md)|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_family_by_id**
> bool delete_family_by_id(org_slug, slug, id)



Delete a specific document family in the current version of a store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.delete_family_by_id(org_slug, slug, id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->delete_family_by_id: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **id** | **str**|  |

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

# **delete_family_by_path**
> bool delete_family_by_path(org_slug, slug)



Delete document family by path in the current version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.delete_family_by_path(org_slug, slug)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->delete_family_by_path: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
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

# **delete_family_by_path_with_version**
> bool delete_family_by_path_with_version(org_slug, slug, version)



Delete document family by path in a specific version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.delete_family_by_path_with_version(org_slug, slug, version)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->delete_family_by_path_with_version: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
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

# **delete_family_id_with_version**
> bool delete_family_id_with_version(org_slug, slug, version, id)



Delete a specific document family in a version of a store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.delete_family_id_with_version(org_slug, slug, version, id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->delete_family_id_with_version: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **id** | **str**|  |

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

# **delete_rows**
> delete_rows(org_slug, slug)



Delete the rows from the current version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_rows(org_slug, slug)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->delete_rows: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |

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

# **delete_rows_with_version**
> delete_rows_with_version(org_slug, slug, version)



Delete the rows from a specific version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_rows_with_version(org_slug, slug, version)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->delete_rows_with_version: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |

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

# **delete_store**
> bool delete_store(organization_slug, slug)



Delete the current version of the given object

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.delete_store(organization_slug, slug)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->delete_store: %s\n" % e)
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

# **delete_version_store**
> bool delete_version_store(organization_slug, slug, version)



Delete the specified version of the given object

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.delete_version_store(organization_slug, slug, version)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->delete_version_store: %s\n" % e)
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

# **get_content_object_image**
> str get_content_object_image(org_slug, slug, document_family_id, page)



Generate a preview for a page of the latest content in a document family in the current version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    document_family_id = "documentFamilyId_example" # str | 
    page = 1 # int | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_content_object_image(org_slug, slug, document_family_id, page)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->get_content_object_image: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **document_family_id** | **str**|  |
 **page** | **int**|  |

### Return type

**str**

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

# **get_content_object_image_with_version**
> str get_content_object_image_with_version(org_slug, slug, version, document_family_id, page)



Generate a preview for a page of the latest content in a document family in a specific version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    document_family_id = "documentFamilyId_example" # str | 
    page = 1 # int | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_content_object_image_with_version(org_slug, slug, version, document_family_id, page)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->get_content_object_image_with_version: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **document_family_id** | **str**|  |
 **page** | **int**|  |

### Return type

**str**

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

# **get_family**
> DocumentFamily get_family(org_slug, slug, id)



Get a specific document family in the current version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.document_family import DocumentFamily
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_family(org_slug, slug, id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->get_family: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **id** | **str**|  |

### Return type

[**DocumentFamily**](DocumentFamily.md)

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

# **get_family_by_path**
> DocumentFamily get_family_by_path(org_slug, slug)



Get the document family for a path in the current version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.document_family import DocumentFamily
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_family_by_path(org_slug, slug)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->get_family_by_path: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |

### Return type

[**DocumentFamily**](DocumentFamily.md)

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

# **get_family_by_path_with_version**
> DocumentFamily get_family_by_path_with_version(org_slug, slug, version)



Get the document family for a path in the specific version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.document_family import DocumentFamily
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_family_by_path_with_version(org_slug, slug, version)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->get_family_by_path_with_version: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |

### Return type

[**DocumentFamily**](DocumentFamily.md)

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

# **get_family_events**
> [PlatformEvent] get_family_events(org_slug, slug, id)



Get events for a specific document family in the current version of a store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
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
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_family_events(org_slug, slug, id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->get_family_events: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **id** | **str**|  |

### Return type

[**[PlatformEvent]**](PlatformEvent.md)

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

# **get_family_events_with_version**
> [PlatformEvent] get_family_events_with_version(org_slug, slug, version, id)



Get events for a specific document family in a version of a store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
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
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_family_events_with_version(org_slug, slug, version, id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->get_family_events_with_version: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **id** | **str**|  |

### Return type

[**[PlatformEvent]**](PlatformEvent.md)

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

# **get_family_table_counts**
> {str: (int,)} get_family_table_counts(org_slug, slug, version, id)



Get the counts of extracted data, by parent taxon, for a specific family

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_family_table_counts(org_slug, slug, version, id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->get_family_table_counts: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **id** | **str**|  |

### Return type

**{str: (int,)}**

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

# **get_family_with_version**
> DocumentFamily get_family_with_version(org_slug, slug, version, id)



Get a specific document family in a version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.document_family import DocumentFamily
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_family_with_version(org_slug, slug, version, id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->get_family_with_version: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **id** | **str**|  |

### Return type

[**DocumentFamily**](DocumentFamily.md)

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

# **get_rows**
> PageStoredRow get_rows(org_slug, slug, query_context)



Get the paginated rows from the current version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.page_stored_row import PageStoredRow
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
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    query_context = QueryContext(
        page_size__default_20=1,
        page_number__default_1=1,
        sorts_to_apply="sorts_to_apply_example",
        simple_filter_to_apply="simple_filter_to_apply_example",
    ) # QueryContext | 
    query = "*" # str |  (optional) if omitted the server will use the default value of "*"
    table = "" # str |  (optional) if omitted the server will use the default value of ""
    parent = "" # str |  (optional) if omitted the server will use the default value of ""
    document_family_id = "" # str |  (optional) if omitted the server will use the default value of ""
    store_ref = "" # str |  (optional) if omitted the server will use the default value of ""

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_rows(org_slug, slug, query_context)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->get_rows: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_rows(org_slug, slug, query_context, query=query, table=table, parent=parent, document_family_id=document_family_id, store_ref=store_ref)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->get_rows: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **query_context** | **QueryContext**|  |
 **query** | **str**|  | [optional] if omitted the server will use the default value of "*"
 **table** | **str**|  | [optional] if omitted the server will use the default value of ""
 **parent** | **str**|  | [optional] if omitted the server will use the default value of ""
 **document_family_id** | **str**|  | [optional] if omitted the server will use the default value of ""
 **store_ref** | **str**|  | [optional] if omitted the server will use the default value of ""

### Return type

[**PageStoredRow**](PageStoredRow.md)

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

# **get_rows_with_version**
> PageStoredRow get_rows_with_version(org_slug, slug, version, query_context)



Get the paginated rows from a specific version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.page_stored_row import PageStoredRow
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
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    query_context = QueryContext(
        page_size__default_20=1,
        page_number__default_1=1,
        sorts_to_apply="sorts_to_apply_example",
        simple_filter_to_apply="simple_filter_to_apply_example",
    ) # QueryContext | 
    query = "*" # str |  (optional) if omitted the server will use the default value of "*"
    table = "" # str |  (optional) if omitted the server will use the default value of ""
    parent = "" # str |  (optional) if omitted the server will use the default value of ""
    document_family_id = "" # str |  (optional) if omitted the server will use the default value of ""
    store_ref = "" # str |  (optional) if omitted the server will use the default value of ""

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_rows_with_version(org_slug, slug, version, query_context)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->get_rows_with_version: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_rows_with_version(org_slug, slug, version, query_context, query=query, table=table, parent=parent, document_family_id=document_family_id, store_ref=store_ref)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->get_rows_with_version: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **query_context** | **QueryContext**|  |
 **query** | **str**|  | [optional] if omitted the server will use the default value of "*"
 **table** | **str**|  | [optional] if omitted the server will use the default value of ""
 **parent** | **str**|  | [optional] if omitted the server will use the default value of ""
 **document_family_id** | **str**|  | [optional] if omitted the server will use the default value of ""
 **store_ref** | **str**|  | [optional] if omitted the server will use the default value of ""

### Return type

[**PageStoredRow**](PageStoredRow.md)

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

# **get_store**
> Store get_store(organization_slug, slug)



Get the current version of the object with given slug

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
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
    api_instance = stores_api.StoresApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_store(organization_slug, slug)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->get_store: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |

### Return type

[**Store**](Store.md)

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

# **get_store_metadata**
> dict get_store_metadata(org_slug, slug)



Get a specific document family in a version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_store_metadata(org_slug, slug)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->get_store_metadata: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |

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

# **get_store_metadata_with_version**
> dict get_store_metadata_with_version(org_slug, slug, version)



Get a specific document family in a version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_store_metadata_with_version(org_slug, slug, version)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->get_store_metadata_with_version: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |

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

# **get_taxonomies**
> [Taxonomy] get_taxonomies(org_slug, slug)



Get the taxonomies that are referenced (data store) in the current version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
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
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_taxonomies(org_slug, slug)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->get_taxonomies: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |

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

# **get_taxonomies_by_version**
> [Taxonomy] get_taxonomies_by_version(org_slug, slug, version)



Get the taxonomies that are referenced (data store) in a specific version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
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
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_taxonomies_by_version(org_slug, slug, version)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->get_taxonomies_by_version: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |

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

# **get_version_store**
> Store get_version_store(organization_slug, slug, version)



Get the specific version of the object with given slug

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
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
    api_instance = stores_api.StoresApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_version_store(organization_slug, slug, version)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->get_version_store: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |

### Return type

[**Store**](Store.md)

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

# **list_families**
> PageDocumentFamily list_families(org_slug, slug, query_context)



List (with pagination) the document families in the current version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.page_document_family import PageDocumentFamily
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
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    query_context = QueryContext(
        page_size__default_20=1,
        page_number__default_1=1,
        sorts_to_apply="sorts_to_apply_example",
        simple_filter_to_apply="simple_filter_to_apply_example",
    ) # QueryContext | 
    query = "*" # str |  (optional) if omitted the server will use the default value of "*"

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.list_families(org_slug, slug, query_context)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->list_families: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.list_families(org_slug, slug, query_context, query=query)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->list_families: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **query_context** | **QueryContext**|  |
 **query** | **str**|  | [optional] if omitted the server will use the default value of "*"

### Return type

[**PageDocumentFamily**](PageDocumentFamily.md)

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

# **list_families_with_version**
> PageDocumentFamily list_families_with_version(org_slug, slug, version, query_context)



List (with pagination) the enriched (include transition events, and extracted data counts) document families in a specific version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.page_document_family import PageDocumentFamily
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
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    query_context = QueryContext(
        page_size__default_20=1,
        page_number__default_1=1,
        sorts_to_apply="sorts_to_apply_example",
        simple_filter_to_apply="simple_filter_to_apply_example",
    ) # QueryContext | 
    query = "*" # str |  (optional) if omitted the server will use the default value of "*"

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.list_families_with_version(org_slug, slug, version, query_context)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->list_families_with_version: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.list_families_with_version(org_slug, slug, version, query_context, query=query)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->list_families_with_version: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **query_context** | **QueryContext**|  |
 **query** | **str**|  | [optional] if omitted the server will use the default value of "*"

### Return type

[**PageDocumentFamily**](PageDocumentFamily.md)

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

# **list_store**
> PageStore list_store(organization_slug)



Get a paginated list of the objects for an organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.page_store import PageStore
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    query = "*" # str |  (optional) if omitted the server will use the default value of "*"
    include_public = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.list_store(organization_slug)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->list_store: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.list_store(organization_slug, query=query, include_public=include_public)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->list_store: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **query** | **str**|  | [optional] if omitted the server will use the default value of "*"
 **include_public** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**PageStore**](PageStore.md)

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

# **lock_family**
> lock_family(org_slug, slug, family_id)



Lock the given family in the current version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    family_id = "familyId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.lock_family(org_slug, slug, family_id)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->lock_family: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **family_id** | **str**|  |

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

# **lock_family_with_version**
> lock_family_with_version(org_slug, slug, version, family_id)



Lock the given family in the given version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    family_id = "familyId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.lock_family_with_version(org_slug, slug, version, family_id)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->lock_family_with_version: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **family_id** | **str**|  |

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

# **reindex_content_objects**
> reindex_content_objects(org_slug, slug)



Reindex  documents or data families in current version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.reindex_content_objects(org_slug, slug)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->reindex_content_objects: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |

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

# **reindex_content_objects_with_version**
> reindex_content_objects_with_version(org_slug, slug, version)



Reindex documents or data in specified version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.reindex_content_objects_with_version(org_slug, slug, version)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->reindex_content_objects_with_version: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |

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

# **rename_family**
> DocumentFamily rename_family(org_slug, slug)



### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.document_family import DocumentFamily
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    rename = "rename_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.rename_family(org_slug, slug)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->rename_family: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.rename_family(org_slug, slug, rename=rename)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->rename_family: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **rename** | **str**|  | [optional]

### Return type

[**DocumentFamily**](DocumentFamily.md)

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

# **rename_family_with_version**
> DocumentFamily rename_family_with_version(org_slug, slug, version)



Rename the path of a document family in the current version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.document_family import DocumentFamily
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    rename = "rename_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.rename_family_with_version(org_slug, slug, version)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->rename_family_with_version: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.rename_family_with_version(org_slug, slug, version, rename=rename)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->rename_family_with_version: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **rename** | **str**|  | [optional]

### Return type

[**DocumentFamily**](DocumentFamily.md)

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

# **reprocess_assistants**
> reprocess_assistants(org_slug, slug, reprocess_request)



Reprocess content in the store, allow you to provide a list of the family ID's

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.reprocess_request import ReprocessRequest
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    reprocess_request = ReprocessRequest(
        assistant_ids=[
            "assistant_ids_example",
        ],
        family_ids=[
            "family_ids_example",
        ],
    ) # ReprocessRequest | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.reprocess_assistants(org_slug, slug, reprocess_request)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->reprocess_assistants: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **reprocess_request** | [**ReprocessRequest**](ReprocessRequest.md)|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **reprocess_assistants_for_family**
> reprocess_assistants_for_family(org_slug, slug, id, assistant_id)



Reprocess content in this family for a specific set of assistants in the current version of a store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    id = "id_example" # str | 
    assistant_id = [
        "assistantId_example",
    ] # [str] | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.reprocess_assistants_for_family(org_slug, slug, id, assistant_id)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->reprocess_assistants_for_family: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **id** | **str**|  |
 **assistant_id** | **[str]**|  |

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

# **reprocess_assistants_for_family_with_version**
> reprocess_assistants_for_family_with_version(org_slug, slug, version, id, assistant_id)



Reprocess content in this family for a specific set of assistants in a version of a store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    id = "id_example" # str | 
    assistant_id = [
        "assistantId_example",
    ] # [str] | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.reprocess_assistants_for_family_with_version(org_slug, slug, version, id, assistant_id)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->reprocess_assistants_for_family_with_version: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **id** | **str**|  |
 **assistant_id** | **[str]**|  |

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

# **reprocess_assistants_with_version**
> reprocess_assistants_with_version(org_slug, slug, version, reprocess_request)



Reprocess content in the store, allow you to provide a list of the family ID's

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.reprocess_request import ReprocessRequest
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    reprocess_request = ReprocessRequest(
        assistant_ids=[
            "assistant_ids_example",
        ],
        family_ids=[
            "family_ids_example",
        ],
    ) # ReprocessRequest | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.reprocess_assistants_with_version(org_slug, slug, version, reprocess_request)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->reprocess_assistants_with_version: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **reprocess_request** | [**ReprocessRequest**](ReprocessRequest.md)|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search_family**
> [SearchContent] search_family(org_slug, slug, id, query)



Perform a search on a specific document family

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.search_content import SearchContent
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    id = "id_example" # str | 
    query = "query_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.search_family(org_slug, slug, id, query)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->search_family: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **id** | **str**|  |
 **query** | **str**|  |

### Return type

[**[SearchContent]**](SearchContent.md)

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

# **search_family_with_version**
> [SearchContent] search_family_with_version(org_slug, slug, version, id, query)



Perform a search on a specific document family

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.search_content import SearchContent
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    id = "id_example" # str | 
    query = "query_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.search_family_with_version(org_slug, slug, version, id, query)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->search_family_with_version: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **id** | **str**|  |
 **query** | **str**|  |

### Return type

[**[SearchContent]**](SearchContent.md)

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

# **unlock_family**
> unlock_family(org_slug, slug, family_id)



Unlock the given family in the current version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    family_id = "familyId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.unlock_family(org_slug, slug, family_id)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->unlock_family: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **family_id** | **str**|  |

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

# **unlock_family_with_version**
> unlock_family_with_version(org_slug, slug, version, family_id)



Unlock the given family in the current version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    family_id = "familyId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.unlock_family_with_version(org_slug, slug, version, family_id)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->unlock_family_with_version: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **family_id** | **str**|  |

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

# **update_content_object_in_family**
> DocumentFamily update_content_object_in_family(org_slug, slug, version, id, object_id)



Update the contents of an object in a family (note that this will overwrite any content and not store a transition)

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.document_family import DocumentFamily
from kodexa.client.model.inline_object1 import InlineObject1
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    id = "id_example" # str | 
    object_id = "objectId_example" # str | 
    inline_object1 = InlineObject1(
        document=open('/path/to/file', 'rb'),
    ) # InlineObject1 |  (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_content_object_in_family(org_slug, slug, version, id, object_id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->update_content_object_in_family: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.update_content_object_in_family(org_slug, slug, version, id, object_id, inline_object1=inline_object1)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->update_content_object_in_family: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **id** | **str**|  |
 **object_id** | **str**|  |
 **inline_object1** | [**InlineObject1**](InlineObject1.md)|  | [optional]

### Return type

[**DocumentFamily**](DocumentFamily.md)

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

# **update_family**
> DocumentFamily update_family(org_slug, slug, version, id, document_family)



Update the metadata for a specific document family in a version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.document_family import DocumentFamily
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    id = "id_example" # str | 
    document_family = DocumentFamily(
        id="id_example",
        document_status_id="document_status_id_example",
        assignments=[
            DocumentAssignment(
                user_id="user_id_example",
            ),
        ],
        store_ref="store_ref_example",
        path="path_example",
        locked=True,
        created=dateutil_parser('1970-01-01T00:00:00.00Z'),
        modified=dateutil_parser('1970-01-01T00:00:00.00Z'),
        size=1,
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
        transitions=[
            DocumentTransition(
                id="id_example",
                transition_type="DERIVED",
                source_content_object_id="source_content_object_id_example",
                destination_content_object_id="destination_content_object_id_example",
                execution_id="execution_id_example",
                date_time=dateutil_parser('1970-01-01T00:00:00.00Z'),
                actor=DocumentActor(
                    actor_id="actor_id_example",
                    actor_type="USER",
                ),
                label="label_example",
            ),
        ],
        labels=[
            "labels_example",
        ],
        mixins=[
            "mixins_example",
        ],
        classes=[
            ContentClassification(
                label="label_example",
                taxonomy="taxonomy_example",
                selector="selector_example",
                confidence=3.14,
            ),
        ],
    ) # DocumentFamily | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_family(org_slug, slug, version, id, document_family)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->update_family: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **id** | **str**|  |
 **document_family** | [**DocumentFamily**](DocumentFamily.md)|  |

### Return type

[**DocumentFamily**](DocumentFamily.md)

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

# **update_overlay**
> DocumentFamily update_overlay(org_slug, slug, version, id, object_id, overlay_id)



Update a overlay on a content object

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.document_family import DocumentFamily
from kodexa.client.model.inline_object import InlineObject
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    id = "id_example" # str | 
    object_id = "objectId_example" # str | 
    overlay_id = "overlayId_example" # str | 
    inline_object = InlineObject(
        feature_set=open('/path/to/file', 'rb'),
    ) # InlineObject |  (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_overlay(org_slug, slug, version, id, object_id, overlay_id)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->update_overlay: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.update_overlay(org_slug, slug, version, id, object_id, overlay_id, inline_object=inline_object)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->update_overlay: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **id** | **str**|  |
 **object_id** | **str**|  |
 **overlay_id** | **str**|  |
 **inline_object** | [**InlineObject**](InlineObject.md)|  | [optional]

### Return type

[**DocumentFamily**](DocumentFamily.md)

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

# **update_row**
> StoredRow update_row(org_slug, slug, query_context, row_id, stored_row)



Get the paginated rows from the current version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.stored_row import StoredRow
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
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    query_context = QueryContext(
        page_size__default_20=1,
        page_number__default_1=1,
        sorts_to_apply="sorts_to_apply_example",
        simple_filter_to_apply="simple_filter_to_apply_example",
    ) # QueryContext | 
    row_id = "rowId_example" # str | 
    stored_row = StoredRow(
        id="id_example",
        org_slug="org_slug_example",
        slug="slug_example",
        version="version_example",
        taxonomy_ref="taxonomy_ref_example",
        path="path_example",
        row_num=1,
        source_ordering="source_ordering_example",
        date_time=dateutil_parser('1970-01-01T00:00:00.00Z'),
        lineage=DataLineage(
            store_ref="store_ref_example",
            document_family_id="document_family_id_example",
            execution_id="execution_id_example",
            content_object_id="content_object_id_example",
        ),
        cells=[
            DataCell(
                value="value_example",
                truncated=True,
                data_type="STRING",
                tag="tag_example",
                tag_uuid="tag_uuid_example",
                date_value="date_value_example",
                decimal_value=3.14,
                number_value=1,
                boolean_value=True,
                string_value="string_value_example",
                validation_state="VALID",
                validation_messages=[
                    CellValidationMessage(
                        message="message_example",
                        validation_features={
                            "key": {},
                        },
                    ),
                ],
                data_features={
                    "key": {},
                },
                audit_events=[
                    AuditEvent(
                        id="id_example",
                        audit_user="audit_user_example",
                        created=dateutil_parser('1970-01-01T00:00:00.00Z'),
                        cell_override=DataCell(),
                    ),
                ],
                label="label_example",
            ),
        ],
        parent_id="parent_id_example",
        table="table_example",
        data={
            "key": "key_example",
        },
    ) # StoredRow | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_row(org_slug, slug, query_context, row_id, stored_row)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->update_row: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **query_context** | **QueryContext**|  |
 **row_id** | **str**|  |
 **stored_row** | [**StoredRow**](StoredRow.md)|  |

### Return type

[**StoredRow**](StoredRow.md)

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

# **update_row_with_version**
> StoredRow update_row_with_version(org_slug, slug, version, query_context, row_id, stored_row)



Get the paginated rows from the current version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.stored_row import StoredRow
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
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    query_context = QueryContext(
        page_size__default_20=1,
        page_number__default_1=1,
        sorts_to_apply="sorts_to_apply_example",
        simple_filter_to_apply="simple_filter_to_apply_example",
    ) # QueryContext | 
    row_id = "rowId_example" # str | 
    stored_row = StoredRow(
        id="id_example",
        org_slug="org_slug_example",
        slug="slug_example",
        version="version_example",
        taxonomy_ref="taxonomy_ref_example",
        path="path_example",
        row_num=1,
        source_ordering="source_ordering_example",
        date_time=dateutil_parser('1970-01-01T00:00:00.00Z'),
        lineage=DataLineage(
            store_ref="store_ref_example",
            document_family_id="document_family_id_example",
            execution_id="execution_id_example",
            content_object_id="content_object_id_example",
        ),
        cells=[
            DataCell(
                value="value_example",
                truncated=True,
                data_type="STRING",
                tag="tag_example",
                tag_uuid="tag_uuid_example",
                date_value="date_value_example",
                decimal_value=3.14,
                number_value=1,
                boolean_value=True,
                string_value="string_value_example",
                validation_state="VALID",
                validation_messages=[
                    CellValidationMessage(
                        message="message_example",
                        validation_features={
                            "key": {},
                        },
                    ),
                ],
                data_features={
                    "key": {},
                },
                audit_events=[
                    AuditEvent(
                        id="id_example",
                        audit_user="audit_user_example",
                        created=dateutil_parser('1970-01-01T00:00:00.00Z'),
                        cell_override=DataCell(),
                    ),
                ],
                label="label_example",
            ),
        ],
        parent_id="parent_id_example",
        table="table_example",
        data={
            "key": "key_example",
        },
    ) # StoredRow | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_row_with_version(org_slug, slug, version, query_context, row_id, stored_row)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->update_row_with_version: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **query_context** | **QueryContext**|  |
 **row_id** | **str**|  |
 **stored_row** | [**StoredRow**](StoredRow.md)|  |

### Return type

[**StoredRow**](StoredRow.md)

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

# **update_store**
> Store update_store(organization_slug, slug, store)



Update the current version object with given slug in the organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
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
    api_instance = stores_api.StoresApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    store = Store(
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
    ) # Store | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_store(organization_slug, slug, store)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->update_store: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |
 **store** | [**Store**](Store.md)|  |

### Return type

[**Store**](Store.md)

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

# **update_store_metadata**
> dict update_store_metadata(org_slug, slug, unknown_base_type)



Get a specific document family in a version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.unknownbasetype import UNKNOWNBASETYPE
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    unknown_base_type =  # UNKNOWN_BASE_TYPE | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_store_metadata(org_slug, slug, unknown_base_type)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->update_store_metadata: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **unknown_base_type** | [**UNKNOWN_BASE_TYPE**](UNKNOWN_BASE_TYPE.md)|  |

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

# **update_store_metadata_with_version**
> dict update_store_metadata_with_version(org_slug, slug, version, unknown_base_type)



Get a specific document family in a version of the store

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
from kodexa.client.model.unknownbasetype import UNKNOWNBASETYPE
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = stores_api.StoresApi(api_client)
    org_slug = "orgSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    unknown_base_type =  # UNKNOWN_BASE_TYPE | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_store_metadata_with_version(org_slug, slug, version, unknown_base_type)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->update_store_metadata_with_version: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **unknown_base_type** | [**UNKNOWN_BASE_TYPE**](UNKNOWN_BASE_TYPE.md)|  |

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

# **update_version_store**
> Store update_version_store(organization_slug, slug, version, store)



Update the object with given slug and version in the organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import stores_api
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
    api_instance = stores_api.StoresApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    store = Store(
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
    ) # Store | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_version_store(organization_slug, slug, version, store)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling StoresApi->update_version_store: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **store** | [**Store**](Store.md)|  |

### Return type

[**Store**](Store.md)

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

