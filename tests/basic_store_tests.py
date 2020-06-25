import shutil

from kodexa import JsonDocumentStore
from kodexa.model import DocumentMetadata, Document


def get_test_document():
    document = Document(DocumentMetadata())
    node = document.create_node(type='foo')
    node.content = "cheese"
    document.content_node = node

    document.content_node.add_child(document.create_node(type='bar', content='fishstick'))
    return document


def test_basic_json_store():
    store = JsonDocumentStore(store_path='/tmp/json-store', force_initialize=True)

    assert store.count() == 0
    # need to add more than one document to the store to make sure indexes are written 
    # to the index.json correctly
    store.add(get_test_document())
    store.add(get_test_document())

    store2 = JsonDocumentStore(store_path='/tmp/json-store')
    assert store2.count() == 2