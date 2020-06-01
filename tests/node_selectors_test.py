import os

from kodexa import selectors, Document
from kodexa.selectors.engine import Selector


def get_test_directory():
    return os.path.dirname(os.path.abspath(__file__)) + "/../test_documents/"


def test_selector_1():
    document = Document.from_text("Hello World")
    selector = Selector('.')
    results = selector.execute(document.content_node)
    assert len(results) == 1
    assert results[0].content == "Hello World"


def test_selector_2():
    document = Document.from_text("Hello World")
    selector = Selector('*')
    results = selector.execute(document.content_node)
    assert len(results) == 1
    assert results[0].content == "Hello World"


def test_selector_complex_doc_1():
    document = Document.from_msgpack(open(os.path.join(get_test_directory(), 'news.kdxa'), 'rb').read())
    all_nodes = Selector('//*').execute(document.content_node)
    assert len(all_nodes) == 39

    all_ps = Selector('//p').execute(document.content_node)
    assert len(all_ps) == 18


def test_tagged_content():
    document = Document.from_msgpack(open(os.path.join(get_test_directory(), 'news-tagged.kdxa'), 'rb').read())
    all_nodes = Selector('//*[tag:ORG]').execute(document.content_node)
    assert len(all_nodes) == 8
