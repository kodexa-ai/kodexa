# DataCell


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value** | **str** |  | [optional] 
**truncated** | **bool** |  | [optional] 
**data_type** | **str** |  | [optional] 
**tag** | **str** |  | [optional] 
**tag_uuid** | **str** |  | [optional] 
**date_value** | **str** |  | [optional] 
**decimal_value** | **float** |  | [optional] 
**number_value** | **int** |  | [optional] 
**boolean_value** | **bool** |  | [optional] 
**string_value** | **str** |  | [optional] 
**validation_state** | **str** | The current validation state | [optional] 
**validation_messages** | [**[CellValidationMessage]**](CellValidationMessage.md) | A list of messages relating to the validity | [optional] 
**data_features** | **{str: ({str: (bool, date, datetime, dict, float, int, list, str, none_type)},)}** | Additional features for the data | [optional] 
**audit_events** | [**[AuditEvent]**](AuditEvent.md) |  | [optional] 
**label** | **str** |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


