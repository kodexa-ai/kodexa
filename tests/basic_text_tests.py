import os

from kodexa import InMemoryDocumentSink, Pipeline, FolderConnector, Document, FolderSink
from kodexa.steps.common import TextParser
from kodexa.testing.test_utils import compare_document


def get_test_directory():
    return os.path.dirname(os.path.abspath(__file__)) + "/../test_documents/"


def get_test_pipeline(filename):
    document_sink = InMemoryDocumentSink()

    pipeline = Pipeline(FolderConnector(path=str(get_test_directory()), file_filter=filename + '.txt'))
    pipeline.add_step(TextParser())
    pipeline.set_sink(document_sink)
    pipeline.run()

    # Make sure the finders are available
    document = document_sink.get_document(0)
    return document


def test_folder_sink_from_file():

    if os.path.exists('/tmp/hello.txt.kdxa'):
        os.remove('/tmp/hello.txt.kdxa')

    pipeline = Pipeline(FolderConnector(path=str(get_test_directory()), file_filter='hello.txt'))
    pipeline.add_step(TextParser())
    pipeline.set_sink(FolderSink('/tmp'))
    pipeline.run()

    assert os.path.exists('/tmp/hello.txt.kdxa') is True


def test_caching():

    if os.path.exists('/tmp/hello.txt.kdxa'):
        os.remove('/tmp/hello.txt.kdxa')

    pipeline = Pipeline(FolderConnector(path=str(get_test_directory()), file_filter='hello.txt'))
    pipeline.add_step(TextParser(), cache_path="/tmp")
    pipeline.set_sink(FolderSink('/tmp'))
    pipeline.run()

    assert os.path.exists('/tmp/hello.txt.kdxa') is True

    os.remove('/tmp/hello.txt.kdxa')


def test_hello_txt():
    filename = 'hello'
    document = get_test_pipeline(filename)

    assert document.content_node.node_type == 'text'
    assert document.content_node.content == 'Hello World'

    compare_document(document, 'test_hello_txt.json')


def test_text_find():
    document = Document.from_text('Hello world')
    nodes = document.content_node.findall(node_type_re='.*')

    assert len(nodes) == 1

    document = Document.from_text('Hello world')
    nodes = document.content_node.findall(content_re='.*')

    assert len(nodes) == 1

    compare_document(document, 'test_text_find.json')


def test_folder_connector_unpack_wildcard():

    document_sink = InMemoryDocumentSink()
    pipeline = Pipeline(FolderConnector(path=str(get_test_directory()) + 'folder_unpack_test', file_filter='*.*', unpack=True))
    pipeline.set_sink(document_sink)
    pipeline.run()

    # let's make sure we properly unpacked each document and have all ContentNodes
    for doc in document_sink.documents:
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
    assert len(doc.get_root().children) == 0
    assert len(doc.get_root().get_all_content()) > 0


    # next, test with all content being placed the root's children
    pipeline = Pipeline.from_file(get_test_directory() + 'multiline_text.txt')
    pipeline.add_step(TextParser(lines_as_child_nodes=True))
    context = pipeline.run()

    doc = context.output_document
    assert len(doc.get_root().children) > 0
    assert doc.get_root().get_content() == None

