"""
Connectors provide a way to access document (files or otherwise) from a source, and they form the starting point
for Pipelines
"""
from .connectors import (
    FolderConnector,
    FileHandleConnector,
    UrlConnector,
    registered_connectors,
    get_connectors,
    get_connector,
    add_connector,
    get_source,
)
