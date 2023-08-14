import os

from kodexa import Document
from kodexa.model import ContentException


def get_test_directory():
    return os.path.dirname(os.path.abspath(__file__)) + "/../test_documents/"


def test_basic_exception():
    document = Document()
    exception = ContentException("Test", "Testing exception")
    document.add_exception(exception)

    assert len(document.get_exceptions()) == 1


def test_update_exception():

    document = Document.from_kddb(os.path.join(get_test_directory(), 'exceptions-v4.kddb'), detached=True)
    assert len(document.get_exceptions()) == 0

    content_exception = ContentException("Test", "Testing exception", exception_type_id="123123")
    document.add_exception(content_exception)

    assert len(document.get_exceptions()) == 1

    document.to_kddb("/tmp/exceptions-v6.kddb")
    document.close()

    document = Document.from_kddb("/tmp/exceptions-v6.kddb")

    assert len(document.get_exceptions()) == 1

    assert document.get_exceptions()[0].exception_type_id == "123123"
