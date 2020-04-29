"""
Stores
------

Stores are persistence components for Documents,  typically they can act as either a Connector or a Sink
"""
from .stores import JsonDocumentStore, TableDataStore, DictDataStore, DataStoreHelper
