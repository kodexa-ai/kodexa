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


def find(self, content_re=".*", type_re=".*", direction=FindDirection.CHILDREN, tag_name=None, instance=1,
         tag_name_re=None, use_all_content=False):
    """
    Return a node related to this node (parent or child) that matches the content and/or type specified by regular expressions.

        >>> document.get_root().find(content_re='.*Cheese.*',instance=2)
        <kodexa.model.model.ContentNode object at 0x7f80605e53c8>

    :param content_re: The regular expression to match against the node's content; default is '.*'.
    :type content_re: str, optional
    :param type_re: The regular expression to match against the node's type; default is '.*'.
    :type type_re: str, optional
    :param direction: The direction to search (CHILDREN or PARENT); default is FindDirection.CHILDREN.
    :type direction: FindDirection(enum), optional
    :param tag_name: The tag name that must exist on the node; default is None.
    :type tag_name: str, optional
    :param instance: The instance of the matching node to return (may have multiple matches).  Value must be greater than zero; default is 1.
    :type instance: int, optional
    :param tag_name_re: The regular expression that will match the tag_name that must exist on the node;  default is None.
    :type tag_name_re: str, optional
    :param use_all_content: Match content_re against the content of this node concatenated with the content of its child nodes; default is False.
    :type use_all_content: bool, optional

    :return: Matching node (if found), or None.
    :rtype: ContentNode or None.
    """
    results = self.findall(content_re, type_re, direction, tag_name, tag_name_re, use_all_content)
    if instance < 1 or len(results) < instance:
        return None
    else:
        return results[instance-1]


def find_with_feature_value(self, feature_type, feature_name, value, direction=FindDirection.CHILDREN, instance=1):
    """
    Return a node related to this node (parent or child) that has a specific feature type, feature name, and feature value.

        >>> document.content_node.find_with_feature_value(feature_type='tag',feature_name='is_cheese',value=[1,10,'The Cheese has moved'])
        <kodexa.model.model.ContentNode object at 0x7f80605e53c8>

    :param str feature_type: The feature type.
    :param str feature_name: The feature name.
    :param Any value: The feature value.
    :param direction: The direction to search (CHILDREN or PARENT); default is FindDirection.CHILDREN.
    :type direction: FindDirection(enum), optional
    :param instance: The instance of the matching node to return (may have multiple matches).  Value must be greater than zero; default is 1.
    :type instance: int, optional

    :return: Matching node (if found), or None.
    :rtype: ContentNode or None
    """

    if instance < 1:
        return None
    else:
        return next(
            itertools.islice(self.findall_with_feature_value(feature_type, feature_name, value, direction), instance - 1, 1), None)


def findall_with_feature_value(self, feature_type, feature_name, value, direction=FindDirection.CHILDREN):
    """
    Get all nodes related to this node (parents or children) that have a specific feature type, feature name, and feature value.

        >>> document.content_node.findall_with_feature_value(feature_type='tag',feature='is_cheese', value=[1,10,'The Cheese has moved'])
        [<kodexa.model.model.ContentNode object at 0x7f80605e53c8>]

    :param str feature_type: The feature type.
    :param str feature_name: The feature name.
    :param Any value: The feature value.
    :param direction: The direction to search (CHILDREN or PARENT); default is FindDirection.CHILDREN.
    :type direction: FindDirection(enum), optional

    :return: list of the matching content nodes
    :rtype: list[ContentNode]
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
    Determines if this node is the first child of its parent or has no parent.
    
    :return: True if this node is the first child of its parent or if this node has no parent; else, False;
    :rtype: bool
    """
    if not self.parent:
        return True
    else:
        return self.index == 0


def is_last_child(self):
    """
    Determines if this node is the last child of its parent or has no parent.

    :return: True if this node is the last child of its parent or if this node has no parent; else, False;
    :rtype: bool
    """

    if not self.parent:
        return True
    else:
        return self.index == self.parent.get_last_child_index()


