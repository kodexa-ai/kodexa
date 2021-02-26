from kodexa import LocalDocumentStore
from kodexa.assistant.assistant import AssistantMetadata
from kodexa.testing import Document, ExtensionPackUtil


def test_basic_assistant():
    # In order to test an assistant we will basically need a LocalDocumentStore
    # The assistant will monitor this and so we will actually interact through the store to
    # see the processing

    extension_pack_util = ExtensionPackUtil("tests/kodexa-assistant.yml")
    lds = LocalDocumentStore('/tmp/assistant-lds', force_initialize=True)
    assistant_harness = extension_pack_util.get_assistant_test_harness("my-assistant", stores=[lds],
                                                                       assistant_metadata=AssistantMetadata(
                                                                           'test-assistant-1', 'My Test Assistant'))

    # OK - for our test our assistant is just going to try and run a pipeline to label something
    # we are keeping it very simple - note in the harness that everything is synchronous, in the Kodexa
    # Platform this will be async

    lds.put('cheesy-puff.txt', Document.from_text('Hello World'))

    # There should now be a document family at the path we pushed, and we should see that there are now
    # two documents related

    assert lds.get_family_by_path('missing') is None
    document_family = lds.get_family_by_path('cheesy-puff.txt')
    assert document_family.get_document_count() == 2
