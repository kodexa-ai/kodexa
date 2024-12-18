import os

from kodexa import Document


def get_test_directory():
    return os.path.dirname(os.path.abspath(__file__)) + "/../test_documents/"


def test_basic_tag():
    document = Document.from_kddb(os.path.join(get_test_directory(), 'fax2.kddb'), detached=True)
    document.get_root().tag('test', tag_uuid='1234')
    tag_feature = document.get_root().get_feature('tag', 'test')
    assert tag_feature.get_value()['uuid'] == '1234'
    print(document.get_root().get_feature('tag', 'test'))
