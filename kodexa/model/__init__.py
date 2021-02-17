"""
Model represents the core model at the heart of the Kodexa Content Model and architecture.

It allows you to define:

* Documents
* Pipelines
* Steps

and much more....

Document families allow the organization of documents based on relationships and actors
"""
from .document_families import DocumentRelationship, DocumentFamily
from .model import DocumentMetadata, ContentNode, ContentFeature, SourceMetadata, \
    Document, Store, DocumentStore, RemoteStore, ModelStore, ContentObject, ContentType
