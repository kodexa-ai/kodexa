import logging

import pytest

from kodexa import RemoteStep
from kodexa.model import DocumentMetadata, Document, ContentObject, ContentType
from kodexa.pipeline import Pipeline
from kodexa.steps.common import TextParser, DocumentStoreWriter
from kodexa.stores import LocalDocumentStore


def create_document():
    document = Document(DocumentMetadata())
    document.source.original_filename = "test.doc"
    node = document.create_node(node_type='foo')
    node.content = "cheese"
    document.content_node = node

    foo2 = document.create_node(node_type='bar')
    foo2.content = "fishstick"
    document.content_node.add_child(foo2)
    return document


def test_simplified_remote_action_reference():
    pipeline = Pipeline.from_text('hello')
    pipeline.add_step('kodexa/ner-tagger', options={"option": "test"})

    assert len(pipeline.steps) == 1
    assert isinstance(pipeline.steps[0].step, RemoteStep)
    assert "option" in pipeline.steps[0].step.options


def test_basic_local_document_store():
    JSON_STORE = "/tmp/test-json-store.jsonkey"
    document_store = LocalDocumentStore(store_path=JSON_STORE, force_initialize=True)
    document_store.put("test.doc", create_document())

    new_document_store = LocalDocumentStore(store_path=JSON_STORE)

    assert (new_document_store.count() == 1)


def test_co():
    # Just confirm the Pydantic Constructor
    new_content_object = ContentObject(**{'contentType': 'DOCUMENT'})
    new_content_object.content_type = ContentType.document
    assert new_content_object.content_type == ContentType.document


def test_pipeline_example():
    document_store = LocalDocumentStore()
    document_store.put("test.doc", create_document())

    pipeline = Pipeline(document_store)
    stats = pipeline.run().statistics

    assert stats.documents_processed == 1


def test_class_step_step_with_context():
    document_store = LocalDocumentStore()
    document_store.put('test.doc', create_document())

    new_document_store = LocalDocumentStore()

    class MyProcessingStep:

        def get_name(self):
            return "test-step"

        def process(self, doc, context):
            doc.metadata.cheese = context.execution_id
            logging.error("Hello")
            return doc

    pipeline = Pipeline(document_store)
    pipeline.add_step(MyProcessingStep())
    pipeline.add_step(DocumentStoreWriter(new_document_store))
    ctxt = pipeline.run()

    assert ctxt.statistics.documents_processed == 1
    assert ctxt.statistics.document_exceptions == 0
    assert new_document_store.get_latest_document("test.doc").metadata.cheese == pipeline.context.execution_id


def test_function_step_with_context():
    document_store = LocalDocumentStore()
    document_store.put("test.doc", create_document())
    new_document_store = LocalDocumentStore()

    def my_function(doc, context):
        doc.metadata.cheese = context.execution_id
        logging.error("Hello")
        return doc

    assert new_document_store.count() == 0
    pipeline = Pipeline(document_store)
    pipeline.add_step(my_function)
    pipeline.add_step(DocumentStoreWriter(new_document_store))
    stats = pipeline.run().statistics

    assert stats.documents_processed == 1
    assert stats.document_exceptions == 0
    assert new_document_store.count() == 1
    assert new_document_store.get_latest_document("test.doc").metadata.cheese == pipeline.context.execution_id


def test_function_step():
    document_store = LocalDocumentStore()
    document_store.put("test.doc", create_document())
    new_document_store = LocalDocumentStore()

    def my_function(doc):
        doc.metadata.cheese = "fishstick"
        logging.error("Hello")
        return doc

    assert new_document_store.count() == 0
    pipeline = Pipeline(document_store)
    pipeline.add_step(my_function)
    pipeline.add_step(DocumentStoreWriter(new_document_store))
    stats = pipeline.run().statistics

    assert stats.documents_processed == 1
    assert stats.document_exceptions == 0
    assert new_document_store.count() == 1
    assert new_document_store.get_latest_document("test.doc").metadata.cheese == 'fishstick'


def test_fluent_pipeline():
    def my_function(doc):
        doc.metadata.cheese = "fishstick"
        logging.error("Hello")
        return doc

    document = create_document()
    new_document_store = LocalDocumentStore()

    stats = Pipeline(document).add_step(my_function).add_step(my_function).add_step(
        DocumentStoreWriter(new_document_store)).run().statistics

    assert stats.documents_processed == 1
    assert stats.document_exceptions == 0
    assert new_document_store.count() == 1
    assert new_document_store.get_latest_document("test.doc").metadata.cheese == 'fishstick'


def test_url_pipeline():
    document = Document.from_url("http://www.google.com")
    new_document_store = LocalDocumentStore()

    stats = Pipeline(document).add_step(TextParser(encoding='ISO-8859-1')).add_step(
        DocumentStoreWriter(new_document_store)).run().statistics

    assert stats.documents_processed == 1
    assert stats.document_exceptions == 0
    assert new_document_store.count() == 1

    new_doc = new_document_store.get_latest_document("http://www.google.com")
    print(new_doc.content_node.get_all_content())


def test_function_step_with_exception():
    document_store = LocalDocumentStore()
    document_store.put("test.doc", create_document())
    new_document_store = LocalDocumentStore()

    def my_function(doc):
        doc.metadata.cheese = "fishstick"
        raise Exception("hello world")

    assert new_document_store.count() == 0
    pipeline = Pipeline(document_store, stop_on_exception=False)
    pipeline.add_step(my_function)
    pipeline.add_step(DocumentStoreWriter(new_document_store))
    stats = pipeline.run().statistics

    assert stats.documents_processed == 1
    assert stats.document_exceptions == 1
    assert new_document_store.count() == 1

    assert len(new_document_store.get_latest_document("test.doc").exceptions) == 1


def test_basic_url_pipeline():
    url = 'http://www.google.com'
    pipeline = Pipeline.from_url(url)
    pipeline.run()

    doc = pipeline.context.output_document
    assert doc.source.original_path == url


def test_basic_text_pipeline():
    text = 'The Normans (Norman: Nourmands; French: Normands; Latin: Normanni) ' \
           'were the people who in the 10th and 11th centuries gave their name to ' \
           'Normandy, a region in France. They were descended from Norse ' \
           '(\"Norman\" comes from \"Norseman\") raiders and pirates from Denmark, ' \
           'Iceland and Norway who, under their leader Rollo, ' \
           'agreed to swear fealty to King Charles III of West Francia. ' \
           'Through generations of assimilation and mixing with the native ' \
           'Frankish and Roman-Gaulish populations, their descendants would gradually ' \
           'merge with the Carolingian-based cultures of West Francia. ' \
           'The distinct cultural and ethnic identity of the Normans emerged initially ' \
           'in the first half of the 10th century, ' \
           'and it continued to evolve over the succeeding centuries.'
    pipeline = Pipeline.from_text(text)
    pipeline.run()
    doc = pipeline.context.output_document

    assert len(doc.get_root().get_all_content()) == 742


# TODO having problems with CI
@pytest.mark.skip
def test_basic_folder_pipeline():
    context = Pipeline.from_folder('../test_documents/recursion_test', '*.txt', recursive=True, relative=True).run()
    assert context.statistics.documents_processed == 4
    context = Pipeline.from_folder('../test_documents/recursion_test', '*.txt', recursive=False, relative=True).run()
    assert context.statistics.documents_processed == 1
