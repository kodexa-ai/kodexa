import os

from anytree import AsciiStyle

from kodexa import Document


def get_test_directory():
    return os.path.dirname(os.path.abspath(__file__)) + "/../test_documents/"


def test_kodexa_service():
    from anytree import RenderTree
    document = Document.from_msgpack(open(os.path.join(get_test_directory(), 'news-tagged.kdxa'), 'rb').read())
    for pre, _, node in RenderTree(document.content_node):
        print("%s%s" % (pre, f"{node.content} ({node.node_type})"))

    print(RenderTree(document.content_node, style=AsciiStyle()).by_attr("type"))

    print(RenderTree(document.select_as_node('//ul'), style=AsciiStyle()).by_attr("type"))
