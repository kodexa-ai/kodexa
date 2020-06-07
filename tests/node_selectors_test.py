import os

from kodexa import selectors, Document, Pipeline, NodeTagger


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


def test_tag_regex():
    document = Document.from_text("Hello World")
    results = document.content_node.select('*[typeRegex("te.*")]')
    assert len(results) == 1
    assert results[0].content == "Hello World"
    results2 = document.content_node.select('*[typeRegex("chee.*")]')
    assert len(results2) == 0


def test_selector_regex():
    document = Document.from_text("Hello World")

    results = document.select('hasTag() = false()')
    assert len(results) == 1

    results = document.select('hasTag()')
    assert len(results) == 0

    results = document.content_node.select('.')
    assert len(results) == 1
    assert results[0].content == "Hello World"

    results = document.content_node.select('*[contentRegex("Hello.*")]')
    assert len(results) == 1
    assert results[0].content == "Hello World"

    results2 = document.content_node.select('*[contentRegex("Cheese.*")]')
    assert len(results2) == 0

    results = document.content_node.select('*[content()="Hello World"]')
    assert len(results) == 1
    assert results[0].content == "Hello World"


def test_selector_operators():
    document = Document.from_text("Hello World")

    # combining multiple functions

    # Feeling crazy?
    assert len(document.content_node.select('//*[typeRegex("te.*") and contentRegex("H.*D")]')) == 0
    # no dice - handle your capitalization correctly! :-)

    assert len(document.content_node.select('//*[typeRegex("te.*") or contentRegex("H.*D")]')) == 1

    # This should obviously return zero nodes, as 'Howdy' isn't in the document
    assert len(document.content_node.select('//*[typeRegex("te.*") and contentRegex("Howdy")]')) == 0

    # What about this?  There's an H and a W...
    assert len(document.content_node.select('//*[typeRegex("te.*") and contentRegex("H*W")]')) == 0

    # Try that again, but modify the contentRegex
    assert len(document.content_node.select('//*[typeRegex("te.*") and contentRegex("H.*W")]')) == 1
    # yea!

    # Another variation - we expect success
    assert len(document.content_node.select('//*[typeRegex("te.*") and contentRegex("H.*d")]')) == 1
    # ...and we're rewarded


def test_selector_complex_doc_1():
    document = Document.from_msgpack(open(os.path.join(get_test_directory(), 'news.kdxa'), 'rb').read())
    all_nodes = document.content_node.select('//*')
    assert len(all_nodes) == 39

    all_ps = document.content_node.select('//p')
    assert len(all_ps) == 18


def test_tagged_content():
    document = Document.from_msgpack(open(os.path.join(get_test_directory(), 'news-tagged.kdxa'), 'rb').read())

    all_nodes = document.content_node.select('//*[hasTag($entityName)]', {"entityName": "ORG"})
    assert len(all_nodes) == 9

    all_nodes = document.content_node.select('//p stream *[hasTag("ORG")] stream *[hasTag("ORG")]')
    assert len(all_nodes) == 7

    all_nodes = document.content_node.select('//p intersect //*[hasTag("ORG")]')
    assert len(all_nodes) == 7

    # Has any tag to start
    tagged_nodes = document.content_node.select('//*[hasTag()]')
    assert len(tagged_nodes) == 22

    feature_nodes = document.content_node.select('//*[hasFeature()]')
    assert len(feature_nodes) == 32

    all_nodes = document.content_node.select('//*[hasTag("ORG")]')
    assert len(all_nodes) == 9

    union_nodes = document.content_node.select('//*[hasTag("ORG")] | //*[hasTag("ORG")]')
    assert len(union_nodes) == 18

    node_match = all_nodes[0].select('*[tagRegex("O.*")]')
    assert len(node_match) == 1

    node_match2 = all_nodes[0].select('*[tagRegex("CHE.*")]')
    assert len(node_match2) == 0


def test_instance_indexes():
    document = Document.from_msgpack(open(os.path.join(get_test_directory(), 'news-tagged.kdxa'), 'rb').read())
    first_paragraph = document.select('(//p)[0]')
    assert len(first_paragraph) == 1

    # Note this is important - the index here is not the position in the results
    # but the index of the node itself
    first_paragraph = document.select('//p[0]')
    assert len(first_paragraph) == 18


def test_spatial_doc_sample_one():
    document = Document.from_kdxa(get_test_directory() + 'before_fail.kdxa')
    nodes = document.select('//page[contentRegex("line.*",true)]')
    assert len(nodes) == 18


def test_spatial_doc_sample_two():
    # This test document and this portion of code is a snippet
    # from a test in the spatial actions tests.  Adding this saved doc
    # and this section to ensure NodeTagger is tested.
    page_footer_re = r'Page \d+ of \d+$'
    pipeline = Pipeline(Document.from_kdxa(get_test_directory() + 'before_fail.kdxa'))

    pipeline.add_step(
        NodeTagger(selector='//*[typeRegex("line.*")]', content_re=page_footer_re, tag_to_apply='page_footer'))
    pipeline.run()

    doc = pipeline.context.output_document

    assert doc.get_root() is not None
