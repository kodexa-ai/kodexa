from kodexa import get_source
from kodexa.stores import TableDataStore


class NodeTagger:
    """
    A node tagger allows you to provide a type and content regular expression and then
    tag content in all matching nodes.

    It allows for multiple matching groups to be defined, also the ability to use all content
    and also just tag the node (ignoring the matching groups)
    """

    def __init__(self, selector, tag_to_apply, content_re=".*", use_all_content=True, node_only=False):
        self.selector = selector
        self.content_re = content_re
        self.use_all_content = use_all_content
        self.tag_to_apply = tag_to_apply
        self.node_only = node_only

    def get_name(self):
        return f"Node Tagger [selector='{self.selector}' use_all_content='{self.use_all_content}']"

    def process(self, document):
        document.content_node.tag(selector=self.selector, tag_to_apply=self.tag_to_apply, content_re=self.content_re,
                                  use_all_content=self.use_all_content,
                                  node_only=self.node_only)

        return document


class TextParser:
    """
    The text parser can load a source file as a text document and creates a single content node with the
    text
    """

    def __init__(self, decode=False, encoding="utf-8"):
        self.decode = decode
        self.encoding = encoding

    @staticmethod
    def get_name():
        return "Text Parser"

    def process(self, document):
        with get_source(document) as fh:
            data = fh.read()

            try:
                data = data.decode(self.encoding)
            except (UnicodeDecodeError, AttributeError):
                pass

            text_node = document.create_node(node_type='text', content=data if self.decode else data)
            document.content_node = text_node
            document.add_mixin('text')

        return document


class RollupTransformer:
    """
    The rollup step allows you to decide how you want to collapse content in a document by removing nodes
    while maintaining content and features as needed
    """

    def __init__(self, collapse_type_res=None, reindex: bool = True, selector: str = ".",
                 separator_character: str = None, get_all_content: bool = False):
        if collapse_type_res is None:
            collapse_type_res = []
        self.collapse_type_res = collapse_type_res
        self.reindex = reindex
        self.selector = selector
        self.separator_character = separator_character if separator_character else ''
        self.get_all_content = get_all_content

    def get_name(self):
        return "Rollup Transformer"

    def process(self, document):

        if document.get_root():
            # Select those nodes that we want to do the 'rollup' in
            selected_nodes = document.select(self.selector)
            for selected_node in selected_nodes:

                for node_type_re in self.collapse_type_res:
                    nodes = selected_node.findall(node_type_re=node_type_re)

                    final_nodes = []
                    node_ids = [node.uuid for node in nodes]
                    # Remove any nodes where the parent node is in the list as well
                    for node in nodes:
                        if not self.is_node_in_list(node.parent, node_ids):
                            final_nodes.append(node)

                    for node in final_nodes:
                        if node.parent:
                            if node.parent.content_parts:

                                # We need to insert into the content part that represents the child - then remove the child
                                content_part_index = node.parent.content_parts.index(node.index)
                                node.parent.content_parts.remove(node.index)
                                node.parent.content_parts[content_part_index:content_part_index] = node.content_parts
                                child_node_index = node.parent.children.index(node)
                                node.parent.children[child_node_index:child_node_index] = node.children
                                node.parent.children.remove(node)

                                node.parent.content = ""
                                for content_part in node.parent.content_parts:
                                    if isinstance(content_part, str):
                                        node.parent.content = node.parent.content + self.separator_character + content_part

                            else:
                                # We just need to bring the content onto the end of the parent content and remove
                                # this node
                                if self.get_all_content:
                                    node.parent.content = node.parent.content + self.separator_character + \
                                                          node.get_all_content() if node.parent.content else node.get_all_content()
                                else:
                                    node.parent.content = node.parent.content + self.separator_character + node.content \
                                        if node.parent.content else node.content
                                node.parent.children.remove(node)

                            if self.reindex:

                                # Reindex all the children
                                idx = 0
                                for child in node.parent.children:
                                    child.index = idx
                                    idx += 1
                                # Reindex content parts
                                if node.parent.content_parts:
                                    idx = 0
                                    final_cps = []
                                    for cp in node.parent.content_parts:
                                        if not isinstance(cp, str):
                                            final_cps.append(idx)
                                            idx += 1
                                        else:
                                            final_cps.append(cp)
                                    node.parent.content_parts = final_cps

        return document

    def is_node_in_list(self, node, node_ids):
        if node.uuid in node_ids:
            return True

        if node.parent:
            return self.is_node_in_list(node.parent, node_ids)
        else:
            return False


class TagsToKeyValuePairExtractor:
    """
    Extract all the tags from a document into a key/value pair table store
    """

    def __init__(self, store_name, include=[], exclude=[], include_node_content=True):
        self.store_name = store_name
        self.include = include
        self.exclude = exclude
        self.include_node_content = include_node_content

    @staticmethod
    def get_name():
        return "Extract Tags to Key/Value"

    def get_default_store(self):
        if self.include_node_content:
            return TableDataStore(columns=['tag', 'tagged_content', 'node_content'])
        else:
            return TableDataStore(columns=['tag', 'tagged_content'])

    def process(self, document, context):

        table_store = context.get_store(self.store_name, self.get_default_store())

        if document.content_node:
            self.process_node(table_store, document.content_node)

        return document

    def process_node(self, table_store, node):
        for feature in node.get_features():
            if feature.feature_type == 'tag' \
                    and (feature.name in self.include or len(self.include) == 0) \
                    and (feature.name not in self.exclude or len(self.exclude) == 0):
                tagged_text = node.content
                if 'start' in feature.value[0]:
                    tagged_text = node.content[feature.value[0]['start']:feature.value[0]['end']]

                if self.include_node_content:
                    table_store.add([feature.name, tagged_text, node.content])
                else:
                    table_store.add([feature.name, tagged_text])

        for child in node.children:
            self.process_node(table_store, child)
