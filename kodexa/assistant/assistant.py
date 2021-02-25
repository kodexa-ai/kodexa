"""
Provides the high-level classes and definition for an Assistant that can be implemented in Kodexa and run on an
instance of the Kodexa platform
"""

from typing import List

from kodexa.model import ContentEvent
from kodexa.pipeline import Pipeline


class AssistantContext:
    """The Assistant Context provides a way to interact with additional services and capabilities
    while processing an event
    """

    def __init__(self, options=None):
        if options is None:
            options = {}
        self.options = options
        pass


class AssistantResponse:
    """
    An assistant response allows you to provide the response from an assistant to a specific
    event.
    """

    def __init__(self, pipelines: List[Pipeline]):
        """
        Initialize the response from the assistant

        Args:
            pipelines: zero or more pipelines that you want executed on the content object for which the
                       event was raised
        """
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
