import os

from kodexa import get_source
from kodexa.model import DocumentMetadata, Document
from kodexa.model.model import ProcessingStep
from kodexa.testing.test_utils import compare_document


def get_test_directory():
    return os.path.dirname(os.path.abspath(__file__)) + "/../test_documents/"


def get_test_document():
    document = Document(DocumentMetadata())
    node = document.create_node(node_type='foo')
    node.content = "cheese"
    document.content_node = node

    document.content_node.add_child(document.create_node(node_type='bar', content='fishstick'))
    return document


def get_test_document_with_three_children():
    document = Document(DocumentMetadata())
    node = document.create_node(node_type='foo')
    node.content = "cheese"
    document.content_node = node

    document.content_node.add_child(document.create_node(node_type='bar', content='fishstick'))
    document.content_node.add_child(document.create_node(node_type='bar', content='cheeseburger'))
    document.content_node.add_child(document.create_node(node_type='bar', content='beans'))

    return document


def test_get_nodes_between():
    document = get_test_document_with_three_children()

    nodes = document.content_node.get_children()[0].collect_nodes_to(document.content_node.get_children()[2])
    assert len(nodes) == 2



def test_external_data_for_existing_document():
    document = Document.from_kddb("test_documents/bank-statement.kddb")

    document.set_external_data({"cheese": "foo"}, "new")
    document.set_external_data({"cheese": "bar"}, "new")
    assert document.get_external_data("new")["cheese"] == "bar"
    assert document.get_external_data() is not None
    assert document.get_external_data() == {}
    assert document.get_external_data_keys() == ["default", "new"]
    print(document.get_external_data())



def test_external_data():
    document = Document()

    document.set_external_data({"cheese": "bar"})
    assert document.get_external_data()["cheese"] == "bar"

    assert document.get_external_data() is not None
    assert document.get_external_data_keys() == ["default"]

    print(document.get_external_data())

def test_document_steps():
    # Create a new document instance
    document = Document()

    # Create some processing steps
    step1 = ProcessingStep(name="Step 1")
    step2 = ProcessingStep(name="Step 2")
    step3 = ProcessingStep(name="Step 3")

    # Add children to the steps
    step1.add_child(step2)
    step2.add_child(step3)

    # Set the steps to the document
    document.set_steps([step1, step2, step3])

    # Retrieve the steps from the document
    retrieved_steps = document.get_steps()

    # Validate the retrieved steps
    assert len(retrieved_steps) == 3
    assert retrieved_steps[0].name == "Step 1"
    assert retrieved_steps[1].name == "Step 2"
    assert retrieved_steps[2].name == "Step 3"

    # Validate the parent-child relationships
    assert retrieved_steps[0].children[0].name == "Step 2"
    assert retrieved_steps[1].children[0].name == "Step 3"
    assert retrieved_steps[2].parents[0].name == "Step 2"
    assert retrieved_steps[1].parents[0].name == "Step 1"



def test_persistence_cache():
    document = Document.from_text('The sun is very bright today.')
    print("Initial document UUID:", document.uuid)
    print("Content node ID:", document.get_root().id)
    
    # Save to KDDB
    kddb_bytes = document.to_kddb()
    print("Document saved to KDDB")
    
    # Tag the root node
    document.get_root().tag('cheese')
    print("Root node tagged with 'cheese'")
    print("Root node features:", document.get_root().get_features())
    print("Root has tags:", document.get_root().has_tags())
    print("Root tag features:", document.get_root().get_tag_features())
    
    # Debug tags
    print("Debugging tags on original document:")
    document.get_persistence().debug_tags()
    
    # Save the tagged document to KDDB
    tagged_kddb = document.to_kddb()
    print("Tagged document saved to KDDB")
    
    # Load the document from KDDB
    loaded_document = document.from_kddb(tagged_kddb)
    print("Loaded document UUID:", loaded_document.uuid)
    print("Loaded content node ID:", loaded_document.get_root().id)
    print("Loaded root node features:", loaded_document.get_root().get_features())
    print("Loaded root has tags:", loaded_document.get_root().has_tags())
    print("Loaded root tag features:", loaded_document.get_root().get_tag_features())
    
    # Debug tags on the loaded document
    print("Debugging tags on loaded document:")
    loaded_document.get_persistence().debug_tags()
    
    assert loaded_document.get_root().has_tags() is True



