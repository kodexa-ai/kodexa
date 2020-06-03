import itertools
import re
from enum import Enum

from addict import Dict

from kodexa.mixins.util import add_method_to_node


class FindDirection(Enum):
    CHILDREN = 1
    PARENT = 2


class Traverse(Enum):
    SIBLING = 1
    CHILDREN = 2
    PARENT = 3
    ALL = 4


def update_content_markup(self):
    """
    This will tag (see Feature Tagging) the expression groups identified by the regular expression
    """


def find(self, content_re=".*", type_re=".*", direction=FindDirection.CHILDREN, tag_name=None, instance=0,
         tag_name_re=None, use_all_content=False):
    """
    Search for a node that matches on the value and or type using regular expressions

        >>> document.content_node.find(content_re='.*Cheese.*',instance=2)
        <kodexa.model.model.ContentNode object at 0x7f80605e53c8>

    :param content_re: the regular expression to match the nodes content (default '.*')
    :param type_re: the regular expression to match the nodes type (default '.*')
    :param direction: the direction to search, either FindDirection.CHILDREN or FindDirection.PARENT (default CHILDREN)
    :param tag_name: the tag name that must exist
    :param instance: the instance to return (0=first)
    :param tag_name_re: the regular expression to match for the tag_name
    :param use_all_content: match the content for all child nodes to (default False)

    :return: either an instance of ContentNode (if found), or None
    """
    results = self.findall(content_re, type_re, direction, tag_name, tag_name_re, use_all_content)
    if len(results) < instance + 1:
        return None
    else:
        return results[instance]


def find_with_feature_value(self, feature_type, feature, value, direction=FindDirection.CHILDREN, instance=1):
    """
    Search for a node with a specific feature type, name and value

        >>> document.content_node.find_with_feature_value(feature_type='tag',feature='is_cheese',value=[1,10,'The Cheese has moved'])
        <kodexa.model.model.ContentNode object at 0x7f80605e53c8>

    :param feature_type: the feature type
    :param feature: the feature name
    :param value: the feature value
    :param direction: the direction to search, either FindDirection.CHILDREN or FindDirection.PARENT (default CHILDREN)
    :param instance: the instance to get (defaul 1)

    :return: either an instance of ContentNode (if found), or None
    """
    return next(
        itertools.islice(self.findall_with_feature_value(feature_type, feature, value, direction), instance - 1, 1),
        None)


def findall_with_feature_value(self, feature_type, feature_name, value, direction=FindDirection.CHILDREN):
    """
    Search for all nodes with a specific feature type, name and value

        >>> document.content_node.findall_with_feature_value(feature_type='tag',feature='is_cheese', value=[1,10,'The Cheese has moved'])
        [<kodexa.model.model.ContentNode object at 0x7f80605e53c8>]

    :param feature_type: the feature type
    :param feature_name: the feature name
    :param value: the feature value
    :param direction: the direction to search, either FindDirection.CHILDREN or FindDirection.PARENT (default CHILDREN)

    :return: list of the matching content nodes
    """
    if self.has_feature(feature_type, feature_name) and value == self.get_feature_value(feature_type, feature_name):
        yield self

    if direction is FindDirection.CHILDREN:
        for child in self.get_children():
            yield from child.findall_with_feature_value(feature_type, feature_name, value, direction)
    else:
        if self.parent:
            yield from self.parent.findall_with_feature_value(feature_type, feature_name, value, direction)


def is_first_child(self):
    """
    Returns True if this is the first child, also True if it has no parent

    :return: True if this is the first child
    """

    if not self.parent:
        return True
    else:
        return self.index == 0


def is_last_child(self):
    """
    Returns True if this is the last child, also True if it has no parent

    :return: True if this is the first child
    """

    if not self.parent:
        return True
    else:
        return self.index == self.parent.get_last_child_index()


def get_last_child_index(self):
    """
    Returns the max index value for the children of this node, if the node has no children
    it returns None

    :return: Thhe max index of the children of this node, or None is no children
    """

    if not self.children:
        return None

    max_index = 0
    for child in self.children:
        if child.index > max_index:
            max_index = child.index

    return max_index


def get_node_at_index(self, index):
    """
    Returns the node at a specific index,  if the index it outside the first (0), or
    last index it will return null, if not it will return the node at index, if there
    isn't a node at that index it will return a 'virtual' node that will represent
    the node to the side of this node and have an index and no features or content

    :param index: The index (zero-based) for the child node

    :return: Node at index, or None is the index is outside the boundaries of child nodes
    """
    if self.children:

        if index < self.children[0].index:
            virtual_node = self.document.create_node(type=self.children[0].type, virtual=True, parent=self,
                                                     index=index)
            return virtual_node

        last_child = None
        for child in self.children:
            if child.index < index:
                last_child = child
            elif child.index == index:
                return child
            else:
                break

        if last_child:
            if last_child.index is not index and index < self.children[-1].index:
                virtual_node = self.document.create_node(type=last_child.type, virtual=True, parent=self,
                                                         index=index)
                return virtual_node
        else:
            return None
    else:
        return None


def has_next_node(self, type_re=".*", skip_virtual=False):
    """
    Returns True if the node has a next node

    :param type_re: Type name (regular expression)
    :param skip_virtual: True to skip any virtual nodes and only return the next real node (default False)

    :return: True if there is a next sibling node
    """
    return self.next_node(type_re, skip_virtual=skip_virtual) is not None


