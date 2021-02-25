"""
Provides the high-level classes and definition for an Assistant that can be implemented in Kodexa and run on an
instance of the Kodexa platform
"""

from kodexa.model import ContentEvent


class AssistantContext:
    """The Assistant Context provides a way to interact with additional services and capabilities
    while processing an event
    """

    def __init__(self, path_to_kodexa_metadata: str = 'kodexa.yml'):
        """
        Initialize the context based with a path to the kodexa file

        Args:
            path_to_kodexa_metadata (str): the path to the kodexa.yml (note it can also open a kodexa.json)
        """
        from kodexa.testing import ExtensionPackUtil
        self.extension_pack_util = ExtensionPackUtil(path_to_kodexa_metadata)

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


class AssistantResponse:
    """
    An assistant response allows you to provide the response from an assistant to a specific
    event.
    """

    def __init__(self, pipelines=None):
        """
        Initialize the response from the assistant

        Args:
            pipelines: zero or more pipelines that you want executed on the content object for which the
                       event was raised
        """
        if pipelines is None:
            pipelines = []
        self.pipelines = pipelines
        """The list of pipelines that you wish to have executed against the content object from the event"""


class Assistant:
    """An assistant is a rich-API to allow you to work with a reactive content store or with an end user
    that is working with set of content
    """

    def process_event(self, event: ContentEvent, context: AssistantContext = None) -> AssistantResponse:
        """The assistant will need to examine the event to determine if it wants to respond

        The event will focus on a specific content object (that will be stored and available).  Based on the
        metadata from the content object the assistant can then return a response which can include zero or more
        pipelines that it wishes to execute.

        This pipelines will be run asynchronously and the result of the pipelines might well
        return as another event for the assistant

        Args:
          event: the content event to react to
          context: the assistant context
          event: ContentEvent:
          context: AssistantContext:  (Default value = None)

        Returns:
          AssistantResponse: the response to the event

        """

        pass
