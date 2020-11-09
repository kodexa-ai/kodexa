"""
Core Model
----------

The core model provides the object structure for Documents, ContentNodes and Features which is used as the foundation
for working with unstructured data in the framework.

Create a new instance of a Document, you will be required to provide a DocumentMetadata object

    >>> document = Document(DocumentMetadata())
"""
from .model import DocumentMetadata, ContentNode, ContentFeature, SourceMetadata, \
    Document, Store, DocumentStore, LocalModelStore, RemoteStore, ModelStore, RemoteModelStore
