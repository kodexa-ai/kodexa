"""
Stores
------

Stores are persistence components for Documents.  Typically, they can act as either a Connector or a Sink
"""
from .stores import JsonDocumentStore, TableDataStore, DictDataStore, DataStoreHelper, LocalDocumentStore, \
    RemoteDocumentStore, RemoteDictDataStore, RemoteTableDataStore, RemoteModelStore, LocalModelStore
