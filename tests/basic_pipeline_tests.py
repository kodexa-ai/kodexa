import logging
import os
from pathlib import Path

from kodexa.model import DocumentMetadata, Document
from kodexa.pipeline import Pipeline
from kodexa.steps.common import TextParser
from kodexa.stores import JsonDocumentStore, TableDataStore, DictDataStore


def create_document():
    document = Document(DocumentMetadata())
    node = document.create_node(type='foo')
    node.content = "cheese"
    document.content_node = node

    foo2 = document.create_node(type='bar')
    foo2.content = "fishstick"
    document.content_node.add_child(foo2)
    return document


def test_basic_json_store():
    JSON_STORE = "/tmp/test-json-store.json"
    if Path(JSON_STORE).is_file():
        os.remove(JSON_STORE)
    document_store = JsonDocumentStore("/tmp/test-json-store.json")
    document_store.add(create_document())

    new_document_store = JsonDocumentStore("/tmp/test-json-store.json")

    assert (new_document_store.count() == 1)


def test_pipeline_example():
    document_store = JsonDocumentStore("/tmp/test-json-store", force_initialize=True)
    document_store.add(create_document())

    if Path("/tmp/test-json-store2/index..json").is_file():
        os.remove("/tmp/test-json-store2")

    new_document_store = JsonDocumentStore("/tmp/test-json-store2", force_initialize=True)

    assert new_document_store.count() == 0
    pipeline = Pipeline(document_store)
    pipeline.set_sink(new_document_store)
    stats = pipeline.run().statistics

    assert stats.documents_processed == 1
    assert new_document_store.count() == 1


def test_class_step_step_with_context():
    document_store = JsonDocumentStore("/tmp/test-json-store", force_initialize=True)
    document_store.add(create_document())
    new_document_store = JsonDocumentStore("/tmp/test-json-store2", force_initialize=True)

    class MyProcessingStep:

        def get_name(self):
            return "test-step"

        def process(self, doc, context):
            doc.metadata.cheese = context.transaction_id
            logging.error("Hello")
            return doc

    assert new_document_store.count() == 0
    pipeline = Pipeline(document_store)
    pipeline.add_step(MyProcessingStep())
    pipeline.set_sink(new_document_store)
    stats = pipeline.run().statistics

    assert stats.documents_processed == 1
    assert stats.document_exceptions == 0
    assert new_document_store.count() == 1
    assert new_document_store.get_document(0).metadata.cheese == pipeline.context.transaction_id

    print(new_document_store.get_document(0).log)


def test_function_step_with_context():
    document_store = JsonDocumentStore("/tmp/test-json-store", force_initialize=True)
    document_store.add(create_document())
    new_document_store = JsonDocumentStore("/tmp/test-json-store2", force_initialize=True)

    def my_function(doc, context):
        doc.metadata.cheese = context.transaction_id
        logging.error("Hello")
        return doc

    assert new_document_store.count() == 0
    pipeline = Pipeline(document_store)
    pipeline.add_step(my_function)
    pipeline.set_sink(new_document_store)
    stats = pipeline.run().statistics

    assert stats.documents_processed == 1
    assert stats.document_exceptions == 0
    assert new_document_store.count() == 1
    assert new_document_store.get_document(0).metadata.cheese == pipeline.context.transaction_id

    print(new_document_store.get_document(0).log)


def test_function_step():
    document_store = JsonDocumentStore("/tmp/test-json-store", force_initialize=True)
    document_store.add(create_document())
    new_document_store = JsonDocumentStore("/tmp/test-json-store2", force_initialize=True)

    def my_function(doc):
        doc.metadata.cheese = "fishstick"
        logging.error("Hello")
        return doc

    assert new_document_store.count() == 0
    pipeline = Pipeline(document_store)
    pipeline.add_step(my_function)
    pipeline.set_sink(new_document_store)
    stats = pipeline.run().statistics

    assert stats.documents_processed == 1
    assert stats.document_exceptions == 0
    assert new_document_store.count() == 1
    assert new_document_store.get_document(0).metadata.cheese == 'fishstick'

    print(new_document_store.get_document(0).log)


def test_fluent_pipeline():
    def my_function(doc):
        doc.metadata.cheese = "fishstick"
        logging.error("Hello")
        return doc

    document = create_document()
    new_document_store = JsonDocumentStore("/tmp/test-json-store", force_initialize=True)

    stats = Pipeline(document).add_step(my_function).add_step(my_function).set_sink(new_document_store).run().statistics

    assert stats.documents_processed == 1
    assert stats.document_exceptions == 0
    assert new_document_store.count() == 1
    assert new_document_store.get_document(0).metadata.cheese == 'fishstick'

    print(new_document_store.get_document(0).log)


def test_url_pipeline():
    document = Document(DocumentMetadata({"connector": "url", "connector_options": {"url": "http://www.google.com"}}))
    new_document_store = JsonDocumentStore("/tmp/test-json-store", force_initialize=True)

    stats = Pipeline(document).add_step(TextParser(encoding='ISO-8859-1')).set_sink(new_document_store).run().statistics

    assert stats.documents_processed == 1
    assert stats.document_exceptions == 0
    assert new_document_store.count() == 1

    new_doc = new_document_store.get_document(0)
    new_doc.add_mixin('core')
    print(new_doc.content_node.get_all_content())



def test_function_step_with_exception():
    document_store = JsonDocumentStore("/tmp/test-json-store", force_initialize=True)
    document_store.add(create_document())
    new_document_store = JsonDocumentStore("/tmp/test-json-store2", force_initialize=True)

    def my_function(doc):
        doc.metadata.cheese = "fishstick"
        raise Exception("hello world")
        return doc

    assert new_document_store.count() == 0
    pipeline = Pipeline(document_store, stop_on_exception=False)
    pipeline.add_step(my_function)
    pipeline.set_sink(new_document_store)
    stats = pipeline.run().statistics

    assert stats.documents_processed == 1
    assert stats.document_exceptions == 1
    assert new_document_store.count() == 1

    assert len(new_document_store.get_document(0).exceptions) == 1

    print(new_document_store.get_document(0).exceptions)


def test_dict_stores_with_extractor():
    document_store = JsonDocumentStore("/tmp/test-json-store", force_initialize=True)
    document_store.add(create_document())
    pipeline = Pipeline(document_store, stop_on_exception=False)
    pipeline.add_store('output', DictDataStore())

    def extractor(document, context):
        # An example of how we might
        # extract into a dict
        #
        context.get_store('output').add(
            {
                'cheese': 'test'
            }
        )

        return document

    pipeline.add_step(extractor)

    stats = pipeline.run().statistics

    assert pipeline.context.get_store('output').count() == 1


def test_table_stores_with_extractor():
    document_store = JsonDocumentStore("/tmp/test-json-store", force_initialize=True)
    document_store.add(create_document())
    pipeline = Pipeline(document_store, stop_on_exception=False)
    pipeline.add_store('output', TableDataStore(columns=['cheese']))

    def extractor(document, context):
        # An example of how we might
        # extract into a dict
        #
        context.get_store('output').add(['test'])

        return document

    pipeline.add_step(extractor)

    context = pipeline.run()

    assert pipeline.context.get_store('output').count() == 1