def test_tag_nodes_between():
    document = get_test_document_with_three_children()
    document.content_node.get_children()[0].tag_nodes_to(document.content_node.get_children()[2], 'test-tag',
                                                         'unit-test-1')
    assert len(document.content_node.select('//*[hasTag("test-tag")]')) == 2


def test_basic_document_with_content_node():
    document = get_test_document()
    print(document.to_json())
    assert document.to_json() is not None


def test_finder():
    document = get_test_document()
    node = document.get_root().select("//bar")[0]
    assert node.node_type == 'bar'


def test_navigation():
    document = get_test_document()

    document.content_node.add_child(document.create_node(node_type='bar', content='cheeseburger'))
    document.content_node.add_child(document.create_node(node_type='bar', content='lemon'))

    assert document.content_node.get_children()[0]._parent_id is not None
    assert document.content_node.get_children()[0].get_parent() is not None
    assert document.content_node.get_children()[0].get_parent().id == document.content_node.id

    assert document.content_node.get_children()[0].next_node().content == 'cheeseburger'
    assert document.content_node.get_children()[2].previous_node().content == 'cheeseburger'


def test_virtual_navigation_with_no_0_index():
    document = Document(DocumentMetadata())
    node = document.create_node(node_type='loopy')
    node.content = "banana"
    document.content_node = node

    document.content_node.add_child(document.create_node(node_type='loopy', content='banana2'), index=2)

    assert document.content_node.get_node_at_index(0).content is None
    assert document.content_node.get_node_at_index(0).next_node().content is None
    assert document.content_node.get_node_at_index(0).next_node().next_node().content == 'banana2'

    test_kddb = document.to_kddb()
    new_kddb = Document.from_kddb(test_kddb)

    assert new_kddb.content_node.get_node_at_index(0).content is None
    assert new_kddb.content_node.get_node_at_index(0).next_node().content is None
    assert new_kddb.content_node.get_node_at_index(0).next_node().next_node().content == 'banana2'


def test_virtual_navigation():
    document = get_test_document()
    document.content_node.add_child(document.create_node(node_type='bar', content='cheeseburger'), index=2)
    document.content_node.add_child(document.create_node(node_type='bar', content='lemon'), index=5)

    document.add_mixin('navigation')

    assert document.content_node.get_node_at_index(0).content == "fishstick"

    assert document.content_node.get_children()[0].next_node().content is None
    assert document.content_node.get_children()[0].next_node().next_node().next_node().index == 3
    assert document.content_node.get_children()[0].next_node().next_node().next_node().next_node().index == 4
    assert document.content_node.get_children()[
               0].next_node().next_node().next_node().next_node().next_node().index == 5
    # assert document.content_node.get_children()[
    #            0].next_node().next_node().next_node().next_node().next_node().next_node().next_node() is None

    #assert document.content_node.get_children()[0].next_node().next_node().content == 'cheeseburger'


