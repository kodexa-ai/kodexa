import os

from kodexa import Document, Pipeline, DocumentMetadata, JsonDocumentStore, TagsToKeyValuePairExtractor, NodeTagger
from kodexa.testing.test_utils import compare_store


def get_test_directory():
    return os.path.dirname(os.path.abspath(__file__)) + "/../test_documents/"


def get_test_document():
    document = Document(DocumentMetadata())
    node = document.create_node(node_type='foo')
    node.content = "cheese"
    document.content_node = node

    document.content_node.add_child(document.create_node(node_type='bar', content='fishstick'))
    return document


def test_basic_json_store():
    store = JsonDocumentStore(store_path='/tmp/json-store', force_initialize=True)

    assert store.count() == 0
    # need to add more than one document to the store to make sure indexes are written 
    # to the index.idx correctly
    store.add(get_test_document())
    store.add(get_test_document())

    store2 = JsonDocumentStore(store_path='/tmp/json-store')
    assert store2.count() == 2


def test_table_data_store():
    # Testing with 'include_node_content' set to True.  Should result in 3 columns
    pipeline = Pipeline(Document.from_kdxa(os.path.join(get_test_directory(), 'tongue_twister.kdxa')))
    pipeline.add_step(NodeTagger(selector='//*[contentRegex(".*flue.*")]', tag_to_apply='has_flue', node_only=True))
    pipeline.add_step(TagsToKeyValuePairExtractor(store_name='tagged_data', include_node_content=True))
    context = pipeline.run()

    compare_store(context, 'tagged_data', 'basic_store_tagged_data1.json')

    # Testing with 'include_node_content' set to False.  Should result in 2 columns
    pipeline2 = Pipeline(Document.from_kdxa(os.path.join(get_test_directory(), 'tongue_twister.kdxa')))
    pipeline2.add_step(NodeTagger(selector='//*[contentRegex(".*flue.*")]', tag_to_apply='has_flue', node_only=True))
    pipeline2.add_step(TagsToKeyValuePairExtractor(store_name='tagged_data_2', include_node_content=False))
    context2 = pipeline2.run()

    compare_store(context2, 'tagged_data_2', 'basic_store_tagged_data2.json')
