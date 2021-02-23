"""
Model represents the core model at the heart of the Kodexa Content Model and architecture.

It allows you to define:

* Documents
* Pipelines
* Steps

and much more....

Document families allow the organization of documents based on transitions and actors
"""
from .model import ContentEvent, ContentFeature, ContentNode, ContentObject, ContentType, Document, DocumentActor, \
    DocumentFamily, DocumentMetadata, DocumentStore, DocumentTransition, ModelStore, RemoteStore, SourceMetadata, Store, \
    TransitionType
