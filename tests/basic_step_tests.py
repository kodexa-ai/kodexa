import os

from kodexa import Document, Pipeline, PipelineContext, TagsToKeyValuePairExtractor, RollupTransformer


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

    # after rollup
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


def test_tag_key_value_include_exclude():

    # Testing include parameter
    include_tags = ['DATE', 'LOC']
    document = Document.from_msgpack(open(os.path.join(get_test_directory(), 'news-tagged.kdxa'), 'rb').read())
    step = TagsToKeyValuePairExtractor(store_name='test_store', include=include_tags)
    context = PipelineContext()
    step.process(document, context)
    assert context.get_store('test_store').count() == 11

    # Testing exclude parameter
    exclude_tags = ['DATE', 'LOC']
    document = Document.from_msgpack(open(os.path.join(get_test_directory(), 'news-tagged.kdxa'), 'rb').read())
    step = TagsToKeyValuePairExtractor(store_name='test_store', exclude=exclude_tags)
    context = PipelineContext()
    step.process(document, context)
    assert context.get_store('test_store').count() == 34

    # Testing both include and exclude parameters
    include_tags = ['LOC']
    exclude_tags = ['DATE']
    document = Document.from_msgpack(open(os.path.join(get_test_directory(), 'news-tagged.kdxa'), 'rb').read())
    step = TagsToKeyValuePairExtractor(store_name='test_store', include=include_tags, exclude=exclude_tags)
    context = PipelineContext()
    step.process(document, context)
    assert context.get_store('test_store').count() == 5

    # Testing both include - this should be the same as before as 'exclude' shouldn't have really done anything
    include_tags = ['LOC']
    document = Document.from_msgpack(open(os.path.join(get_test_directory(), 'news-tagged.kdxa'), 'rb').read())
    step = TagsToKeyValuePairExtractor(store_name='test_store', include=include_tags)
    context = PipelineContext()
    step.process(document, context)
    assert context.get_store('test_store').count() == 5


def test_rollup_of_pdf():
    # first test - collapsing words and lines up to their common parent
    test_doc = Document.from_kdxa(get_test_directory() + '20200709loanboss.kdxa')

    # how many pre-rollup lines?
    assert len(test_doc.select('//line')) == 3824
    # how many pre-rollup words?
    assert len(test_doc.select('//word')) == 52903
    # how many pre-rollup content-areas?
    assert len(test_doc.select('//content-area')) == 817
    # what is the pre-rollup length of ALL the content in the document?
    assert len(test_doc.get_root().get_all_content()) == 329792

    rollup_pipeline = Pipeline(test_doc)
    rollup_pipeline.add_step(RollupTransformer(collapse_type_res=["word", "line"], separator_character=' '))
    rollup_pipeline.run()

    collapsed_doc = rollup_pipeline.context.output_document

    # how many post-rollup lines?
    assert len(test_doc.select('//line')) == 0
    # how many post-rollup words?
    assert len(test_doc.select('//word')) == 0
    # how many post-rollup content-areas?
    assert len(test_doc.select('//content-area')) == 817
    # what is the post-rollup length of ALL the content in the document?
    assert len(test_doc.get_root().get_all_content()) == 329792

    assert len(collapsed_doc.select("//content-area")[12].get_all_content()) == 235

    # second test - just collapse the line up to its parent (content-area) - roll up the line's children
    test_doc = Document.from_kdxa(get_test_directory() + '20200709loanboss.kdxa')

    rollup_pipeline = Pipeline(test_doc)
    rollup_pipeline.add_step(
        RollupTransformer(collapse_type_res=["line"], separator_character=' ', get_all_content=True))
    rollup_pipeline.run()

    collapsed_doc = rollup_pipeline.context.output_document

    # how many post-rollup lines?
    assert len(test_doc.select('//line')) == 0
    # how many post-rollup words?
    assert len(test_doc.select('//word')) == 0
    # how many post-rollup content-areas?
    assert len(test_doc.select('//content-area')) == 817
    # what is the post-rollup length of ALL the content in the document?
    assert len(test_doc.get_root().get_all_content()) == 329792

    # verify that we can collapse line nodes AND include their children
    assert len(collapsed_doc.select("//content-area")[12].get_all_content()) == 235

    # third test - select specific nodes in which we'll do the roll ups
    test_doc = Document.from_kdxa(get_test_directory() + '20200709loanboss.kdxa')

    node_selector = "//content-area[contentRegex('.*LOAN AGREEMENT.*', true)]"

    # verify we have 3 nodes match this selector
    node_matches = test_doc.select(node_selector)
    assert len(node_matches) == 3

    # before we rollup, let's make sure the matching nodes conform to known expectations
    assert len(node_matches[0].select('//word')) == 2
    assert len(node_matches[0].select('//line')) == 1
    assert len(node_matches[0].select('//content-area')) == 1
    assert len(node_matches[0].get_all_content()) == 14

    assert len(node_matches[1].select('//word')) == 2
    assert len(node_matches[1].select('//line')) == 1
    assert len(node_matches[1].select('//content-area')) == 1
    assert len(node_matches[1].get_all_content()) == 14

    assert len(node_matches[2].select('//word')) == 71
    assert len(node_matches[2].select('//line')) == 6
    assert len(node_matches[2].select('//content-area')) == 1
    assert len(node_matches[2].get_all_content()) == 500

    rollup_pipeline = Pipeline(test_doc)
    rollup_pipeline.add_step(RollupTransformer(selector="//content-area[contentRegex('.*LOAN AGREEMENT.*', true)]",
                                               collapse_type_res=["line"], separator_character=' ',
                                               get_all_content=True))
    rollup_pipeline.run()

    collapsed_doc = rollup_pipeline.context.output_document

    # check those matching nodes - we shouldn't have any words or lines, but
    # all other node_types should exist and the content should stay the same.
    assert len(node_matches[0].select('//word')) == 0
    assert len(node_matches[0].select('//line')) == 0
    assert len(node_matches[0].select('//content-area')) == 1
    assert len(node_matches[0].get_all_content()) == 14

    assert len(node_matches[1].select('//word')) == 0
    assert len(node_matches[1].select('//line')) == 0
    assert len(node_matches[1].select('//content-area')) == 1
    assert len(node_matches[1].get_all_content()) == 14

    assert len(node_matches[2].select('//word')) == 0
    assert len(node_matches[2].select('//line')) == 0
    assert len(node_matches[2].select('//content-area')) == 1
    assert len(node_matches[2].get_all_content()) == 500

    # how many post-rollup lines? (still have some lines, but fewer than we started with)
    assert len(test_doc.select('//line')) == 3816
    # how many post-rollup words? (still have some words, but fewer than we started with)
    assert len(test_doc.select('//word')) == 52828
    # how many post-rollup content-areas? (same number of content-areas)
    assert len(test_doc.select('//content-area')) == 817
    # what is the post-rollup length of ALL the content in the document?
    assert len(test_doc.get_root().get_all_content()) == 329792

    # verify that we can collapse line nodes AND include their children
    assert len(collapsed_doc.select("//content-area")[12].get_all_content()) == 235
