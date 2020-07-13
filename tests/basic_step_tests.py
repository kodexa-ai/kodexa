import os

from kodexa import Document, DocumentRender, Pipeline, PipelineContext, TagsToKeyValuePairExtractor, RollupTransformer


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

def test_rollup_of_pdf():

    # first test - collapsing words and lines up to their common parent
    test_doc = Document.from_kdxa(get_test_directory() + '20200709loanboss.kdxa')

    rollup_pipeline = Pipeline(test_doc)
    rollup_pipeline.add_step(RollupTransformer(collapse_type_res=["word", "line"]))
    rollup_pipeline.run()

    collapsed_doc = rollup_pipeline.context.output_document

    ## This will collapse all word nodes into lines and then lines into content-areas, but there are no spaces retained
    ## all the text rolls together
    print(collapsed_doc.select("//content-area")[12].get_all_content())
    #'follows:aswarrantandrepresentagree,covenant,herebyheretopartiestheAgreement,thisinforthsetwarrantiesandrepresentationsagreements,covenants,theandLenderbyLoantheofmakingtheofconsiderationinTHEREFORE,NOW'


    ## second test - just collapse the line up to its parent (content-area)
    test_doc = Document.from_kdxa(get_test_directory() + '20200709loanboss.kdxa')

    rollup_pipeline = Pipeline(test_doc)
    rollup_pipeline.add_step(RollupTransformer(collapse_type_res=["line"]))
    rollup_pipeline.run()

    collapsed_doc = rollup_pipeline.context.output_document

    ## there is no text on the content-area because we're not getting all content for the node we're collapsing
    ## and the line had no content of it's own, it was it's children
    print(collapsed_doc.select("//content-area")[12].get_all_content())