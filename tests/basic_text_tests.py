import os

from kodexa import Pipeline, FolderConnector, LocalDocumentStore
from kodexa.steps.common import TextParser
from kodexa.testing.test_utils import compare_document


def get_test_directory():
    return os.path.dirname(os.path.abspath(__file__)) + "/../test_documents/"


def get_test_pipeline(filename):
    pipeline = Pipeline(FolderConnector(path=str(get_test_directory()), file_filter=filename + '.txt'))
    pipeline.add_step(TextParser())
    context = pipeline.run()

    # Make sure the finders are available
    document = context.output_document
    return document


def test_hello_txt():
    filename = 'hello'
    document = get_test_pipeline(filename)

    assert document.content_node.node_type == 'text'
    assert document.content_node.content == 'Hello World'

    compare_document(document, 'test_hello_txt.json')


def test_folder_connector_unpack_wildcard():
    document_sink = LocalDocumentStore()
    pipeline = Pipeline(
        FolderConnector(path=str(get_test_directory()) + 'folder_unpack_test', file_filter='*.*', unpack=True))
    pipeline.run()

    # let's make sure we properly unpacked each document and have all ContentNodes
    for document_family in document_sink.query_families():
        doc = document_sink.get_latest_document_in_family(document_family)
        if doc.get_root().get_all_content().find('HSBC') > -1:
            assert len(doc.select("//*")) == 39
        elif doc.get_root().get_all_content().find('flea') > -1:
            assert len(doc.select("//*")) == 6


def test_lines_of_text():
    # first test with all content being placed on root ContentNode
    pipeline = Pipeline.from_file(get_test_directory() + 'multiline_text.txt')
    pipeline.add_step(TextParser)
    context = pipeline.run()

    doc = context.output_document
    assert len(doc.get_root().get_children()) == 0
    assert len(doc.get_root().get_all_content()) > 0

    # next, test with all content being placed the root's children
    pipeline = Pipeline.from_file(get_test_directory() + 'multiline_text.txt')
    pipeline.add_step(TextParser(lines_as_child_nodes=True))
    context = pipeline.run()

    doc = context.output_document
    assert len(doc.get_root().get_children()) > 0
    assert doc.get_root().get_content() is None
