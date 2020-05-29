import os

from kodexa import Document, DocumentRender, PipelineContext
from kodexa.steps.common import Rollup, ExtractTagsToKeyValuePair


def get_test_directory():
    return os.path.dirname(os.path.abspath(__file__)) + "/../test_documents/"


def test_html_rollup():
    document = Document.from_msgpack(open(os.path.join(get_test_directory(), 'news.mdoc'), 'rb').read())

    # Collapse out all the <a> tags
    step = Rollup(collapse_type_res=["a"])
    result = step.process(document)
    print(DocumentRender(result).to_text())


def test_html_rollup():
    document = Document.from_msgpack(open(os.path.join(get_test_directory(), 'news.mdoc'), 'rb').read())

    # Collapse out all the <a> tags
    step = Rollup(collapse_type_res=["a"])
    result = step.process(document)


def test_tag_key_value():
    document = Document.from_msgpack(open(os.path.join(get_test_directory(), 'news-tagged.mdoc'), 'rb').read())

    # Collapse out all the <a> tags
    step = ExtractTagsToKeyValuePair(store_name='test_store')
    context = PipelineContext()
    result = step.process(document, context)
    print(context.get_store('test_store').rows)
