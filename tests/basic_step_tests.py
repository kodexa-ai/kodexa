import os

from kodexa import Document, DocumentRender, PipelineContext
from kodexa.steps.common import RollupTransformer, TagsToKeyValuePairExtractor


def get_test_directory():
    return os.path.dirname(os.path.abspath(__file__)) + "/../test_documents/"


def test_html_rollup():
    document = Document.from_msgpack(open(os.path.join(get_test_directory(), 'news.kdxa'), 'rb').read())

    # Collapse out all the <a> tags
    step = RollupTransformer(collapse_type_res=["a"])
    result = step.process(document)


def test_tag_key_value():
    document = Document.from_msgpack(open(os.path.join(get_test_directory(), 'news-tagged.kdxa'), 'rb').read())

    # Collapse out all the <a> tags
    step = TagsToKeyValuePairExtractor(store_name='test_store')
    context = PipelineContext()
    result = step.process(document, context)
    print(context.get_store('test_store').rows)
