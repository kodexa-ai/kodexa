from kodexa.assistant.assistant import AssistantMetadata
from kodexa.testing import ExtensionPackUtil


def test_basic_assistant():
    # In order to test an assistant we will basically need a LocalDocumentStore
    # The assistant will monitor this and so we will actually interact through the store to
    # see the processing

    extension_pack_util = ExtensionPackUtil("tests/kodexa-assistant.yml")
    extension_pack_util.get_assistant_test_harness("my-assistant", stores=[],
                                                   assistant_metadata=AssistantMetadata(
                                                       'test-assistant-1', 'My Test Assistant'))
