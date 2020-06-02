import os

from kodexa import selectors, Document


def get_test_directory():
    return os.path.dirname(os.path.abspath(__file__)) + "/../test_documents/"


def test_selector_1():
    document = Document.from_text("Hello World")
    results = document.content_node.select('.')
    assert len(results) == 1
    assert results[0].content == "Hello World"


def test_selector_2():
    document = Document.from_text("Hello World")
    results = document.content_node.select('*')
    assert len(results) == 1
    assert results[0].content == "Hello World"


def test_selector_regex():
    document = Document.from_text("Hello World")
    results = document.content_node.select('*[contentRegex("Hello.*")]')
    assert len(results) == 1
    assert results[0].content == "Hello World"

    results2 = document.content_node.select('*[contentRegex("Cheese.*")]')
    assert len(results2) == 0

    results = document.content_node.select('*[content()="Hello World"]')
    assert len(results) == 1
    assert results[0].content == "Hello World"

def test_selector_complex_doc_1():
    document = Document.from_msgpack(open(os.path.join(get_test_directory(), 'news.kdxa'), 'rb').read())
    all_nodes = document.content_node.select('//*')
    assert len(all_nodes) == 39

    all_ps = document.content_node.select('//p')
    assert len(all_ps) == 18


def test_tagged_content():
    document = Document.from_msgpack(open(os.path.join(get_test_directory(), 'news-tagged.kdxa'), 'rb').read())
    all_nodes = document.content_node.select('//*[hasTag("ORG")]')
    assert len(all_nodes) == 9

    union_nodes = document.content_node.select('//*[hasTag("ORG")] | //*[hasTag("ORG")]')
    assert len(union_nodes) == 18
