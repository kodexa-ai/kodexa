from kodexa import Document


def test_fixed_tagging():
    doc = Document.from_text("Hello Philip")
    doc.content_node.tag('name', fixed_position=[6, 12])

    assert doc.content_node.get_tag_values('name')[0] == 'Philip'


def test_fixed_tagging_with_child():
    doc = Document.from_text("Hello")
    doc.content_node.add_child_content("text", "Philip")
    doc.content_node.add_child_content("text", "Dodds")

    #Hello Philip Dodds
    #012345678901234567

    doc.content_node.tag('name', fixed_position=[6, 11], separator=" ")

    doc.content_node.tag('lastName', fixed_position=[13, 17], separator=" ")
    print(doc.content_node.tag_text_tree())

    assert doc.content_node.get_tag_values('name', include_children=True)[0] == 'Philip'
    assert doc.content_node.get_tag_values('lastName', include_children=True)[0] == 'Dodds'
