# kodexa.client.TaxonomiesApi

All URIs are relative to *https://lehua.kodexa.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_taxonomy**](TaxonomiesApi.md#create_taxonomy) | **POST** /api/taxonomies/{organizationSlug} | 
[**delete_taxonomy**](TaxonomiesApi.md#delete_taxonomy) | **DELETE** /api/taxonomies/{organizationSlug}/{slug} | 
[**delete_version**](TaxonomiesApi.md#delete_version) | **DELETE** /api/taxonomies/{organizationSlug}/{slug}/{version} | 
[**get_taxonomy**](TaxonomiesApi.md#get_taxonomy) | **GET** /api/taxonomies/{organizationSlug}/{slug} | 
[**get_version**](TaxonomiesApi.md#get_version) | **GET** /api/taxonomies/{organizationSlug}/{slug}/{version} | 
[**list_taxonomy**](TaxonomiesApi.md#list_taxonomy) | **GET** /api/taxonomies/{organizationSlug} | 
[**update_taxonomy**](TaxonomiesApi.md#update_taxonomy) | **PUT** /api/taxonomies/{organizationSlug}/{slug} | 
[**update_version**](TaxonomiesApi.md#update_version) | **PUT** /api/taxonomies/{organizationSlug}/{slug}/{version} | 


# **create_taxonomy**
> Taxonomy create_taxonomy(organization_slug, taxonomy)



Create a new instance of the object in the organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import taxonomies_api
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
    api_instance = taxonomies_api.TaxonomiesApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    taxonomy = Taxonomy(
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
    ) # Taxonomy | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_taxonomy(organization_slug, taxonomy)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling TaxonomiesApi->create_taxonomy: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **taxonomy** | [**Taxonomy**](Taxonomy.md)|  |

### Return type

[**Taxonomy**](Taxonomy.md)

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

# **delete_taxonomy**
> bool delete_taxonomy(organization_slug, slug)



Delete the current version of the given object

### Example

```python
import time
import kodexa.client
from kodexa.client.api import taxonomies_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = taxonomies_api.TaxonomiesApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.delete_taxonomy(organization_slug, slug)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling TaxonomiesApi->delete_taxonomy: %s\n" % e)
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

# **delete_version**
> bool delete_version(organization_slug, slug, version)



Delete the specified version of the given object

### Example

```python
import time
import kodexa.client
from kodexa.client.api import taxonomies_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = taxonomies_api.TaxonomiesApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.delete_version(organization_slug, slug, version)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling TaxonomiesApi->delete_version: %s\n" % e)
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

# **get_taxonomy**
> Taxonomy get_taxonomy(organization_slug, slug)



Get the current version of the object with given slug

### Example

```python
import time
import kodexa.client
from kodexa.client.api import taxonomies_api
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
    api_instance = taxonomies_api.TaxonomiesApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_taxonomy(organization_slug, slug)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling TaxonomiesApi->get_taxonomy: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |

### Return type

[**Taxonomy**](Taxonomy.md)

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

# **get_version**
> Taxonomy get_version(organization_slug, slug, version)



Get the specific version of the object with given slug

### Example

```python
import time
import kodexa.client
from kodexa.client.api import taxonomies_api
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
    api_instance = taxonomies_api.TaxonomiesApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_version(organization_slug, slug, version)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling TaxonomiesApi->get_version: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |

### Return type

[**Taxonomy**](Taxonomy.md)

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

# **list_taxonomy**
> PageTaxonomy list_taxonomy(organization_slug)



Get a paginated list of the objects for an organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import taxonomies_api
from kodexa.client.model.page_taxonomy import PageTaxonomy
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = taxonomies_api.TaxonomiesApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    query = "*" # str |  (optional) if omitted the server will use the default value of "*"
    include_public = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.list_taxonomy(organization_slug)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling TaxonomiesApi->list_taxonomy: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.list_taxonomy(organization_slug, query=query, include_public=include_public)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling TaxonomiesApi->list_taxonomy: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **query** | **str**|  | [optional] if omitted the server will use the default value of "*"
 **include_public** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**PageTaxonomy**](PageTaxonomy.md)

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

# **update_taxonomy**
> Taxonomy update_taxonomy(organization_slug, slug, taxonomy)



Update the current version object with given slug in the organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import taxonomies_api
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
    api_instance = taxonomies_api.TaxonomiesApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    taxonomy = Taxonomy(
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
    ) # Taxonomy | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_taxonomy(organization_slug, slug, taxonomy)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling TaxonomiesApi->update_taxonomy: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |
 **taxonomy** | [**Taxonomy**](Taxonomy.md)|  |

### Return type

[**Taxonomy**](Taxonomy.md)

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

# **update_version**
> Taxonomy update_version(organization_slug, slug, version, taxonomy)



Update the object with given slug and version in the organization

### Example

```python
import time
import kodexa.client
from kodexa.client.api import taxonomies_api
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
    api_instance = taxonomies_api.TaxonomiesApi(api_client)
    organization_slug = "organizationSlug_example" # str | 
    slug = "slug_example" # str | 
    version = "version_example" # str | 
    taxonomy = Taxonomy(
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
    ) # Taxonomy | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_version(organization_slug, slug, version, taxonomy)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling TaxonomiesApi->update_version: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_slug** | **str**|  |
 **slug** | **str**|  |
 **version** | **str**|  |
 **taxonomy** | [**Taxonomy**](Taxonomy.md)|  |

### Return type

[**Taxonomy**](Taxonomy.md)

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

