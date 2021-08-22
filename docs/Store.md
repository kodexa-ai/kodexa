# Store

Provides the definition and metadata for a store

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**slug** | **str** | The slug used when referencing this metadata object | 
**type** | **str** | The type of metadata object | 
**name** | **str** | The name of the object | 
**schema_version** | **int** | The version of the schema | [optional] 
**org_slug** | **str** | The slug of the organization that owns this metadata object | [optional] 
**description** | **str** | The description of the object | [optional] 
**version** | **str** | The version of the object | [optional] 
**deployed** | **datetime** | The date/time the object was deployed into this Kodexa instance | [optional] 
**public_access** | **bool** | Is the metadata object publicly accessible by other organizations | [optional] 
**ref** | **str** | The reference to the metadata object | [optional] 
**url_of_image_for_assistant** | **str** |  | [optional] 
**a_list_of_associated_tags** | [**[MetadataTag]**](MetadataTag.md) |  | [optional] 
**extension_pack_ref** | **str** | The reference to the extension pack (if the metadata object was created by an extension pack) | [optional] 
**store_type** | **str** | The type of object the store will contain | [optional] 
**searchable** | **bool** | Is the store indexed, and thus searchable | [optional] 
**store_purpose** | **str** | The purpose of the store (used by UI and assistants to understand how to interact with the store events) | [optional] 
**metadata** | **dict** |  | [optional] 
**view_options** | [**StoreViewOptions**](StoreViewOptions.md) |  | [optional] 
**saved_filters** | [**[SavedFilter]**](SavedFilter.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


