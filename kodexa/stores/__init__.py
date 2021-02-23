"""
Stores are persistence components for Documents.  Typically, they can act as either a Connector or a Sink
"""
from .local import LocalDocumentStore, LocalModelStore, TableDataStore
from .stores import DataStoreHelper, RemoteDocumentStore, RemoteModelStore, RemoteTableDataStore
