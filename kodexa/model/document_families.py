import uuid
from enum import Enum
from typing import List

from kodexa.model.model import ContentObject, ContentType, Document


class ContentEventType(Enum):
    NEW_OBJECT = 'NEW_OBJECT'
    DERIVED_DOCUMENT = 'DERIVED_DOCUMENT'


class ContentEvent:

    def __init__(self, content_object: ContentObject, event_type: ContentEventType, document_family):
        self.content_object = content_object
        self.event_type = event_type
        self.document_family: DocumentFamily = document_family


class DocumentRelationship:
    """
    A document relationship represents a link between two documents
    """

    def __init__(self, relationship_type, source_content_object_id, destination_content_object_id, actor=None):
        if actor is None:
            actor = {}
        self.relationship_type = relationship_type
        self.source_content_object_id = source_content_object_id
        self.destination_content_object_id = destination_content_object_id
        self.actor = actor


class DocumentFamily:
    """
    A document family represents a collection of related documents which together represent different views of the same
    source material

    This approach allows parsed representations to he linked to native, derived representations, labelled etc all to be
    part of a family of content views that can be used together to understand the document and its content
    """

    def __init__(self, path: str, store_ref: str):
        """
        Creates a new document family at the given path and optionally with the
        document as its first entry

        :param path: the path at which this document family exists (i.e. my-file.pdf)
        :param store_ref: the reference to the store holding this family
        """
        self.id: str = str(uuid.uuid4())
        self.relationships: List[DocumentRelationship] = []
        self.content_objects: List[ContentObject] = []
        self.path = path
        self.store_ref = store_ref

    def add_document(self, document: Document, relationship: DocumentRelationship = None) -> ContentEvent:
        new_content_object = ContentObject()
        new_content_object.store_ref = self.store_ref
        new_content_object.content_type = ContentType.DOCUMENT
        new_content_object.metadata = document.metadata
        new_content_object.labels = document.labels

        self.content_objects.append(new_content_object)

        if relationship is not None:
            relationship.destination_content_object_id = new_content_object.id
            self.relationships.append(relationship)

        new_event = ContentEvent(new_content_object, ContentEventType.NEW_OBJECT, self)
        return new_event

    def get_latest_content(self) -> ContentObject:
        """
        Returns the latest content object that we have in place

        :return:
        """
        return self.content_objects[-1]

    def get_content_objects(self) -> List[ContentObject]:
        """
        Returns all the content objects in the family

        :return: a list of the content objects
        """
        return self.content_objects

    def get_document_count(self) -> int:
        """
        Return the number of documents in the family

        :return: number of documents in the family
        """
        return len(self.content_objects)
