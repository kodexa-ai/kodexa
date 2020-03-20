import os

import pytest

from kodexa import InMemoryDocumentSink, Pipeline, FolderConnector, KodexaService


def get_test_directory():
    return os.path.dirname(os.path.abspath(__file__)) + "/../test_documents/"


# Commented out while we work on test credentials

@pytest.mark.skip(reason="not part of core tests")
def test_kodexa_example():
    document_sink = InMemoryDocumentSink()

    pipeline = Pipeline(FolderConnector(path=str(get_test_directory()), file_filter='*.pdf'))

    pipeline.add_step(KodexaService(organization='kodexa', service='pdf-parse', attach_source=True,
                                    cloud_url='http://localhost:8080'))
    pipeline.add_step(KodexaService(organization='kodexa', service='analyze', cloud_url='http://localhost:8080'))
    pipeline.set_sink(document_sink)
    pipeline.run()

    # Make sure the finders are available
    document = document_sink.get_document(0)

    assert document

    print(document.to_json())
