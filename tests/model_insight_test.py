import os

from kodexa import Document
from kodexa.model.model import ModelInsight


def get_test_directory():
    return os.path.dirname(os.path.abspath(__file__)) + "/../test_documents/"


def test_model_insight_add_old_doc():
    document = Document.from_kddb(os.path.join(get_test_directory(), 'fax2.kddb'), detached=True)
    document.add_model_insight(ModelInsight(model_ref='test', insight_type='test', description='hello world'))

    document2 = Document.from_kddb(document.to_kddb())

    assert len(document2.get_model_insights()) == 1
    assert document2.get_model_insights()[0].model_ref == 'test'
    assert document2.get_model_insights()[0].insight_type == 'test'
    assert document2.get_model_insights()[0].description == 'hello world'


def test_model_insight_add_new_doc():
    document = Document()
    document.add_model_insight(ModelInsight(model_ref='test', insight_type='test', description='hello world'))

    document2 = Document.from_kddb(document.to_kddb())

    assert len(document2.get_model_insights()) == 1
    assert document2.get_model_insights()[0].model_ref == 'test'
    assert document2.get_model_insights()[0].insight_type == 'test'
    assert document2.get_model_insights()[0].description == 'hello world'
