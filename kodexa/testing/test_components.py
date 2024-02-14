import os

from kodexa import KodexaClient, KodexaPlatform
from kodexa.assistant import (
    Assistant,
    AssistantContext,
    AssistantResponse,
    AssistantPipeline,
)
from kodexa.model.objects import BaseEvent
from kodexa.pipeline import Pipeline


class TestAction:
    """ """

    def __init__(self, cheese: str = None):
        self.cheese = cheese


class TestAssistant(Assistant):
    """ """

    def process_event(
            self, event: BaseEvent, context: AssistantContext = None
    ) -> AssistantResponse:
        """

        Args:
          event: BaseEvent:
          context: AssistantContext:  (Default value = None)

        Returns:

        """
        # This is just an example of an assistant
        # basically we are just going to return a pipeline that
        # adds a label to the document - creating a new version

        pipeline = Pipeline()
        pipeline.add_label("hello")

        return AssistantResponse(
            pipelines=[AssistantPipeline(pipeline=pipeline, write_back_to_store=True)]
        )


def test_profile_default():
    """
    :assert: Checks if the default profile is set correctly
    """
    kodexa_url = os.getenv("URL")
    access_token = os.getenv("ACCESS_TOKEN")
    KodexaPlatform.configure(kodexa_url, access_token)
    assert KodexaPlatform.get_url() == kodexa_url and KodexaPlatform.get_access_token() == access_token


def test_profile_custom():
    """
    :assert: Checks if the custom profile is set correctly
    """
    kodexa_url = os.getenv("URL")
    access_token = os.getenv("ACCESS_TOKEN")
    profile = "dev-profile"
    KodexaPlatform.configure(kodexa_url, access_token, profile)
    assert KodexaPlatform.get_url(profile) == kodexa_url and KodexaPlatform.get_access_token(profile) == access_token


def test_kodexa_client_default_profile():
    kodexa_cli = KodexaClient()
    assert kodexa_cli.base_url == KodexaPlatform.get_url("default") and \
           kodexa_cli.access_token == KodexaPlatform.get_access_token("default")


def test_kodexa_client_custom_profile():
    kodexa_cli = KodexaClient(profile="dev-profile")
    assert kodexa_cli.base_url == KodexaPlatform.get_url("dev-profile") and \
           kodexa_cli.access_token == KodexaPlatform.get_access_token("dev-profile")


def test_customized_kodexe_client():
    kodexa_url = "https://test.test.com"
    access_token = "test-token"
    kodexa_cli = KodexaClient(kodexa_url, access_token)
    assert kodexa_cli.base_url != KodexaPlatform.get_url() and kodexa_cli.access_token != KodexaPlatform.get_access_token()
