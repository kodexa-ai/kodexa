import dataclasses
import itertools
import json
import os
import re
import shutil
import uuid
from enum import Enum
from pathlib import Path
from typing import List, Optional, Any

import msgpack
from addict import Dict

from kodexa.mixins import registry


class Store:
    """
    Base interface for Store
    """

    def get_name(self):
        pass

    def merge(self, other_store):
        pass

    def to_dict(self):
        pass

    def set_pipeline_context(self, pipeline_context):
        pass

    def count(self):
        pass


class RemoteStore:
    """
    A remote store is one that refers to a Kodexa platform  instance
    """

    def get_ref(self) -> str:
        """
        Get the reference to the store on the platform (i.e. kodexa/my-store:1.1.0)

        :return: The reference
        """
        pass


class DocumentMetadata(Dict):
    """
    A flexible dict based approach to capturing metadata for the document
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Tag(Dict):

    def __init__(self, start=None, end=None, value=None, data=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start = start
        self.end = end
        self.value = value
        self.data = data


class FindDirection(Enum):
    CHILDREN = 1
    PARENT = 2


class Traverse(Enum):
    SIBLING = 1
    CHILDREN = 2
    PARENT = 3
    ALL = 4


class ContentNode(object):
    """
    A Content Node identifies a section of the document containing logical
    grouping of information.

    The node will have content and can include any number of features.

    You should always create a node using the Document's create_node method to
    ensure that the correct mixins are applied.

        >>> new_page = document.create_node(node_type='page')
        <kodexa.model.model.ContentNode object at 0x7f80605e53c8>
        >>> current_content_node.add_child(new_page)

    or

        >>> new_page = document.create_node(node_type='page', content='This is page 1')
        <kodexa.model.model.ContentNode object at 0x7f80605e53c8>
        >>> current_content_node.add_child(new_page)
    """

    def __init__(self, document, node_type: str, content="", content_parts=None):
        if content_parts is None:
            content_parts = []
        self.node_type: str = node_type
        self.content: str = content
        self.document: Document = document
        self.content_parts: List[Any] = content_parts
        self.parent: Optional[ContentNode] = None
        self.children: List[ContentNode] = []
        self.index: int = 0
        self.uuid: str = str(uuid.uuid4())
        self.virtual: bool = False
        # Added for performance
        self._feature_map: Dict[str, ContentFeature] = {}

    def __str__(self):
        return f"ContentNode [node_type:{self.node_type}] ({len(self.get_features())} features, {len(self.children)} children) [" + str(
            self.content) + "]"

    def to_json(self):
        """
        Create a JSON string representation of this ContentNode.

            >>> node.to_json()

        :return: The JSON formatted string representation of this ContentNode.
        :rtype: str
        """
        return json.dumps(self.to_dict())

    def to_dict(self):
        """
        Create a dictionary representing this ContentNode's structure and content.

            >>> node.to_dict()

        :return: The properties of this ContentNode and all of its children structured as a dictionary.
        :rtype: dict
        """
        new_dict = {'node_type': self.node_type, 'content': self.content, 'content_parts': self.content_parts,
                    'features': [],
                    'index': self.index, 'children': [], 'uuid': self.uuid}
        for feature in self.get_features():
            new_dict['features'].append(feature.to_dict())

        for child in self.children:
            new_dict['children'].append(child.to_dict())
        return new_dict

    @staticmethod
    def from_dict(document, content_node_dict: Dict):
        """
        Build a new ContentNode from a dictionary representtion.

            >>> ContentNode.from_dict(document, content_node_dict)

        :param Document document: The Kodexa document from which the new ContentNode will be created (not added).
        :param dict content_node_dict: The dictionary-structured representation of a ContentNode.  This value will be unpacked into a ContentNode.

        :return: A ContentNode containing the unpacked values from the content_node_dict parameter.
        :rtype: ContentNode
        """

        node_type = content_node_dict['type'] if document.version == Document.PREVOUS_VERSION else content_node_dict[
            'node_type']

        new_content_node = document.create_node(node_type=node_type, content=content_node_dict[
            'content'] if 'content' in content_node_dict else None)
        if 'uuid' in content_node_dict:
            new_content_node.uuid = content_node_dict['uuid']

        if 'content_parts' in content_node_dict:
            new_content_node.content_parts = content_node_dict['content_parts']

        for dict_feature in content_node_dict['features']:
            new_feature = new_content_node.add_feature(dict_feature['name'].split(':')[0],
                                                       dict_feature['name'].split(':')[1],
                                                       dict_feature['value'], dict_feature['single'], True)
        for dict_child in content_node_dict['children']:
            new_content_node.add_child(ContentNode.from_dict(document, dict_child), dict_child['index'])
        return new_content_node

    def add_child_content(self, node_type, content, index=None):
        """
        Convenience method to allow you to quick add a child node with a type and content

        :param node_type: the node type
        :param content: the content
        :param index: the index (optional)
        :return: the new ContentNode
        """
        new_node = self.document.create_node(node_type=node_type)
        new_node.content = content
        self.add_child(new_node, index)
        return new_node

    def add_child(self, child, index=None):
        """
        Add a ContentNode as a child of this ContentNode

            >>> new_page = document.create_node(node_type='page')
            <kodexa.model.model.ContentNode object at 0x7f80605e53c8>
            >>> current_content_node.add_child(new_page)

        :param ContentNode child: The node that will be added as a child of this node
        :param index: The index at which this child node should be added; defaults to None.  If None, index is set as the count of child node elements.
        :type index: int, optional
        """
        if not index:
            child.index = len(self.children)
        else:
            child.index = index
        self.children.append(child)
        child.parent = self

    def get_children(self):
        """
        Returns a list of the children of this node.

           >>> node.get_children()

        :return: The list of child nodes for this ContentNode.
        :rtype: list[ContentNode]
        """
        return self.children

    def set_feature(self, feature_type, name, value):
        """
        Sets a feature for this ContentNode, replacing the value if a feature by this type and name already exists.

           >>> new_page = document.create_node(node_type='page')
           <kodexa.model.model.ContentNode object at 0x7f80605e53c8>
           >>> new_page.add_feature('pagination','pageNum',1)

        :param str feature_type: The type of feature to be added to the node.
        :param str name: The name of the feature.
        :param Any value: The value of the feature.

        :return: The feature that was added to this ContentNode
        :rtype: ContentFeature
        """
        self.remove_feature(feature_type, name)
        return self.add_feature(feature_type, name, value)

    def add_feature(self, feature_type, name, value, single=True, serialized=False):
        """
        Add a new feature to this ContentNode.

        Note: if a feature for this feature_type/name already exists, the new value will be added to the existing feature; therefore the feature value might become a list.

           >>> new_page = document.create_node(node_type='page')
           <kodexa.model.model.ContentNode object at 0x7f80605e53c8>
           >>> new_page.add_feature('pagination','pageNum',1)

        :param str feature_type: The type of feature to be added to the node.
        :param str name: The name of the feature.
        :param Any value: The value of the feature.
        :param single: Indicates that the value is singular, rather than a collection (ex: str vs list); defaults to True.
        :type single: bool, optional
        :param serialized: Indicates that the value is/is not already serialized; defaults to False.
        :type serialized: bool, optional

        :return: The feature that was added to this ContentNode.
        :rtype: ContentFeature
        """
        if self.has_feature(feature_type, name):
            feature = self.get_feature(feature_type, name)
            feature.single = False  # always setting to false if we already have a feature of this type/name
            feature.value.append(value)
            return feature
        else:
            # Make sure that we treat the value as list all the time
            new_feature = ContentFeature(feature_type, name,
                                         [value] if single and not serialized else value, single=single)
            self._feature_map[new_feature.feature_type + ":" + new_feature.name] = new_feature
            return new_feature

    def delete_children(self, nodes: Optional[List] = None,
                        exclude_nodes: Optional[List] = None):
        """Delete the children of this node, you can either supply a list of the nodes to delete
           or the nodes to exclude from the delete, if neither are supplied then we delete all the children.

           Note there is precedence in place, if you have provided a list of nodes to delete then the nodes
           to exclude is ignored.

           :param nodes:Optional[List[ContentNode]] a list of content nodes that are children to delete
           :param exclude_nodes:Optional[List[ContentNode]] a list of content node that are children not to delete

        """
        children_to_delete = []

        for child_node in self.children:
            if nodes is not None:
                for node_to_delete in nodes:
                    if node_to_delete.uuid == child_node.uuid:
                        children_to_delete.append(child_node)
            elif exclude_nodes is not None:
                if len(exclude_nodes) == 0:
                    children_to_delete.append(child_node)
                else:
                    for nodes_to_exclude in exclude_nodes:
                        if nodes_to_exclude.uuid != child_node.uuid:
                            children_to_delete.append(child_node)
            else:
                children_to_delete.append(child_node)

        for child_to_delete in children_to_delete:
            if child_to_delete in self.children:
                self.children.remove(child_to_delete)

    def get_feature(self, feature_type, name):
        """
        Gets the value for the given feature.

           >>> new_page.get_feature('pagination','pageNum')
           1

        :param str feature_type: The type of the feature.
        :param str name: The name of the feature.

        :return: The feature with the specified type & name.  If no feature is found, None is returned.
        :rtype: ContentFeature or None
        """
        return self._feature_map[feature_type + ":" + name] if feature_type + ":" + name in self._feature_map else None

    def get_features_of_type(self, feature_type):
        """
        Get all features of a specific type.

           >>> new_page.get_features_of_type('my_type')
           []

        :param str feature_type: The type of the feature.

        :return: A list of feature with the specified type.  If no features are found, an empty list is returned.
        :rtype: list[ContentFeature]
        """
        return [i for i in self.get_features() if i.feature_type == feature_type]

    def has_feature(self, feature_type, name):
        """
        Determines if a feature with the given feature and name exists on this content node.

           >>> new_page.has_feature('pagination','pageNum')
           True

        :param str feature_type: The type of the feature.
        :param str name: The name of the feature.

        :return: True if the feature is present; else, False.
        :rtype: bool
        """
        return feature_type + ":" + name in self._feature_map

    def get_features(self):
        """
        Get all features on this ContentNode.

        :return: A list of the features on this ContentNode.
        :rtype: list[ContentFeature]
        """
        return list(self._feature_map.values())

    def remove_feature(self, feature_type, name):
        """
        Removes the feature with the given name and type from this node.

           >>> new_page.remove_feature('pagination','pageNum')

        :param str feature_type: The type of the feature.
        :param str name: The name of the feature.
        """
        results = self.get_feature(feature_type, name)
        if results:
            del self._feature_map[feature_type + ":" + name]

    def get_feature_value(self, feature_type, name):
        """
        Get the value for a feature with the given name and type on this ContentNode.

           >>> new_page.get_feature_value('pagination','pageNum')
           1

        :param str feature_type: The type of the feature.
        :param str name: The name of the feature.

        :return: The value of the feature if it exists on this ContentNode otherwise, None.
        :rtype: Any or None
        """
        feature = self.get_feature(feature_type, name)

        # Need to make sure we handle the idea of a single value for a feature
        return None if feature is None else feature.value[0] if feature.single else feature.value

    def get_content(self):
        """
        Get the content of this node.

           >>> new_page.get_content()
           "This is page one"

        :return: The content of this ContentNode.
        :rtype: str
        """
        return self.content

    def get_node_type(self):
        """
        Get the type of this node.

           >>> new_page.get_content()
           "page"

        :return: The type of this ContentNode.
        :rtype: str
        """
        return self.node_type

    def select(self, selector, variables=None):
        """
        Select and return the child nodes of this node that match the selector value.

        >>> document.get_root().select('.')
           [ContentNode]

        or

        >>> document.get_root().select('//*[hasTag($tagName)]', {"tagName": "div"})
           [ContentNode]

        :param str selector: The selector (ie. //*)
        :param variables: A dictionary of variable name/value to use in substituion; defaults to None.  Dictionary keys should match a variable specified in the selector.
        :type variables: dict, optional

        :return: A list of the matching content nodes.  If no matches are found, the list will be empty.
        :rtype: list[ContentNode]
        """
        if variables is None:
            variables = {}
        from kodexa.selectors import parse
        parsed_selector = parse(selector)
        return parsed_selector.resolve(self, variables)

    def select_as_node(self, selector, variables=None):
        """
        Select and return the child nodes of this content node that match the selector value.
        Matching nodes will be returned as the children of a new proxy content node.

        Note this doesn't impact this content node's children.  They are not adopted by the proxy node,
        therefore their parents remain intact.

        >>> document.content_node.select_as_node('//line')
           ContentNode

        or

        >>> document.get_root().select_as_node('//*[hasTag($tagName)]', {"tagName": "div"})
           ContentNode

        :param str selector: The selector (ie. //*)
        :param variables: A dictionary of variable name/value to use in substituion; defaults to None.  Dictionary keys should match a variable specified in the selector.
        :type variables: dict, optional

        :return: A new proxy ContentNode with the matching (selected) nodes as its children.  If no matches are found, the list of children will be empty.
        :rtype: ContentNode
        """
        new_node = self.document.create_node(node_type='result')
        new_node.children = self.select(selector, variables)
        return new_node

    def get_all_content(self, separator=" "):
        """
        Get this node's content, concatenated with all of its children's content.

            >>> document.content_node.get_all_content()
            "This string is made up of multiple nodes"

        :param separator: The separator to use in joining content together; defaults to " ".
        :type separator: str, optional

        :return: The complete content for this node concatenated with the content of all child nodes.
        :rtype: str
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

            >>> # Get first node of type 'line' from the first page
            >>> target_child = document.get_root().select('//page')[0].select('//line')[0]
            >>> # Get sixth node of type 'page'
            >>> target_parent = document.get_root().select('//page')[5]
            >>> # Move target_child (line) to the target_parent (sixth page)
            >>> document.get_root().move_child_to_parent(target_child, target_parent)

        :param ContentNode target_child: The child node that will be moved to a new parent node (target_parent).
        :param ContentNode target_parent: The parent node that the target_child will be added to.  The target_child will be added at the end of the children collection.
        """
        self.children.remove(target_child)
        target_parent.add_child(target_child)

    def adopt_children(self, children, replace=False):
        """
        This will take a list of content nodes and adopt them under this node, ensuring they are re-parented.

            >>> # select all nodes of type 'line', then the root node 'adopts' them
            >>> # and replaces all it's existing children with these 'line' nodes.
            >>> document.get_root().adopt_children(document.select('//line'), replace=True)

        :param list[ContentNode] children: A list of ContentNodes that will be added to the end of this node's children collection
        :param bool replace: If True, will remove all current children and replace them with the new list; defaults to True
        """

        if replace:
            for child in self.children:
                self.parent = None
            self.children = []

        for child in children:
            self.add_child(child)

    def remove_tag(self, tag_name):
        """
        Remove a tag from this content node.

            >>> document.get_root().remove_tag('foo')

        :param str tag_name: The name of the tag that should be removed.
        """
        self.remove_feature('tag', tag_name)

    def collect_nodes_to(self, end_node):
        """
        Get the the sibling nodes between the current node and the end_node.

            >>> document.content_node.children[0].collect_nodes_to(end_node=document.content_node.children[5])

        :param ContentNode end_node: The node to end at

        :return: A list of sibling nodes between this node and the end_node.
        :rtype: list[ContentNode]
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

    def tag_nodes_to(self, end_node, tag_to_apply):
        """
        Tag all the nodes from this node to the end_node with the given tag name

            >>> document.content_node.children[0].tag_nodes_to(document.content_node.children[5], tag_name='foo')

        :param ContentNode end_node: The node to end with
        :param str tag_to_apply: The tag name that will be applied to each node
        """
        [node.tag(tag_to_apply) for node in self.collect_nodes_to(end_node)]

    def tag_range(self, start_content_re, end_content_re, tag_to_apply, node_type_re='.*', use_all_content=False):
        """
        This will tag all the child nodes between the start and end content regular expressions

             >>> document.content_node.tag_range(start_content_re='.*Cheese.*', end_content_re='.*Fish.*', tag_to_apply='foo')

        :param start_content_re: The regular expression to match the starting child
        :param end_content_re: The regular expression to match the ending child
        :param tag_to_apply: The tag name that will be applied to the nodes in range
        :param node_type_re: The node type to match (default is all)
        :param use_all_content: Use full content (including child nodes, default is False)
        """

        # Could be line, word, or content-area
        all_nodes = self.findall(node_type_re=node_type_re)

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
            [node.tag(tag_to_apply) for node in all_nodes[start_index:end_index]]

    def tag_text_tree(self):
        """
        Return a text tree
        :return:
        """
        from anytree import RenderTree
        result = ""
        for pre, _, node in RenderTree(self):
            result = result + ("%s%s" % (pre, f"{node.content} ({node.node_type}) {node.get_tags()}\n"))
        return result

    def tag(self, tag_to_apply, selector=".", content_re=None,
            use_all_content=False, node_only=None,
            fixed_position=None, data=None, separator=" "):
        """
        This will tag (see Feature Tagging) the expression groups identified by the regular expression.

            >>> document.content_node.tag('is_cheese')

        Note that if you use the flag use_all_content then node_only will default to True if not set, else it
        will default to False

        :param tag_to_apply: the name of tag that will be applied to the node
        :param selector: The selector to identify the source nodes to work on (default . - the current node)
        :param content_re: the regular expression that you wish to use to tag, note that we will create a tag for each matching group
        :param use_all_content: apply the regular expression to the all_content (include content from child nodes)
        :param separator: Separator to use for use_all_content
        :param node_only: Ignore the matching groups and tag the whole node
        :param fixed_position: use a fixed position, supplied as a tuple i.e. - (4,10) tag from position 4 to 10 (default None)
        :param data: Attach the a dictionary of data for the given tag

        """

        if use_all_content and node_only is None:
            node_only = True
        elif node_only is None:
            node_only = False

        def tag_node_position(node_to_check, start, end, node_data):

            content_length = 0

            # Make sure we have content on the node
            if node_to_check.content:
                if len(node_to_check.content) > 0:
                    if start < len(node_to_check.content) and end < len(node_to_check.content):
                        node_to_check.add_feature('tag', tag_to_apply,
                                                  Tag(start, end,
                                                      node_to_check.content[start:end],
                                                      data=node_data))
                        return -1
                    elif start < len(node_to_check.content) <= end:
                        node_to_check.add_feature('tag', tag_to_apply,
                                                  Tag(start,
                                                      len(node_to_check.content),
                                                      value=node_to_check.content[start:],
                                                      data=node_data))

                end = end - len(node_to_check.content) + len(separator)
                content_length = len(node_to_check.content) + len(separator)
                start = 0 if start - len(node_to_check.content) - len(separator) < 0 else start - len(
                    node_to_check.content) - len(separator)

            for child_node in node_to_check.children:
                result = tag_node_position(child_node, start, end, node_data)
                content_length = content_length + result
                if result < 0:
                    return -1
                else:
                    end = end - result
                    start = 0 if start - result < 0 else start - result

            return content_length

        if content_re:
            pattern = re.compile(content_re)

        for node in self.select(selector):
            if fixed_position:
                tag_node_position(node, fixed_position[0], fixed_position[1], data)

            else:
                if not content_re:
                    node.add_feature('tag', tag_to_apply, Tag(data=data))
                else:
                    if not use_all_content:
                        if node.content:
                            content = node.content
                        else:
                            content = None
                    else:
                        content = node.get_all_content(separator=separator)

                    if content is not None:
                        match = pattern.match(content)
                        if match:
                            if node_only:
                                node.add_feature('tag', tag_to_apply, Tag(data=data))
                            else:
                                for index, m in enumerate(match.groups()):
                                    idx = index + 1

                                    if node_only:
                                        node.add_feature('tag', tag_to_apply,
                                                         Tag(match.start(idx), match.end(idx), match.group(idx),
                                                             data=data))
                                    else:
                                        # We need to work out where the content is in the child nodes
                                        start_offset = match.start(idx)
                                        end_offset = match.end(idx)

                                        tag_node_position(node, start_offset, end_offset, data)

    def get_tags(self):
        """
        Returns a list of the names of the tags on the given node

            >>> document.content_node.select('*').get_tags()
            ['is_cheese']

        :return: A list of the tag name
        """
        return [i.name for i in self.get_features_of_type("tag")]

    def get_tag_values(self, tag_name, include_children=False):
        """
        Get the values for a specific tag name

        :param tag_name: tag name
        :param include_children: include the children of this node
        :return: a list of the tag values
        """
        values = []
        for tag in self.get_tag(tag_name):
            values.append(tag.value)

        if include_children:
            for child in self.get_children():
                values.extend(child.get_tag_values(tag_name, include_children))

        return values

    def get_tag(self, tag_name):
        """
        Returns the value of a tag, this can be either a single list [start,end,value] or if multiple parts of the
        content of this node match you can end up with a list of lists i.e. [[start1,end1,value1],[start2,end2,value2]]

            >>> document.content_node.find(content_re='.*Cheese.*').get_tag('is_cheese')
            [0,10,'The Cheese Moved']

        :param tag_name: The name of the tag

        :return: A list tagged location and values for this label in this node
        """
        tag_details = self.get_feature_value('tag', tag_name)

        if tag_details is None:
            return []

        if isinstance(tag_details, list):
            return tag_details
        else:
            return [tag_details]

    def get_all_tags(self):
        """
        Get the names of all tags that have been applied to this node or to its children.

            >>> document.content_node.find(content_re='.*Cheese.*').get_all_tags()
            ['is_cheese']

        :return: A list of the tag names belonging to this node and/or its children.
        :rtype: list[str]
        """
        tags = []
        tags.extend(self.get_tags())
        for child in self.children:
            tags.extend(child.get_all_tags())
        return list(set(tags))

    def has_tags(self):
        """
        Determines if this node has any tags at all.

            >>> document.content_node.find(content_re='.*Cheese.*').has_tags()
            True

        :return: True if node has any tags; else, False;
        :rtype: bool
        """
        return len([i.value for i in self.get_features_of_type("tag")]) > 0

    def has_tag(self, tag):
        """
        Determine if this node has a tag with the specified name.

            >>> document.content_node.find(content_re='.*Cheese.*').has_tag('is_cheese')
            True
            >>> document.content_node.find(content_re='.*Cheese.*').has_tag('is_fish')
            False

        :param str tag: The name of the tag.

        :return: True if node has a tag by the specified name; else, False;
        :rtype: bool
        """
        for feature in self.get_features():
            if feature.feature_type == 'tag' and feature.name == tag:
                return True
        return False

    def find(self, content_re=".*", node_type_re=".*", direction=FindDirection.CHILDREN, tag_name=None, instance=1,
             tag_name_re=None, use_all_content=False):
        """
        Return a node related to this node (parent or child) that matches the content and/or node type specified by regular expressions.

            >>> document.get_root().find(content_re='.*Cheese.*',instance=2)
            <kodexa.model.model.ContentNode object at 0x7f80605e53c8>

        :param content_re: The regular expression to match against the node's content; default is '.*'.
        :type content_re: str, optional
        :param node_type_re: The regular expression to match against the node's type; default is '.*'.
        :type node_type_re: str, optional
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
        results = self.findall(content_re, node_type_re, direction, tag_name, tag_name_re, use_all_content)
        if instance < 1 or len(results) < instance:
            return None
        else:
            return results[instance - 1]

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
                itertools.islice(self.findall_with_feature_value(feature_type, feature_name, value, direction),
                                 instance - 1, 1), None)

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
        will have the node type of its nearest sibling and will have an index value, but will have no features or content.

        :param int index: The index (zero-based) for the child node.

        :return: Node at index, or None if the index is outside the boundaries of child nodes.
        :rtype: ContentNode or None
        """
        if self.children:

            if index < self.children[0].index:
                virtual_node = self.document.create_node(node_type=self.children[0].node_type, virtual=True,
                                                         parent=self,
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
                    virtual_node = self.document.create_node(node_type=last_child.node_type, virtual=True, parent=self,
                                                             index=index)
                    return virtual_node
            else:
                return None
        else:
            return None

    def has_next_node(self, node_type_re=".*", skip_virtual=False):
        """
        Determine if this node has a next sibling that matches the type specified by the node_type_re regex.

        :param node_type_re: The regular expression to match against the next sibling node's type; default is '.*'.
        :type node_type_re: str, optional
        :param skip_virtual: Skip virtual nodes and return the next real node; default is False.
        :type skip_virtual: bool, optional

        :return: True if there is a next sibling node matching the specified type regex; else, False.
        :rtype: bool
        """
        return self.next_node(node_type_re, skip_virtual=skip_virtual) is not None

    def has_previous_node(self, node_type_re=".*", skip_virtual=False):
        """
        Determine if this node has a previous sibling that matches the type specified by the node_type_re regex.

        :param node_type_re: The regular expression to match against the previous sibling node's type; default is '.*'.
        :type node_type_re: str, optional
        :param skip_virtual: Skip virtual nodes and return the next real node; default is False.
        :type skip_virtual: bool, optional

        :return: True if there is a previous sibling node matching the specified type regex; else, False.
        :rtype: bool
        """
        return self.previous_node(node_type_re=node_type_re, skip_virtual=skip_virtual) is not None

    def next_node(self, node_type_re='.*', skip_virtual=False, has_no_content=True):
        """
        Returns the next sibling content node.

        Note:  This logic relies on node indexes.  Documents allow for sparse representation and child nodes may not have consecutive index numbers.
        Therefore, the next node might actually be a virtual node that is created to fill a gap in the document.  You can skip virtual nodes by setting the
        skip_virtual parameter to False.

        :param node_type_re: The regular expression to match against the next sibling node's type; default is '.*'.
        :type node_type_re: str, optional
        :param skip_virtual: Skip virtual nodes and return the next real node; default is False.
        :type skip_virtual: bool, optional
        :param has_no_content: Allow a node that has no content to be returned; default is True.
        :type has_no_content: bool, optional

        :return: The next node or None, if no node exists
        :rtype: ContentNode or None
        """
        search_index = self.index + 1
        compiled_node_type_re = re.compile(node_type_re)

        while True:
            node = self.parent.get_node_at_index(search_index)

            if not node:
                return node

            if compiled_node_type_re.match(node.node_type) and (not skip_virtual or not node.virtual):
                if (not has_no_content and node.content) or (has_no_content):
                    return node

            search_index += 1

    def previous_node(self, node_type_re='.*', skip_virtual=False, has_no_content=False, traverse=Traverse.SIBLING):
        """
        Returns the previous sibling content node.

        Note:  This logic relies on node indexes.  Documents allow for sparse representation and child nodes may not have consecutive index numbers.
        Therefore, the previous node might actually be a virtual node that is created to fill a gap in the document.  You can skip virtual nodes by setting the
        skip_virtual parameter to False.

        :param node_type_re: The regular expression to match against the previous node's type; default is '.*'.
        :type node_type_re: str, optional
        :param skip_virtual: Skip virtual nodes and return the next real node; default is False.
        :type skip_virtual: bool, optional
        :param has_no_content: Allow a node that has no content to be returned; default is False.
        :type has_no_content: bool, optional
        :param traverse: The relationship you'd like to traverse (SIBLING, CHILDREN, PARENT, or ALL); default is Traverse.SIBLING.
        :type traverse: Traverse(enum), optional

        :return: The previous node or None, if no node exists
        :rtype: ContentNode or None
        """

        # TODO: impement/differentiate traverse logic for CHILDREN and SIBLING
        if self.index == 0:
            if traverse == traverse.ALL or traverse == traverse.PARENT and self.parent:
                # Lets look for a previous node on the parent
                return self.parent.previous_node(node_type_re, skip_virtual, has_no_content, traverse)
            else:
                return None

        search_index = self.index - 1
        compiled_node_type_re = re.compile(node_type_re)

        while True:
            node = self.parent.get_node_at_index(search_index)

            if not node:
                return node

            if compiled_node_type_re.match(node.node_type) and (not skip_virtual or not node.virtual):
                if (not has_no_content) or (has_no_content and not node.content):
                    return node

            search_index -= 1

    def findall(self, content_re=".*", node_type_re=".*", direction=FindDirection.CHILDREN, tag_name=None,
                tag_name_re=None, use_all_content=False):
        """
        Search for related nodes (child or parent) that match the content and/or type specified by regular expressions.

            >>> document.content_node.findall(content_re='.*Cheese.*')
            [<kodexa.model.model.ContentNode object at 0x7f80605e53c8>,
            <kodexa.model.model.ContentNode object at 0x7f80605e53c8>]

        :param content_re: The regular expression to match against the node's content; default is '.*'.
        :type content_re: str, optional
        :param node_type_re: The regular expression to match against the node's type; default is '.*'.
        :type node_type_re: str, optional
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
        node_type_compiled = re.compile(node_type_re)
        if tag_name_re:
            tag_name_re_compiled = re.compile(tag_name_re)
        else:
            tag_name_re_compiled = None
        return self.findall_compiled(value_compiled, node_type_compiled, direction, tag_name, tag_name_re_compiled,
                                     use_all_content)

    def findall_compiled(self, value_re_compiled, node_type_re_compiled, direction, tag_name, tag_name_compiled,
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

        if value_re_compiled.match(content) and node_type_re_compiled.match(self.get_node_type()):

            if tag_name_compiled:
                for tag_name in self.get_tags():
                    if tag_name_compiled.match(tag_name):
                        hits.append(self)
                        break

            elif not tag_name or self.has_tag(tag_name):
                hits.append(self)

        if direction is FindDirection.CHILDREN:
            for child in self.get_children():
                hits.extend(child.findall_compiled(value_re_compiled, node_type_re_compiled, direction, tag_name,
                                                   tag_name_compiled, use_all_content))
        else:
            if self.parent:
                hits.extend(self.parent.findall_compiled(value_re_compiled, node_type_re_compiled, direction, tag_name,
                                                         tag_name_compiled, use_all_content))

        return hits


class ContentFeature(object):
    """
    A feature that has been added to a ContentNode
    """

    def __init__(self, feature_type, name, value, description=None, single=True):
        self.feature_type = feature_type
        self.name = name
        self.value = value
        self.description = description
        self.single = single

    def __str__(self):
        return f"Feature [type='{self.feature_type}' name='{self.name}' value='{self.value}' single='{self.single}']"

    def to_dict(self):
        """
        Create a dictionary representing this ContentFeature's structure and content.

            >>> node.to_dict()

        :return: The properties of this ContentFeature structured as a dictionary.
        :rtype: dict
        """
        return {'name': self.feature_type + ':' + self.name, 'value': self.value, 'single': self.single}


@dataclasses.dataclass()
class SourceMetadata:
    """
    Class for keeping track of the original source information for a
    document
    """
    original_filename: Optional[str] = None
    original_path: Optional[str] = None
    checksum: Optional[str] = None
    last_modified: Optional[str] = None
    created: Optional[str] = None
    connector: Optional[str] = None
    mime_type: Optional[str] = None
    headers: Optional[Dict] = None


class Document(object):
    """
    A Document is a collection of metadata and a set of content nodes.
    """

    PREVOUS_VERSION: str = "1.0.0"
    CURRENT_VERSION: str = "2.0.0"

    def __str__(self):
        return f"kdxa//{self.uuid}/{self.metadata}"

    def __init__(self, metadata=None, content_node: ContentNode = None, source=SourceMetadata()):
        if metadata is None:
            metadata = DocumentMetadata()
        self.metadata: DocumentMetadata = metadata
        self.content_node: Optional[ContentNode] = content_node
        self.virtual: bool = False
        self._mixins: List[str] = []
        self.uuid: str = str(uuid.uuid4())
        self.exceptions: List = []
        self.log: List[str] = []
        self.version = Document.CURRENT_VERSION
        self.add_mixin('core')
        self.source: SourceMetadata = source
        self.labels: List[str] = []

        # Make sure we apply all the mixins
        registry.apply_to_document(self)

    def add_label(self, label: str):
        """
        Add a label to the document

        :param label:str Label to add
        :return: the document
        """
        if label not in self.labels:
            self.labels.append(label)

        return self

    def remove_label(self, label: str):
        """
        Remove a label to the document

        :param label:str Label to remove
        :return: the document
        """
        self.labels.remove(label)
        return self

    @classmethod
    def from_text(cls, text):
        new_document = Document()
        new_document.content_node = new_document.create_node(node_type='text', content=text)
        new_document.add_mixin('text')
        return new_document

    def get_root(self):
        """
        Get the root content node for the document (same as content_node)


            >>> node = document.get_node()
        """
        return self.content_node

    def to_kdxa(self, file_path: str):
        """
        Write the document to the kdxa format (msgpack) which can be
        used with the Kodexa platform

            >>> document.to_mdoc('my-document.kdxa')

        :param file_path: the path to the mdoc you wish to create
        """
        with open(file_path, 'wb') as outfile:
            msgpack.pack(self.to_dict(), outfile, use_bin_type=True)

    @staticmethod
    def from_kdxa(file_path):
        """
        Read an .kdxa file from the given file_path and

            >>> document = Document.from_kdxa('my-document.kdxa')

        :param file_path: the path to the mdoc file
        """
        with open(file_path, 'rb') as data_file:
            data_loaded = msgpack.unpack(data_file, raw=False)
        return Document.from_dict(data_loaded)

    def to_msgpack(self):
        """
        Convert this document object structure into a message pack

            >>> document.to_msgpack()
        """
        return msgpack.packb(self.to_dict(), use_bin_type=True)

    def to_json(self):
        """
        Create a JSON string representation of this Document.

            >>> document.to_json()

        :return: The JSON formatted string representation of this Document.
        :rtype: str
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)

    def to_dict(self):
        """
        Create a dictionary representing this Document's structure and content.

            >>> document.to_dict()

        :return: A dictionary representation of this Document.
        :rtype: dict
        """
        return {'version': Document.CURRENT_VERSION, 'metadata': self.metadata,
                'content_node': self.content_node.to_dict() if self.content_node else None,
                'source': dataclasses.asdict(self.source),
                'mixins': self._mixins,
                'exceptions': self.exceptions,
                'log': self.log,
                'labels': self.labels,
                'uuid': self.uuid}

    @staticmethod
    def from_dict(doc_dict):
        """
        Build a new Document from a dictionary.

            >>> Document.from_dict(doc_dict)

        :param dict doc_dict: A dictionary representation of a Kodexa Document.

        :return: A complete Kodexa Document
        :rtype: Document
        """
        new_document = Document(DocumentMetadata(doc_dict['metadata']))
        for mixin in doc_dict['mixins']:
            registry.add_mixin_to_document(mixin, new_document)
        new_document.version = doc_dict['version'] if 'version' in doc_dict and doc_dict[
            'version'] else Document.PREVOUS_VERSION  # some older docs don't have a version or it's None
        new_document.log = doc_dict['log'] if 'log' in doc_dict else []
        new_document.exceptions = doc_dict['exceptions'] if 'exceptions' in doc_dict else []
        new_document.uuid = doc_dict['uuid'] if 'uuid' in doc_dict else str(
            uuid.uuid5(uuid.NAMESPACE_DNS, 'kodexa.com'))
        if 'content_node' in doc_dict and doc_dict['content_node']:
            new_document.content_node = ContentNode.from_dict(new_document, doc_dict['content_node'])
        if 'source' in doc_dict and doc_dict['source']:
            new_document.source = SourceMetadata(**doc_dict['source'])
        if 'labels' in doc_dict and doc_dict['labels']:
            new_document.labels = doc_dict['labels']
        return new_document

    @staticmethod
    def from_json(json_string):
        """
        Create an instance of a Document from a JSON string.

            >>> Document.from_json(json_string)

        :param str json_string: A JSON string representation of a Kodexa Document

        :return: A complete Kodexa Document
        :rtype: Document
        """
        return Document.from_dict(json.loads(json_string))

    @staticmethod
    def from_msgpack(bytes):
        """
        Create an instance of a Document from a message pack byte array.

            >>> Document.from_msgpack(open(os.path.join('news-doc.kdxa'), 'rb').read())

        :param bytes bytes: A message pack byte array.

        :return: A complete Kodexa Document
        :rtype: Document
        """
        return Document.from_dict(msgpack.unpackb(bytes, raw=False))

    def get_mixins(self):
        """
        Get the list of mixins that have been enabled on this document.


            >>> document.get_mixins()
            ['spatial','finders']
        """
        return self._mixins

    def add_mixin(self, mixin):
        """
        Add the given mixin to this document,  this will apply the mixin to all the content nodes,
        and also register it with the document so that future invocations of create_node will ensure
        the node has the mixin appled.

            >>> document.add_mixin('spatial')
        """
        registry.add_mixin_to_document(mixin, self)

    def create_node(self, node_type: str, content: str = None, virtual: bool = False, parent: ContentNode = None,
                    index: int = 0):
        """
        Creates a new node for the document.  The new node is not added to the document, but any mixins that have been
        applied to the document will also be available on the new node.

            >>> document.create_node(node_type='page')
            <kodexa.model.model.ContentNode object at 0x7f80605e53c8>


        :param str node_type: The type of node.
        :param str content: The content for the node; defaults to None.
        :param bool virtual: Indicates if this is a 'real' or 'virtual' node; default is False.  'Real' nodes contain document content.
        'Virtual' nodes are synthesized as necessary to fill gaps in between non-consecutively indexed siblings.  Such indexing arises when document content is sparse.
        :param ContentNode parent: The parent for this newly created node; default is None;
        :param int index: The index property to be set on this node; default is 0;

        :return: This newly created node.
        :rtype: ContentNode

        """
        content_node = ContentNode(document=self, node_type=node_type, content=content)
        content_node.parent = parent
        content_node.index = index
        content_node.virtual = virtual
        registry.add_mixins_to_document_node(self, content_node)
        if virtual:
            for mixin_name in self.get_mixins():
                mixin = registry.get_mixin(mixin_name)
                add_features_to_virtual_node = getattr(mixin, "add_features_to_virtual_node", None)
                if callable(add_features_to_virtual_node):
                    add_features_to_virtual_node(content_node)
        return content_node

    @classmethod
    def from_file(cls, file):
        """
        Creates a Document that has a 'file-handle' connector to the specified file.

        :param file file: The file to which the new Document is connected.

        :return: A Document connected to the specified file.
        :rtype: Document
        """
        file_document = Document()
        file_document.metadata.connector = 'file-handle'
        file_document.metadata.connector_options.file = file
        file_document.source.connector = 'file-handle'
        file_document.source.original_filename = os.path.basename(file)
        file_document.source.original_path = file
        return file_document

    @classmethod
    def from_url(cls, url, headers=None):
        """
        Creates a Document that has a 'url' connector for the specified url.

        :param str url: The URL to which the new Document is connected.
        :param dict headers: Headers that should be used when reading from the URL

        :return: A Document connected to the specified URL with the specified headers (if any).
        :rtype: Document
        """
        if headers is None:
            headers = {}
        url_document = Document()
        url_document.metadata.connector = 'url'
        url_document.metadata.connector_options.url = url
        url_document.metadata.connector_options.headers = headers
        url_document.source.connector = 'url'
        import base64
        encoded_url = base64.b64encode(url.encode('ascii'))
        url_document.source.original_filename = encoded_url.decode('ascii')
        url_document.source.original_path = url
        url_document.source.headers = headers
        return url_document

    def select(self, selector, variables=None):
        """
        Execute a selector on the root node and then return a list of the matching nodes.

        >>> document.select('.')
           [ContentNode]

        :param str selector: The selector (ie. //*)
        :param variables: A dictionary of variable name/value to use in substituion; defaults to an empty dictionary.  Dictionary keys should match a variable specified in the selector.
        :type variables: dict, optional

        :return: A list of the matching ContentNodes.  If no matches found, list is empty.
        :rtype: list[ContentNodes]
        """
        if variables is None:
            variables = {}
        if self.content_node:
            result = self.content_node.select(selector, variables)
            if isinstance(result, list):
                return result
            else:
                return [self.content_node] if bool(result) else []
        else:
            return []

    def select_as_node(self, selector, variables=None):
        """
        Execute a selector on the root node and then return new ContentNode with the results set as its children.

        >>> document.select('//line')
           ContentNode

        :param selector: The selector (ie. //*)
        :param variables: A dictionary of variable name/value to use in substituion; defaults to an empty dictionary.  Dictionary keys should match a variable specified in the selector.
        :type variables: dict, optional

        :return: A new ContentNode.  All ContentNodes on this Document that match the selector value are added as the children for the returned ContentNode.
        :rtype: ContentNode
        """
        if variables is None:
            variables = {}
        if self.content_node:
            return self.content_node.select_as_node(selector, variables)
        else:
            return self.create_node(node_type='results')

    def get_labels(self) -> List[str]:
        """
        Return the list of labels associated with this document

        :return: list of associated labels
        """
        return self.labels


class DocumentStore:
    """A document store supports storing, listing and retrieving Kodexa documents"""

    def get_by_uuid(self, uuid_value: str) -> Optional[Document]:
        pass

    def list_objects(self) -> List[Dict]:
        pass

    def list(self):
        objects = self.list_objects()
        self._draw_table(objects)

    def query(self, query: str = "*"):
        objects = self.query_objects(query)
        self._draw_table(objects)

    def _draw_table(self, objects):
        from rich.table import Table
        from rich import print

        table = Table(title=f"Listing Objects")

        cols = ['id', 'content_type', 'path']
        for col in cols:
            table.add_column(col)
        for object_dict in objects:
            row = []

            for col in cols:
                row.append(object_dict[col] if col in object_dict else '')
            table.add_row(*row)

        print(table)

    def query_objects(self, query: str) -> List[Dict]:
        pass

    def put(self, path: str, document: Document):
        pass

    def count(self) -> int:
        return 0

    def accept(self, document: Document):
        return True


class FileStore:
    """A file store supports storing, listing and retrieving native files"""

    def get(self, path: str) -> Document:
        pass

    def list(self) -> List[str]:
        pass

    def put(self, path: str, document: Document):
        pass


class ModelStore:
    """A model store supports storing and retrieving of a ML models"""

    def get(self, path: str):
        pass

    def put(self, path: str, content):
        pass


class LocalModelStore(ModelStore):

    def __init__(self, store_path: str, force_initialize=False):
        self.store_path = store_path
        path = Path(store_path)

        if force_initialize and path.exists():
            shutil.rmtree(store_path)

        if path.is_file():
            raise Exception("Unable to load store, since it is pointing to a file?")
        elif not path.exists():
            path.mkdir(parents=True)

    def to_dict(self):
        return {
            "type": "MODEL",
            "data": {
                "path": self.store_path
            }
        }

    def get(self, object_path: str):
        if Path(os.path.join(self.store_path, object_path)).is_file():
            return open(os.path.join(self.store_path, object_path), 'rb')
        else:
            return None

    def put(self, object_path: str, content):
        path = Path(object_path)
        with open(os.path.join(self.store_path, path), 'wb') as object_file:
            object_file.write(content)


class RemoteModelStore(ModelStore, RemoteStore):

    def to_dict(self):
        return {
            "type": "MODEL",
            "ref": self.ref
        }

    def __init__(self, ref: str):
        self.ref = ref

    def get(self, object_path: str):
        # TODO implement
        pass

    def put(self, object_path: str, content):
        # TODO implement
        pass
