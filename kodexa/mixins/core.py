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


def get_all_content(self, separator=" "):
    """
    This will build the complete content, including the content of children.

        >>> document.content_node.get_all_content()
        "This string is made up of multiple nodes"

    :param separator: the separate to use to join the content together (default is " ")
    """
    s = ""
    if self.get_content():
        s += self.get_content()
        s += separator
    for child in self.children:
        s += child.get_all_content(separator)
        s += separator
    return s.strip()


def move_child_to_parent(self, target_child, target_parent):
    """
    This will move the target_child, which must be a child of the node, to a new parent.

    It will be added to the end of the parent

        >>> document.content_root.move_child_to_parent(document.content_root.find(type_ref='line'), document.content_root)

    :param target_child: the child node that needs to be moved
    :param target_parent: the parent to attach this node to
    """
    self.children.remove(target_child)
    target_parent.add_child(target_child)


def adopt_children(self, children, replace=False):
    """
    This will take a list of content nodes and adopt them under this node, ensuring they are
    re-parented.

    It will be added to the end of the parent

        >>> document.content_root.adopt_children(document.content_root.find(type_ref='line'), replace=True)

    :param children: a list of the children to adopt
    :param replace: if True the node will remove all current children and replace them with the new list
    """

    if replace:
        for child in self.children:
            self.parent = None
        self.children = []

    for child in children:
        self.add_child(child)


def remove_tag(self, tag_name):
    """
        This will remove a tag from the given node

             >>> document.content_node.remove_tag(tag_name='foo')

        :param tag_name: The tag to be applied to the nodes in range
        """
    self.remove_feature('tag', tag_name)


def collect_nodes_to(self, end_node):
    """
    Return a list of the sibling nodes between the current node and the end node

         >>> document.content_node.children[0].collect_nodes_to(end_node=document.content_node.children[5])

    :param end_node: The node to end at
    """
    nodes = []
    current_node = self
    while current_node.uuid != end_node.uuid:
        nodes.append(current_node)
        if current_node.has_next_node():
            current_node = current_node.next_node()
        else:
            break
    return nodes


def tag_nodes_to(self, end_node, tag_name):
    """
    Tag all the nodes from this node to the end node with the given tag name

          >>> document.content_node.children[0].tag_nodes_to(document.content_node.children[5], tag_name='foo')

     :param end_node: The node to end with
     :param tag_name: The tag name
     """
    [node.tag(tag_name) for node in self.collect_nodes_to(end_node)]


def tag_range(self, start_content_re, end_content_re, tag_name, type_re='.*', use_all_content=False):
    """
    This will tag all the child nodes between the start and end content regular expressions

         >>> document.content_node.tag_range(start_content_re='.*Cheese.*', end_content_re='.*Fish.*', tag_name='foo')

    :param start_content_re: The regular expression to match the starting child
    :param end_content_re: The regular expression to match the ending child
    :param tag_name: The tag to be applied to the nodes in range
    :param type_re: The type to match (default is all)
    :param use_all_content: Use full content (including child nodes, default is False)
    """

    # Could be line, word, or content-area
    all_nodes = self.findall(type_re=type_re)

    start_index_list = [n_idx for n_idx, node in enumerate(all_nodes)
                        if re.compile(start_content_re).match(node.get_all_content()
                                                              if use_all_content else node.content)]
    end_index_list = [n_idx for n_idx, node in enumerate(all_nodes)
                      if re.compile(end_content_re).match(node.get_all_content()
                                                          if use_all_content else node.content)]

    start_index = 0 if start_content_re == '' else \
        start_index_list[0] if len(start_index_list) > 0 else None
    if start_index is not None:
        end_index_list = [i for i in end_index_list if i >= start_index]

    end_index = len(all_nodes) if end_content_re == '' else \
        end_index_list[0] if len(end_index_list) > 0 else len(all_nodes)

    if start_index is not None:
        [node.tag(tag_name) for node in all_nodes[start_index:end_index]]


