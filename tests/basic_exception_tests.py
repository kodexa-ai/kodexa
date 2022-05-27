from kodexa import *
from kodexa.model import ContentException


def test_basic_exception():
    document = Document()
    exception = ContentException("Testing exception")
    document.add_exception(exception)
