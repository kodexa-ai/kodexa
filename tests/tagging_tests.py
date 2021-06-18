import pytest

from kodexa import Document, Pipeline, NodeTagger, NodeTagCopy
import os
import uuid
import pandas as pd
import collections


def get_test_directory():
    return os.path.dirname(os.path.abspath(__file__)) + "/../test_documents/"


def test_fixed_tagging():
    doc = Document.from_text("Hello Philip")
    doc.content_node.tag('name', fixed_position=[6, 12])

    assert doc.content_node.get_tag_values('name')[0] == 'Philip'


def test_fixed_tagging_with_child():
    doc = Document.from_text("Hello")
    doc.content_node.add_child_content("text", "Philip")
    doc.content_node.add_child_content("text", "Dodds")

    # Hello Philip Dodds
    # 012345678901234567

    doc.content_node.tag('name', fixed_position=[6, 12], separator=" ")

    doc.content_node.tag('lastName', fixed_position=[13, 18], separator=" ")
    print(doc.content_node.tag_text_tree())

    assert doc.content_node.get_tag_values('name', include_children=True)[0] == 'Philip'
    assert doc.content_node.get_tag_values('lastName', include_children=True)[0] == 'Dodds'
    assert doc.content_node.get_all_content()[6:12] == 'Philip'
    assert doc.content_node.get_all_content()[13:18] == 'Dodds'


def test_node_only_tagging():
    doc = Document.from_text("Hello World")

    doc.content_node.tag(node_only=True, content_re="Hello World", tag_to_apply="test")
    assert len(doc.content_node.get_tag_values("test")) == 1

    doc.content_node.tag(node_only=True, content_re="Hello Cheese", tag_to_apply="test2")
    assert len(doc.content_node.get_tag_values("test2")) == 0


def test_tag_multiple_regex_matches():
    doc_string = "Mary had a little lamb, little lamb, little lamb.  Mary had a little lamb whose fleece was white as snow."

    document = Document.from_text(doc_string)
    pipeline = Pipeline(document)
    pipeline.add_step(NodeTagger(selector='//*', tag_to_apply='SIZE', content_re=r'(little)', node_only=False))
    context = pipeline.run()

    tags = context.output_document.get_root().get_all_tags()
    assert len(tags) == 1

    # we expect 4 tags to be applied, one for each instance of the word 'little'
    feature_values = context.output_document.get_root().get_feature_value('tag', 'SIZE')
    assert type(feature_values) == list and len(feature_values) == 4
    assert feature_values[2]['start'] == 37
    assert feature_values[2]['end'] == 43

    # Because we didn't pass in a tag_uuid to the NodeTagger, each of the feature values should have a different UUID
    features_uuids = list(set(dic['uuid'] for dic in feature_values))
    assert len(features_uuids) == 4

    # Run the multiple tag test again, but this time pass in a tag_uuid
    document = Document.from_text(doc_string)
    pipeline = Pipeline(document)
    pipeline.add_step(NodeTagger(selector='//*', tag_to_apply='SIZE', content_re=r'(little)', node_only=False,
                                 node_tag_uuid=str(uuid.uuid4())))
    context = pipeline.run()

    # Now each of the feature values should have the same UUID
    feature_values = context.output_document.get_root().get_feature_value('tag', 'SIZE')
    features_uuids = list(set(dic['uuid'] for dic in feature_values))
    assert len(features_uuids) == 1

    # Now test that tagging the entire node, rather than references within the node, only produce 1 feature
    document = Document.from_text(doc_string)
    pipeline = Pipeline(document)
    pipeline.add_step(NodeTagger(selector='//*', tag_to_apply='SIZE_2', content_re=r'.*(little).*', node_only=True))
    context = pipeline.run()

    tags = context.output_document.get_root().get_all_tags()
    assert len(tags) == 1

    # we expect one tag to be applied and there to be no start or end value
    feature_values = context.output_document.get_root().get_feature_value('tag', 'SIZE_2')
    assert feature_values['start'] is None and feature_values['end'] is None