def tag(self, tag_name, type_re=None, content_re=None,
        use_all_content=False, node_only=False, include_children=False,
        fixed_position=None, data=None):
    """
    This will tag (see Feature Tagging) the expression groups identified by the regular expression.

        >>> document.content_node.find(content_re='.*Cheese.*').tag('is_cheese')

    :param tag_name: the name of the tag to apply
    :param type_re: regular expression to make the type (default .*)
    :param content_re: the regular expression that you wish to use to tag, note that we will create a tag for each matching group
    :param use_all_content: apply the regular expression to the all_content (include content from child nodes)
    :param node_only: Ignore the matching groups and tag the whole node
    :param include_children: Include recurse into children and tag where matching
    :param fixed_position: use a fixed position, supplied as a tuple i.e. - (4,10) tag from position 4 to 10 (default None)
    :param data: Attach the a dictionary of data for the given tag
    """

    type_match = True

    if fixed_position:
        self.add_feature('tag', tag_name,
                         Tag(fixed_position[0], fixed_position[1], self.content[fixed_position[0]:fixed_position[1]],
                             data))
    else:
        if type_re:
            type_re_compiled = re.compile(type_re)
            type_match = type_re_compiled.match(self.type)

        if type_match:
            if not content_re:
                self.add_feature('tag', tag_name, Tag(data=data))
            else:
                pattern = re.compile(content_re)
                if not use_all_content:
                    if self.content:
                        content = self.content
                    else:
                        return
                else:
                    content = self.get_all_content()

                match = pattern.match(content)
                if match:
                    if node_only:
                        self.add_feature('tag', tag_name, Tag(data=data))
                    else:
                        for index, m in enumerate(match.groups()):
                            idx = index + 1
                            self.add_feature('tag', tag_name,
                                             Tag(match.start(idx), match.end(idx), match.group(idx), data=data))

    if include_children:
        for child in self.children:
            child.tag(tag_name, type_re, content_re, use_all_content, node_only, include_children, fixed_position)


def get_tags(self):
    """
    Returns a list of the names of the tags on the given node

        >>> document.content_node.find(content_re='.*Cheese.*').get_tags()
        ['is_cheese']

    :return: A list of the tag name
    """
    return [i.name for i in self.get_features_of_type("tag")]


def get_tag(self, tag_name):
    """
    Returns the value of a tag, this can be either a single list [start,end,value] or if multiple parts of the
    content of this node match you can end up with a list of lists i.e. [[start1,end1,value1],[start2,end2,value2]]

        >>> document.content_node.find(content_re='.*Cheese.*').get_tag('is_cheese')
        [0,10,'The Cheese Moved']

    :param tag_name: The name of the tag

    :return: The tagged location and value (or a list if more than one)
    """
    return self.get_feature_value('tag', tag_name)


def get_all_tags(self):
    """
    Returns a list of the names of the tags on the given node and all its children

        >>> document.content_node.find(content_re='.*Cheese.*').get_all_tags()
        ['is_cheese']

    :return: A list of the tag names
    """
    tags = []
    tags.extend(self.get_tags())
    for child in self.children:
        tags.extend(child.get_all_tags())
    return list(set(tags))


def has_tags(self):
    """
    Returns True if the node has any tags

        >>> document.content_node.find(content_re='.*Cheese.*').has_tags()
        True

    :return: True if node has any tags else False
    """
    return len([i.value for i in self.get_features_of_type("tag")]) > 0


def has_tag(self, tag):
    """
    Returns True if the node has given tag

        >>> document.content_node.find(content_re='.*Cheese.*').has_tag('is_cheese')
        True
        >>> document.content_node.find(content_re='.*Cheese.*').has_tag('is_fish')
        False

    :param tag: The tag name

    :return: True if node has tag else False
    """
    for feature in self.get_features():
        if feature.feature_type == 'tag' and feature.name == tag:
            return True
    return False


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
        add_method_to_node(get_all_content, node)
        add_method_to_node(get_all_tags, node)
        add_method_to_node(get_tag, node)
        add_method_to_node(find, node)
        add_method_to_node(tag, node)
        add_method_to_node(tag_range, node)
        add_method_to_node(has_tag, node)
        add_method_to_node(has_tags, node)
        add_method_to_node(findall, node)
        add_method_to_node(findall_compiled, node)
        add_method_to_node(find_with_feature_value, node)
        add_method_to_node(findall_with_feature_value, node)
        add_method_to_node(get_tags, node)
        add_method_to_node(move_child_to_parent, node)
        add_method_to_node(adopt_children, node)
        add_method_to_node(remove_tag, node)
        add_method_to_node(collect_nodes_to, node)
        add_method_to_node(tag_nodes_to, node)
        add_method_to_node(get_node_at_index, node)
        add_method_to_node(has_next_node, node)
        add_method_to_node(has_previous_node, node)
        add_method_to_node(next_node, node)
        add_method_to_node(previous_node, node)
        add_method_to_node(get_last_child_index, node)
        add_method_to_node(is_first_child, node)
        add_method_to_node(is_last_child, node)


class Tag(Dict):

    def __init__(self, start=None, end=None, value=None, data=None):
        self.start = start
        self.end = end
        self.value = value
        self.data = None
