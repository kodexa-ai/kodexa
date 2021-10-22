import pytest

from kodexa import *


def test_basic_local_document_store():
    lds = LocalDocumentStore('/tmp/lds-test', force_initialize=True)

    d1 = Document.from_text("Hello World")

    # First up we will create a family by adding a simple document
    lds.put("my_document.txt", d1)

    # Next up we will want to add a new document to this family

    family = lds.get_family_by_path("my_document.txt")

    assert family is not None

    lds.add_related_document_to_family(family.id,
                                       DocumentTransition(transitionType=TransitionType.derived,
                                                          sourceContentObjectId=family.get_latest_content().id),
                                       Document.from_text('Hello again world'))

    assert lds.get_family_by_path("my_document.txt").get_document_count() == 2


@pytest.mark.skip
def test_basic_remote_document_store():

    KodexaPlatform.set_url("http://localhost:8082")

    remote_document_store = RemoteDocumentStore(
        'philiptest3/8a8a832877458ca70177459a89c70004-training-document-store:1.0.0')

    d1 = Document.from_text("Hello World")

    # First lets delete the document if it exists
    family = remote_document_store.get_family_by_path("my_document.txt")

    if family is not None:
        remote_document_store.delete("my_document.txt")

    # First up we will create a family by adding a simple document
    new_family = remote_document_store.put("my_document.txt", d1)

    # Next up we will want to add a new document to this family

    family = remote_document_store.get_family_by_path("my_document.txt")

    assert family is not None

    remote_document_store.add_related_document_to_family(family.id,
                                                         DocumentTransition(TransitionType.DERIVED,
                                                                            family.get_latest_content().id),
                                                         Document.from_text('Hello again world'))

    assert remote_document_store.get_family_by_path("my_document.txt").get_document_count() == 2
