import os

from kodexa import InMemoryDocumentSink, Pipeline, FolderConnector, registry, DocumentRender
from kodexa.steps.common import TextParser


def get_test_directory():
    return os.path.dirname(os.path.abspath(__file__)) + "/../test_documents/"

def get_text_layout_analysis(filename):
    document_sink = InMemoryDocumentSink()

    pipeline = Pipeline(FolderConnector(path=str(get_test_directory()), file_filter=filename + '.txt'))
    pipeline.add_step(TextParser())
    pipeline.set_sink(document_sink)
    pipeline.run()

    # Make sure the finders are available
    document = document_sink.get_document(0)
    registry.add_mixin_to_document("core", document)
    return document


def test_hello_txt():
    filename = 'hello'
    document = get_text_layout_analysis(filename)

    assert document.content_node.type == 'text'
    assert document.content_node.content == 'Hello World'
    DocumentRender(document).to_text()