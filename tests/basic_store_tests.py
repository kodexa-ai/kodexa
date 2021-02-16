import os

from kodexa import Document, Pipeline, DocumentMetadata, TagsToKeyValuePairExtractor, NodeTagger, \
    LocalDocumentStore, TableDataStore
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


def test_table_data_store():
    # Testing with 'include_node_content' set to True.  Should result in 3 columns
    pipeline = Pipeline(Document.from_kdxa(os.path.join(get_test_directory(), 'tongue_twister.kdxa')))
    pipeline.add_step(NodeTagger(selector='//*[contentRegex(".*flue.*")]', tag_to_apply='has_flue', node_only=True,
                                 node_tag_uuid='test'))
    pipeline.add_step(TagsToKeyValuePairExtractor(store_name='tagged_data', include_node_content=True))
    context = pipeline.run()

    compare_store(context, 'tagged_data', 'basic_store_tagged_data1.json')

    # Testing with 'include_node_content' set to False.  Should result in 2 columns
    pipeline2 = Pipeline(Document.from_kdxa(os.path.join(get_test_directory(), 'tongue_twister.kdxa')))
    pipeline2.add_step(NodeTagger(selector='//*[contentRegex(".*flue.*")]', tag_to_apply='has_flue', node_only=True))
    pipeline2.add_step(TagsToKeyValuePairExtractor(store_name='tagged_data_2', include_node_content=False))
    context2 = pipeline2.run()

    compare_store(context2, 'tagged_data_2', 'basic_store_tagged_data2.json')


def test_basic_local_document_store():
    lds = LocalDocumentStore('/tmp/lds', force_initialize=True)
    lds.put('my-doc', Document.from_text('hello!'))

    assert len(lds.list_objects()) == 1

    lds2 = LocalDocumentStore('/tmp/lds')
    assert len(lds2.list_objects()) == 1


def test_predefined_table_store():
    def process(document, context):
        if context.get_store('prediction-data-store'):
            document.get_root().content = 'We have a data store name'
        elif context.get_store_names() and len(context.get_store_names()) > 0:
            document.get_root().content = ' '.join(context.get_store_names())
        else:
            document.get_root().content = 'No stores on context'

        return document

    pipeline = Pipeline.from_text("Hello World")
    pipeline.add_store('prediction-data-store', TableDataStore())
    pipeline.add_step(process)

    context = pipeline.run()

    new_doc = context.output_document
    print(new_doc.content_node.content)

    assert new_doc.content_node.content == 'We have a data store name'
