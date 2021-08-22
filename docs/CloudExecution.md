# CloudExecution


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**org_slug** | **str** |  | [optional] 
**pipeline_ref** | **str** |  | [optional] 
**action_ref** | **str** |  | [optional] 
**assistant_ref** | **str** |  | [optional] 
**assistant_id** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**targets** | [**[ExecutionTarget]**](ExecutionTarget.md) |  | [optional] 
**session_id** | **str** |  | [optional] 
**pipeline_template_id** | **str** |  | [optional] 
**start** | **datetime** |  | [optional] 
**end** | **datetime** |  | [optional] 
**processing_time** | **int** |  | [optional] 
**status** | **str** |  | [optional] 
**exception_details** | [**ExceptionDetails**](ExceptionDetails.md) |  | [optional] 
**initial_source_metadata** | [**SourceMetadata**](SourceMetadata.md) |  | [optional] 
**lineage_document_uuid** | **str** |  | [optional] 
**steps** | [**[CloudExecutionStep]**](CloudExecutionStep.md) |  | [optional] 
**parameters** | **{str: ({str: (bool, date, datetime, dict, float, int, list, str, none_type)},)}** |  | [optional] 
**custom_options** | **{str: ({str: (bool, date, datetime, dict, float, int, list, str, none_type)},)}** |  | [optional] 
**context** | **{str: ({str: (bool, date, datetime, dict, float, int, list, str, none_type)},)}** |  | [optional] 
**content_objects** | [**[ContentObject]**](ContentObject.md) |  | [optional] 
**stores** | [**[CloudStore]**](CloudStore.md) |  | [optional] 
**input_id** | **str** |  | [optional] 
**output_id** | **str** |  | [optional] 
**document_family_id** | **str** |  | [optional] 
**store_ref** | **str** |  | [optional] 
**number_of_steps** | **int** |  | [optional] 
**steps_completed** | **int** |  | [optional] 
**related_executions** | [**[RelatedExecution]**](RelatedExecution.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


