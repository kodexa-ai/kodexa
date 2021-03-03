"""
Provides the high-level classes and definition for an Assistant that can be implemented in Kodexa and run on an
instance of the Kodexa platform
"""
from typing import List, Optional


class AssistantMetadata:
    """
    A set of metadata for the assistant that can be made available on from the context
    """

    def __init__(self, assistant_id: str, assistant_name: str):
        self.assistant_id = assistant_id
        """The ID of the assistant"""
        self.assistant_name = assistant_name
        """The name of the assistant"""


class AssistantContext:
    """The Assistant Context provides a way to interact with additional services and capabilities
    while processing an event
    """

    from kodexa.model.model import ContentEvent, DocumentStore

    def __init__(self, metadata: AssistantMetadata, path_to_kodexa_metadata: str = 'kodexa.yml',
                 stores: List[DocumentStore] = []):
        """
        Initialize the context based with a path to the kodexa file

        Args:
            metadata (AssistantMetadata): metadata for the assistant being setup in context
            path_to_kodexa_metadata (str): the path to the kodexa.yml (note it can also open a kodexa.json)
            stores: A list of the stores that are available to the assistant (note these are local stores usually)
        """
        from kodexa.testing import ExtensionPackUtil
        self.extension_pack_util = ExtensionPackUtil(path_to_kodexa_metadata)
        self.metadata: AssistantMetadata = metadata
        self.stores = stores

    def get_step(self, step: str, options=None):
        """
        Returns an instance of a step that is packaged in the same extension pack as the
        assistant, this allows you to build pipelines when you don't know the owning organization

        Args:
            step (str): The step name (ie. pdf-parser)
            options: A dictionary of the options to create the step

        Returns:
            The step

        """
        if options is None:
            options = {}
        return self.extension_pack_util.get_step(step, options)

    def get_store(self, event: ContentEvent) -> DocumentStore:
        """
        Get a document store for the event (based on the document family ID)

        Args:
          event: ContentEvent:

        Returns:
          The instance of the document store
        """
        for store in self.stores:
            if event.document_family.store_ref == store.get_ref():
                return store

        if event.document_family.store_ref is not None:
            from kodexa import RemoteDocumentStore
            return RemoteDocumentStore(event.document_family.store_ref)

        raise Exception(f"Unable to get store ref {event.document_family.store_ref}")


class AssistantPipeline:

    def __init__(self, pipeline, description=None, write_back_to_store: bool = False):
        self.pipeline = pipeline
        self.description = description
        self.write_back_to_store = write_back_to_store


class AssistantIntent:
    """
    The representation of an available intention from the assistant
    """

    def __init__(self, intent_id: str, text: str):
        self.intent_id = intent_id
        """The ID of the intention"""
        self.text = text
        """Text description of the intention"""


class AssistantResponse:
    """
    An assistant response allows you to provide the response from an assistant to a specific
    event.
    """

    def __init__(self, pipelines: List[AssistantPipeline] = None, text: Optional[str] = None, available_intents=None):
        """
        Initialize the response from the assistant

        Args:
            pipelines: zero or more pipelines that you want executed on the content object for which the
                       event was raised
            text: the to be presented with the response
            available_intents: a list of the available intents that you can return for this document
        """
        if available_intents is None:
            available_intents = []
        if pipelines is None:
            pipelines = []

        self.pipelines = pipelines
        """The list of pipelines that you wish to have executed against the content object from the event"""

        self.text = text
        """The text that will be provided back to the user from the assistant"""

        self.available_intents = available_intents
        """Any available intentions that the assistant will further respond to"""


class Assistant:
    """An assistant is a rich-API to allow you to work with a reactive content store or with an end user
    that is working with set of content
    """

    from kodexa.model.model import BaseEvent

    def process_event(self, event: BaseEvent, context: AssistantContext) -> AssistantResponse:
        """The assistant will need to examine the event to determine if it wants to respond

        The event will focus on a specific content object (that will be stored and available).  Based on the
        metadata from the content object the assistant can then return a response which can include zero or more
        pipelines that it wishes to execute.

        This pipelines will be run asynchronously and the result of the pipelines might well
        return as another event for the assistant

        Args:
          event: BaseEvent: the event being provided to the assistant
          context: AssistantContext:  the context for the assistant

        Returns:
          AssistantResponse: the response to the event

        """

        pass
