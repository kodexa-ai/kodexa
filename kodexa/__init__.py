"""
    Kodexa is a Python framework to enable flexible data engineering with semi-structured and unstructured documents and
    data.
"""
from .cloud import RemoteSession, RemotePipeline, RemoteAction, KodexaPlatform
from .connectors import FolderConnector, FileHandleConnector, UrlConnector, registered_connectors, get_connectors, \
    get_connector, add_connector, get_source
from .extractors import *
from .model import DocumentMetadata, ContentNode, ContentFeature, SourceMetadata, \
    Document, LocalModelStore, RemoteStore, RemoteModelStore, DocumentStore
from .pipeline import Pipeline, PipelineStatistics, PipelineContext
from .sinks import InMemoryDocumentSink, FolderSink
from .steps import NodeTagger, TextParser, RollupTransformer, TagsToKeyValuePairExtractor
from .stores import JsonDocumentStore, TableDataStore, DictDataStore, DataStoreHelper, LocalDocumentStore, \
    RemoteDocumentStore
