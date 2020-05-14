import os

import pytest
from texttable import Texttable

from kodexa import InMemoryDocumentSink, Pipeline, FolderConnector, KodexaCloudService, KodexaCloudPipeline, Document
from kodexa_cloud.cloud import CloudSession


def get_test_directory():
    return os.path.dirname(os.path.abspath(__file__)) + "/../test_documents/"


# Commented out while we work on test credentials

@pytest.mark.skip(reason="not part of core tests")
def test_kodexa_service():
    document_sink = InMemoryDocumentSink()

    pipeline = Pipeline(FolderConnector(path=str(get_test_directory()), file_filter='*.pdf'))
    pipeline.add_step(
        KodexaCloudService(slug='kodexa/pdf-parse', attach_source=True, cloud_url="https://quantum.kodexa.com"))
    pipeline.set_sink(document_sink)
    pipeline.run()

    # Make sure the finders are available
    document = document_sink.get_document(0)

    assert document is not None
    assert document.content_node is not None

    print(document.to_json())


@pytest.mark.skip(reason="not part of core tests")
def test_kodexa_pipeline():
    context = KodexaCloudPipeline("kodexa/news-reader-demo", cloud_url="https://quantum.kodexa.com").execute(
        get_test_directory() + "/news.html")

    print(context.get_store_names())
    print_store(context.get_store("tag_pairs"))


def print_store(store):
    table = Texttable()
    table.header(store.columns)
    table.add_rows(store.rows)
    print(table.draw() + "\n")


def test_model():
    session = CloudSession(**{"id": "cheese", "type": "pipeline", "sessionState": "OPEN"})
    print(session.json())

    assert session.json() != ""


def test_tag_selector():
    new_document = Document.from_text("Hello World")
    nodes = new_document.content_node.findall(tag_name_re=".*")

    assert len(nodes) == 0
