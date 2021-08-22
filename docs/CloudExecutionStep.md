# CloudExecutionStep


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**status** | **str** |  | [optional] 
**exception_details** | [**ExceptionDetails**](ExceptionDetails.md) |  | [optional] 
**name** | **str** |  | [optional] 
**start** | **datetime** |  | [optional] 
**end** | **datetime** |  | [optional] 
**processing_time** | **int** |  | [optional] 
**parameterized** | **bool** |  | [optional] 
**conditional** | **bool** |  | [optional] 
**enabled** | **bool** |  | [optional] 
**condition** | **str** |  | [optional] 
**options** | **{str: ({str: (bool, date, datetime, dict, float, int, list, str, none_type)},)}** |  | [optional] 
**option_types** | **{str: (str,)}** |  | [optional] 
**context** | **{str: ({str: (bool, date, datetime, dict, float, int, list, str, none_type)},)}** |  | [optional] 
**content_objects** | [**[ContentObject]**](ContentObject.md) |  | [optional] 
**stores** | [**[CloudStore]**](CloudStore.md) |  | [optional] 
**input_id** | **str** |  | [optional] 
**output_id** | **str** |  | [optional] 
**ref** | **str** |  | [optional] 
**deployment_type** | **str** |  | [optional] 
**service_name** | **str** |  | [optional] 
**container_name** | **str** |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


