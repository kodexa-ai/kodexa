# ModelContentMetadata


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | The type of content metadata | [optional] 
**state** | **str** | The state of the model in this store | [optional] 
**parameters** | **{str: ({str: (bool, date, datetime, dict, float, int, list, str, none_type)},)}** | The parameters passed to this model instance | [optional] 
**build_statistics** | **{str: ({str: (bool, date, datetime, dict, float, int, list, str, none_type)},)}** | Build statistics (note this will update if the model is training) | [optional] 
**final_statistics** | **{str: ({str: (bool, date, datetime, dict, float, int, list, str, none_type)},)}** | Final statistics from the model | [optional] 
**deployment** | **{str: ({str: (bool, date, datetime, dict, float, int, list, str, none_type)},)}** | Details of the model deployment (if available) | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


