"""
Kodexa is a Python framework to enable flexible data engineering with semi-structured and unstructured documents and
data.


.. include:: ./documentation.md
"""
from .assistant import Assistant, AssistantContext, AssistantResponse
from .connectors import FileHandleConnector, FolderConnector, UrlConnector, add_connector, get_connector, \
    get_connectors, get_source, registered_connectors
from .model import ContentEvent, ContentFeature, ContentNode, Document, DocumentActor, DocumentFamily, DocumentMetadata, \
    DocumentStore, DocumentTransition, SourceMetadata, TransitionType
from .model.objects import Taxonomy
from .pipeline import Pipeline, PipelineContext, PipelineStatistics
from .platform import KodexaPlatform, RemoteStep, RemotePipeline, RemoteSession, KodexaClient
from .steps import NodeTagCopy, NodeTagger, RollupTransformer, TagsToKeyValuePairExtractor, TextParser, \
    KodexaProcessingException
from .stores import LocalDocumentStore, LocalModelStore, RemoteDocumentStore, \
    RemoteModelStore, RemoteDataStore, TableDataStore
