"""
The Kodexa python client allows you to work with unstructured documents and the Kodexa platform to enabled Intelligent
Document Automation.
"""
from .assistant import Assistant, AssistantContext, AssistantResponse
from .connectors import (
    FileHandleConnector,
    FolderConnector,
    UrlConnector,
    add_connector,
    get_connector,
    get_connectors,
    get_source,
    registered_connectors,
)
from .model import (
    ContentEvent,
    ContentFeature,
    ContentNode,
    Document,
    DocumentActor,
    DocumentMetadata,
    DocumentTransition,
    SourceMetadata,
    TransitionType,
)
from .model.objects import Taxonomy
from .pipeline import Pipeline, PipelineContext, PipelineStatistics
from .platform import (
    KodexaPlatform,
    RemoteStep,
    RemotePipeline,
    RemoteSession,
    KodexaClient,
)
from .steps import (
    NodeTagCopy,
    NodeTagger,
    RollupTransformer,
    TextParser,
    KodexaProcessingException,
)
