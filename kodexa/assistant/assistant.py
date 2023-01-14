"""
Provides the high-level classes and definition for an Assistant that can be implemented in Kodexa and run on an
instance of the Kodexa platform
"""
from typing import List, Optional

from kodexa.model import ContentObject, Document
from kodexa.model.objects import Store, Taxonomy, BaseEvent
from kodexa.platform.client import DocumentStoreEndpoint


class AssistantMetadata:
    """
    A set of metadata for the assistant that can be made available on from the context
    """

    def __init__(self, assistant_id: str, assistant_name: str, project_id: Optional[str] = None):
        self.assistant_id = assistant_id
        """The ID of the assistant"""
        self.assistant_name = assistant_name
        """The name of the assistant"""
        self.project_id = project_id
        """The ID of the project that the assistant is owned by"""


class AssistantPipeline:
    """
    The wrapper for a pipeline that they assistant will request to be executed
    """

    def __init__(self, pipeline, description=None, write_back_to_store: bool = False,
                 data_store: Optional[Store] = None,
                 taxonomies: Optional[List[Taxonomy]] = None, labels_to_apply: Optional[List[str]] = None):
        self.pipeline = pipeline
        """The pipeline to execute"""
        self.description = description
        """Optional description for the pipeline"""
        self.write_back_to_store = write_back_to_store
        """Should the document be written back to the store from which it was read"""
        self.data_store = data_store
        """Optionally the datastore that we want to extract the labelled content to"""
        self.taxonomies = taxonomies
        """Optionally a list of the taxonomies to use when extracting the labels"""
        self.labels_to_apply = labels_to_apply
        """Optionally a list of the labels to apply to the document when complete"""


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

    def __init__(self, pipelines: List[AssistantPipeline] = None, text: Optional[str] = None,
                 output_document: Document = None, enabled_logging=False):
        """
        Initialize the response from the assistant

        Args:
            pipelines: zero or more pipelines that you want executed on the content object for which the
                       event was raised
            text: the to be presented with the response
            enabled_logging: should logging be enabled for this response
            output_document: the output document, if the assistant has created a document directly
        """
        if pipelines is None:
            pipelines = []

        self.pipelines = pipelines
        """The list of pipelines that you wish to have executed against the content object from the event"""

        self.text = text
        """The text that will be provided back to the user from the assistant"""

        self.output_document = output_document
        """The output document, if the assistant has directly created one"""

        self.enabled_logging = enabled_logging
        """Should logging be enabled for this response"""


class AssistantContext:
    """The Assistant Context provides a way to interact with additional services and capabilities
    while processing an event
    """

    from kodexa.model import ContentEvent

    def __init__(self, metadata: AssistantMetadata, path_to_kodexa_metadata: str = 'kodexa.yml',
                 stores=None, content_provider=None, extension_pack_util=None):
        """
        Initialize the context based with a path to the kodexa file

        Args:
            metadata (AssistantMetadata): metadata for the assistant being setup in context
            path_to_kodexa_metadata (str): the path to the kodexa.yml (note it can also open a kodexa.json)
            stores: A list of the stores that are available to the assistant (note these are local stores usually)
            content_provider: the content provider will have a get/put content method to allow interaction with caches
            extension_pack_util: If you provide the extension pack util we will ignore the path_to_kodexa_metadata and
                                 use this
        """
        if stores is None:
            stores = []
        from kodexa.testing import ExtensionPackUtil
        if extension_pack_util is None:
            self.extension_pack_util = ExtensionPackUtil(path_to_kodexa_metadata)
        else:
            self.extension_pack_util = extension_pack_util
        self.metadata: AssistantMetadata = metadata
        self.stores = stores
        self.content_provider = content_provider

    def get_content(self, content_object: ContentObject):
        """
        Puts a content object using the content provider

        :param content_object: Content Object to put
        """
        if self.content_provider:
            self.content_provider.get_content(content_object)

    def put_content(self, content_object: ContentObject, content):
        """
        Puts the content object and its content based through the content provider

        :param content_object: The content object
        :param content: the content
        """
        if self.content_provider:
            self.content_provider.put_content(content_object, content)

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

    def get_store(self, event: ContentEvent) -> DocumentStoreEndpoint:
        """
        Get a document store for the event (based on the document family ID)

        Args:
          event: ContentEvent:

        Returns:
          The instance of the document store
        """
        for store in self.stores:
            if event.document_family.store_ref == store.ref:
                return store

        if event.document_family.store_ref is not None:
            from kodexa import KodexaClient
            return KodexaClient().get_object_by_ref('store', event.document_family.store_ref)

        raise Exception(f"Unable to get store ref {event.document_family.store_ref}")


class Assistant:
    """An assistant is a rich-API to allow you to work with a reactive content store or with an end user
    that is working with set of content
    """

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