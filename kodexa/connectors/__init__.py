"""
Connectors
----------

Connectors provide a way to access document (files or otherwise) from a source, and they form the starting point
for Pipelines
"""
from .connectors import add_connector, get_connector, get_connectors, get_source, FileHandleConnector, FolderConnector
