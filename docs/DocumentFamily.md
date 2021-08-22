# DocumentFamily

A document family is the representation of a single peice of external content (ie. a PDF) and all the related document representations of that file

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** | The path to the document family in the store | 
**id** | **str** | The unique ID of the document family | [optional] 
**document_status_id** | **str** | The ID of the document status (note this is project specific) | [optional] 
**assignments** | [**[DocumentAssignment]**](DocumentAssignment.md) | A list of the assignments to users for this document | [optional] 
**store_ref** | **str** | The reference to the store that is holding this document family | [optional] 
**locked** | **bool** | Is the document family locked. If locked then you can no longer modify or add any new document transitions | [optional] 
**created** | **datetime** |  | [optional] 
**modified** | **datetime** |  | [optional] 
**size** | **int** |  | [optional] 
**content_objects** | [**[ContentObject]**](ContentObject.md) | An ordered list of the content objects in the document family | [optional] 
**transitions** | [**[DocumentTransition]**](DocumentTransition.md) | An ordered list of the transitions in the document family | [optional] 
**labels** | **[str]** | The labels from the latest content object in the family | [optional] 
**mixins** | **[str]** | The mixins from the latest content object in the family | [optional] 
**classes** | [**[ContentClassification]**](ContentClassification.md) | The classification classes from the latest content object in the family | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


