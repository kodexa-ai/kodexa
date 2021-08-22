# DocumentTransition

Provides the definition of a transition for a document, where a change was applied by an assistant, user or external process

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | ID of the transition | [optional] 
**transition_type** | **str** | The type of transition | [optional]  if omitted the server will use the default value of "DERIVED"
**source_content_object_id** | **str** | The content object ID that was the source of the transition | [optional] 
**destination_content_object_id** | **str** | The content object ID that was the destination of the transition | [optional] 
**execution_id** | **str** | The execution that performed the transition | [optional] 
**date_time** | **datetime** | The date/time of the transition | [optional] 
**actor** | [**DocumentActor**](DocumentActor.md) |  | [optional] 
**label** | **str** | A label for the transition (this can be used later if we want to prune based on a label) | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


