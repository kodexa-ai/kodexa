from typing import List

from kodexa.model.document_families import ContentEvent
from kodexa.pipeline import Pipeline


class AssistantContext:
    """
    The Assistant Context provides a way to interact with additional services and capabilities
    while processing an event
    """
    pass


class Assistant:
    """
    An assistant is a rich-API to allow you to work with a reactive content store or with an end user
    that is working with set of content
    """

    def process_event(self, event: ContentEvent, context: AssistantContext = None) -> List[Pipeline]:
        """
        The assistant will need to examine the event to determine if it wants to respond

        The event will focus on a specific content object (that will be stored and available).  Based on the
        metadata from the content object the assistant can then return one or more pipelines that it wishes
        to execute.

        This pipelines will be run asynchronously and the result of the pipelines might well
        return as another event for the assistant

        :param event: the content event to react to
        :param context: the assistant context
        :return: a list of pipelines that you wish to execute
        """

        pass
