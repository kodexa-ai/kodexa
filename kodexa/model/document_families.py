"""
Provides the implementation of a content event and document family
"""

import uuid
from enum import Enum
from typing import List, Optional

from kodexa.model.model import ContentObject, ContentType, Document


class TransitionType(Enum):
    """
    The type of transition
    """
    DERIVED = 'DERIVED'
    """A transition that derived a new document"""
    FRAGMENT = 'FRAGMENT'
    """A transition that placed a fragment of the document in another document"""


class ContentEventType(Enum):
    """
    The type of event that occurred on the content
    """
    NEW_OBJECT = 'NEW_OBJECT'
    DERIVED_DOCUMENT = 'DERIVED_DOCUMENT'


class ContentEvent:
    """A content event represents a change, update or deletion that has occurred in a document family
    in a store, and can be relayed for a reaction
    """

    def __init__(self, content_object: ContentObject, event_type: ContentEventType, document_family):
        """
        Initialize a content event
        Args:
            content_object: the content object on which the event occurred
            event_type: the type of event
            document_family: the document family to which the object belongs
        """
        self.content_object = content_object
        """The content object that raised the event"""
        self.event_type = event_type
        """The event type"""
        self.document_family: DocumentFamily = document_family
        """The document family containing the content object"""


class DocumentActor:
    """A document actor is something that can create a new document in a family and is
    part of the document transition
    """

    def __init__(self, actor_id: str, actor_type: str):
        """
        Initialize a document actor

        Args:
            actor_id: the ID of the actor (this typically has meaning within the scope of the actor type)
            actor_type: the type of actor
        """
        self.actor_id = actor_id
        """The ID of the actor (based on the type)"""
        self.actor_type = actor_type
        """The type of actor"""


class DocumentTransition:
    """
    A document transition represents a link between two documents and tries to capture the actor that was involved
    in the transition as well at the type of transition that exists
    """

    def __init__(self, transition_type: TransitionType, source_content_object_id: str,
                 destination_content_object_id: Optional[str] = None,
                 actor: Optional[DocumentActor] = None):
        """
        Create a document transition

        Args:
            transition_type:TransitionType: the type of transition
            source_content_object_id:str: the ID of the source content object
            destination_content_object_id:Optional[str] the ID of the destination content object
            actor:Optional[DocumentActor]: the actor (Defaults to None)
        """
        self.transition_type = transition_type
        """The type of transition"""
        self.source_content_object_id = source_content_object_id
        """The ID of the source content object"""
        self.destination_content_object_id = destination_content_object_id
        """The ID of the destination content object"""
        self.actor = actor
        """The actor in the transition"""

    @classmethod
    def from_dict(cls, transition_dict):
        """
        Converts a dictionary from a REST call back into a DocumentTransition
        Args:
            transition_dict: Dictionary

        Returns: A document transition

        """
        transition = DocumentTransition(transition_dict['transitionType'], transition_dict['sourceContentObjectId'],
                                        transition_dict['destinationContentObjectId'])
        return transition


class DocumentFamily:
    """A document family represents a collection of related documents which together represent different views of the same
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
        self.transitions: List[DocumentTransition] = []
        self.content_objects: List[ContentObject] = []
        self.path = path
        self.store_ref = store_ref

    def add_document(self, document: Document, transition: Optional[DocumentTransition] = None) -> ContentEvent:
        """

        Args:
          document: Document:
          transition: DocumentTransition:  (Default value = None)

        Returns:

        """
        new_content_object = ContentObject()
        new_content_object.store_ref = self.store_ref
        new_content_object.content_type = ContentType.DOCUMENT
        new_content_object.metadata = document.metadata
        new_content_object.labels = document.labels

        self.content_objects.append(new_content_object)

        if transition is not None:
            transition.destination_content_object_id = new_content_object.id
            self.transitions.append(transition)

        new_event = ContentEvent(new_content_object, ContentEventType.NEW_OBJECT, self)
        return new_event

    def get_latest_content(self) -> ContentObject:
        """Returns the latest content object that we have in place

        Returns:
            The latest content object in the family
        """
        return self.content_objects[-1]

    def get_content_objects(self) -> List[ContentObject]:
        """Returns all the content objects in the family

        Returns:
            a list of the content objects


        """
        return self.content_objects

    def get_document_count(self) -> int:
        """
        Count of content objects in the family

        Returns:
          number of documents in the family

        """
        return len(self.content_objects)

    @classmethod
    def from_dict(cls, family_dict: dict):
        """
        Convert a dictionary from a REST call into the Document Family

        Args:
            param: the document family object as a dictionary

        Returns:
            An instance of the document family
        """
        document_family = DocumentFamily(family_dict['path'], family_dict['storeRef'])
        document_family.id = family_dict['id']
        document_family.content_objects = []
        for co_dict in family_dict['contentObjects']:
            document_family.content_objects.append(ContentObject.from_dict(co_dict))
        for transition_dict in family_dict['documentTransitions']:
            document_family.transitions.append(DocumentTransition.from_dict(transition_dict))
        return document_family
