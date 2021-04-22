from kodexa import get_source
from kodexa.stores import TableDataStore


class KodexaProcessingException(Exception):
    """
    This is a specialized exception, if thrown while in the Kodexa Platform we will include the
    additional exception details so that they can be presented back to the user
    """

    def __init__(self, message, description, advice=None, documentation_url=None):
        self.description = description
        """The description of the problem, this is longer description"""
        self.advice = advice
        """Any advice on how to handle the problem, this can also include markdown to help present possible solutions"""
        self.message = message
        """A short message to express the problem"""
        self.documentation_url = documentation_url
        """A link to a URL where the user might find more information on the problem"""
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}  {self.description}'


class NodeTagger:
    """A node tagger allows you to provide a type and content regular expression and then
    tag content in all matching nodes.
    
    It allows for multiple matching groups to be defined, also the ability to use all content
    and also just tag the node (ignoring the matching groups)
    """

    def __init__(self, selector, tag_to_apply, content_re=".*", use_all_content=True, node_only=False,
                 node_tag_uuid=None):
        self.selector = selector
        """The selector to use to find the node(s) to tag"""
        self.content_re = content_re
        """A regular expression used to match the content in the identified nodes"""
        self.use_all_content = use_all_content
        """A flag that will assume that all content should be tagged (there will be no start/end)"""
        self.tag_to_apply = tag_to_apply
        """The tag to apply to the node(s)"""
        self.node_only = node_only
        """Tag the node only and no content"""
        self.node_tag_uuid = node_tag_uuid
        """The UUID to use on the tag"""

    def get_name(self):
        """ """
        return f"Node Tagger [selector='{self.selector}' use_all_content='{self.use_all_content}']"

    def process(self, document):
        """
        """
        document.content_node.tag(selector=self.selector, tag_to_apply=self.tag_to_apply, content_re=self.content_re,
                                  use_all_content=self.use_all_content,
                                  node_only=self.node_only, tag_uuid=self.node_tag_uuid)

        return document


class NodeTagCopy:
    """The NodeTagCopy action allows you select nodes specified by the selector and create copies of the existing_tag (if it exists) with the new_tag_name.
    If a tag with the 'existing_tag_name' does not exist on a selected node, no action is taken for that node.
    """

    def __init__(self, selector, existing_tag_name, new_tag_name):
        self.selector = selector
        """The selector to match the nodes"""
        self.existing_tag_name = existing_tag_name
        """The existing tag name that will be the source"""
        self.new_tag_name = new_tag_name
        """The new tag name that will be the destination"""

    def get_name(self):
        """ """
        return f"Node Tag Copy [selector='{self.selector}' existing_tag_name='{self.existing_tag_name} new_tag_name={self.new_tag_name}']"

    def process(self, document):
        """
        """
        document.content_node.copy_tag(selector=self.selector, existing_tag_name=self.existing_tag_name,
                                       new_tag_name=self.new_tag_name)
        return document


class TextParser:
    """Parser to load a source file as a text document.  The text from the document may be placed on the root ContentNode or on the root's child nodes (controlled by lines_as_child_nodes).
    """

    def __init__(self, encoding="utf-8", lines_as_child_nodes=False):
        self.encoding = encoding
        """The encoding that should be used when attempting to decode data  (default 'utf-8')"""
        self.lines_as_child_nodes = lines_as_child_nodes
        """If True, the lines of the file will be set as children of the root ContentNode; otherwise, the entire file content is set on the root ContentNode.  (default False)"""

    @staticmethod
    def get_name():
        """ """
        return "Text Parser"

    def decode_text(self, data):
        """
        """
        try:
            data = data.decode(self.encoding)
        except (UnicodeDecodeError, AttributeError):
            pass
        return data

    def process(self, document):
        """
        """
        with get_source(document) as fh:

            if self.lines_as_child_nodes:
                lines = fh.readlines()
                document.content_node = document.create_node(node_type='text')

                for data in lines:
                    text_node = document.create_node(node_type='text', content=self.decode_text(data).strip())
                    document.content_node.add_child(text_node)
            else:
                data = fh.read()
                text_node = document.create_node(node_type='text', content=self.decode_text(data))
                document.content_node = text_node

            document.add_mixin('text')

        return document


class RollupTransformer:
    """The rollup step allows you to decide how you want to collapse content in a document by removing nodes
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
        """ """
        return "Rollup Transformer"

    def process(self, document):
        """

        """

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
        """

        Args:
          node: 
          node_ids: 

        Returns:

        """
        if node.uuid in node_ids:
            return True

        if node.parent:
            return self.is_node_in_list(node.parent, node_ids)
        else:
            return False


class TagsToKeyValuePairExtractor:
    """Extract all the tags from a document into a key/value pair table store"""

    def __init__(self, store_name, include=[], exclude=[], include_node_content=True):
        self.store_name = store_name
        self.include = include
        self.exclude = exclude
        self.include_node_content = include_node_content

    @staticmethod
    def get_name():
        """ """
        return "Extract Tags to Key/Value"

    def get_default_store(self):
        """ """
        if self.include_node_content:
            return TableDataStore(columns=['tag', 'tagged_content', 'node_content'])
        else:
            return TableDataStore(columns=['tag', 'tagged_content'])

    def process(self, document, context):
        """
        """

        table_store = context.get_store(self.store_name, self.get_default_store())

        if document.content_node:
            self.process_node(table_store, document.content_node)

        return document

    def process_node(self, table_store, node):
        """
        """
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
