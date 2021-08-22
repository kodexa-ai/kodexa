# CloudSessionEvent


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**type** | **str** |  | 
**session_id** | **str** |  | 
**token** | **str** |  | 
**execution_id** | **str** |  | [optional] 
**store_ref** | **str** |  | [optional] 
**document_family_id** | **str** |  | [optional] 
**sub_type** | **str** |  | [optional] 
**step** | [**CloudExecutionStep**](CloudExecutionStep.md) |  | [optional] 
**connector** | [**CloudConnector**](CloudConnector.md) |  | [optional] 
**assistant** | [**CloudAssistant**](CloudAssistant.md) |  | [optional] 
**source** | **{str: ({str: (bool, date, datetime, dict, float, int, list, str, none_type)},)}** |  | [optional] 
**payload** | **{str: ({str: (bool, date, datetime, dict, float, int, list, str, none_type)},)}** |  | [optional] 
**content_objects** | [**[ContentObject]**](ContentObject.md) |  | [optional] 
**input_id** | **str** |  | [optional] 
**target_deployment_type** | **str** |  | [optional] 
**target** | **str** |  | [optional] 
**platform_url** | **str** |  | [optional] 
**debug** | **bool** |  | [optional] 
**created** | **datetime** |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


