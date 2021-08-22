# AssistantDefinition


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**slug** | **str** | The slug used when referencing this metadata object | 
**type** | **str** | The type of metadata object | 
**name** | **str** | The name of the object | 
**schema_version** | **int** | The version of the schema | [optional] 
**org_slug** | **str** | The slug of the organization that owns this metadata object | [optional] 
**description** | **str** | The description of the object | [optional] 
**version** | **str** | The version of the object | [optional] 
**deployed** | **datetime** | The date/time the object was deployed into this Kodexa instance | [optional] 
**public_access** | **bool** | Is the metadata object publicly accessible by other organizations | [optional] 
**ref** | **str** | The reference to the metadata object | [optional] 
**url_of_image_for_assistant** | **str** |  | [optional] 
**a_list_of_associated_tags** | [**[MetadataTag]**](MetadataTag.md) |  | [optional] 
**extension_pack_ref** | **str** | The reference to the extension pack (if the metadata object was created by an extension pack) | [optional] 
**the_assistant_can_be_scheduled** | **bool** |  | [optional] 
**the_assistant_is_reactive_to_content_changes** | **bool** |  | [optional] 
**the_implementation_of_the_assistant** | [**AssistantImplementation**](AssistantImplementation.md) |  | [optional] 
**additional_metadata_for_the_assistant** | [**AssistantMetadata**](AssistantMetadata.md) |  | [optional] 
**services_used_by_the_assistant** | **[dict]** |  | [optional] 
**taxonomies_that_the_assistant_uses** | [**[AssistantTaxonomy]**](AssistantTaxonomy.md) |  | [optional] 
**options_for_the_assistant** | [**[Option]**](Option.md) |  | [optional] 
**event_types_that_the_assistant_is_able_to_response_to** | [**[EventType]**](EventType.md) |  | [optional] 
**event_filters** | [**[EventFilter]**](EventFilter.md) |  | [optional] 
**the_default_schedules_that_the_assistant_has** | [**[AssistantSchedule]**](AssistantSchedule.md) |  | [optional] 
**the_default_subscriptions_that_the_assistant_has** | [**[AssistantSubscription]**](AssistantSubscription.md) |  | [optional] 
**the_full_description_of_the_assistant** | **str** |  | [optional] 
**a_help_url_where_you_can_learn_more_about_the_assistant** | **str** |  | [optional] 
**the_category_of_assistant** | **str** |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