def has_previous_node(self, type_re=".*", skip_virtual=False):
    """
     Returns True if the node has a previous node

    :param type_re: Type name (regular expression)
    :param skip_virtual: True to skip any virtual nodes and only return the next real node (default False)

     :return: True if there is a previous sibling node
     """
    return self.previous_node(type_re=type_re, skip_virtual=skip_virtual) is not None


def next_node(self, type_re='.*', skip_virtual=False, has_no_content=False, traverse=Traverse.SIBLING):
    """
    Returns the next sibling content node, note that this logic is based on the index,
    therefore the next node might actually be a virtual node that is created to fill a gap
    in the document,  since the index allows for sparse documents

    :param type_re: the regular expression for the type of node (default '.*')
    :param skip_virtual: True to skip any virtual nodes and only return the next real node (default False)
    :param has_no_content: True if you only want to return a node that has no content
    :param traverse: By default we traverse siblings, however you can include CHILDREN, PARENT or ALL

    :return: the next node or None if no node exists
    """
    search_index = self.index + 1
    compiled_type_re = re.compile(type_re)

    while True:
        node = self.parent.get_node_at_index(search_index)

        if not node:
            return node

        if compiled_type_re.match(node.type) and (not skip_virtual or not node.virtual):
            if (not has_no_content) or (has_no_content and not node.content):
                return node
        if not node:
            return node
        search_index += 1


def previous_node(self, type_re='.*', skip_virtual=False, has_no_content=False, traverse=Traverse.SIBLING):
    """
    Returns the previous sibling content node, note that this logic is based on the index,
    therefore the next node might actually be a virtual node that is created to fill a gap
    in the document,  since the index allows for sparse documents

    :param type_re: the regular expression for the type of node (default '.*')
    :param skip_virtual: True to skip any virtual nodes and only return the next real node (default False)
    :param has_no_content: True if you only want to return a node that no content
    :param traverse: By default we traverse siblings, however you can include CHILDREN, PARENT or ALL

    :return: the previous node or None if no node exists
    """
    if self.index == 0:
        if traverse == traverse.ALL or traverse == traverse.PARENT and self.parent:
            # Lets look for a previous node on the parent
            return self.parent.previous_node(type_re, skip_virtual, has_no_content, traverse)
        else:
            return None

    search_index = self.index - 1
    compiled_type_re = re.compile(type_re)

    while True:
        node = self.parent.get_node_at_index(search_index)

        if not node:
            return node

        if compiled_type_re.match(node.type) and (not skip_virtual or not node.virtual):
            if (not has_no_content) or (has_no_content and not node.content):
                return node

        search_index -= 1


def findall(self, content_re=".*", type_re=".*", direction=FindDirection.CHILDREN, tag_name=None,
            tag_name_re=None, use_all_content=False):
    """
    Search for nodes that matches on the value and or type using regular expressions

        >>> document.content_node.findall(content_re='.*Cheese.*')
        [<kodexa.model.model.ContentNode object at 0x7f80605e53c8>,
        <kodexa.model.model.ContentNode object at 0x7f80605e53c8>]

    :param content_re: the regular expression to match the nodes content (default '.*')
    :param type_re: the regular expression to match the nodes type (default '.*')
    :param direction: the direction to search, either FindDirection.CHILDREN or FindDirection.PARENT (default CHILDREN)
    :param tag_name: the tag name that must exist
    :param tag_name_re: the regular expression to match for the tag_name
    :param use_all_content: match the content for all child nodes to (default False)

    :return: list of matching content nodes


    """
    value_compiled = re.compile(content_re)
    type_compiled = re.compile(type_re)
    if tag_name_re:
        tag_name_re_compiled = re.compile(tag_name_re)
    else:
        tag_name_re_compiled = None
    return self.findall_compiled(value_compiled, type_compiled, direction, tag_name, tag_name_re_compiled,
                                 use_all_content)


def findall_compiled(self, value_re_compiled, type_re_compiled, direction, tag_name, tag_name_compiled,
                     use_all_content):
    """
    Search for a node that matches on the value and or type using
    regular expressions using compiled expressions
    """
    hits = []

    if use_all_content:
        content = self.get_all_content()
    else:
        content = "" if not self.get_content() else self.get_content()

    if value_re_compiled.match(content) and type_re_compiled.match(self.get_type()):

        if tag_name_compiled:
            for tag_name in self.get_tags():
                if tag_name_compiled.match(tag_name):
                    hits.append(self)
                    break

        elif not tag_name or self.has_tag(tag_name):
            hits.append(self)

    if direction is FindDirection.CHILDREN:
        for child in self.get_children():
            hits.extend(child.findall_compiled(value_re_compiled, type_re_compiled, direction, tag_name,
                                               tag_name_compiled, use_all_content))
    else:
        if self.parent:
            hits.extend(self.parent.findall_compiled(value_re_compiled, type_re_compiled, direction, tag_name,
                                                     tag_name_compiled, use_all_content))

    return hits


class CoreMixin:

    @staticmethod
    def get_name():
        return "core"

    @staticmethod
    def get_renderer(document):
        return None

    @staticmethod
    def apply_to(node):
        add_method_to_node(find, node)
        add_method_to_node(findall, node)
        add_method_to_node(findall_compiled, node)
        add_method_to_node(find_with_feature_value, node)
        add_method_to_node(findall_with_feature_value, node)

        add_method_to_node(get_node_at_index, node)
        add_method_to_node(has_next_node, node)
        add_method_to_node(has_previous_node, node)
        add_method_to_node(next_node, node)
        add_method_to_node(previous_node, node)
        add_method_to_node(get_last_child_index, node)
        add_method_to_node(is_first_child, node)
        add_method_to_node(is_last_child, node)