def test_add_feature():
    document = get_test_document()
    document.content_node.add_child(document.create_node(node_type='bar', content='cheeseburger'), index=2)
    document.content_node.add_child(document.create_node(node_type='bar', content='lemon'), index=5)

    # add feature accepting "add_feature" defaults
    new_feature = document.content_node.get_children()[0].add_feature('test', 'test', 'cheese')
    assert len(new_feature.value) == 1
    assert new_feature.value[0] == "cheese"

    # adding a 2nd feature with the same type/name
    another_feature = document.content_node.get_children()[0].add_feature('test', 'test', 'pickels')
    assert len(another_feature.value) == 2
    assert another_feature.value[0] == "cheese"
    assert another_feature.value[1] == "pickels"

    # adding a 3rd feature with the same type/name - changing default values
    yet_another_feature = document.content_node.get_children()[0].add_feature('test', 'test', 'lettuce')
    assert len(yet_another_feature.value) == 3
    assert yet_another_feature.value[0] == "cheese"
    assert yet_another_feature.value[1] == "pickels"
    assert yet_another_feature.value[2] == "lettuce"

    # adding completely new feature and changing the default values

    # Setting a feature with single=False
    # This allows me to set a string as if it was a collection...and later I can't add to it with append.  Not sure that's the desiered behavior
    document.content_node.get_children()[0].add_feature('test_2', 'test_2_name', 'sesame_seeds')

    # This would fail, as the original value 'seasme_seeds' is not a collection, even though it was stated to be one
    # new_again_2 = document.content_node.get_children()[0].add_feature('test_2', 'test_2_name', 'special_sauce')


def test_feature_find():
    document = get_test_document()
    document.content_node.add_child(document.create_node(node_type='bar', content='cheeseburger'), index=1)
    document.content_node.add_child(document.create_node(node_type='bar', content='lemon'), index=5)

    document.content_node.get_children()[0].add_feature('test', 'test', 'cheese')
    document.content_node.get_children()[1].add_feature('test', 'test', 'fishstick')

    assert document.get_root().get_children()[1].get_all_content() == 'cheeseburger'


def test_finder_and_tag():
    document = get_test_document()
    node = document.get_root().select("//bar")[0]
    assert node.node_type == "bar"

    node = document.get_root().select('//bar')[0]
    node.tag("sticky", content_re="fish(.*)", tag_uuid='unit-test')
    print(node.to_json())
    assert len(node.get_tags()) == 1

    node.tag("sticky2", tag_uuid='unit-test-2')
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

    document = document.from_kddb(document.to_kddb())
    print(document.content_node.get_bbox())

    assert document.content_node.get_bbox() == [1, 1, 1, 1]


def test_document_uuid():
    doc_1 = Document.from_text('The sun is very bright today.')
    doc_2 = Document.from_text('Fluffy clouds float through the sky.')
    assert doc_1.uuid != doc_2.uuid


def test_basic_tagging():
    doc = Document.from_text('It is going to be a great day')
    doc.content_node.tag('cheese', fixed_position=[1, 2])
    doc.content_node.tag('cheese', fixed_position=[3, 4])
    assert isinstance(doc.content_node.get_tag('cheese'), list)


def test_basic_tagging2():
    doc = Document.from_text('It is going to be a great day')
    doc.content_node.tag('cheese', fixed_position=[1, 2])
    assert isinstance(doc.content_node.get_tag('cheese'), list)


def test_kbbd():
    doc = Document.from_text('It is going to be a great day')
    doc.content_node.tag('cheese', fixed_position=[1, 2])
    doc.content_node.tag('foo', fixed_position=[3, 4])
    doc2 = doc.from_kddb(doc.to_kddb())
    assert doc2.content_node.get_all_content() == 'It is going to be a great day'
    assert len(doc2.content_node.get_features()) == 2


def test_doc_from_text():
    doc = Document.from_text('It is going to be a great day')
    assert doc.get_root().content == 'It is going to be a great day'
    assert len(doc.get_root().get_children()) == 0

    doc = Document.from_text('It is going to be a great day', separator=' ')
    assert doc.get_root().content is None
    assert len(doc.get_root().get_children()) == 8
    assert doc.get_root().get_children()[4].content == 'be'


def test_get_source():
    document = Document.from_url('https://www.google.com')

    with get_source(document) as fh:
        data = fh.read()
        print(data)


def test_in_memory_kddb_conversion():
    document = Document.from_kddb(
        Document.from_msgpack(open(os.path.join(get_test_directory(), 'news-tagged.kdxa'), 'rb').read()).to_kddb(),
        inmemory=True)
    document.to_kddb('/tmp/test.kddb')
    new_document = Document.from_kddb('/tmp/test.kddb')
    new_document.to_kddb('/tmp/test2.kddb')
