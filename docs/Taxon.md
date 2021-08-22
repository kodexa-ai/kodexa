# Taxon

A taxon is an individual label within a taxonomy

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The ID of the taxon | [optional] 
**label** | **str** | The text to display for this taxon | [optional] 
**generate_name** | **bool** | Is the name generated, this allows that you can change displays without impacted existing content | [optional] 
**group** | **bool** | Is this taxon a group, and therefore can&#39;t have a value, can only have children | [optional] 
**name** | **str** | The name to be used, note based on the hierarchy the actual label in the document will have the parent name too | [optional] 
**value_path** | **str** | Where to get the value for this taxon when extracting | [optional] 
**metadata_value** | **str** | If the type is metadata this will be the metadata option | [optional] 
**data_path** | **str** | The path to the data, based on the data inside the label (tag) within the document | [optional] 
**expression** | **str** | If the taxon is based on expression, this is the expression based on the available objects | [optional] 
**description** | **str** | The description of the taxon | [optional] 
**enabled** | **bool** | Is the taxon enabled (used in the UI) | [optional] 
**color** | **str** | Hex encoding of the color to use for the taxon | [optional] 
**children** | [**[Taxon]**](Taxon.md) | The child taxons under this taxon | [optional] 
**options** | [**[Option]**](Option.md) | Options that can be shown for the taxon (usually used in processing taxonomies) | [optional] 
**node_types** | **[str]** | A list of the node types that this taxon applies to (empty means everything), used in the UI | [optional] 
**taxon_type** | **str** | Expected data type to coalesce to | [optional] 
**type_features** | **{str: ({str: (bool, date, datetime, dict, float, int, list, str, none_type)},)}** | Additional features for the type handling | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


