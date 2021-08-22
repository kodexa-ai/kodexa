# Assistant


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**assistant_definition_ref** | **str** |  | 
**id** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**definition** | [**AssistantDefinition**](AssistantDefinition.md) |  | [optional] 
**active** | **bool** |  | [optional] 
**run_on_existing_content** | **bool** |  | [optional] 
**stores** | **[str]** |  | [optional] 
**store_mapping** | **{str: (str,)}** |  | [optional] 
**options** | **{str: ({str: (bool, date, datetime, dict, float, int, list, str, none_type)},)}** |  | [optional] 
**subscriptions** | [**[AssistantSubscription]**](AssistantSubscription.md) |  | [optional] 
**schedules** | [**[AssistantSchedule]**](AssistantSchedule.md) |  | [optional] 
**validation_errors** | [**[ValidationError]**](ValidationError.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


