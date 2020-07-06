import os

from kodexa import Document, DocumentRender, PipelineContext, TagsToKeyValuePairExtractor, RollupTransformer


def get_test_directory():
    return os.path.dirname(os.path.abspath(__file__)) + "/../test_documents/"


def test_html_rollup():
    document = Document.from_msgpack(open(os.path.join(get_test_directory(), 'news.kdxa'), 'rb').read())

    # before rollup
    assert document.select('//a')[0].content == 'HSBC'
    assert document.select('//a')[1].content == 'Hang Seng Index'
    assert len(document.select('//*[contentRegex(".*Hang Seng Index.*")]')[0].content_parts) == 1

    # Collapse out all the <a> tags
    step = RollupTransformer(collapse_type_res=["a"])
    step.process(document)
    
    #after rollup
    assert len(document.select('//a')) == 0
    # see where the href rolled up
    assert len(document.select('//*[contentRegex(".*Hang Seng Index.*")]')[0].content_parts) == 3



def test_tag_key_value():
    document = Document.from_msgpack(open(os.path.join(get_test_directory(), 'news-tagged.kdxa'), 'rb').read())
    step = TagsToKeyValuePairExtractor(store_name='test_store')
    context = PipelineContext()
    step.process(document, context)
    
    assert context.get_store('test_store').count() == 45
    assert context.get_store('test_store').rows[14][0] == 'LOC'
    assert context.get_store('test_store').rows[14][1] == 'Europe'
