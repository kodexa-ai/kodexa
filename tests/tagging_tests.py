from kodexa import Document, Pipeline, NodeTagger
import os
import uuid

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

    doc.content_node.tag('name', fixed_position=[6, 11], separator=" ")

    doc.content_node.tag('lastName', fixed_position=[13, 17], separator=" ")
    print(doc.content_node.tag_text_tree())

    assert doc.content_node.get_tag_values('name', include_children=True)[0] == 'Philip'
    assert doc.content_node.get_tag_values('lastName', include_children=True)[0] == 'Dodds'


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
    features_uuids = list(set(dic['uuid'] for dic in feature_values ))
    assert len(features_uuids) == 4


    # Run the multiple tag test again, but this time pass in a tag_uuid
    document = Document.from_text(doc_string)
    pipeline = Pipeline(document)
    pipeline.add_step(NodeTagger(selector='//*', tag_to_apply='SIZE', content_re=r'(little)', node_only=False, node_tag_uuid=str(uuid.uuid4())))
    context = pipeline.run()

    # Now each of the feature values should have the same UUID
    feature_values = context.output_document.get_root().get_feature_value('tag', 'SIZE')
    features_uuids = list(set(dic['uuid'] for dic in feature_values ))
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
    assert feature_values['start'] == None and feature_values['end'] == None


def test_tag_copy():

    doc_string = "Mary had a little lamb, little lamb, little lamb.  Mary had a little lamb whose fleece was white as snow."
    # data setup - creating a single tag with multiple matches...and then copying it 
    document = Document.from_text(doc_string)
    pipeline = Pipeline(document)
    pipeline.add_step(NodeTagger(selector='//*', tag_to_apply='SIZE', content_re=r'(little)', node_only=False))
    context = pipeline.run()
    
    # now, let's copy the SIZE tags and create new ones called LAMB_INFO
    for n in document.select('//*[hasTag("SIZE")]'):
        n.copy_tag('SIZE', 'LAMB_INFO')

    # we should now have 4 feature values for 'LAMB_INFO' and 4 feature values for 'SIZE' - all with different UUIDs
    size_feature_values = context.output_document.get_root().get_feature_value('tag', 'SIZE')
    assert type(size_feature_values) == list and len(size_feature_values) == 4
    size_features_uuids = set(dic['uuid'] for dic in size_feature_values )
    assert len(list(size_features_uuids)) == 4

    lamb_info_feature_values = context.output_document.get_root().get_feature_value('tag', 'LAMB_INFO')
    assert type(lamb_info_feature_values) == list and len(lamb_info_feature_values) == 4
    lamb_info_features_uuids = set(dic['uuid'] for dic in lamb_info_feature_values )
    assert len(list(lamb_info_features_uuids)) == 4

    # the uuids for the SIZE and LAMB_INFO features should all be unique
    uuid_intersection = size_features_uuids.intersection(lamb_info_features_uuids)
    assert len(list(uuid_intersection)) == 0

    # Now test that tagging the entire node, rather than references within the node, only produce 1 feature
    pipeline = Pipeline(document)
    pipeline.add_step(NodeTagger(selector='//*', tag_to_apply='SIZE_2', content_re=r'.*(little).*', node_only=True))
    context = pipeline.run()

    # now, let's copy the SIZE_2 tags and create new ones called LAMB_INFO
    for n in document.select('//*[hasTag("SIZE_2")]'):
        n.copy_tag('SIZE_2', 'LAMB_INFO_2')

    # we should now have 1 feature values for 'LAMB_INFO_2' and 1 feature values for 'SIZE_2'
    size_2_feature_values = context.output_document.get_root().get_feature_value('tag', 'SIZE_2')
    assert type(size_2_feature_values) != list
    lamb_info_2_feature_values = context.output_document.get_root().get_feature_value('tag', 'LAMB_INFO_2')
    assert type(lamb_info_2_feature_values) != list

    # the uuids for the SIZE_2 and LAMB_INFO_2 features should be different
    assert size_2_feature_values['uuid'] != lamb_info_2_feature_values['uuid']