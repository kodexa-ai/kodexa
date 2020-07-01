from kodexa.model import DocumentMetadata, Document


def get_test_document():
    document = Document(DocumentMetadata())
    node = document.create_node(type='foo')
    node.content = "cheese"
    document.content_node = node

    document.content_node.add_child(document.create_node(type='bar', content='fishstick'))
    return document


def get_test_document_with_three_children():
    document = Document(DocumentMetadata())
    node = document.create_node(type='foo')
    node.content = "cheese"
    document.content_node = node

    document.content_node.add_child(document.create_node(type='bar', content='fishstick'))
    document.content_node.add_child(document.create_node(type='bar', content='cheeseburger'))
    document.content_node.add_child(document.create_node(type='bar', content='beans'))

    return document


def test_get_nodes_between():
    document = get_test_document_with_three_children()
    document.add_mixin("core")

    nodes = document.content_node.children[0].collect_nodes_to(document.content_node.children[2])
    assert len(nodes) == 2


def test_tag_nodes_between():
    document = get_test_document_with_three_children()
    document.add_mixin("core")

    document.content_node.children[0].tag_nodes_to(document.content_node.children[2], 'test-tag')
    assert len(document.content_node.findall(tag_name_re='test-tag')) == 2


def test_basic_document_with_content_node():
    document = get_test_document()
    print(document.to_json())
    assert document.to_json() is not None


def test_finder():
    document = get_test_document()
    document.add_mixin("core")
    node = document.get_root().find(type_re="bar")
    assert node.type == 'bar'


def test_navigation():
    document = get_test_document()

    document.add_mixin('core')

    document.content_node.add_child(document.create_node(type='bar', content='cheeseburger'))
    document.content_node.add_child(document.create_node(type='bar', content='lemon'))

    assert document.content_node.children[0].next_node().content == 'cheeseburger'
    assert document.content_node.children[2].previous_node().content == 'cheeseburger'
    pass


def test_virtual_navigation_with_no_0_index():
    document = Document(DocumentMetadata())
    document.add_mixin('core')
    node = document.create_node(type='loopy')
    node.content = "banana"
    document.content_node = node

    document.content_node.add_child(document.create_node(type='loopy', content='banana2'), index=2)

    assert document.content_node.get_node_at_index(0).content is None
    assert document.content_node.get_node_at_index(0).next_node().content is None
    assert document.content_node.get_node_at_index(0).next_node().next_node().content is 'banana2'


def test_virtual_navigation():
    document = get_test_document()
    document.content_node.add_child(document.create_node(type='bar', content='cheeseburger'), index=2)
    document.content_node.add_child(document.create_node(type='bar', content='lemon'), index=5)

    document.add_mixin('navigation')

    assert document.content_node.get_node_at_index(0).content is "fishstick"

    assert document.content_node.children[0].next_node().content is None
    assert document.content_node.children[0].next_node().next_node().next_node().index is 3
    assert document.content_node.children[0].next_node().next_node().next_node().next_node().index is 4
    assert document.content_node.children[0].next_node().next_node().next_node().next_node().next_node().index is 5
    assert document.content_node.children[
               0].next_node().next_node().next_node().next_node().next_node().next_node() is None

    assert document.content_node.children[0].next_node().next_node().content is 'cheeseburger'


def test_feature_find():
    document = get_test_document()
    document.content_node.add_child(document.create_node(type='bar', content='cheeseburger'), index=2)
    document.content_node.add_child(document.create_node(type='bar', content='lemon'), index=5)

    document.add_mixin('core')

    document.content_node.children[0].add_feature('test', 'test', 'cheese')
    document.content_node.children[1].add_feature('test', 'test', 'fishstick')

    assert document.get_root().find_with_feature_value('test', 'test', 'cheese') is not None

    assert document.get_root().children[1].get_all_content() == 'cheeseburger'


def test_finder_and_tag():
    document = get_test_document()
    document.add_mixin("core")
    node = document.get_root().find(type_re="bar")
    assert node.type == "bar"

    node = document.get_root().find(type_re="bar")
    node.tag("sticky", content_re="fish(.*)")
    print(node.to_json())
    assert len(node.get_tags()) == 1

    node.tag("sticky2")
    print(node.to_json())
    assert len(node.get_tags()) == 2
    node.remove_tag("sticky2")
    assert len(node.get_tags()) == 1


def test_basic_spatial_serialization():
    document = get_test_document()
    document.add_mixin('spatial')
    document.content_node.set_bbox([1, 1, 1, 1])

    print(document.content_node.get_bbox())
    assert document.content_node.get_bbox() == [1, 1, 1, 1]

    document = document.from_json(document.to_json())
    print(document.content_node.get_bbox())

    assert document.content_node.get_bbox() == [1, 1, 1, 1]


def test_document_uuid():
    doc_1 = Document.from_text('The sun is very bright today.')
    doc_2 = Document.from_text('Fluffy clouds float through the sky.')
    assert doc_1.uuid != doc_2.uuid
