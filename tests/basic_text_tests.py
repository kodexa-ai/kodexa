import os

from kodexa import InMemoryDocumentSink, Pipeline, FolderConnector, Document
from kodexa.mixins import registry
from kodexa.steps.common import TextParser


def get_test_directory():
    return os.path.dirname(os.path.abspath(__file__)) + "/../test_documents/"


def get_test_pipeline(filename):
    document_sink = InMemoryDocumentSink()

    pipeline = Pipeline(FolderConnector(path=str(get_test_directory()), file_filter=filename + '.txt'))
    pipeline.add_step(TextParser(decode=True))
    pipeline.set_sink(document_sink)
    pipeline.run()

    # Make sure the finders are available
    document = document_sink.get_document(0)
    return document


def test_hello_txt():
    filename = 'hello'
    document = get_test_pipeline(filename)

    assert document.content_node.node_type == 'text'
    assert document.content_node.content == 'Hello World'


def test_text_find():
    document = Document.from_text('Hello world')
    nodes = document.content_node.findall(node_type_re='.*')

    assert len(nodes) == 1

    document = Document.from_text('Hello world')
    nodes = document.content_node.findall(content_re='.*')

    assert len(nodes) == 1
