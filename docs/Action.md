# Action


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**slug** | **str** | The slug used when referencing this metadata object | 
**type** | **str** | The type of metadata object | 
**name** | **str** | The name of the object | 
**extension_pack_ref** | **str** | The reference to the extension pack (if the metadata object was created by an extension pack) | [optional] 
**step** | [**StepImplementation**](StepImplementation.md) |  | [optional] 
**metadata** | [**ObjectMetadata**](ObjectMetadata.md) |  | [optional] 
**readme** | **str** |  | [optional] 
**schema_version** | **int** | The version of the schema | [optional] 
**org_slug** | **str** | The slug of the organization that owns this metadata object | [optional] 
**description** | **str** | The description of the object | [optional] 
**version** | **str** | The version of the object | [optional] 
**deployed** | **datetime** | The date/time the object was deployed into this Kodexa instance | [optional] 
**public_access** | **bool** | Is the metadata object publicly accessible by other organizations | [optional] 
**ref** | **str** | The reference to the metadata object | [optional] 
**url_of_image_for_assistant** | **str** |  | [optional] 
**a_list_of_associated_tags** | [**[MetadataTag]**](MetadataTag.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


