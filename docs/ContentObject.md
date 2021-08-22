# ContentObject

An ordered list of the content objects in the document family

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content_type** | **str** |  | 
**id** | **str** |  | [optional] 
**document_version** | **str** |  | [optional] 
**labels** | **[str]** |  | [optional] 
**classes** | [**[ContentClassification]**](ContentClassification.md) |  | [optional] 
**metadata** | **{str: ({str: (bool, date, datetime, dict, float, int, list, str, none_type)},)}** |  | [optional] 
**source** | [**SourceMetadata**](SourceMetadata.md) |  | [optional] 
**mixins** | **[str]** |  | [optional] 
**content_metadata** | **{str: ({str: (bool, date, datetime, dict, float, int, list, str, none_type)},)}** |  | [optional] 
**overlays** | [**[FeatureOverlay]**](FeatureOverlay.md) |  | [optional] 
**created** | **datetime** |  | [optional] 
**modified** | **datetime** |  | [optional] 
**size** | **int** |  | [optional] 
**created_date** | **datetime** |  | [optional] 
**modified_date** | **datetime** |  | [optional] 
**store_ref** | **str** |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