def get_last_child_index(self):
    """
    Returns the max index value for the children of this node. If the node has no children, returns None.

    :return: The max index of the children of this node, or None if there are no children.
    :rtype: int or None
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
    Returns the child node at the specified index. If the specified index is outside the first (0), or
    last child's index, None is returned.  
    
    Note:  documents allow for sparse representation and child nodes may not have consecutive index numbers. 
    If there isn't a child node at the specfied index, a 'virtual' node will be returned.  This 'virtual' node
    will have the type of its nearest sibling and will have an index value, but will have no features or content.

    :param int index: The index (zero-based) for the child node.

    :return: Node at index, or None if the index is outside the boundaries of child nodes.
    :rtype: ContentNode or None
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
    Determine if this node has a next sibling that matches the type specified by the type_re regex.

    :param type_re: The regular expression to match against the next sibling node's type; default is '.*'.
    :type type_re: str, optional
    :param skip_virtual: Skip virtual nodes and return the next real node; default is False.
    :type skip_virtual: bool, optional

    :return: True if there is a next sibling node matching the specified type regex; else, False.
    :rtype: bool
    """
    return self.next_node(type_re, skip_virtual=skip_virtual) is not None


def has_previous_node(self, type_re=".*", skip_virtual=False):
    """
    Determine if this node has a previous sibling that matches the type specified by the type_re regex.

    :param type_re: The regular expression to match against the previous sibling node's type; default is '.*'.
    :type type_re: str, optional
    :param skip_virtual: Skip virtual nodes and return the next real node; default is False.
    :type skip_virtual: bool, optional

    :return: True if there is a previous sibling node matching the specified type regex; else, False.
    :rtype: bool
     """
    return self.previous_node(type_re=type_re, skip_virtual=skip_virtual) is not None


def next_node(self, type_re='.*', skip_virtual=False, has_no_content=False):
    """
    Returns the next sibling content node. 
    
    Note:  This logic relies on node indexes.  Documents allow for sparse representation and child nodes may not have consecutive index numbers.
    Therefore, the next node might actually be a virtual node that is created to fill a gap in the document.  You can skip virtual nodes by setting the 
    skip_virtual parameter to False.

    :param type_re: The regular expression to match against the next sibling node's type; default is '.*'.
    :type type_re: str, optional
    :param skip_virtual: Skip virtual nodes and return the next real node; default is False.
    :type skip_virtual: bool, optional
    :param has_no_content: Allow a node that has no content to be returned; default is False.
    :type has_no_content: bool, optional

    :return: The next node or None, if no node exists
    :rtype: ContentNode or None
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
    Returns the previous sibling content node. 
    
    Note:  This logic relies on node indexes.  Documents allow for sparse representation and child nodes may not have consecutive index numbers.
    Therefore, the previous node might actually be a virtual node that is created to fill a gap in the document.  You can skip virtual nodes by setting the 
    skip_virtual parameter to False.

    :param type_re: The regular expression to match against the previous node's type; default is '.*'.
    :type type_re: str, optional
    :param skip_virtual: Skip virtual nodes and return the next real node; default is False.
    :type skip_virtual: bool, optional
    :param has_no_content: Allow a node that has no content to be returned; default is False.
    :type has_no_content: bool, optional
    :param traverse: The relationship you'd like to traverse (SIBLING, CHILDREN, PARENT, or ALL); default is Traverse.SIBLING.
    :type traverse: Traverse(enum), optional

    :return: The previous node or None, if no node exists
    :rtype: ContentNode or None
    """

    #TODO: impement/differentiate traverse logic for CHILDREN and SIBLING
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
    Search for related nodes (child or parent) that match the content and/or type specified by regular expressions.

        >>> document.content_node.findall(content_re='.*Cheese.*')
        [<kodexa.model.model.ContentNode object at 0x7f80605e53c8>,
        <kodexa.model.model.ContentNode object at 0x7f80605e53c8>]

    :param content_re: The regular expression to match against the node's content; default is '.*'.
    :type content_re: str, optional
    :param type_re: The regular expression to match against the node's type; default is '.*'.
    :type type_re: str, optional
    :param direction: The direction to search (CHILDREN or PARENT); default is FindDirection.CHILDREN.
    :type direction: FindDirection(enum), optional
    :param tag_name: The tag name that must exist on the node; default is None.
    :type tag_name: str, optional
    :param tag_name_re: The regular expression that will match the tag_name that must exist on the node;  default is None.
    :type tag_name_re: str, optional
    :param use_all_content: Match content_re against the content of this node concatenated with the content of its child nodes; default is False.
    :type use_all_content: bool, optional

    :return: List of matching content nodes
    :rtype: list[ContentNode]
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
