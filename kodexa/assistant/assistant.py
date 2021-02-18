"""
Provides the high-level classes and definition for an Assistant that can be implemented in Kodexa and run on an
instance of the Kodexa platform
"""


from typing import List

from kodexa.model.document_families import ContentEvent
from kodexa.pipeline import Pipeline


class AssistantContext:
    """The Assistant Context provides a way to interact with additional services and capabilities
    while processing an event

    Args:

    Returns:

    """
    pass


class Assistant:
    """An assistant is a rich-API to allow you to work with a reactive content store or with an end user
    that is working with set of content

    Args:

    Returns:

    """

    def process_event(self, event: ContentEvent, context: AssistantContext = None) -> List[Pipeline]:
        """The assistant will need to examine the event to determine if it wants to respond
        
        The event will focus on a specific content object (that will be stored and available).  Based on the
        metadata from the content object the assistant can then return one or more pipelines that it wishes
        to execute.
        
        This pipelines will be run asynchronously and the result of the pipelines might well
        return as another event for the assistant

        Args:
          event: the content event to react to
          context: the assistant context
          event: ContentEvent: 
          context: AssistantContext:  (Default value = None)

        Returns:
          a list of pipelines that you wish to execute

        """

        pass