def test_tag_copy():
    doc_string = "Mary had a little lamb, little lamb, little lamb.  Mary had a little lamb whose fleece was white as snow."
    # data setup - creating a single tag with multiple matches...and then copying it
    document = Document.from_text(doc_string)
    pipeline = Pipeline(document)
    pipeline.add_step(NodeTagger(selector='//*', tag_to_apply='SIZE', content_re=r'(little)', node_only=False))
    context = pipeline.run()

    # both existing and new tag names must be provided, and they must be different, test for that first.
    for n in document.select('//*[hasTag("SIZE")]'):
        n.copy_tag(existing_tag_name=None, new_tag_name='NewTagNone')

    for n in document.select('//*[hasTag("SIZE")]'):
        n.copy_tag(existing_tag_name='SIZE', new_tag_name=None)

    for n in document.select('//*[hasTag("SIZE")]'):
        n.copy_tag(existing_tag_name='SIZE', new_tag_name='SIZE')

    # verify that the only tag that exists is tag 'SIZE' and that there are only 4 feature values for it
    assert len(document.get_root().get_all_tags()) == 1
    assert 'SIZE' in document.get_root().get_all_tags()

    # now, let's copy the SIZE tags and create new ones called LAMB_INFO
    # reusing the previously tagged document and testing out NodeTagCopy action
    pipeline = Pipeline(document)
    pipeline.add_step(NodeTagCopy(selector='//*[hasTag("SIZE")]', existing_tag_name='SIZE', new_tag_name='LAMB_INFO'))
    context = pipeline.run()

    # we should now have 4 feature values for 'LAMB_INFO' and 4 feature values for 'SIZE' - all with different UUIDs
    size_feature_values = context.output_document.get_root().get_feature_value('tag', 'SIZE')
    assert type(size_feature_values) == list and len(size_feature_values) == 4

    lamb_info_feature_values = context.output_document.get_root().get_feature_value('tag', 'LAMB_INFO')
    assert type(lamb_info_feature_values) == list and len(lamb_info_feature_values) == 4
    lamb_info_features_uuids = set(dic['uuid'] for dic in lamb_info_feature_values)
    assert len(list(lamb_info_features_uuids)) == 4

    # Now test that tagging the entire node, rather than references within the node, only produce 1 feature
    document = Document.from_text(doc_string)  # starting with a clean document
    pipeline = Pipeline(document)
    pipeline.add_step(NodeTagger(selector='//*', tag_to_apply='SIZE_2', content_re=r'.*(little).*', node_only=True))
    context = pipeline.run()

    # now, let's copy the SIZE_2 tags and create new ones called LAMB_INFO (using node's tag_copy)
    for n in document.select('//*[hasTag("SIZE_2")]'):
        n.copy_tag(existing_tag_name='SIZE_2', new_tag_name='LAMB_INFO_2')

    # we should now have 1 feature values for 'LAMB_INFO_2' and 1 feature values for 'SIZE_2'
    size_2_feature_values = context.output_document.get_root().get_feature_value('tag', 'SIZE_2')
    assert type(size_2_feature_values) != list
    lamb_info_2_feature_values = context.output_document.get_root().get_feature_value('tag', 'LAMB_INFO_2')
    assert type(lamb_info_2_feature_values) != list

    # now we need to test that when features are related (indicated by the same tag_uuid), they remain related when copying
    document = Document.from_text(doc_string)  # starting with a clean document
    pipeline = Pipeline(document)
    pipeline.add_step(
        NodeTagger(selector='//*', tag_to_apply='FLEECE_INFO', content_re=r'((white|snow))', node_only=False,
                   node_tag_uuid=str(uuid.uuid4())))
    context = pipeline.run()

    # now, let's copy the SIZE tags and create new ones called LAMB_INFO
    pipeline = Pipeline(document)  # reusing the previously tagged document & testing out the NodeTagCopy action
    pipeline.add_step(
        NodeTagCopy(selector='//*[hasTag("FLEECE_INFO")]', existing_tag_name='FLEECE_INFO', new_tag_name='WOOL_INFO'))
    context = pipeline.run()

    # The feature values should have the same UUID - for both WOOL_INFO and FLEECE_INFO
    wool_values = context.output_document.get_root().get_feature_value('tag', 'WOOL_INFO')
    assert type(wool_values) == list and len(wool_values) == 2
    wool_uuids = set(dic['uuid'] for dic in wool_values)
    assert len(list(wool_uuids)) == 1

    fleece_info_values = context.output_document.get_root().get_feature_value('tag', 'FLEECE_INFO')
    assert type(fleece_info_values) == list and len(fleece_info_values) == 2


@pytest.mark.skip
def test_tagging_issue_with_html():
    kdxa_doc = Document.from_kdxa(get_test_directory() + 'tagging_issue.kdxa')

    print(kdxa_doc.content_node.get_all_content())
    # assert "IIJ" == kdxa_doc.content_node.get_all_content()[4277:4280]

    print(kdxa_doc.content_node.get_all_content()[4200:4400])
    print("-----")
    print(kdxa_doc.content_node.get_all_content()[4160 + 116:4400])
    # Now we tag the same location and try and get the content from the tag
    kdxa_doc.content_node.tag("test_tag", use_all_content=True, node_only=False, fixed_position=(4277, 4280))

    print("-------")

    node = kdxa_doc.select('//*[hasTag("test_tag")]')[0]
    feature = node.get_feature_value("tag", "test_tag")
    print(feature)
    all_content = node.get_all_content()

    print(node.get_all_content()[feature.start:feature.end])
    print(node.get_all_content()[feature.start - 20:feature.end + 20])
    print(kdxa_doc.select_as_node("//*[hasTag('test_tag')]").get_all_content())

    print(kdxa_doc.select("//*[hasTag('test_tag')]")[0].get_all_content().index('ers. IIJ'))
    assert "IIJ" == kdxa_doc.select("//*[hasTag('test_tag')]")[0].get_all_content()[feature.start:feature.end]


def test_fax_tagging():
    kdxa_doc = Document.from_kdxa(get_test_directory() + 'fax.kdxa')

    kdxa_doc.select_as_node("//line").tag('cheesy', fixed_position=[5, 30])
    print(kdxa_doc.select_as_node("//line").get_all_content())


def test_fax2tagging():
    kdxa_doc = Document.from_kdxa(get_test_directory() + 'fax2.kdxa')

    kdxa_doc.content_node.tag("phone", use_all_content=True, fixed_position=[171, 183])
    assert kdxa_doc.select_as_node("//*[hasTag('phone')]").get_all_content() == '785-368-1772'
