from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyUrl, Field, RootModel, BaseModel, ConfigDict

from kodexa.model.base import StandardDateTime


class ExceptionResponse(BaseModel):
    """
    This class represents the response structure for exceptions in the application.

    Attributes:
        date_time (Optional[StandardDateTime]): The date and time when the exception occurred.
        message (Optional[str]): The error message.
        incident_id (Optional[str]): The ID of the incident associated with the"""
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )

    date_time: Optional[StandardDateTime] = Field(None, alias="dateTime")
    message: Optional[str] = None
    incident_id: Optional[str] = Field(None, alias="incidentId")
    context_path: Optional[str] = Field(None, alias="contextPath")
    errors: Optional[Dict[str, Any]] = None
    stack_trace: Optional[str] = Field(None, alias="stackTrace")
    root_cause_stack_trace: Optional[List[str]] = Field(
        None, alias="rootCauseStackTrace"
    )


class StatusType(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )

    reason_phrase: Optional[str] = Field(None, alias="reasonPhrase")
    status_code: Optional[int] = Field(None, alias="statusCode")


class StackTraceItem(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    class_loader_name: Optional[str] = Field(None, alias="classLoaderName")
    module_name: Optional[str] = Field(None, alias="moduleName")
    module_version: Optional[str] = Field(None, alias="moduleVersion")
    method_name: Optional[str] = Field(None, alias="methodName")
    file_name: Optional[str] = Field(None, alias="fileName")
    line_number: Optional[int] = Field(None, alias="lineNumber")
    native_method: Optional[bool] = Field(None, alias="nativeMethod")
    class_name: Optional[str] = Field(None, alias="className")


class StackTraceItem1(BaseModel):
    """

    :class:`StackTraceItem1` represents a stack trace item.

    Attributes:
        model_config (ConfigDict): Configuration dictionary for the model.
        class_loader_name (str, optional): The name of the class loader used.
        module_name (str, optional): The name of the module"""
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    class_loader_name: Optional[str] = Field(None, alias="classLoaderName")
    module_name: Optional[str] = Field(None, alias="moduleName")
    module_version: Optional[str] = Field(None, alias="moduleVersion")
    method_name: Optional[str] = Field(None, alias="methodName")
    file_name: Optional[str] = Field(None, alias="fileName")
    line_number: Optional[int] = Field(None, alias="lineNumber")
    native_method: Optional[bool] = Field(None, alias="nativeMethod")
    class_name: Optional[str] = Field(None, alias="className")


class Cause(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    stack_trace: Optional[List[StackTraceItem1]] = Field(None, alias="stackTrace")
    message: Optional[str] = None
    localized_message: Optional[str] = Field(None, alias="localizedMessage")


class StackTraceItem2(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    class_loader_name: Optional[str] = Field(None, alias="classLoaderName")
    module_name: Optional[str] = Field(None, alias="moduleName")
    module_version: Optional[str] = Field(None, alias="moduleVersion")
    method_name: Optional[str] = Field(None, alias="methodName")
    file_name: Optional[str] = Field(None, alias="fileName")
    line_number: Optional[int] = Field(None, alias="lineNumber")
    native_method: Optional[bool] = Field(None, alias="nativeMethod")
    class_name: Optional[str] = Field(None, alias="className")


class SuppressedItem(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    cause: Optional[Cause] = None
    stack_trace: Optional[List[StackTraceItem2]] = Field(None, alias="stackTrace")
    message: Optional[str] = None
    localized_message: Optional[str] = Field(None, alias="localizedMessage")


class ThrowableProblem(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    cause: Optional[ThrowableProblem] = None
    stack_trace: Optional[List[StackTraceItem]] = Field(None, alias="stackTrace")
    message: Optional[str] = None
    instance: Optional[AnyUrl] = None
    type: Optional[AnyUrl] = None
    parameters: Optional[Dict[str, Any]] = None
    title: Optional[str] = None
    detail: Optional[str] = None
    status: Optional[StatusType] = None
    suppressed: Optional[List[SuppressedItem]] = None
    localized_message: Optional[str] = Field(None, alias="localizedMessage")


class FavoriteLink(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    link: Optional[str] = None


class UserStorage(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    favorite_links: Optional[List[FavoriteLink]] = Field(None, alias="favoriteLinks")


class CompletePasswordReset(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    reset_token: str = Field(..., alias="resetToken")
    password: str


class Organization(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    name: str
    slug: str = Field(pattern=r"^[a-zA-Z0-9\-_]{0,100}$")
    public_access: Optional[bool] = Field(None, alias="publicAccess")
    description: Optional[str] = None
    has_image: Optional[bool] = Field(None, alias="hasImage")


class Team(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    name: Optional[str] = None
    description: Optional[str] = None
    organization: Optional[Organization] = None


class AssistantImplementation(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    The implementation of the assistant
    """

    package: Optional[str] = None
    class_: Optional[str] = Field(None, alias="class")


class AssistantTaxonomy(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    Taxonomies that the assistant uses
    """

    ref: Optional[str] = None


class Avatar(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    icon: Optional[str] = None
    icon_group: Optional[str] = Field(None, alias="iconGroup")


class Card(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = None
    type: Optional[str] = Field(None, description="The type of the card")
    properties: Optional[Dict[str, Any]] = None
    children: Optional[List[Card]] = None


class ColumnState(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    field: Optional[str] = None
    title: Optional[str] = None
    cell: Optional[str] = None
    width: Optional[str] = None
    groupable: Optional[bool] = None
    sortable: Optional[bool] = None
    resizeable: Optional[bool] = None


class ContainerResources(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    memory: Optional[str] = None
    cpu: Optional[str] = None


class ContentMetadata(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    The metadata for this store
    """

    type: Optional[str] = None


class DashboardWidget(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    children: Optional[List[DashboardWidget]] = None


class DataFormSource(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None


class DataFormView(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = None
    data_object_subscription: Optional[str] = Field(
        None, alias="dataObjectSubscription"
    )
    properties: Optional[Dict[str, Any]] = None
    data_source_id: Optional[str] = Field(None, alias="dataSourceId")
    name: Optional[str] = None
    cards: Optional[List[Card]] = None


class DeploymentType(Enum):
    """
    Represents the types of deployment options available.

    Attributes:
        kubernetes (str): Represents a Kubernetes deployment.
        aws_lambda (str): Represents an AWS Lambda deployment.
        azure_cloud_function (str): Represents an Azure Cloud Function deployment.
        none (str): Represents no deployment type.
    """
    kubernetes = "KUBERNETES"
    aws_lambda = "AWS_LAMBDA"
    azure_cloud_function = "AZURE_CLOUD_FUNCTION"
    none = "NONE"


class DocumentColumn(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    label: Optional[str] = Field(
        None, description="The label to use for the column heading"
    )
    path: Optional[str] = Field(None, description="The path to the data")


class DocumentMetadataProperty(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    name: Optional[str] = None
    values: Optional[List[Dict[str, Any]]] = None
    query_available: Optional[bool] = Field(None, alias="queryAvailable")


class Status(Enum):
    """

    """
    pending = "PENDING"
    building = "BUILDING"
    built = "BUILT"
    available = "AVAILABLE"
    failed = "FAILED"
    undeployed = "UNDEPLOYED"
    awaiting_deployment = "AWAITING_DEPLOYMENT"
    deploying = "DEPLOYING"
    deployment_failed = "DEPLOYMENT_FAILED"


class ExtensionPackSource(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    type: Optional[str] = None


class MatchLabel(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    label: Optional[str] = None
    value: Optional[str] = None


class MetadataTag(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    A list of associated tags
    """

    tag: Optional[str] = None
    image_url: Optional[str] = Field(None, alias="imageUrl")


class State(Enum):
    """

    """

    pending = "PENDING"
    preparing = "PREPARING"
    prepared = "PREPARED"
    training = "TRAINING"
    trained = "TRAINED"
    deployed = "DEPLOYED"
    undeployed = "UNDEPLOYED"
    failed = "FAILED"


class DeploymentType1(Enum):
    """

    """

    local = "LOCAL"
    container = "CONTAINER"


class OverlayCondition(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    pass


class StepType(Enum):
    """

    """

    action = "ACTION"
    model = "MODEL"


class PipelineStepMetadata(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    The metadata for the steps in this pipeline
    """

    name: Optional[str] = Field(None, description="The name of the step")
    ref: Optional[str] = Field(None, description="The reference to the action")
    options: Optional[Dict[str, Any]] = Field(
        None, description="The options for the step in the pipeline"
    )
    step_type: Optional[StepType] = Field(
        None, alias="stepType", description="The type of step (ACTION or MODEL)"
    )


class PossibleValue(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    label: Optional[str] = None
    value: Optional[Any] = None
    description: Optional[str] = None


class ProjectGuidance(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    The guidance that will be created with the project template
    """

    slug: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    template_ref: Optional[str] = Field(None, alias="templateRef")
    ref: Optional[str] = None
    guidance: Optional[List[Guidance]] = Field(None, alias="guidance")


class ProjectDashboard(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    The dashboards that will be created with the project template
    """

    slug: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    widgets: Optional[List[DashboardWidget]] = None
    template_ref: Optional[str] = Field(None, alias="templateRef")
    ref: Optional[str] = None
    single_widget: Optional[DashboardWidget] = Field(None, alias="singleWidget")


class StoreType(Enum):
    """

    """
    document = "DOCUMENT"
    table = "TABLE"
    dictionary = "DICTIONARY"
    model = "MODEL"


class StorePurpose(Enum):
    """

    """
    operational = "OPERATIONAL"
    training = "TRAINING"


class ProjectStore(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    The stores that will be created with the project template
    """

    slug: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    store_type: Optional[StoreType] = Field(None, alias="storeType")
    store_purpose: Optional[StorePurpose] = Field(None, alias="storePurpose")
    template_ref: Optional[str] = Field(None, alias="templateRef")
    ref: Optional[str] = None

    show_thumbnails: Optional[bool] = Field(
        None, description="Show thumbnails in dtore", alias="showThumbnails"
    )

    showSearch: Optional[bool] = Field(
        None, description="Show search in store", alias="showSearch"
    )

    allowDataEditing: Optional[bool] = Field(
        None, description="Allow data editing", alias="allowDataEditing"
    )


class TaxonomyType(Enum):
    """

    """

    content = "CONTENT"
    classification = "CLASSIFICATION"
    processing = "PROCESSING"
    model = "MODEL"


class Category(Enum):
    """

    """

    task = "TASK"
    document = "DOCUMENT"
    connector = "CONNECTOR"
    machine_learning = "MACHINE_LEARNING"
    supplemental = "SUPPLEMENTAL"


class Purpose(Enum):
    """

    """
    suggestion = "SUGGESTION"
    source = "SOURCE"


class RelatedTaxon(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    A list of relationships to other taxons and the purpose of the relationship
    """

    path: Optional[str] = None
    purpose: Optional[Purpose] = None
    priority: Optional[int] = None


class ScheduleDefinition(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    The default schedules that the assistant has
    """

    type: Optional[str] = None
    cron_expression: Optional[str] = Field(None, alias="cronExpression")
    last_event: Optional[StandardDateTime] = Field(None, alias="lastEvent")
    next_event: Optional[StandardDateTime] = Field(None, alias="nextEvent")


class SelectionOption(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    If data type is SELECTION, this is the list of available options
    """

    label: Optional[str] = None
    id: Optional[str] = None
    description: Optional[str] = None


class SlugBasedMetadata1(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    ref: Optional[str] = Field(None, description="The reference to the metadata object")
    template: Optional[bool] = Field(
        None,
        description="Is this component a template that can be used to create new components",
    )
    schema_version: Optional[int] = Field(
        None, alias="schemaVersion", description="The version of the schema"
    )
    org_slug: Optional[str] = Field(
        None,
        alias="orgSlug",
        description="The slug of the organization that owns this metadata object",
    )
    slug: str = Field(
        None,
        description="The slug used when referencing this metadata object",
        pattern=r"^[a-zA-Z0-9\-_]{0,255}$",
    )
    type: str = Field(None, description="The type of metadata object")
    name: str = Field(None, description="The name of the object")
    description: Optional[str] = Field(
        None, description="The description of the object"
    )
    version: Optional[str] = Field(
        None,
        description="The version of the object",
        pattern=r"^\d+\.\d+\.\d+(?:\-\d+)?$",
    )
    deployed: Optional[StandardDateTime] = Field(
        None,
        description="The date/time the object was deployed into this Kodexa instance",
    )
    public_access: Optional[bool] = Field(
        None,
        alias="publicAccess",
        description="Is the metadata object publicly accessible by other organizations",
    )
    image_url: Optional[str] = Field(
        None,
        alias="imageUrl",
        description="URL of image when presenting this object in a UI",
    )
    icon: Optional[str] = Field(None, description="Material Icon name to use in the UI")
    overview_markdown: Optional[str] = Field(
        None,
        alias="overviewMarkdown",
        description="Markdown that is used to present the overview of the object",
    )
    metadata_tag: Optional[List[MetadataTag]] = Field(
        None, alias="metadataTag", description="A list of associated tags"
    )
    provider: Optional[str] = Field(None, description="The details of the of provider")
    provider_url: Optional[str] = Field(
        None, alias="providerUrl", description="The link to the provider website"
    )
    provider_image_url: Optional[str] = Field(
        None, alias="providerImageUrl", description="The link to the model image"
    )


class StepImplementation(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    package: Optional[str] = None
    class_: Optional[str] = Field(None, alias="class")


class StoreViewOptions(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    Options for viewing this store
    """

    show_last_event: Optional[bool] = Field(None, alias="showLastEvent")
    show_extension: Optional[bool] = Field(None, alias="showExtension")
    show_created: Optional[bool] = Field(None, alias="showCreated")
    show_modified: Optional[bool] = Field(None, alias="showModified")
    show_path_counts: Optional[bool] = Field(None, alias="showPathCounts")
    show_classifications: Optional[bool] = Field(None, alias="showClassifications")
    show_size: Optional[bool] = Field(None, alias="showSize")
    show_assignments: Optional[bool] = Field(None, alias="showAssignments")
    show_status: Optional[bool] = Field(None, alias="showStatus")
    additional_columns: Optional[List[DocumentColumn]] = Field(
        None, alias="additionalColumns"
    )
    column_states: Optional[Dict[str, List[ColumnState]]] = Field(
        None, alias="columnStates"
    )


class OptionTab(BaseModel):
    """

    Class OptionTab

    This class represents an option tab that can be used in a UI for configuring models.

    Attributes:
    - `model_config` (ConfigDict): A dictionary that stores the model configuration.
    - `name` (Optional[str]): The name of the option tab.
    - `description` (Optional[str]): The description of the option"""
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    show_if: Optional[str] = Field(None, alias="showIf")
    option_names: Optional[List[str]] = Field(None, alias="optionNames")
    show_in_training: Optional[bool] = Field(None, alias="showInTraining")


class ValuePath(Enum):
    """
    Enum class representing different types of value paths.

    :cvar value_or_all_content: Represents a value or all content.
    :cvar value_only: Represents a value only.
    :cvar all_content: Represents all content.
    :cvar data_path: Represents a data path.
    :cvar metadata: Represents metadata.
    :cvar expression: Represents an expression.
    :cvar script: Represents a script.
    """

    value_or_all_content = "VALUE_OR_ALL_CONTENT"
    value_only = "VALUE_ONLY"
    all_content = "ALL_CONTENT"
    data_path = "DATA_PATH"
    metadata = "METADATA"
    expression = "EXPRESSION"
    script = "SCRIPT"


class MetadataValue(Enum):
    """Enumeration representing different metadata values.

    Attributes:
        filename (str): The filename metadata value.
        transaction_uuid (str): The transaction UUID metadata value.
        created_datetime (str): The created datetime metadata value.
    """

    filename = "FILENAME"
    transaction_uuid = "TRANSACTION_UUID"
    created_datetime = "CREATED_DATETIME"


class TaxonType(Enum):
    """
    An enumeration representing different types of taxonomic data.

    The TaxonType class defines constants for various taxonomic data types, including strings, dates, numbers,
    and more.

    Usage:
        Use the TaxonType enumeration to represent the type of taxonomic data in your code.

    Example:
        ::

            taxon_type = TaxonType.string
            if taxon_type == TaxonType.date:
                print("This is a date type")
            elif taxon"""

    string = "STRING"
    date = "DATE"
    date_time = "DATE_TIME"
    number = "NUMBER"
    decimal = "DECIMAL"
    float = "FLOAT"
    boolean = "BOOLEAN"
    currency = "CURRENCY"
    url = "URL"
    email_address = "EMAIL_ADDRESS"
    phone_number = "PHONE_NUMBER"
    selection = "SELECTION"
    question = "QUESTION"


class TaxonomyType1(Enum):
    """
    Represents the taxonomy types for classification.

    The possible values are:
    - content: Represents the content taxonomy type.
    - classification: Represents the classification taxonomy type.
    - processing: Represents the processing taxonomy type.
    - model: Represents the model taxonomy type.
    """

    content = "CONTENT"
    classification = "CLASSIFICATION"
    processing = "PROCESSING"
    model = "MODEL"


class ViewPreset(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    View presets that have been saved for this store
    """

    id: Optional[str] = None
    name: Optional[str] = None
    filter_string: Optional[str] = Field(None, alias="filterString")
    enabled_taxons: Optional[Dict[str, bool]] = Field(None, alias="enabledTaxons")


class ReprocessRequest(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    assistant_ids: Optional[List[str]] = Field(None, alias="assistantIds")
    family_ids: Optional[List[str]] = Field(None, alias="familyIds")
    all: Optional[bool] = None


class AssistantSchedule(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    type: Optional[str] = None
    cron_expression: Optional[str] = Field(None, alias="cronExpression")
    last_event: Optional[StandardDateTime] = Field(None, alias="lastEvent")
    next_event: Optional[StandardDateTime] = Field(None, alias="nextEvent")
    id: Optional[str] = None


class StatusType1(Enum):
    """
    Enumeration class representing the status types.

    Each status type has a string value associated with it.

    :ivar unresolved: The unresolved status type.
    :vartype unresolved: StatusType1
    :ivar resolved: The resolved status type.
    :vartype resolved: StatusType1
    """
    unresolved = "UNRESOLVED"
    resolved = "RESOLVED"


class AttributeStatus(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    color: Optional[str] = None
    icon: Optional[str] = None
    status: Optional[str] = None
    status_type: Optional[StatusType1] = Field(None, alias="statusType")


class ContentType(Enum):
    """A class representing the content type of a document or native file."""

    document = "DOCUMENT"
    native = "NATIVE"


class ActorType(Enum):
    """
    The ActorType class is an enumeration that represents different types of actors in a system.

    Usage:
        Use the ActorType enum to specify the type of an actor in your system.

    Attributes:
        - user: Represents a user actor.
        - assistant: Represents an assistant actor.
        - access_token: Represents an access token actor.
        - api: Represents an API actor.

    Example:
        actor = ActorType.user
        print(actor)  # Output: ActorType.user

    Notes:
        - The values of the ActorType enum are"""

    user = "USER"
    assistant = "ASSISTANT"
    access_token = "ACCESS_TOKEN"
    api = "API"


class DocumentActor(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    Provides the definition of an actor in a transition
    """

    actor_id: Optional[str] = Field(
        None,
        alias="actorId",
        description="The ID for the actor (dependent on the actor type)",
    )
    actor_type: Optional[ActorType] = Field(
        None, alias="actorType", description="The type of actor"
    )


class StatusType2(Enum):
    """Module containing the `StatusType2` class.

    This class represents the status types for a particular issue or task.

    """
    unresolved = "UNRESOLVED"
    resolved = "RESOLVED"


class DocumentStatus(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    color: Optional[str] = None
    icon: Optional[str] = None
    status: str
    status_type: Optional[StatusType2] = Field(None, alias="statusType")


class TransitionType(Enum):
    """
    Defines the different types of transitions.

    :cvar derived: The transition is derived from previous data.
    """

    derived = "DERIVED"


class DocumentTransition(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    Provides the definition of a transition for a document, where a change was applied by an assistant, user or external process
    """

    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    unknown_fields: Optional[Dict[str, str]] = Field(None, alias="unknownFields")
    transition_type: Optional[TransitionType] = Field(
        None, alias="transitionType", description="The type of transition"
    )
    index: Optional[int] = None
    date_time: Optional[StandardDateTime] = Field(
        None, alias="dateTime", description="The date/time of the transition"
    )
    actor: Optional[DocumentActor] = None
    label: Optional[str] = Field(
        None,
        description="A label for the transition (this can be used later if we want to prune based on a label)",
    )
    source_content_object_id: Optional[str] = Field(None, alias="sourceContentObjectId")
    destination_content_object_id: Optional[str] = Field(
        None, alias="destinationContentObjectId"
    )


class Status1(Enum):
    """

    The Status1 Enumeration Class
    ------------------------

    This class represents a set of possible statuses.

    Attributes:
        pending (str): The pending status.
        running (str): The running status.
        succeeded (str): The succeeded status.
        failed (str): The failed status.
        requested (str): The requested status.
        skipped (str): The skipped status.
        cancelling (str): The cancelling status.
        cancelled (str): The cancelled status.
        pending_reprocessing (str): The pending reprocessing status.

    """
    pending = "PENDING"
    running = "RUNNING"
    succeeded = "SUCCEEDED"
    failed = "FAILED"
    requested = "REQUESTED"
    skipped = "SKIPPED"
    cancelling = "CANCELLING"
    cancelled = "CANCELLED"
    pending_reprocessing = "PENDING_REPROCESSING"


class Status2(Enum):
    """

    :class:`Status2` Enum

    Enumeration class representing the status of a task. The possible values are:

    - `pending`: The task is pending and has not started yet.
    - `running`: The task is currently running.
    - `succeeded`: The task has successfully completed.
    - `failed`: The task has failed to complete.
    - `requested`: The task has been requested to start but has not yet started.
    - `skipped`: The task has been skipped.
    - `cancelling`: The task is currently being cancelled.
    """
    pending = "PENDING"
    running = "RUNNING"
    succeeded = "SUCCEEDED"
    failed = "FAILED"
    requested = "REQUESTED"
    skipped = "SKIPPED"
    cancelling = "CANCELLING"
    cancelled = "CANCELLED"
    pending_reprocessing = "PENDING_REPROCESSING"


class Status3(Enum):
    """

    """
    pending = "PENDING"
    running = "RUNNING"
    succeeded = "SUCCEEDED"
    failed = "FAILED"
    requested = "REQUESTED"
    skipped = "SKIPPED"
    cancelling = "CANCELLING"
    cancelled = "CANCELLED"
    pending_reprocessing = "PENDING_REPROCESSING"


class StepType1(Enum):
    """
    Enumerates the possible step types for a specific class.

    :class: StepType1

    Attributes:
        action (str): Constant representing an action step type.
        model (str): Constant representing a model step type.
    """
    action = "ACTION"
    model = "MODEL"


class Type(Enum):
    """
    A class representing different types.

    Attributes:
        document_store (str): Represents the type for document store.
        taxonomy_store (str): Represents the type for taxonomy store.
        data_store (str): Represents the type for data store.

    Examples:
        The `document_store` attribute can be accessed as follows:

        >>> Type.document_store
        <Type.document_store: 'DOCUMENT_STORE'>

        The `taxonomy_store` attribute can be accessed as follows:

        >>> Type.taxonomy_store
        <Type.taxonomy_store"""
    document_store = "DOCUMENT_STORE"
    taxonomy_store = "TAXONOMY_STORE"
    data_store = "DATA_STORE"


class ExecutionTarget(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    type: Optional[Type] = None
    ref: Optional[str] = None
    document_family_id: Optional[str] = Field(None, alias="documentFamilyId")
    content_object_id: Optional[str] = Field(None, alias="contentObjectId")
    actor: Optional[DocumentActor] = None
    taxonomy_refs: Optional[List[str]] = Field(None, alias="taxonomyRefs")
    labels_to_apply: Optional[List[str]] = Field(None, alias="labelsToApply")


class ExecutionTargets(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    instances: Optional[List[ExecutionTarget]] = None


class Label(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    The labels from the latest content object in the family
    """

    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    name: str
    color: Optional[str] = None
    label: str


class ProjectTag(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    A project tag
    """

    id: Optional[str] = Field(None, description="The ID of the object")
    name: str
    color: Optional[str] = None


class PathExtractedData(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = None
    taxonomy_id: Optional[str] = Field(None, alias="taxonomyId")
    path: Optional[str] = None
    label: Optional[str] = None
    count: Optional[int] = None
    exception_count: Optional[int] = Field(None, alias="exceptionCount")


class ProjectMemory(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    recent_filters: Optional[Dict[str, List[str]]] = Field(None, alias="recentFilters")


class ProjectMetadata(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    tags: Optional[List[str]] = Field(default_factory=list, set=True)


class State1(Enum):
    """
    .. py:class:: State1(Enum)

       Enumeration class representing different states.

       The ``State1`` class is an enumeration that represents different states. It is implemented as an enum in Python.
       The available states are "open" and "closed".

       The states are defined with corresponding string values, allowing for easy comparison and assignment.

       :cvar open: Represents the "OPEN" state.
       :vartype open: str
       :cvar closed: Represents the "CLOSED" state.
       :v"""
    open = "OPEN"
    closed = "CLOSED"


class Session(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    token: Optional[str] = None
    last_accessed: Optional[StandardDateTime] = Field(None, alias="lastAccessed")


class Status4(Enum):
    """

    :class:`Status4` is an enumeration class that represents different status values.

    Attributes:
        * :attr:`Status4.pending`: Represents the "PENDING" status.
        * :attr:`Status4.running`: Represents the "RUNNING" status.
        * :attr:`Status4.succeeded`: Represents the "SUCCEEDED" status.
        * :attr:`Status4.failed`: Represents the "FAILED" status.
        * :attr:`Status4.requested`: Represents the "REQUESTED" status.
        * :"""
    pending = "PENDING"
    running = "RUNNING"
    succeeded = "SUCCEEDED"
    failed = "FAILED"
    requested = "REQUESTED"
    skipped = "SKIPPED"
    cancelling = "CANCELLING"
    cancelled = "CANCELLED"
    pending_reprocessing = "PENDING_REPROCESSING"


class StatusDetails(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    status: Optional[Status4] = None
    message: Optional[str] = None
    detail: Optional[str] = None
    progress_max: Optional[int] = Field(None, alias="progressMax")
    progress: Optional[int] = None


class ValidationError(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    message: Optional[str] = None
    option: Optional[str] = None
    description: Optional[str] = None


class ValidationResults(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    instances: Optional[List[ValidationError]] = None


class BulkCopy(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    target_store_ref: Optional[str] = Field(None, alias="targetStoreRef")
    all: Optional[bool] = None
    document_family_ids: Optional[List[str]] = Field(None, alias="documentFamilyIds")


class FamilyRename(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    path: str


class ContentFeature(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    feature_type: Optional[str] = Field(None, alias="featureType")
    name: Optional[str] = None
    value: Optional[List[Dict[str, Any]]] = None
    single: Optional[bool] = None


class NodeFeatures(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    node_uuid: Optional[str] = Field(None, alias="nodeUuid")
    features: Optional[List[ContentFeature]] = None


class DataException(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    A data exception
    """

    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    message: str
    exception_details: Optional[str] = Field(None, alias="exceptionDetails")
    severity: Optional[str] = None
    exception_type: Optional[str] = Field(None, alias="exceptionType")
    closing_comment: Optional[str] = Field(None, alias="closingComment")
    open: Optional[bool] = None
    data_object: Optional[DataObject] = Field(None, alias="dataObject")
    data_attribute: Optional[DataAttribute] = Field(None, alias="dataAttribute")
    data_object_id: Optional[str] = Field(None, alias="dataObjId")


class DataLineage(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    store_ref: Optional[str] = Field(None, alias="storeRef")
    document_family_id: Optional[str] = Field(None, alias="documentFamilyId")
    execution_id: Optional[str] = Field(None, alias="executionId")
    content_object_id: Optional[str] = Field(None, alias="contentObjectId")


class WorkflowDefinition(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    description: Optional[str] = None
    definition_xml: Optional[str] = Field(None, alias="definitionXml")


class ProjectResourcesUpdate(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    taxonomy_refs: Optional[List[str]] = Field(None, alias="taxonomyRefs")
    store_refs: Optional[List[str]] = Field(None, alias="storeRefs")
    dashboard_refs: Optional[List[str]] = Field(None, alias="dashboardRefs")
    data_form_refs: Optional[List[str]] = Field(None, alias="dataFormRefs")


class Role1(Enum):
    """

    """
    owner = "OWNER"
    read = "READ"
    write = "WRITE"


class DeploymentType2(Enum):
    """

    """
    kubernetes = "KUBERNETES"
    aws_lambda = "AWS_LAMBDA"
    azure_cloud_function = "AZURE_CLOUD_FUNCTION"
    none = "NONE"


class DeploymentOptions(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    deployment_type: Optional[DeploymentType2] = Field(None, alias="deploymentType")
    max_replicas: Optional[int] = Field(None, alias="maxReplicas")
    min_replicas: Optional[int] = Field(None, alias="minReplicas")
    reserved_concurrency: Optional[int] = Field(None, alias="reservedConcurrency")
    memory_assigned: Optional[str] = Field(None, alias="memoryAssigned")
    cpu: Optional[str] = None
    pod_match_labels: Optional[List[MatchLabel]] = Field(None, alias="podMatchLabels")
    child_process: Optional[bool] = Field(None, alias="childProcess")


class SourceType(Enum):
    """

    """
    data_object = "DATA_OBJECT"
    data_attribute = "DATA_ATTRIBUTE"
    fixed = "FIXED"


class DataFormSourceParameter(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    name: Optional[str] = None
    required: Optional[bool] = None


class DataFormProviderExchange(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    method: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    payload: Optional[Dict[str, Any]] = None


class PlatformConfiguration(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    welcome_markdown: Optional[str] = Field(None, alias="welcomeMarkdown")
    news_markdown: Optional[str] = Field(None, alias="newsMarkdown")
    about_markdown: Optional[str] = Field(None, alias="aboutMarkdown")
    login_message: Optional[str] = Field(None, alias="loginMessage")
    base_org_slug: Optional[str] = Field(None, alias="baseOrgSlug")
    title: Optional[str] = None
    organization_title: Optional[str] = Field(None, alias="organizationTitle")
    organizations_title: Optional[str] = Field(None, alias="organizationsTitle")
    organization_description: Optional[str] = Field(
        None, alias="organizationDescription"
    )
    project_title: Optional[str] = Field(None, alias="projectTitle")
    projects_title: Optional[str] = Field(None, alias="projectsTitle")
    project_description: Optional[str] = Field(None, alias="projectDescription")
    developer_links: Optional[bool] = Field(None, alias="developerLinks")
    allow_registration: Optional[bool] = Field(None, alias="allowRegistration")
    allow_password_reset: Optional[bool] = Field(None, alias="allowPasswordReset")
    default_to_design: Optional[bool] = Field(None, alias="defaultToDesign")
    extension_pack_bridge: Optional[str] = Field(None, alias="extensionPackBridge")
    fallback_feature_flags: Optional[str] = Field(None, alias="fallbackFeatureFlags")


class UserActivation(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    password: Optional[str] = None


class ModelTraining(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    name: Optional[str] = None
    state: Optional[str] = None
    training_materials_generated: Optional[bool] = Field(
        None, alias="trainingMaterialsGenerated"
    )
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    training_date: Optional[StandardDateTime] = Field(None, alias="trainingDate")
    content: Optional[bool] = Field(None, description="Has content")
    user_test: Optional[bool] = Field(None, alias="userTest")

    properties: Optional[Dict[str, Any]] = None
    training_parameters: Optional[Dict[str, Any]] = Field(
        None,
        alias="trainingParameters",
        description="The values for the training options",
    )


class Status5(Enum):
    """

    """
    pending = "PENDING"
    running = "RUNNING"
    succeeded = "SUCCEEDED"
    failed = "FAILED"
    requested = "REQUESTED"
    skipped = "SKIPPED"
    cancelling = "CANCELLING"
    cancelled = "CANCELLED"
    pending_reprocessing = "PENDING_REPROCESSING"


class BaseEvent1(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    type: Optional[str] = Field(None, description="The type of the event")


class ObjectEventType(Enum):
    """

    """
    new_object = "NEW_OBJECT"
    derived_object = "DERIVED_OBJECT"


class ExecutionEventType(Enum):
    """

    """
    start_execution = "START_EXECUTION"
    step_update = "STEP_UPDATE"
    assistant_event = "ASSISTANT_EVENT"
    assistant_response = "ASSISTANT_RESPONSE"
    abend = "ABEND"


class Status6(Enum):
    """

    """
    pending = "PENDING"
    running = "RUNNING"
    succeeded = "SUCCEEDED"
    failed = "FAILED"
    requested = "REQUESTED"
    skipped = "SKIPPED"
    cancelling = "CANCELLING"
    cancelled = "CANCELLED"
    pending_reprocessing = "PENDING_REPROCESSING"


class ExecutionLogEntry(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    log_date: Optional[StandardDateTime] = Field(None, alias="logDate")
    entry: Optional[str] = None


class LoginRequest(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    email: str
    password: str


class RegisterUser(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    email: str
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")


class PasswordReset(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    email: str


class PasswordChange(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    old_password: str = Field(..., alias="oldPassword")
    new_password: str = Field(..., alias="newPassword")


class PlatformOverview(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    Provides details on the version, build and environment that is currently running
    """

    name: Optional[str] = None
    release: Optional[str] = None
    description: Optional[str] = None
    host_name: Optional[str] = Field(
        None, alias="hostName", description="The hostname for this instance"
    )
    environment: Optional[str] = Field(
        None,
        description="The name of the environment in which this instance is running",
    )
    commit_id: Optional[str] = Field(
        None,
        alias="commitId",
        description="The git commit ID for this API server instance running",
    )
    build_time: Optional[str] = Field(
        None,
        alias="buildTime",
        description="The build time for this API server instance running",
    )
    version: Optional[str] = Field(
        None, description="The version of API server instance running"
    )
    recommended_client_version: Optional[str] = Field(
        None,
        alias="recommendedClientVersion",
        description="The recommended version of the Kodexa client to use",
    )
    extension_packs: Optional[List[Dict[str, str]]] = Field(
        None, alias="extensionPacks", description="Installed extension packs"
    )


class QueryContext(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    page_size: Optional[int] = Field(
        None, alias="pageSize", description="Page size (default 20)"
    )
    page: Optional[int] = Field(None, description="Page number (default 1)")
    sort: Optional[str] = Field(None, description="Sorts to apply")
    filter: Optional[str] = Field(None, description="Simple filter to apply")
    query: Optional[str] = Field(
        None, description="Simple query to apply (if available)"
    )


class SortObject(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    empty: Optional[bool] = None
    unsorted: Optional[bool] = None
    sorted: Optional[bool] = None


class SearchEntity(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    Entities identified in search content
    """

    id: Optional[str] = None
    entity: Optional[str] = Field(None, description="The type of entity")
    value: Optional[str] = Field(None, description="The entity value")
    start: Optional[int] = Field(None, description="Start position")
    end: Optional[int] = Field(None, description="End position")


class EventType(Enum):
    """

    """
    created = "CREATED"
    deleted = "DELETED"
    updated = "UPDATED"


class DataAttributeValues(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    value: Optional[str] = None
    truncated: Optional[bool] = None
    tag: str
    tag_uuid: Optional[str] = Field(None, alias="tagUuid")
    date_value: Optional[StandardDateTime] = Field(None, alias="dateValue")
    float_value: Optional[float] = Field(None, alias="floatValue")
    decimal_value: Optional[float] = Field(None, alias="decimalValue")
    number_value: Optional[int] = Field(None, alias="numberValue")
    boolean_value: Optional[bool] = Field(None, alias="booleanValue")
    string_value: Optional[str] = Field(None, alias="stringValue")
    attribute_status: Optional[AttributeStatus] = Field(None, alias="attributeStatus")
    confidence: Optional[float] = None


class BulkDelete(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    all: Optional[bool] = None
    document_family_ids: Optional[List[str]] = Field(None, alias="documentFamilyIds")


class User(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    A user within the Kodexa platform
    """

    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    email: Optional[str] = None
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    activated: Optional[bool] = None
    platform_admin: Optional[bool] = Field(None, alias="platformAdmin")
    password_reset_date: Optional[StandardDateTime] = Field(
        None, alias="passwordResetDate"
    )
    last_connected: Optional[StandardDateTime] = Field(None, alias="lastConnected")
    user_storage: Optional[UserStorage] = Field(None, alias="userStorage")
    has_image: Optional[bool] = Field(None, alias="hasImage")
    show_developer_tools: Optional[bool] = Field(None, alias="showDeveloperTools")


class DeploymentMetadata(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    deployment_type: Optional[DeploymentType] = Field(None, alias="deploymentType")
    min_replicas: Optional[int] = Field(None, alias="minReplicas")
    max_replicas: Optional[int] = Field(None, alias="maxReplicas")
    reserved_concurrency: Optional[int] = Field(None, alias="reservedConcurrency")
    limits: Optional[ContainerResources] = None
    requests: Optional[ContainerResources] = None
    memory_assigned: Optional[str] = Field(None, alias="memoryAssigned")
    scheduler_token: Optional[str] = Field(None, alias="schedulerToken")
    service_name: Optional[str] = Field(None, alias="serviceName")
    container_name: Optional[str] = Field(None, alias="containerName")
    function_arn: Optional[str] = Field(None, alias="functionArn")
    environment: Optional[Dict[str, str]] = None
    pod_match_labels: Optional[List[MatchLabel]] = Field(None, alias="podMatchLabels")
    subscription_id: Optional[str] = Field(None, alias="subscriptionId")
    plan_name: Optional[str] = Field(None, alias="planName")
    resource_group: Optional[str] = Field(None, alias="resourceGroup")
    function_url: Optional[str] = Field(None, alias="functionUrl")
    app_key: Optional[str] = Field(None, alias="appKey")
    child_process: Optional[bool] = Field(None, alias="childProcess")


class DockerSource(ExtensionPackSource):
    """

    """
    location: Optional[str] = None


class DocumentMetadataDefaults(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    document_metadata_properties: Optional[List[DocumentMetadataProperty]] = Field(
        None, alias="documentMetadataProperties"
    )


class ExtensionPackProvided(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    ref: Optional[str] = Field(None, description="The reference to the metadata object")
    template: Optional[bool] = Field(
        None,
        description="Is this component a template that can be used to create new components",
    )
    schema_version: Optional[int] = Field(
        None, alias="schemaVersion", description="The version of the schema"
    )
    org_slug: Optional[str] = Field(
        None,
        alias="orgSlug",
        description="The slug of the organization that owns this metadata object",
    )
    slug: str = Field(
        ...,
        description="The slug used when referencing this metadata object",
        pattern=r"^[a-zA-Z0-9\-_\.]{0,255}$",
    )
    type: str = Field(..., description="The type of metadata object")
    name: str = Field(..., description="The name of the object")
    description: Optional[str] = Field(
        None, description="The description of the object"
    )
    version: Optional[str] = Field(
        None,
        description="The version of the object",
        pattern=r"^\d+\.\d+\.\d+(?:\-\d+)?$",
    )
    deployed: Optional[StandardDateTime] = Field(
        None,
        description="The date/time the object was deployed into this Kodexa instance",
    )
    public_access: Optional[bool] = Field(
        None,
        alias="publicAccess",
        description="Is the metadata object publicly accessible by other organizations",
    )
    image_url: Optional[str] = Field(
        None,
        alias="imageUrl",
        description="URL of image when presenting this object in a UI",
    )
    lifecycle: Optional[str] = Field(
        None, description="The lifecycle stage of the component"
    )
    icon: Optional[str] = Field(None, description="Material Icon name to use in the UI")
    overview_markdown: Optional[str] = Field(
        None,
        alias="overviewMarkdown",
        description="Markdown that is used to present the overview of the object",
    )
    metadata_tag: Optional[List[MetadataTag]] = Field(
        None, alias="metadataTag", description="A list of associated tags"
    )
    provider: Optional[str] = Field(None, description="The details of the of provider")
    provider_url: Optional[str] = Field(
        None, alias="providerUrl", description="The link to the provider website"
    )
    provider_image_url: Optional[str] = Field(
        None, alias="providerImageUrl", description="The link to the model image"
    )
    extension_pack_ref: Optional[str] = Field(
        None,
        alias="extensionPackRef",
        description="The reference to the extension pack (if the metadata object was created by an extension pack)",
    )
    change_sequence: Optional[int] = Field(
        None, alias="changeSequence", description="The change sequence"
    )
    delete_protection: Optional[bool] = Field(
        None, description="Delete protection", alias="deleteProtection"
    )


class Option(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    Options available for this event
    """

    group_options: Optional[List[Option]] = Field(None, alias="groupOptions")
    tab_name: Optional[str] = Field(None, alias="tabName")
    name: Optional[str] = None
    label: Optional[str] = None
    false_label: Optional[str] = Field(None, alias="falseLabel")
    hint: Optional[str] = None
    required: Optional[bool] = None
    type: Optional[str] = None
    list_type: Optional[str] = Field(None, alias="listType")
    list_label: Optional[str] = Field(None, alias="listLabel")
    list_description: Optional[str] = Field(None, alias="listDescription")
    feature_flag: Optional[str] = Field(None, alias="featureFlag")
    default: Optional[Any] = None
    description: Optional[str] = None
    support_article: Optional[str] = Field(None, alias="supportArticle")
    overview_markdown: Optional[str] = Field(None, alias="overviewMarkdown")
    show_if: Optional[str] = Field(None, alias="showIf")
    show_on_popup: Optional[bool] = Field(None, alias="showOnPopup")
    possible_values: Optional[List[PossibleValue]] = Field(None, alias="possibleValues")
    properties: Optional[Dict[str, Any]] = None


class Overlay(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    Overlays provide the ability to apply validation, normalization and enrichment
    """

    id: Optional[str] = Field(None, description="The ID of the taxon")
    name: Optional[str] = None
    conditions: Optional[List[OverlayCondition]] = None


class PipelineImplementationMetadata(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    Metadata captured when publishing a pipeline definition
    """

    steps: Optional[List[PipelineStepMetadata]] = Field(
        None, description="The metadata for the steps in this pipeline"
    )


class ConnectionType(Enum):
    """

    """
    STORE = "STORE"
    DOCUMENT_FAMILY = "DOCUMENT_FAMILY"
    DATA_OBJECT = "DATA_OBJECT"
    WORKSPACE = "WORKSPACE"
    CHANNEL = "CHANNEL"


class ProjectAssistantConnection(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    A template for an assistant subscription
    """
    source_ref: Optional[str] = Field(None, description="The reference to the metadata object to source",
                                      alias="sourceRef")
    source_type: Optional[ConnectionType] = Field(None, description="The type of the source", alias="sourceType")
    target_ref: Optional[str] = Field(None, description="The reference to the metadata object to target",
                                      alias="targetRef")
    target_type: Optional[ConnectionType] = Field(None, description="The type of the target", alias="targetType")
    subscription: Optional[str] = None
    active: Optional[bool] = True


class ProjectAssistant(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    The assistants that will be created with the project template
    """

    name: Optional[str] = None
    description: Optional[str] = None
    assistant_definition_ref: Optional[str] = Field(
        None, alias="assistantDefinitionRef"
    )
    options: Optional[Dict[str, Any]] = None
    stores: Optional[List[str]] = Field(default_factory=list)
    schedules: Optional[List[ScheduleDefinition]] = Field(default_factory=list)
    subscription: Optional[str] = None
    connections: Optional[List[ProjectAssistantConnection]] = Field(default_factory=list)
    logging_enabled: Optional[bool] = Field(None, alias="loggingEnabled")
    show_in_training: Optional[bool] = Field(None, alias="showInTraining")
    priority_hint: Optional[int] = Field(None, alias="priorityHint")


class Taxon(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    A taxon is an individual label within a taxonomy
    """

    id: Optional[str] = Field(None, description="The ID of the taxon")
    label: Optional[str] = Field(None, description="The text to display for this taxon")
    generate_name: Optional[bool] = Field(
        None,
        alias="generateName",
        description="Is the name generated, this allows that you can change displays without impacted existing content",
    )
    group: Optional[bool] = Field(
        None,
        description="Is this taxon a group, and therefore can't have a value, can only have children",
    )
    name: str = Field(
        ..., description="The name to be used", pattern=r"^[a-zA-Z0-9\-_]{0,255}$"
    )
    external_name: Optional[str] = Field(
        None,
        alias="externalName",
        description="The name to be used when we are publishing this taxon to external systems",
    )
    value_path: Optional[ValuePath] = Field(
        None,
        alias="valuePath",
        description="Where to get the value for this taxon when extracting",
    )
    metadata_value: Optional[MetadataValue] = Field(
        None,
        alias="metadataValue",
        description="If the type is metadata this will be the metadata option",
    )
    data_path: Optional[str] = Field(
        None,
        alias="dataPath",
        description="The path to the data, based on the data inside the label (tag) within the document",
    )
    expression: Optional[str] = Field(
        None,
        description="If the taxon is based on expression, this is the expression based on the available objects",
    )
    enable_fallback_expression: Optional[bool] = Field(
        None,
        alias="enableFallbackExpression",
        description="Allow for the use of a fallback expression if the taxon wasn't found",
    )
    fallback_expression: Optional[str] = Field(
        None,
        alias="fallbackExpression",
        description="Fallback expression if enabled, this is the expression based on the available objects",
    )
    nullable: Optional[bool] = Field(
        None, description="Determine if the value of the taxon can be null (unknown)"
    )
    null_value: Optional[str] = Field(
        None,
        alias="nullValue",
        description="Allows the setting of a value to replace null if the taxon is nullable",
    )
    description: Optional[str] = Field(None, description="The description of the taxon")
    overview_markdown: Optional[str] = Field(None, alias="overviewMarkdown")
    enabled: Optional[bool] = Field(
        None, description="Is the taxon enabled (used in the UI)"
    )
    color: Optional[str] = Field(
        None, description="Hex encoding of the color to use for the taxon"
    )
    children: Optional[List[Taxon]] = Field(
        None, description="The children under this taxon"
    )
    options: Optional[List[Option]] = Field(
        None,
        description="Options that can be shown for the taxon (usually used in assistant taxonomies)",
    )
    related_taxons: Optional[List[RelatedTaxon]] = Field(
        None,
        alias="relatedTaxons",
        description="A list of relationships to other taxons and the purpose of the relationship",
    )
    node_types: Optional[List[str]] = Field(
        None,
        alias="nodeTypes",
        description="A list of the node types that this taxon applies to (empty means everything), used in the UI",
    )
    taxon_type: Optional[TaxonType] = Field(
        None,
        alias="taxonType",
        description="Expected data type to coalesce to (defaults to STRING)",
    )
    selection_options: Optional[List[SelectionOption]] = Field(
        None,
        alias="selectionOptions",
        description="If data type is SELECTION, this is the list of available options",
    )
    type_features: Optional[Dict[str, Any]] = Field(
        None,
        alias="typeFeatures",
        description="Additional features for the type handling",
    )
    path: Optional[str] = Field(None, description="The path to the node")
    multi_value: Optional[bool] = Field(
        None, alias="multiValue", description="Does this taxon allow multiple values"
    )
    user_editable: Optional[bool] = Field(
        None,
        alias="userEditable",
        description="Can the value of this taxon be edited by a user",
    )
    denormalize_to_children: Optional[bool] = Field(
        None,
        alias="denormalizeToChildren",
        description="Should the value of this taxon be denormalized to the children",
    )
    not_user_labelled: Optional[bool] = Field(
        None,
        alias="notUserLabelled",
        description="The taxon is not user labelled",
    )
    use_post_expression: Optional[bool] = Field(
        None, alias="usePostExpression", description="Use a post extraction expression"
    )
    post_expression: Optional[str] = Field(
        None,
        alias="postExpression",
        description="An expression that is applied post extraction of the data",
    )
    semantic_definition: Optional[str] = Field(
        None,
        alias="semanticDefinition",
        description="The semantic definition of the taxon",
    )
    examples: Optional[List[GuidanceTagResult]] = Field(
        None,
        description="A list of examples of the taxon values, used to understand the taxon",
    )

    synonyms: Optional[List[str]] = Field(
        None,
        description="A list of synonyms of the taxon values, used to understand the taxon",
    )

    def update_path(self, parent_path=None):
        if parent_path is None:
            parent_path = ""
        self.path = parent_path + self.name
        if self.children is not None:
            for child in self.children:
                child.update_path(self.path + "/")


class ContentObject(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    content_type: ContentType = Field(
        ..., alias="contentType", description="The type of content"
    )
    document_version: Optional[str] = Field(None, alias="documentVersion")
    index: Optional[int] = None
    labels: Optional[List[Label]] = Field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None
    mixins: Optional[List[str]] = Field(default_factory=list)
    created: Optional[StandardDateTime] = None
    modified: Optional[StandardDateTime] = None
    size: Optional[int] = None
    store_ref: Optional[str] = Field(None, alias="storeRef")
    document_family_id: Optional[str] = Field(None, alias="documentFamilyId")


class DocumentAssignment(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    A list of the assignments to users for this document
    """

    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    user: User


class ExceptionDetails(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    message: Optional[str] = None
    status_code: Optional[int] = Field(None, alias="statusCode")
    error_message: Optional[str] = Field(None, alias="errorMessage")
    error_type: Optional[str] = Field(None, alias="errorType")
    executed_version: Optional[str] = Field(None, alias="executedVersion")
    advice: Optional[str] = None
    description: Optional[str] = None
    cause: Optional[Dict[str, Any]] = None
    documentation_url: Optional[str] = Field(None, alias="documentationUrl")
    stack_trace: Optional[List[Dict[str, Any]]] = Field(None, alias="stackTrace")
    help: Optional[str] = None
    option_errors: Optional[Dict[str, Any]] = Field(None, alias="optionErrors")
    validation_errors: Optional[List[ValidationError]] = Field(
        None, alias="validationErrors"
    )


class ExecutionStep(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = None
    status: Optional[Status3] = None
    exception_details: Optional[ExceptionDetails] = Field(
        None, alias="exceptionDetails"
    )
    name: Optional[str] = None
    start: Optional[StandardDateTime] = None
    end: Optional[StandardDateTime] = None
    processing_time: Optional[int] = Field(None, alias="processingTime")
    options: Optional[Dict[str, Any]] = None
    option_types: Optional[Dict[str, str]] = Field(None, alias="optionTypes")
    context: Optional[Dict[str, Any]] = None
    content_objects: Optional[List[ContentObject]] = Field(None, alias="contentObjects")
    input_id: Optional[str] = Field(None, alias="inputId")
    output_id: Optional[str] = Field(None, alias="outputId")
    ref: Optional[str] = None
    extension_pack_ref: Optional[str] = Field(None, alias="extensionPackRef")
    step_type: Optional[StepType1] = Field(None, alias="stepType")
    conditional: Optional[str] = None

class ProjectStatus(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    status: Optional[str] = Field(None, description="The status of the project")
    color: Optional[str] = None
    organization: Organization
    icon: Optional[str] = None


class ProjectOptions(BaseModel):

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )

    options: List[Option] = Field(None, description="The options for the project")
    properties: Dict[str, Any] = Field(None, description="The properties for the project")
    

class Project(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    organization: Optional[Organization] = None
    name: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[ProjectMetadata] = None
    show_tasks: Optional[bool] = Field(None, alias="showTasks")
    show_thumbnails: Optional[bool] = Field(None, alias="showThumbnails")
    show_notes_on_project: Optional[bool] = Field(None, alias="showNotesOnProject")
    show_exceptions_on_project: Optional[bool] = Field(
        None, alias="showExceptionsOnProject"
    )
    use_new_labeling: Optional[bool] = Field(None, alias="useNewLabeling")
    show_search: Optional[bool] = Field(None, alias="showSearch")
    show_tooltips_on_labeling: Optional[bool] = Field(
        None, alias="showTooltipsOnLabeling"
    )

    has_image: Optional[bool] = Field(None, alias="hasImage")

    project_template_ref: Optional[str] = Field(None, alias="projectTemplateRef")
    memory: Optional[ProjectMemory] = None
    document_statuses: Optional[List[DocumentStatus]] = Field(
        None, alias="documentStatuses"
    )
    attribute_statuses: Optional[List[AttributeStatus]] = Field(
        None, alias="attributeStatuses"
    )
    status: Optional[ProjectStatus] = None
    owner: Optional[User] = None
    options: Optional[ProjectOptions] = Field(None, alias="options")


class FeatureSet(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    owner_uri: Optional[str] = Field(None, alias="ownerUri")
    node_features: Optional[List[NodeFeatures]] = Field(None, alias="nodeFeatures")


class DocumentViewState(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = Field(None, description="The ID of the document view")
    index: Optional[int] = None
    document_family_id: Optional[str] = Field(None, alias="documentFamilyId")
    properties: Optional[Dict[str, Any]] = None
    current_page: Optional[int] = Field(None, alias="currentPage")
    selected_node_ids: Optional[List[str]] = Field(None, alias="selectedNodeIds")


class DataFormState(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = Field(None, description="The ID of the document view")
    index: Optional[int] = None
    properties: Optional[Dict[str, Any]] = None

    data_form_ref: Optional[str] = Field(None, alias="dataFormRef")
    document_family_ids: Optional[List[str]] = Field(None, alias="documentFamilyIds")
    data_object_ids: Optional[List[str]] = Field(None, alias="dataObjectIds")


class WorkspaceStorage(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    document_view_states: Optional[List[DocumentViewState]] = Field(
        None, alias="documentViewStates"
    )
    data_form_states: Optional[List[DataFormState]] = Field(
        None, alias="dataFormStates"
    )
    current_view_id: Optional[str] = Field(None, alias="currentViewId")
    default_sidebar: Optional[str] = Field(None, alias="defaultSidebar")
    overview: Optional[str] = None
    available_panels: Optional[Dict[str, bool]] = Field(None, alias="availablePanels")


class Workspace(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = Field(None, description="The ID of the workspace")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    project: Optional[Project] = None
    name: Optional[str] = None
    description: Optional[str] = None
    workspace_storage: Optional[WorkspaceStorage] = Field(
        None, alias="workspaceStorage"
    )


class ProjectWorkspace(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    name: Optional[str] = None
    description: Optional[str] = None
    workspace_storage: Optional[WorkspaceStorage] = Field(
        None, alias="workspaceStorage"
    )


class ChannelParticipant(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
    )
    """
    A participant in a channel
    """

    user: Optional[User] = None
    assistant: Optional[Assistant] = None


class Channel(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = Field(None, description="The ID of the channel")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    workspace: Optional[Workspace] = None
    project: Optional[Project] = None
    name: Optional[str] = None
    is_private: Optional[bool] = Field(None, alias="isPrivate")
    participants: Optional[List[ChannelParticipant]] = Field(None, alias="participants")


class MessageBlock(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = Field(None, description="The ID of the message block")
    type: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    channel: Optional[Channel] = None
    children: Optional[List[MessageBlock]] = Field(None, alias="children")


class MessageFeedbackResponse(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
    )
    """
    A response to a message feedback
    """

    id: Optional[str] = None
    options: Optional[Dict[str, Any]] = None


class MessageFeedbackOption(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
    )
    """
    A message feedback option
    """

    id: Optional[str] = None
    label: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    options: Optional[List[Option]] = None


class MessageFeedback(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    options: Optional[List[MessageFeedbackOption]] = Field(None, alias="options")


class Message(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = Field(None, description="The ID of the message")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    channel: Optional[Channel] = None
    block: Optional[MessageBlock] = Field(None, alias="block")
    message_type: Optional[str] = Field(None, alias="messageType")
    content: Optional[str] = None
    feedback: Optional[MessageFeedback] = Field(None, alias="feedback")
    assistant: Optional[Assistant] = None
    user: Optional[User] = None
    context: Optional[MessageContext] = None


class DataAttribute(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    value: Optional[str] = None
    truncated: Optional[bool] = None
    data_exceptions: Optional[List[DataException]] = Field(
        None,
        alias="dataExceptions",
        description="A list of the data exceptions",
    )
    tag: str
    tag_uuid: Optional[str] = Field(None, alias="tagUuid")
    date_value: Optional[StandardDateTime] = Field(None, alias="dateValue")
    float_value: Optional[float] = Field(None, alias="floatValue")
    decimal_value: Optional[float] = Field(None, alias="decimalValue")
    number_value: Optional[int] = Field(None, alias="numberValue")
    boolean_value: Optional[bool] = Field(None, alias="booleanValue")
    string_value: Optional[str] = Field(None, alias="stringValue")
    attribute_status: Optional[AttributeStatus] = Field(None, alias="attributeStatus")
    owner_uri: Optional[str] = Field(None, alias="ownerUri")
    confidence: Optional[float] = None
    data_features: Optional[Dict[str, Any]] = Field(
        None, alias="dataFeatures", description="Additional features for the data"
    )
    path: Optional[str] = None
    data_obj_id: Optional[str] = Field(None, alias="dataObjId")
    label: Optional[str] = None


class Role(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    A role that can be used to manage rights
    """

    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    name: str
    users: Optional[List[User]] = Field(default_factory=list)
    teams: Optional[List[Team]] = Field(default_factory=list)


class Membership(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    role: Optional[Role1] = None
    organization: Optional[Organization] = None
    user: Optional[User] = None


class DataFormSourceMethod(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    name: Optional[str] = None
    parameters: Optional[List[DataFormSourceParameter]] = None


class PageableObject(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    offset: Optional[int] = None
    paged: Optional[bool] = None
    unpaged: Optional[bool] = None
    page_number: Optional[int] = Field(None, alias="pageNumber")
    page_size: Optional[int] = Field(None, alias="pageSize")


class PageTeam(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[Team]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageModelTraining(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[ModelTraining]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageDataAttribute(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[DataAttribute]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageSession(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[Session]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageRole(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[Role]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageProject(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[Project]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageAssistant(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[Assistant]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageWorkspace(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[Workspace]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageMessage(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[Message]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageChannel(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[Channel]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageOrganization(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[Organization]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageMembership(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[Membership]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageExecutionLogEntry(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[ExecutionLogEntry]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class CustomEvent(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    A Custom Event allows you to define an subtype of assistant event with options
    """

    name: Optional[str] = Field(
        None, description="The name of the event", pattern=r"^[a-zA-Z0-9\-_]{0,40}$"
    )
    icon: Optional[str] = Field(
        None, description="The name of a Material Design Icon to use for the event"
    )
    label: Optional[str] = Field(
        None, description="The label to use on the event in the UI"
    )
    description: Optional[str] = Field(
        None, description="The long description for the event"
    )
    content_object: Optional[bool] = Field(
        None,
        alias="contentObject",
        description="Does the event require a content object",
    )
    entry_points: Optional[List[str]] = Field(
        None,
        alias="entryPoints",
        description="Entrypoints should we show this event (test, assistantBar, documentFamily)",
    )

    option_tabs: Optional[List[OptionTab]] = Field(
        None,
        alias="optionTabs",
        description="The tab groups that options will be organized into",
    )

    options: Optional[List[Option]] = Field(
        None, description="Options available for this event"
    )


class ObjectMetadata(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    options: Optional[List[Option]] = None


class ProjectTaxonomy(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    The taxonomies that will be created with the project template
    """

    slug: Optional[str] = None

    name: Optional[str] = None
    description: Optional[str] = None
    taxonomy_type: Optional[TaxonomyType] = Field(
        None, alias="taxonomyType", description="The type of taxonomy"
    )
    taxons: Optional[List[Taxon]] = Field(
        None, description="The hierarchical structure of taxon's in this taxonomy"
    )
    template_ref: Optional[str] = Field(None, alias="templateRef")
    ref: Optional[str] = None


class ContentException(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    A list of the content exceptions from the content objects
    """

    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    tag: Optional[str] = None
    message: Optional[str] = None
    exception_type: Optional[str] = Field(None, alias="exceptionType")
    severity: Optional[str] = None
    exception_details: Optional[str] = Field(None, alias="exceptionDetails")
    group_uuid: Optional[str] = Field(None, alias="groupUuid")
    tag_uuid: Optional[str] = Field(None, alias="tagUuid")
    content_object: Optional[ContentObject] = Field(None, alias="contentObject")


class ExecutionPipeline(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    valid: Optional[bool] = None
    ref: Optional[str] = None
    id: Optional[str] = None
    exceptions: Optional[List[ExceptionDetails]] = None
    steps: Optional[List[ExecutionStep]] = None


class DataFormSourceDefinition(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    source_type: Optional[SourceType] = Field(None, alias="sourceType")
    valid: Optional[bool] = None
    methods: Optional[List[DataFormSourceMethod]] = None


class PageUser(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[User]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class Execution(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    description: Optional[str] = None
    targets: Optional[ExecutionTargets] = None
    session: Optional[Session] = None
    start_date: Optional[StandardDateTime] = Field(None, alias="startDate")
    end_date: Optional[StandardDateTime] = Field(None, alias="endDate")
    processing_time: Optional[int] = Field(None, alias="processingTime")
    logging_enabled: Optional[bool] = Field(None, alias="loggingEnabled")
    status: Optional[Status1] = None
    exception_details: Optional[ExceptionDetails] = Field(
        None, alias="exceptionDetails"
    )
    status_details: Optional[StatusDetails] = Field(None, alias="statusDetails")
    pipeline: Optional[ExecutionPipeline] = None
    parameters: Optional[Dict[str, Any]] = None
    custom_options: Optional[Dict[str, Any]] = Field(None, alias="customOptions")
    context: Optional[Dict[str, Any]] = None
    content_objects: Optional[List[ContentObject]] = Field(None, alias="contentObjects")
    child_executions: Optional[List[Execution]] = Field(None, alias="childExecutions")


class ExecutionSnapshot(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    description: Optional[str] = None
    targets: Optional[ExecutionTargets] = None
    session: Optional[Session] = None
    start_date: Optional[StandardDateTime] = Field(None, alias="startDate")
    end_date: Optional[StandardDateTime] = Field(None, alias="endDate")
    processing_time: Optional[int] = Field(None, alias="processingTime")
    logging_enabled: Optional[bool] = Field(None, alias="loggingEnabled")
    status: Optional[Status2] = None
    exception_details: Optional[ExceptionDetails] = Field(
        None, alias="exceptionDetails"
    )
    status_details: Optional[StatusDetails] = Field(None, alias="statusDetails")
    pipeline: Optional[ExecutionPipeline] = None
    parameters: Optional[Dict[str, Any]] = None
    custom_options: Optional[Dict[str, Any]] = Field(None, alias="customOptions")
    context: Optional[Dict[str, Any]] = None
    child_executions: Optional[List[Execution]] = Field(None, alias="childExecutions")
    content_objects: Optional[List[ContentObject]] = Field(None, alias="contentObjects")


class PageExecution(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[Execution]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class ContentMetadata1(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    pass


class SlugBasedMetadata(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    pass


class LabelStatistics(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    label_counts: Optional[Dict[str, int]] = Field(
        None,
        alias="labelCounts",
        description="The counts of each label in the document",
    )

    average_label_confidence: Optional[Dict[str, float]] = Field(
        None,
        alias="averageLabelConfidence",
        description="The average confidence of each label in the document",
    )

    max_label_confidence: Optional[Dict[str, float]] = Field(
        None,
        alias="maxLabelConfidence",
        description="The maximum confidence of each label in the document",
    )

    min_label_confidence: Optional[Dict[str, float]] = Field(
        None,
        alias="minLabelConfidence",
        description="The minimum confidence of each label in the document",
    )


class DocumentEmbedding(BaseModel):
    
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    embedding: Optional[List[float]] = None
    document_family: Optional[DocumentFamily] = Field(None, alias="documentFamily")
    content_object: Optional[ContentObject] = Field(None, alias="contentObject")
    embedding_name: Optional[str] = Field(None, alias="embeddingName")
    node_uuid: Optional[str] = Field(None, alias="nodeUuid")


class DocumentFamily(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    A document family is the representation of a single piece of external content (ie. a PDF) and all the related document representations of that file
    """

    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    document_status: Optional[DocumentStatus] = Field(None, alias="documentStatus")
    summary: Optional[str] = None

    assignments: Optional[List[DocumentAssignment]] = Field(
        None,
        description="A list of the assignments to users for this document",
    )
    store_ref: Optional[str] = Field(
        None,
        alias="storeRef",
        description="The reference to the store that is holding this document family",
    )
    path: str = Field(..., description="The path to the document family in the store")
    locked: Optional[bool] = Field(
        None,
        description="Is the document family locked. If locked then you can no longer modify or add any new document transitions",
    )
    created: Optional[StandardDateTime] = Field(None, description="Date/Time Created")
    modified: Optional[StandardDateTime] = Field(None, description="Date/Time Modified")
    size: Optional[int] = Field(
        None, description="Size of the original native content in bytes"
    )
    indexed: Optional[bool] = Field(
        None, description="Is the document family indexed for search"
    )
    content_objects: Optional[List[ContentObject]] = Field(
        None,
        alias="contentObjects",
        description="An ordered list of the content objects in the document family",
    )
    content_exceptions: Optional[List[ContentException]] = Field(
        default_factory=list,
        alias="contentExceptions",
        description="A list of the content exceptions from the content objects",
    )
    transitions: Optional[List[DocumentTransition]] = Field(
        None,
        description="An ordered list of the transitions in the document family",
    )
    labels: Optional[List[Label]] = Field(
        None,
        description="The labels from the latest content object in the family",
    )
    mixins: Optional[List[str]] = Field(
        None,
        description="The mixins from the latest content object in the family",
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None, description="The metadata from the latest document content object"
    )
    metadata_source: Optional[Dict[str, str]] = Field(
        None,
        alias="metadataSource",
        description="This identified the content object ID that added each of the metadata keys",
    )
    statistics: Optional[DocumentFamilyStatistics] = None

    label_statistics: Optional[LabelStatistics] = Field(
        None,
        alias="labelStatistics",
        description="The statistics about the labels in the document family",
    )


class DocumentFamilyStatistics(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    A collection of statistics about the document family
    """

    path_counts: Optional[List[PathExtractedData]] = Field(None, alias="pathCounts")
    recent_executions: Optional[List[ExecutionOverview]] = Field(
        None, alias="recentExecutions"
    )


class ExecutionAssistant(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    subscription: Optional[str] = None
    schedules: Optional[List[AssistantSchedule]] = Field(default_factory=list)
    project: Optional[Project] = None
    name: str
    description: Optional[str] = None
    assistant_definition_ref: Optional[str] = Field(
        None, alias="assistantDefinitionRef"
    )
    logging_enabled: Optional[bool] = Field(None, alias="loggingEnabled")
    active: Optional[bool] = None
    run_on_existing_content: Optional[bool] = Field(None, alias="runOnExistingContent")
    options: Optional[Dict[str, Any]] = None
    validation_errors: Optional[ValidationResults] = Field(
        None, alias="validationErrors"
    )
    definition: Optional[AssistantDefinition] = None


class ExecutionOverview(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    assistant: Optional[ExecutionAssistant] = None
    execution: Optional[ExecutionSnapshot] = None


class DataObject(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    document_family: Optional[DocumentFamily] = Field(None, alias="documentFamily")
    data_exceptions: Optional[List[DataException]] = Field(
        default_factory=list,
        alias="dataExceptions",
        description="A list of the data exceptions",
    )
    taxonomy_ref: Optional[str] = Field(None, alias="taxonomyRef")
    path: Optional[str] = None
    row_num: Optional[int] = Field(None, alias="rowNum")
    source_ordering: Optional[str] = Field(None, alias="sourceOrdering")
    date_time: Optional[StandardDateTime] = Field(None, alias="dateTime")
    lineage: Optional[DataLineage] = None
    attributes: Optional[List[DataAttribute]] = Field(default_factory=list)
    parent_id: Optional[str] = Field(None, alias="parentId")
    store_ref: Optional[str] = Field(None, alias="storeRef")


class Assistant(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    subscription: Optional[str] = None
    schedules: Optional[List[AssistantSchedule]] = Field(default_factory=list)
    project: Optional[Project] = None
    name: str
    description: Optional[str] = None
    assistant_definition_ref: Optional[str] = Field(
        None, alias="assistantDefinitionRef"
    )
    logging_enabled: Optional[bool] = Field(None, alias="loggingEnabled")
    active: Optional[bool] = None
    run_on_existing_content: Optional[bool] = Field(None, alias="runOnExistingContent")
    options: Optional[Dict[str, Any]] = None
    test_options: Optional[Dict[str, Any]] = Field(None, alias="testOptions")
    validation_errors: Optional[ValidationResults] = Field(
        None, alias="validationErrors"
    )
    definition: Optional[AssistantDefinition] = None
    show_in_training: Optional[bool] = Field(None, alias="showInTraining")
    color: Optional[str] = Field(None, description="The color to use for the assistant")
    priority_hint: Optional[int] = Field(None, alias="priorityHint")


class AssistantExecution(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    assistant_id: Optional[str] = Field(None, alias="assistantId")
    project_id: Optional[str] = Field(None, alias="projectId")
    assistant_name: Optional[str] = Field(None, alias="assistantName")
    ref: Optional[str] = None
    options: Optional[Dict[str, Any]] = None
    option_types: Optional[Dict[str, str]] = Field(None, alias="optionTypes")
    status: Optional[Status5] = None
    exception_details: Optional[ExceptionDetails] = Field(
        None, alias="exceptionDetails"
    )
    event: Optional[
        Union[
            AssistantEvent,
            ContentEvent,
            DataObjectEvent,
            DocumentFamilyEvent,
            ScheduledEvent,
            ChannelEvent,
            WorkspaceEvent,
        ]
    ] = None
    response: Optional[AssistantExecutionResponse] = None
    start_date: Optional[StandardDateTime] = Field(None, alias="startDate")
    end_date: Optional[StandardDateTime] = Field(None, alias="endDate")
    processing_time: Optional[int] = Field(None, alias="processingTime")


class AssistantExecutionResponse(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    text: Optional[str] = None
    pipelines: Optional[List[AssistantResponsePipeline]] = None


class AssistantResponsePipeline(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    description: Optional[str] = None
    pipeline: Optional[Pipeline] = None
    write_back_to_store: Optional[bool] = Field(None, alias="writeBackToStore")
    data_source_ref: Optional[str] = Field(None, alias="dataSourceRef")
    taxonomy_refs: Optional[List[str]] = Field(None, alias="taxonomyRefs")
    labels_to_apply: Optional[List[str]] = Field(None, alias="labelsToApply")
    logging_enabled: Optional[bool] = Field(None, alias="loggingEnabled")


class BaseEvent(
    RootModel[
        Union[
            BaseEvent1,
            "DocumentFamilyEvent",
            "DataObjectEvent",
            "ContentEvent",
            "ScheduledEvent",
            "AssistantEvent",
            "ChannelEvent",
            "WorkspaceEvent"
        ]
    ]
):
    """

    """
    pass


class MessageContext(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )

    active_features: Optional[FeatureSet] = Field(None, alias="activeFeatures")
    active_data: Optional[List[dict[str, Any]]] = Field(None, alias="activeData")
    content_object_id: Optional[str] = Field(None, alias="contentObjectId")
    store_ref: Optional[str] = Field(None, alias="storeRef")
    document_family_id: Optional[str] = Field(None, alias="documentFamilyId")
    selected_node_uuids: Optional[List[str]] = Field(None, alias="selectedNodeUuids")
    page: Optional[int] = None
    message_template: Optional[MessageTemplate] = Field(None, alias="messageTemplate")
    message_feedback_response: Optional[MessageFeedbackResponse] = Field(None, alias="feedbackOption")
    taxonomy_refs: Optional[List[str]] = Field(None, alias="taxonomyRefs")


class MessageEvent(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    message: Optional[Message] = None


class ChannelEvent(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    type: Optional[str] = None
    channel: Optional[Channel] = None
    message_events: Optional[List[MessageEvent]] = Field(None, alias="messageEvents")


class ModelInteraction(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )

    model_id: Optional[str] = Field(None, alias="modelId")
    input_tokens: Optional[int] = Field(None, alias="inputTokens")
    output_tokens: Optional[int] = Field(None, alias="outputTokens")
    duration: Optional[int] = None
    note: Optional[str] = None


class ModelUsage(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )

    interactions: Optional[List[ModelInteraction]] = None


class ExecutionEvent(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    type: ExecutionEventType
    status: Optional[Status6] = None
    execution: Optional[Execution] = None
    store_ref: Optional[str] = Field(None, alias="storeRef")
    document_family_id: Optional[str] = Field(None, alias="documentFamilyId")
    data_object_id: Optional[str] = Field(None, alias="dataObjectId")
    session_id: str = Field(..., alias="sessionId")
    token: str
    pipeline: Optional[ExecutionPipeline] = None
    assistant: Optional[AssistantExecution] = None
    source: Optional[Dict[str, Any]] = None
    payload: Optional[Dict[str, Any]] = None
    input_id: Optional[str] = Field(None, alias="inputId")
    platform_url: Optional[str] = Field(None, alias="platformUrl")
    session_call_back_url: Optional[str] = Field(None, alias="sessionCallBackUrl")
    created: Optional[StandardDateTime] = None
    start_date: Optional[StandardDateTime] = Field(None, alias="startDate")
    end_date: Optional[StandardDateTime] = Field(None, alias="endDate")
    model_usage: Optional[ModelUsage] = Field(None, alias="modelUsage")


class PageTaxonomy(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[Taxonomy]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class GuidanceTagResult(BaseModel):
    """

    """
    value: Optional[str] = None
    line_uuid: Optional[str] = Field(None, alias="lineUuid")


class UserSelection(BaseModel):
    text: Optional[str] = None
    line_uuid: Optional[str] = Field(None, alias="lineUuid")


class Guidance(BaseModel):
    guidance_type: Optional[str] = Field(None, alias="guidanceType")
    taxonomy_ref: Optional[str] = Field(None, alias="taxonomyRef")
    document_name: Optional[str] = Field(None, alias="documentName")
    document_type: Optional[str] = Field(None, alias="documentType")
    document_page: Optional[int] = Field(None, alias="documentPage")
    sample_text: Optional[str] = Field(None, alias="sampleText")
    sample_result: Optional[Dict[str, List[GuidanceTagResult]]] = Field(None, alias="sampleResult")
    section_markers: Optional[List[GuidanceTagResult]] = Field(None, alias="sectionMarkers")
    active: Optional[bool] = None
    applicable_tags: Optional[List[str]] = Field(None, alias="applicableTags")
    priority: Optional[int] = 1
    user_instructions: Optional[str] = Field(None, alias="userInstructions")
    user_instructions_properties: Optional[Dict[str, Any]] = Field(None, alias="userInstructionsProperties")

    # users selected text, text and line_uuid
    user_selection: Optional[List[UserSelection]] = Field(None, alias="userSelection")

    compiled_guidance: Optional[Dict[str, Any]] = Field(None, alias="compiledGuidance")


class GuidanceSet(ExtensionPackProvided):
    """

    """
    guidance: List[Guidance] = Field(None, description="The guidance in the set")


class PageGuidanceSet(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[GuidanceSet]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class TemplateType(Enum):
    """

    """
    fstring = "FSTRING"
    mustache = "MUSTACHE"


class Prompt(ExtensionPackProvided):
    """

    """
    prompt_template: Optional[str] = Field(
        None, description="The prompt template", alias="promptTemplate"
    )
    options: Optional[List[Option]] = Field(
        None, description="Options for the prompt"
    )
    template_type: Optional[TemplateType] = Field(None, alias="templateType")

    def render(self, properties):
        if self.template_type == "FSTRING":
            return self.prompt_template.format(**properties)
        elif self.template_type == "MUSTACHE":
            import chevron
            return chevron.render(self.prompt_template, properties)
        else:
            raise Exception(f"Unknown template type {self.template_type}")


class PagePrompt(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[Prompt]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageStore(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[Store]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageDocumentFamily(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[DocumentFamily]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class SearchContent(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    A document family is the representation of a single peice of external content (ie. a PDF) and all the related document representations of that file
    """

    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    store: Optional[StoreMetadata] = None
    document_family: Optional[DocumentFamily] = Field(None, alias="documentFamily")
    container_type: Optional[str] = Field(
        None, alias="containerType", description="The container node type"
    )
    container_uuid: Optional[str] = Field(
        None, alias="containerUuid", description="The container node UUID"
    )
    container_index: Optional[int] = Field(
        None, alias="containerIndex", description="The index of the container"
    )
    source_ordering: Optional[int] = Field(
        None,
        alias="sourceOrdering",
        description="The source ordering for the content (starting at 0)",
    )
    entities: Optional[List[SearchEntity]] = Field(
        None, description="Entities found in the search content"
    )
    node_uuid: Optional[str] = Field(
        None, alias="nodeUuid", description="The unique ID of the content node"
    )
    node_type: Optional[str] = Field(
        None, alias="nodeType", description="The node type"
    )
    content: Optional[str] = None
    child_content: Optional[List[str]] = Field(
        None, alias="childContent", description="The content broken out in children"
    )


class StoreMetadata(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    The store containing the document family
    """

    template: Optional[bool] = Field(
        None,
        description="Is this component a template that can be used to create new components",
    )
    organization: Optional[Organization] = None
    slug: str
    extension_pack_ref: Optional[str] = Field(None, alias="extensionPackRef")
    id: Optional[str] = None
    uuid: Optional[str] = None
    version: Optional[str] = None
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    name: Optional[str] = None
    public_access: Optional[bool] = Field(
        None,
        alias="publicAccess",
        description="Is this component available to all organizations",
    )
    ref: Optional[str] = None
    projects: Optional[List[Project]] = Field(default_factory=list)
    assistants: Optional[List[Assistant]] = Field(default_factory=list)
    metadata: Optional[Store] = None


class PlatformEvent(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    date_time: Optional[StandardDateTime] = Field(None, alias="dateTime")
    assistant: Optional[Assistant] = None
    event_detail: Optional[
        Union[
            AssistantEvent,
            ContentEvent,
            DataObjectEvent,
            DocumentFamilyEvent,
            ScheduledEvent,
            ChannelEvent,
            WorkspaceEvent
        ]
    ] = Field(None, alias="eventDetail")
    document_family: Optional[DocumentFamily] = Field(None, alias="documentFamily")


class PageDataObject(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[DataObject]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class AuditEvent(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    """
    An audit event captures a data to a data structure or document
    """

    id: Optional[str] = Field(None, description="The ID of the object")
    uuid: Optional[str] = None
    change_sequence: Optional[int] = Field(None, alias="changeSequence")
    created_on: Optional[StandardDateTime] = Field(None, alias="createdOn")
    updated_on: Optional[StandardDateTime] = Field(None, alias="updatedOn")
    platform_user: Optional[User] = Field(None, alias="platformUser")
    document_family: Optional[DocumentFamily] = Field(None, alias="documentFamily")
    data_object: Optional[DataObject] = Field(None, alias="dataObject")
    data_attribute: Optional[DataAttribute] = Field(None, alias="dataAttribute")
    tag: Optional[str] = None
    event_type: Optional[EventType] = Field(None, alias="eventType")
    old_value: Optional[DataAttributeValues] = Field(None, alias="oldValue")
    new_value: Optional[DataAttributeValues] = Field(None, alias="newValue")


class PageAuditEvent(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[AuditEvent]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageRuleSet(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[RuleSet]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageProjectTemplate(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[ProjectTemplate]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PagePipeline(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[Pipeline]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageModelRuntime(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[ModelRuntime]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageSlugBasedMetadata(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[
        List[
            Union[
                SlugBasedMetadata,
                Action,
                AssistantDefinition,
                CredentialDefinition,
                Dashboard,
                DataForm,
                ExtensionPack,
                ModelRuntime,
                Pipeline,
                ProjectTemplate,
                Store,
                Taxonomy,
            ]
        ]
    ] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageExtensionPack(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[ExtensionPack]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PagePlatformEvent(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[PlatformEvent]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageDataException(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[DataException]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageDataForm(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[DataForm]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageDashboard(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[Dashboard]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageCredentialDefinition(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[CredentialDefinition]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageAssistantDefinition(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[AssistantDefinition]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class PageAction(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    total_pages: Optional[int] = Field(None, alias="totalPages")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    size: Optional[int] = None
    content: Optional[List[Action]] = None
    number: Optional[int] = None

    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    last: Optional[bool] = None
    empty: Optional[bool] = None


class DocumentContentMetadata(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    document_metadata: Optional[DocumentMetadataDefaults] = Field(
        None, alias="documentMetadata"
    )
    type: Optional[str] = Field(None, description="The type of content metadata")


class MessageTemplate(BaseModel):
    """

    """
    name: Optional[str] = None
    label: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    requires_context: Optional[bool] = Field(
        None, alias="requiresContext"
    )
    message_block: Optional[MessageBlock] = Field(
        None, alias="messageBlock"
    )


class ModelContentMetadata(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    type: Optional[str] = Field(None, description="The type of content metadata")
    model_runtime_ref: Optional[str] = Field(
        None,
        alias="modelRuntimeRef",
        description="The reference to the model runtime to use",
    )
    state_hash: Optional[str] = Field(
        None,
        alias="stateHash",
        description="The state has is used to determine the last update of the model",
    )
    model_runtime_parameters: Optional[Dict[str, Any]] = Field(
        None,
        alias="modelRuntimeParameters",
        description="The parameters to be passed to the model runtime",
    )
    state: Optional[State] = Field(
        None, description="The state of the model in this store"
    )

    inferable: Optional[bool] = Field(None, description="Can this model be used to infer")

    trainable: Optional[bool] = Field(None, description="Can this model be trained")

    event_aware: Optional[bool] = Field(
        None, alias="eventAware", description="Is this model event aware"
    )

    atomic: Optional[bool] = Field(
        None, description="Is the model uploaded/downloaded atomically"
    )

    use_implementation_from_template: Optional[bool] = Field(
        None,
        alias="useImplementationFromTemplate",
        description="Use implementation from template",
    )

    template_ref: Optional[str] = Field(
        None,
        alias="templateRef",
        description="The template ref that will be used if we are going to use the implementation from the template",
    )

    option_tabs: Optional[List[OptionTab]] = Field(
        None,
        alias="optionTabs",
        description="The tab groups that options will be organized into",
    )

    training_options: Optional[List[Option]] = Field(
        None, alias="trainingOptions", description="The training options for this model"
    )

    message_templates: Optional[List[MessageTemplate]] = Field(
        None, alias="messageTemplates", description="The message templates"
    )

    inference_options: Optional[List[Option]] = Field(
        None,
        alias="inferenceOptions",
        description="The inference options for this model",
    )

    taxonomy: Optional[Taxonomy] = None
    additional_taxon_options: Optional[List[Option]] = Field(
        None,
        alias="additionalTaxonOptions",
        description="This are additional properties that can be set on a label when the model is part of the project",
    )
    contents: Optional[List[str]] = Field(
        None,
        description="A list of the paths (with wildcards) that hold the content of this model",
    )
    ignored_contents: Optional[List[str]] = Field(
        None,
        alias="ignoredContents",
        description="A list of the paths (with wildcards) that are ignored when picking up the content of this model",
    )
    base_dir: Optional[str] = Field(
        None,
        alias="baseDir",
        description="A base directory that was used for uploading of the model",
    )
    keep_zip: Optional[bool] = Field(
        False,
        alias="keepZip",
        description="Should the zip file be kept after the model has been uploaded",
    )


class Action(ExtensionPackProvided):
    """

    """

    step: Optional[StepImplementation] = None
    metadata: Optional[ObjectMetadata] = None


class AssistantDefinition(ExtensionPackProvided):
    """

    """
    template: Optional[bool] = None
    schedulable: Optional[bool] = Field(
        None, description="The assistant can be scheduled"
    )
    reactive: Optional[bool] = Field(
        None, description="The assistant is reactive to content changes"
    )
    assistant: Optional[AssistantImplementation] = None
    services: Optional[List[SlugBasedMetadata]] = Field(
        None, description="Services used by the assistant"
    )
    processing_taxonomies: Optional[List[AssistantTaxonomy]] = Field(
        None,
        alias="processingTaxonomies",
        description="Taxonomies that the assistant uses",
    )

    option_tabs: Optional[List[OptionTab]] = Field(
        None,
        alias="optionTabs",
        description="The tab groups that options will be organized into",
    )

    options: Optional[List[Option]] = Field(
        None, description="Options for the assistant"
    )
    additional_taxon_options: Optional[List[Option]] = Field(
        None,
        alias="additionalTaxonOptions",
        description="This are additional properties that can be set on a label when the assistant is part of the project",
    )
    event_types: Optional[List[CustomEvent]] = Field(
        None,
        alias="eventTypes",
        description="Custom event types that the assistant is able to response to",
    )
    default_schedules: Optional[List[ScheduleDefinition]] = Field(
        None,
        alias="defaultSchedules",
        description="The default schedules that the assistant has",
    )
    subscription: Optional[str] = Field(
        None,
        description="The subscription that the assistant has, this can not be overridden by the subscription in the instance",
    )


class CredentialDefinition(ExtensionPackProvided):
    """

    """

    credential_type: Optional[str] = Field(None, alias="credentialType")
    options: Optional[List[Option]] = Field(
        None, description="Options for the credential type"
    )


class Dashboard(ExtensionPackProvided):
    """

    """
    widgets: Optional[List[DashboardWidget]] = None
    single_widget: Optional[DashboardWidget] = Field(None, alias="singleWidget")
    entry_points: Optional[List[str]] = Field(None, alias="entryPoints")


class DataForm(ExtensionPackProvided):
    """

    """
    entrypoints: Optional[List[str]] = None
    entrypoint: Optional[str] = None
    cards: Optional[List[Card]] = None
    filters: Optional[str] = None


class ProjectDataForm(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    slug: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None

    cards: Optional[List[Card]] = None

    ref: Optional[str] = None


class ExtensionPack(ExtensionPackProvided):
    """

    """
    name: Optional[str] = None
    description: Optional[str] = None
    public_access: Optional[bool] = Field(None, alias="publicAccess")
    pack_uri: Optional[str] = Field(None, alias="packUri")
    status: Optional[Status] = None
    deployable: Optional[bool] = None
    services: Optional[List[SlugBasedMetadata]] = None
    source: Optional[ExtensionPackSource] = None
    deployment: Optional[DeploymentMetadata] = None
    background_task: Optional[str] = Field(None, alias="backgroundTask")


class ModelRuntime(ExtensionPackProvided):
    """

    """

    inference_action: Optional[str] = Field(
        None,
        alias="inferenceAction",
        description="The reference to the action that will be used for inference",
    )
    training_action: Optional[str] = Field(
        None,
        alias="trainingAction",
        description="A reference to the action that will be used for training",
    )
    event_action: Optional[str] = Field(
        None,
        alias="eventAction",
        description="A reference to the action that will be used for event handling",
    )
    deployment_type: Optional[DeploymentType1] = Field(
        None,
        alias="deploymentType",
        description="The deployment to use, local means that the model runtime can be re-used across models, while container means that the model store must be deployed with the model runtime",
    )
    container_url: Optional[str] = Field(
        None,
        alias="containerUrl",
        description="The URL of the container to use if the deployment type is CONTAINER",
    )
    deployment_defaults: Optional[DeploymentMetadata] = Field(
        None, alias="deploymentDefaults"
    )


class Pipeline(ExtensionPackProvided):
    """

    """
    metadata: Optional[PipelineImplementationMetadata] = None


class ProjectTemplate(ExtensionPackProvided):

    stores: Optional[List[ProjectStore]] = Field(
        None, description="The stores that will be created with the project template"
    )
    assistants: Optional[List[ProjectAssistant]] = Field(
        None,
        description="The assistants that will be created with the project template",
    )
    taxonomies: Optional[List[ProjectTaxonomy]] = Field(
        None,
        description="The taxonomies that will be created with the project template",
    )
    dashboards: Optional[List[ProjectDashboard]] = Field(
        None,
        description="The dashboards that will be created with the project template",
    )
    workspaces: Optional[List[ProjectWorkspace]] = Field(
        None,
        description="The workspaces that will be created with the project template",
    )
    guidance: Optional[List[ProjectGuidance]] = Field(
        None,
        description="The guidance that will be created with the project template",
    )
    data_forms: Optional[List[ProjectDataForm]] = Field(
        None,
        alias="dataForms",
        description="The data forms that will be created with the project template",
    )
    help_url: Optional[str] = Field(
        None,
        alias="helpUrl",
        description="A help URL where you can learn more about the assistant",
    )
    category: Optional[Category] = Field(
        None, description="The category of project template"
    )
    document_statuses: Optional[List[DocumentStatus]] = Field(
        None,
        alias="documentStatuses",
        description="The document statuses that will be created with the project template",
    )
    attribute_statuses: Optional[List[AttributeStatus]] = Field(
        None,
        alias="attributeStatuses",
        description="The attribute statuses that will be created with the project template",
    )

    options: Optional[ProjectOptions] = Field(None, alias="options")

    tags: Optional[List[str]] = Field(None, alias="tags")


class Store(ExtensionPackProvided):
    """

    """

    metadata: Optional[ContentMetadata1] = None
    store_type: Optional[StoreType] = Field(
        None, alias="storeType", description="The type of object the store will contain"
    )
    searchable: Optional[bool] = Field(
        None, description="Is the store indexed, and thus searchable"
    )
    store_purpose: Optional[StorePurpose] = Field(
        None,
        alias="storePurpose",
        description="The purpose of the store (used by UI and assistants to understand how to interact with the store events)",
    )
    view_options: Optional[StoreViewOptions] = Field(None, alias="viewOptions")
    view_presets: Optional[List[ViewPreset]] = Field(
        None,
        alias="viewPresets",
        description="View presets that have been saved for this store",
    )

    show_thumbnails: Optional[bool] = Field(
        None, description="Show thumbnails in store", alias="showThumbnails"
    )

    show_search: Optional[bool] = Field(
        None, description="Show search in store", alias="showSearch"
    )

    allow_data_editing: Optional[bool] = Field(
        None, description="Allow data editing", alias="allowDataEditing"
    )

    delete_protection: Optional[bool] = Field(
        None, description="Delete protection", alias="deleteProtection"
    )


class Taxonomy(ExtensionPackProvided):
    """

    """

    type: Optional[str] = Field(None, description="The metadata object type")
    taxonomy_type: Optional[TaxonomyType1] = Field(
        None, alias="taxonomyType", description="The type of taxonomy"
    )
    enabled: Optional[bool] = Field(
        None, description="Is the taxonomy enabled (effects display in the UI)"
    )
    taxons: Optional[List[Taxon]] = Field(
        None, description="The hierarchical structure of taxon's in this taxonomy"
    )
    overlays: Optional[List[Overlay]] = Field(
        None,
        description="Overlays provide the ability to apply validation, normalization and enrichment",
    )
    total_taxons: Optional[int] = Field(
        None,
        alias="totalTaxons",
        description="The total number of taxons in the taxonomy",
    )

    def update_paths(self):
        for taxon in self.taxons:
            taxon.update_path()

    def build_guidance_tags(self, taxons=None, guidance_tags=None):
        if taxons is None:
            taxons = self.taxons
        if guidance_tags is None:
            guidance_tags = {}
        for taxon in taxons:
            new_tags = []
            if taxon.examples is not None:
                for example in taxon.examples:
                    new_tags.append(example)
                guidance_tags[taxon.path] = new_tags

            if taxon.children is not None and len(taxon.children) > 0:
                guidance_tags = self.build_guidance_tags(taxon.children, guidance_tags)

        return guidance_tags


class RuleSet(ExtensionPackProvided):
    """

    """

    ref: Optional[str] = Field(None, description="The reference to the metadata object")
    template: Optional[bool] = Field(
        None,
        description="Is this component a template that can be used to create new components",
    )
    schema_version: Optional[int] = Field(
        None, alias="schemaVersion", description="The version of the schema"
    )
    org_slug: Optional[str] = Field(
        None,
        alias="orgSlug",
        description="The slug of the organization that owns this metadata object",
    )
    slug: Optional[str] = Field(
        None,
        description="The slug used when referencing this metadata object",
        pattern=r"^[a-zA-Z0-9\-_]{0,255}$",
    )
    type: Optional[str] = Field(None, description="The type of metadata object")
    name: Optional[str] = Field(None, description="The name of the object")
    description: Optional[str] = Field(
        None, description="The description of the object"
    )
    version: Optional[str] = Field(
        None,
        description="The version of the object",
        pattern=r"^\d+\.\d+\.\d+(?:\-\d+)?$",
    )

    public_access: Optional[bool] = Field(
        None,
        alias="publicAccess",
        description="Is the metadata object publicly accessible by other organizations",
    )
    image_url: Optional[str] = Field(
        None,
        alias="imageUrl",
        description="URL of image when presenting this object in a UI",
    )
    icon: Optional[str] = Field(None, description="Material Icon name to use in the UI")
    overview_markdown: Optional[str] = Field(
        None,
        alias="overviewMarkdown",
        description="Markdown that is used to present the overview of the object",
    )
    metadata_tag: Optional[List[MetadataTag]] = Field(
        None, alias="metadataTag", description="A list of associated tags"
    )
    provider: Optional[str] = Field(None, description="The details of the of provider")
    provider_url: Optional[str] = Field(
        None, alias="providerUrl", description="The link to the provider website"
    )
    provider_image_url: Optional[str] = Field(
        None, alias="providerImageUrl", description="The link to the model image"
    )
    extension_pack_ref: Optional[str] = Field(
        None,
        alias="extensionPackRef",
        description="The reference to the extension pack (if the metadata object was created by an extension pack)",
    )


class AssistantEvent(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    type: Optional[str] = None
    content_object: Optional[ContentObject] = Field(None, alias="contentObject")
    options: Optional[Dict[str, Any]] = None
    event_type: Optional[str] = Field(None, alias="eventType")
    assistant: Optional[Assistant] = None


class ContentEvent(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    type: Optional[str] = None
    content_object: Optional[ContentObject] = Field(None, alias="contentObject")
    document_family: Optional[DocumentFamily] = Field(None, alias="documentFamily")
    object_event_type: Optional[ObjectEventType] = Field(None, alias="objectEventType")


class DataObjectEvent(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    type: Optional[str] = None
    data_object: Optional[DataObject] = Field(None, alias="dataObject")


class DocumentFamilyEvent(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    type: Optional[str] = None
    document_family: Optional[DocumentFamily] = Field(None, alias="documentFamily")


class WorkspaceEvent(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    type: Optional[str] = None
    workspace: Optional[Workspace] = Field(None, alias="Workspace")
    workspace_update: Optional[dict] = Field(None, alias="workspaceUpdate")


class ScheduledEvent(BaseModel):
    """

    """
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        protected_namespaces=("model_config",),
    )
    type: Optional[str] = None
    last_event: Optional[StandardDateTime] = Field(None, alias="lastEvent")
    next_event: Optional[StandardDateTime] = Field(None, alias="nextEvent")


ThrowableProblem.model_rebuild()
Option.model_rebuild()
Taxon.model_rebuild()
ContentMetadata1.model_rebuild()
SlugBasedMetadata.model_rebuild()
PathExtractedData.model_rebuild()
ExecutionOverview.model_rebuild()
DocumentFamilyStatistics.model_rebuild()
DocumentFamily.model_rebuild()
ExecutionAssistant.model_rebuild()
Assistant.model_rebuild()
AssistantExecution.model_rebuild()
AssistantExecutionResponse.model_rebuild()
AssistantResponsePipeline.model_rebuild()
BaseEvent.model_rebuild()
PageTaxonomy.model_rebuild()
PageStore.model_rebuild()
SearchContent.model_rebuild()
StoreMetadata.model_rebuild()
PlatformEvent.model_rebuild()
PageRuleSet.model_rebuild()
PageProjectTemplate.model_rebuild()
PagePipeline.model_rebuild()
PageModelRuntime.model_rebuild()
PageSlugBasedMetadata.model_rebuild()
PageExtensionPack.model_rebuild()
PageDataForm.model_rebuild()
PageDashboard.model_rebuild()
PageCredentialDefinition.model_rebuild()
PageAssistantDefinition.model_rebuild()
PageAction.model_rebuild()
DocumentContentMetadata.model_rebuild()
ModelContentMetadata.model_rebuild()
Action.model_rebuild()
AssistantDefinition.model_rebuild()
CredentialDefinition.model_rebuild()
Dashboard.model_rebuild()
DataForm.model_rebuild()
ExtensionPack.model_rebuild()
ModelRuntime.model_rebuild()
Pipeline.model_rebuild()
ProjectTemplate.model_rebuild()
Store.model_rebuild()
Taxonomy.model_rebuild()
RuleSet.model_rebuild()
AssistantEvent.model_rebuild()
ContentEvent.model_rebuild()
DataObjectEvent.model_rebuild()
DocumentFamilyEvent.model_rebuild()
ScheduledEvent.model_rebuild()
DataException.model_rebuild()
Workspace.model_rebuild()
AssistantResponsePipeline.model_rebuild()
MessageTemplate.model_rebuild()
Message.model_rebuild()
MessageFeedback.model_rebuild()
MessageFeedbackResponse.model_rebuild()
MessageFeedbackOption.model_rebuild()
