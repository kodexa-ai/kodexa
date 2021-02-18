from typing import List

from kodexa import Assistant, AssistantContext, AssistantResponse, Pipeline
from kodexa.model.document_families import ContentEvent


class TestAction:
    """ """

    def __init__(self, cheese: str = None):
        self.cheese = cheese

    def get_name(self):
        """ """
        return "Hello"


class TestAssistant(Assistant):
    """ """

    def process_event(self, event: ContentEvent, context: AssistantContext = None) -> List[Pipeline]:
        """

        Args:
          event: ContentEvent: 
          context: AssistantContext:  (Default value = None)

        Returns:

        """
        # This is just an example of an assistant
        # basically we are just going to return a pipeline that
        # adds a label to the document - creating a new version

        pipeline = Pipeline()
        pipeline.add_label('hello')

        return AssistantResponse([pipeline])
