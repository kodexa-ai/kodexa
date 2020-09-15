from kodexa import Document


def test_fixed_tagging():
    doc = Document.from_text("Hello Philip")
    doc.content_node.tag('name', fixed_position=[6, 12])

    assert doc.content_node.get_tag_values('name')[0] == 'Philip'


def test_fixed_tagging_with_child():
    doc = Document.from_text("Hello")
    doc.content_node.add_child_content("text", "Philip")
    doc.content_node.add_child_content("text", "Dodds")
    doc.content_node.tag('name', fixed_position=[6, 12])

    assert doc.content_node.get_tag_values('name', include_children=True)[0] == 'Philip'
