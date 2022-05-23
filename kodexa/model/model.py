"""
The core model provides definitions for all the base objects in the Kodexa Content Model
"""
import abc
import dataclasses
import inspect
import json
import os
import re
import uuid
from enum import Enum
from typing import Any, List, Optional

import msgpack
from addict import Dict

from kodexa.mixins import registry
from kodexa.model.objects import ModelContentMetadata, ContentObject, DocumentTransition, Store, DocumentFamily


class Ref:

    def __init__(self, ref: str):
        self.ref: str = ref
        first_part = ref
        self.version: Optional[str] = None
        self.resource: Optional[str] = None
        self.slug: str = ""
        self.org_slug: str = ""

        if ':' in ref:
            (first_part, self.version) = ref.split(":")

            if '/' in self.version:
                (self.version, self.resource) = self.version.split('/')

        (self.org_slug, self.slug) = first_part.split("/")

        self.object_ref = f"{self.org_slug}/{self.slug}:{self.version}" if self.version else f"{self.org_slug}/{self.slug}"


class DocumentMetadata(Dict):
    """A flexible dict based approach to capturing metadata for the document"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ContentException(Dict):
    """A content exception represents an issue identified during labeling or validation at the document level"""

    def __init__(self, tag: str, message: str, group_uuid: Optional[str], tag_uuid: Optional[str], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = tag
        self.message = message
        self.group_uuid = group_uuid
        self.tag_uuid = tag_uuid


class Tag(Dict):
    """A tag represents the metadata for a label that is applies as a feature on a content node"""

    def __init__(self, start: Optional[int] = None, end: Optional[int] = None, value: Optional[str] = None,
                 uuid: Optional[str] = None, data: Any = None, *args, confidence: Optional[float] = None,
                 group_uuid: Optional[str] = None, parent_group_uuid: Optional[str] = None,
                 cell_index: Optional[int] = None, index: Optional[int] = None, bbox: Optional[List[int]] = None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.start: Optional[int] = start
        """The start position (zero indexed) of the content within the node, if None then label is applied to the whole node"""
        self.end: Optional[int] = end
        """The end position (zero indexed) of the content within the node, if None then label is applied to the whole node"""
        self.value: Optional[str] = value
        """A string representing the value that was labelled in the node"""
        self.data: Optional[Any] = data
        """Any data object (JSON serializable) that you wish to associate with the label"""
        self.uuid: Optional[str] = uuid
        """The UUID for this tag instance, this allows tags that are on different content nodes to be related through the same UUID"""
        self.confidence: Optional[float] = confidence
        """The confidence of the tag in a range of 0-1"""
        self.index: Optional[int] = index
        """The tag index, this is used to allow us to order tags, and understand the ordering of parent child tag relationships"""
        self.bbox: Optional[List[int]] = bbox
        """The optional bounding box that can be used if the label is spatial (based on the node as the container)"""
        self.group_uuid: Optional[str] = group_uuid
        """The UUID of the group that this tag belongs to, this is used to allow us to group tags together"""
        self.parent_group_uuid: Optional[str] = parent_group_uuid
        """The UUID of the parent group that this tag belongs to, this is used to allow us to group tags together"""
        self.cell_index: Optional[int] = cell_index
        """The cell index of the cell that this tag belongs to, this is used to allow us to group tags together"""

        # Pull the cell index from the data to the tag if we have it in the data
        if self.cell_index is None:
            if data and 'cell_index' in data:
                self.cell_index = data['cell_index']


class FindDirection(Enum):
    """ """
    CHILDREN = 1
    PARENT = 2


class Traverse(Enum):
    """ """
    SIBLING = 1
    CHILDREN = 2
    PARENT = 3
    ALL = 4


class ContentNode(object):
    """A Content Node identifies a section of the document containing logical
    grouping of information.

    The node will have content and can include any number of features.

    You should always create a node using the Document's create_node method to
    ensure that the correct mixins are applied.

    >>> new_page = document.create_node(node_type='page')
    <kodexa.model.model.ContentNode object at 0x7f80605e53c8>
    >>> current_content_node.add_child(new_page)

    >>> new_page = document.create_node(node_type='page', content='This is page 1')
    <kodexa.model.model.ContentNode object at 0x7f80605e53c8>
    >>> current_content_node.add_child(new_page)

    """

    def __init__(self, document, node_type: str, content: Optional[str] = None,
                 content_parts: Optional[List[Any]] = None, parent=None, index: Optional[int] = None,
                 virtual: bool = False):
        self.node_type: str = node_type
        """The node type (ie. line, page, cell etc)"""
        self.document: Document = document
        """The document that the node belongs to"""
        self._content_parts: Optional[List[Any]] = content_parts
        """The children of the content node"""
        self.index: Optional[int] = index
        """The index of the content node"""
        self.uuid: Optional[int] = None
        """The ID of the content node"""
        self.virtual: bool = virtual
        """Is the node virtual (ie. it doesn't actually exist in the document)"""

        self._parent_uuid = parent.uuid if parent else None

        if content is not None and len(self.get_content_parts()) == 0:
            self.set_content_parts([content])

    def get_content_parts(self):
        return self.document.get_persistence().get_content_parts(self)

    def set_content_parts(self, content_parts):
        self.document.get_persistence().update_content_parts(self, content_parts)

    @property
    def content(self):

        if len(self.get_content_parts()) == 0:
            return None

        s = ""
        for part in self.get_content_parts():
            if isinstance(part, str):
                if s != "":
                    s += " "
                s += part

        return s

    @content.setter
    def content(self, new_content):
        if len(self.get_content_parts()) == 0:
            self.set_content_parts([new_content])
        else:
            # We need to remove all the strings and add this one
            # back at the front
            parts = self.get_content_parts()
            filtered_parts = list(filter(lambda part: isinstance(part, int), parts))
            if new_content is not None and new_content != "":
                filtered_parts.insert(0, new_content)
            self.set_content_parts(filtered_parts)

    def __eq__(self, other):
        return other is not None and self.uuid == other.uuid and (self.uuid is not None and other.uuid is not None)

    def get_parent(self):
        return self.document.get_persistence().get_parent(self)

    def __str__(self):
        return f"ContentNode {self.uuid} [node_type:{self.node_type}] ({len(self.get_features())} features, {len(self.get_children())} children) [" + str(
            self.content) + "]"

    def to_json(self):
        """Create a JSON string representation of this ContentNode.

        Args:

        Returns:
          str: The JSON formatted string representation of this ContentNode.

        >>> node.to_json()
        """
        return json.dumps(self.to_dict())

    def to_dict(self):
        """Create a dictionary representing this ContentNode's structure and content.

        Args:

        Returns:
          dict: The properties of this ContentNode and all of its children structured as a dictionary.

        >>> node.to_dict()
        """
        new_dict = {'node_type': self.node_type, 'content': self.content, 'content_parts': self.get_content_parts(),
                    'features': [],
                    'index': self.index, 'children': [], 'uuid': self.uuid}
        for feature in self.get_features():
            new_dict['features'].append(feature.to_dict())

        for child in self.get_children():
            new_dict['children'].append(child.to_dict())
        return new_dict

    @staticmethod
    def from_dict(document, content_node_dict: Dict, parent=None):
        """Build a new ContentNode from a dictionary represention.

        Args:
          document (Document): The Kodexa document from which the new ContentNode will be created (not added).
          content_node_dict (Dict): The dictionary-structured representation of a ContentNode.  This value will be unpacked into a ContentNode.
          parent (Optional[ContentNode]): Optionally the parent content node
        Returns:
          ContentNode: A ContentNode containing the unpacked values from the content_node_dict parameter.

        >>> ContentNode.from_dict(document, content_node_dict)
        """

        node_type = content_node_dict['type'] if document.version == Document.PREVIOUS_VERSION else content_node_dict[
            'node_type']

        new_content_node = document.create_node(node_type=node_type, content=content_node_dict[
            'content'] if 'content' in content_node_dict else None, index=content_node_dict['index'], parent=parent)

        if 'content_parts' in content_node_dict and len(content_node_dict['content_parts']) > 0:
            new_content_node.set_content_parts(content_node_dict['content_parts'])

        for dict_feature in content_node_dict['features']:

            feature_type = dict_feature['name'].split(':')[0]
            if feature_type == 'tag':
                new_content_node.add_feature(feature_type,
                                             dict_feature['name'].split(':')[1],
                                             dict_feature['value'], dict_feature['single'], True)
            else:
                new_content_node.add_feature(feature_type,
                                             dict_feature['name'].split(':')[1],
                                             dict_feature['value'], dict_feature['single'], True)

        for dict_child in content_node_dict['children']:
            ContentNode.from_dict(document, dict_child, new_content_node)

        return new_content_node

    def add_child_content(self, node_type: str, content: str, index: Optional[int] = None) -> 'ContentNode':
        """Convenience method to allow you to quick add a child node with a type and content

        Args:
          node_type: the node type
          content: the content
          index: the index (optional) (Default value = None)

        Returns:
          the new ContentNode

        """
        new_node = self.document.create_node(node_type=node_type, parent=self, content=content)
        self.add_child(new_node, index)
        return new_node

    def add_child(self, child, index: Optional[int] = None):
        """Add a ContentNode as a child of this ContentNode

        Args:
          child (ContentNode): The node that will be added as a child of this node
          index (Optional[int]): The index at which this child node should be added; defaults to None.  If None, index is set as the count of child node elements.

        Returns:

        >>> new_page = document.create_node(node_type='page')
            <kodexa.model.model.ContentNode object at 0x7f80605e53c8>
            >>> current_content_node.add_child(new_page)
        """
        if index is None:
            if len(self.get_children()) > 0:
                child.index = self.get_children()[-1].index + 1
            else:
                child.index = 0
        else:
            child.index = index

        self.document.get_persistence().add_content_node(child, self)

    def remove_child(self, content_node):
        try:
            child_idx = self.get_children().index(content_node)
            child = self.get_children()[child_idx]
            self.document.get_persistence().remove_content_node(child)
        except ValueError as e:
            import better_exceptions
            import sys
            et, ev, tb = sys.exc_info()
            print("\n".join(
                better_exceptions.format_exception(*sys.exc_info())))

    def get_children(self):
        """Returns a list of the children of this node.

        Returns:
          list[ContentNode]: The list of child nodes for this ContentNode.

        >>> node.get_children()
        """
        return self.document.get_persistence().get_children(self)

    def set_feature(self, feature_type, name, value):
        """Sets a feature for this ContentNode, replacing the value if a feature by this type and name already exists.

        Args:
          feature_type (str): The type of feature to be added to the node.
          name (str): The name of the feature.
          value (Any): The value of the feature.

        Returns:
          ContentFeature: The feature that was added to this ContentNode

        >>> new_page = document.create_node(node_type='page')
           <kodexa.model.model.ContentNode object at 0x7f80605e53c8>
           >>> new_page.add_feature('pagination','pageNum',1)
        """
        self.remove_feature(feature_type, name)
        return self.add_feature(feature_type, name, value)

    def add_feature(self, feature_type, name, value, single=True, serialized=False):
        """
        Add a new feature to this ContentNode.

        Note: if a feature for this feature_type/name already exists, the new value will be added to the existing feature;
        therefore the feature value might become a list.

        Args:
          feature_type (str): The type of feature to be added to the node.
          name (str): The name of the feature.
          value (Any): The value of the feature.
          single (boolean): Indicates that the value is singular, rather than a collection (ex: str vs list); defaults to True.
          serialized (boolean): Indicates that the value is/is not already serialized; defaults to False.

        Returns:
          ContentFeature: The feature that was added to this ContentNode.

        >>> new_page = document.create_node(node_type='page')
           <kodexa.model.model.ContentNode object at 0x7f80605e53c8>
           >>> new_page.add_feature('pagination','pageNum',1)
        """
        if self.has_feature(feature_type, name):
            feature = self.get_feature(feature_type, name)
            feature.single = False  # always setting to false if we already have a feature of this type/name
            feature.value.append(value)
            self.document.get_persistence().remove_feature(self, feature_type, name)
            self.document.get_persistence().add_feature(self, feature)
            return feature
        else:
            # Make sure that we treat the value as list all the time
            new_feature = ContentFeature(feature_type, name,
                                         [value] if single and not serialized else value, single=single)
            self.document.get_persistence().add_feature(self, new_feature)
            return new_feature

    def delete_children(self, nodes: Optional[List] = None,
                        exclude_nodes: Optional[List] = None):
        """Delete the children of this node, you can either supply a list of the nodes to delete
           or the nodes to exclude from the delete, if neither are supplied then we delete all the children.

           Note there is precedence in place, if you have provided a list of nodes to delete then the nodes
           to exclude is ignored.

        Args:
          nodes: Optional[List[ContentNode]] a list of content nodes that are children to delete
          exclude_nodes: Optional[List[ContentNode]] a list of content node that are children not to delete
          nodes: Optional[List]:  (Default value = None)
          exclude_nodes: Optional[List]:  (Default value = None)
        """
        children_to_delete = []

        for child_node in self.get_children():
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
            if child_to_delete in self.get_children():
                self.document.get_persistence().remove_content_node(child_to_delete)

    def get_feature(self, feature_type, name):
        """Gets the value for the given feature.

        Args:
          feature_type (str): The type of the feature.
          name (str): The name of the feature.

        Returns:
          ContentFeature or None: The feature with the specified type & name.  If no feature is found, None is returned.
          Note that if there are more than one instance of the feature you will only get the first one

        >>> new_page.get_feature('pagination','pageNum')
           1
        """
        hits = [i for i in self.get_features() if i.feature_type == feature_type and i.name == name]
        if len(hits) > 0:
            return hits[0]
        else:
            return None

    def get_features_of_type(self, feature_type):
        """Get all features of a specific type.

        Args:
          feature_type (str): The type of the feature.

        Returns:
          list[ContentFeature]: A list of feature with the specified type.  If no features are found, an empty list is returned.

        >>> new_page.get_features_of_type('my_type')
           []
        """
        return [i for i in self.get_features() if i.feature_type == feature_type]

    def has_feature(self, feature_type: str, name: str):
        """Determines if a feature with the given feature and name exists on this content node.

        Args:
          feature_type (str): The type of the feature.
          name (str): The name of the feature.

        Returns:
          bool: True if the feature is present; else, False.

        >>> new_page.has_feature('pagination','pageNum')
           True
        """
        return len([i for i in self.get_features() if i.feature_type == feature_type and i.name == name]) > 0

    def get_features(self):
        """Get all features on this ContentNode.

        Returns:
          list[ContentFeature]: A list of the features on this ContentNode.

        """
        return self.document.get_persistence().get_features(self)

    def remove_feature(self, feature_type: str, name: str, include_children: bool = False):
        """Removes the feature with the given name and type from this node.

        Args:
          feature_type (str): The type of the feature.
          name (str): The name of the feature.
          include_children (bool): also remove the feature from nodes children

        >>> new_page.remove_feature('pagination','pageNum')
        """
        self.document.get_persistence().remove_feature(self, feature_type, name)

        if include_children:
            for child in self.get_children():
                child.remove_feature(feature_type, name, include_children)

    def get_feature_value(self, feature_type: str, name: str) -> Optional[Any]:
        """Get the value for a feature with the given name and type on this ContentNode.

        Args:
          feature_type (str): The type of the feature.
          name (str): The name of the feature.

        Returns:
          Any or None: The value of the feature if it exists on this ContentNode otherwise, None, note this
          only returns the first value (check single to determine if there are multiple)

        >>> new_page.get_feature_value('pagination','pageNum')
           1
        """
        feature = self.get_feature(feature_type, name)

        # Need to make sure we handle the idea of a single value for a feature
        return None if feature is None else feature.value[0]

    def get_feature_values(self, feature_type: str, name: str) -> Optional[List[Any]]:
        """Get the value for a feature with the given name and type on this ContentNode.

        Args:
          feature_type (str): The type of the feature.
          name (str): The name of the feature.

        Returns:
          The list of feature values or None if there is no feature

        >>> new_page.get_feature_value('pagination','pageNum')
           1
        """
        feature = self.get_feature(feature_type, name)

        # Simply return all the feature values
        return None if feature is None else feature.value

    def get_content(self):
        """Get the content of this node.

        Args:

        Returns:
          str: The content of this ContentNode.

        >>> new_page.get_content()
           "This is page one"
        """
        return self.content

    def get_node_type(self):
        """Get the type of this node.

        Args:

        Returns:
          str: The type of this ContentNode.

        >>> new_page.get_content()
           "page"
        """
        return self.node_type

    def select_first(self, selector, variables=None):
        """Select and return the first child of this node that match the selector value.

        Args:
          selector (str): The selector (ie. //*)
          variables (dict, optional): A dictionary of variable name/value to use in substituion; defaults to None.  Dictionary keys should match a variable specified in the selector.

        Returns:
          Optional[ContentNode]: The first matching node or none

        >>> document.get_root().select_first('.')
           ContentNode

        >>> document.get_root().select_first('//*[hasTag($tagName)]', {"tagName": "div"})
           ContentNode
        """
        result = self.select(selector, variables)
        return result[0] if len(result) > 0 else None

    def select(self, selector, variables=None):
        """Select and return the child nodes of this node that match the selector value.

        Args:
          selector (str): The selector (ie. //*)
          variables (dict, optional): A dictionary of variable name/value to use in substituion; defaults to None.  Dictionary keys should match a variable specified in the selector.

        Returns:
          list[ContentNode]: A list of the matching content nodes.  If no matches are found, the list will be empty.

        >>> document.get_root().select('.')
           [ContentNode]

        >>> document.get_root().select('//*[hasTag($tagName)]', {"tagName": "div"})
           [ContentNode]
        """
        if variables is None:
            variables = {}
        from kodexa.selectors import parse
        from kodexa.selectors.ast import SelectorContext
        context = SelectorContext(self.document)
        parsed_selector = parse(selector)
        self.document.get_persistence().flush_cache()
        return parsed_selector.resolve(self, variables, context)

    def get_all_content(self, separator=" ", strip=True):
        """Get this node's content, concatenated with all of its children's content.

        Args:
          separator(str, optional): The separator to use in joining content together; defaults to " ".
          strip(boolean, optional): Strip the result

        Returns:
          str: The complete content for this node concatenated with the content of all child nodes.

        >>> document.content_node.get_all_content()

            "This string is made up of multiple nodes"
        """
        s = ""
        children = self.get_content_parts()
        for part in children:
            if isinstance(part, str):
                if s != "":
                    s += separator
                s += part
            if isinstance(part, int):
                if s != "":
                    s += separator
                s += \
                    [child.get_all_content(separator, strip=strip) for child in self.get_children() if
                     child.index == part][
                        0]

        # We need to determine if we have missing children and add them to the end
        for child in self.get_children():
            if child.index not in self.get_content_parts():
                if s != "":
                    s += separator
                s += child.get_all_content(separator, strip=strip)

        return s.strip() if strip else s

    def adopt_children(self, nodes_to_adopt, replace=False):
        """This will take a list of content nodes and adopt them under this node, ensuring they are re-parented.

        Args:
          children (List[ContentNode]): A list of ContentNodes that will be added to the end of this node's children collection
          replace (bool): If True, will remove all current children and replace them with the new list; defaults to True

        >>> # select all nodes of type 'line', then the root node 'adopts' them
            >>> # and replaces all it's existing children with these 'line' nodes.
            >>> document.get_root().adopt_children(document.select('//line'), replace=True)
        """
        child_idx_base = 0

        # We need to copy this since we might well mutate
        # it as we adopt
        children = nodes_to_adopt.copy()
        for existing_child in self.get_children():
            if existing_child not in children:
                existing_child.index = child_idx_base
                self.document.get_persistence().update_node(existing_child)
            else:
                existing_child.index = children.index(existing_child)
                existing_child._parent_uuid = self.uuid
                self.document.get_persistence().update_node(existing_child)
            child_idx_base += 1

        # Copy to avoid mutation
        for new_child in children.copy():
            if new_child not in self.get_children():
                self.add_child(new_child, children.index(new_child))
                child_idx_base += 1

        if replace:
            # Copy to avoid mutation
            for child in self.get_children().copy():
                if child not in children:
                    self.remove_child(child)

    def remove_tag(self, tag_name):
        """Remove a tag from this content node.

        Args:
          str: tag_name: The name of the tag that should be removed.
          tag_name:

        Returns:

        >>> document.get_root().remove_tag('foo')
        """
        self.remove_feature('tag', tag_name)

    def set_statistics(self, statistics):
        """Set the spatial statistics for this node

        Args:
          statistics: the statistics object

        Returns:

        >>> document.select.('//page')[0].set_statistics(NodeStatistics())
        """
        self.add_feature("spatial", "statistics", statistics)

    def get_statistics(self):
        """Get the spatial statistics for this node


        :return: the statistics object (or None if not set)

        Args:

        Returns:

        >>> document.select.('//page')[0].get_statistics()
            <kodexa.spatial.NodeStatistics object at 0x7f80605e53c8>
        """
        return self.get_feature_value("spatial", "statistics")

    def set_bbox(self, bbox):
        """Set the bounding box for the node, this is structured as:

        [x1,y1,x2,y2]

        Args:
          bbox: the bounding box array


        >>> document.select.('//page')[0].set_bbox([10,20,50,100])
        """
        self.set_feature("spatial", "bbox", bbox)

    def get_bbox(self):
        """Get the bounding box for the node, this is structured as:

        [x1,y1,x2,y2]


        :return: the bounding box array

        >>> document.select.('//page')[0].get_bbox()
            [10,20,50,100]
        """
        return self.get_feature_value("spatial", "bbox")

    def set_bbox_from_children(self):
        """Set the bounding box for this node based on its children"""

        x_min = None
        x_max = None
        y_min = None
        y_max = None

        for child in self.get_children():
            child_bbox = child.get_bbox()
            if child_bbox:
                if not x_min or x_min > child_bbox[0]:
                    x_min = child_bbox[0]
                if not x_max or x_max < child_bbox[2]:
                    x_max = child_bbox[2]
                if not y_min or y_min > child_bbox[1]:
                    y_min = child_bbox[1]
                if not y_max or y_max < child_bbox[3]:
                    y_max = child_bbox[3]

        if x_min:
            self.set_bbox([x_min, y_min, x_max, y_max])

    def set_rotate(self, rotate):
        """Set the rotate of the node

        Args:
          rotate: the rotation of the node

        Returns:

        >>> document.select.('//page')[0].set_rotate(90)
        """
        self.add_feature("spatial", "rotate", rotate)

    def get_rotate(self):
        """Get the rotate of the node


        :return: the rotation of the node

        Args:

        Returns:

        >>> document.select.('//page')[0].get_rotate()
            90
        """
        return self.get_feature_value("spatial", "rotate")

    def get_x(self):
        """Get the X position of the node


        :return: the X position of the node

        Args:

        Returns:

        >>> document.select.('//page')[0].get_x()
            10
        """
        self_bbox = self.get_bbox()
        if self_bbox:
            return self_bbox[0]
        else:
            return None

    def get_y(self):
        """Get the Y position of the node


        :return: the Y position of the node

        Args:

        Returns:

        >>> document.select.('//page')[0].get_y()
            90
        """
        self_bbox = self.get_bbox()
        if self_bbox:
            return self_bbox[1]
        else:
            return None

    def get_width(self):
        """Get the width of the node


        :return: the width of the node

        Args:

        Returns:

        >>> document.select.('//page')[0].get_width()
            70
        """
        self_bbox = self.get_bbox()
        if self_bbox:
            return self_bbox[2] - self_bbox[0]
        else:
            return None

    def get_height(self):
        """Get the height of the node


        :return: the height of the node

        Args:

        Returns:

        >>> document.select.('//page')[0].get_height()
            40
        """
        self_bbox = self.get_bbox()
        if self_bbox:
            return self_bbox[3] - self_bbox[1]
        else:
            return None

    def copy_tag(self, selector=".", existing_tag_name=None, new_tag_name=None):
        """Creates a new tag of 'new_tag_name' on the selected content node(s) with the same information as the tag with 'existing_tag_name'.
        Both existing_tag_name and new_tag_name values are required and must be different from one another.  Otherwise, no action is taken.
        If a tag with the 'existing_tag_name' does not exist on a selected node, no action is taken for that node.

        Args:
          selector: The selector to identify the source nodes to work on (default . - the current node)
          str: existing_tag_name: The name of the existing tag whose values will be copied to the new tag.
          str: new_tag_name: The name of the new tag.  This must be different from the existing_tag_name.
          existing_tag_name:  (Default value = None)
          new_tag_name:  (Default value = None)

        Returns:

        >>> document.get_root().copy_tag('foo', 'bar')
        """
        if existing_tag_name is None or new_tag_name is None or existing_tag_name == new_tag_name:
            return  # do nothing, just exit function

        for node in self.select(selector):
            existing_tag_values = node.get_feature_values('tag', existing_tag_name)
            if existing_tag_values:
                for val in existing_tag_values:
                    tag = Tag(start=val['start'], end=val['end'], value=val['value'], uuid=val['uuid'],
                              data=val['data'])
                    node.add_feature('tag', new_tag_name, tag)

    def collect_nodes_to(self, end_node):
        """Get the the sibling nodes between the current node and the end_node.

        Args:
          ContentNode: end_node: The node to end at
          end_node:

        Returns:
          list[ContentNode]: A list of sibling nodes between this node and the end_node.

        >>> document.content_node.get_children()[0].collect_nodes_to(end_node=document.content_node.get_children()[5])
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

    def tag_nodes_to(self, end_node, tag_to_apply, tag_uuid: str = None):
        """Tag all the nodes from this node to the end_node with the given tag name

        Args:
          end_node (ContentNode): The node to end with
          tag_to_apply (str): The tag name that will be applied to each node
          tag_uuid (str): The tag uuid used if you want to group them

        >>> document.content_node.get_children()[0].tag_nodes_to(document.content_node.get_children()[5], tag_name='foo')
        """
        [node.tag(tag_to_apply, tag_uuid=tag_uuid) for node in self.collect_nodes_to(end_node)]

    def tag_range(self, start_content_re, end_content_re, tag_to_apply, node_type_re='.*', use_all_content=False):
        """This will tag all the child nodes between the start and end content regular expressions

        Args:
          start_content_re: The regular expression to match the starting child
          end_content_re: The regular expression to match the ending child
          tag_to_apply: The tag name that will be applied to the nodes in range
          node_type_re: The node type to match (default is all)
          use_all_content: Use full content (including child nodes, default is False)

        Returns:

        >>> document.content_node.tag_range(start_content_re='.*Cheese.*', end_content_re='.*Fish.*', tag_to_apply='foo')
        """

        # Could be line, word, or content-area
        all_nodes = self.select(f"//*[typeRegex('{node_type_re}')]")

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

    def tag(self, tag_to_apply, selector=".", content_re=None,
            use_all_content=False, node_only=None,
            fixed_position=None, data=None, separator=" ", tag_uuid: str = None, confidence=None, value=None,
            use_match=True, index=None, cell_index=None, group_uuid=None, parent_group_uuid=None):
        """
        This will tag (see Feature Tagging) the expression groups identified by the regular expression.

        Note that if you use the flag use_all_content then node_only will default to True if not set, else it
        will default to False

        Args:
          tag_to_apply: The name of tag that will be applied to the node
          selector: The selector to identify the source nodes to work on (default . - the current node)
          content_re: The regular expression that you wish to use to tag, note that we will create a tag for each matching group (Default value = None)
          use_all_content: Apply the regular expression to the all_content (include content from child nodes) (Default value = False)
          separator: Separator to use for use_all_content (Default value = " ")
          node_only: Ignore the matching groups and tag the whole node (Default value = None)
          fixed_position: Use a fixed position, supplied as a tuple i.e. - (4,10) tag from position 4 to 10 (default None)
          data: A dictionary of data for the given tag (Default value = None)
          tag_uuid: A UUID used to tie tags in order to demonstrate they're related and form a single concept.
            For example, if tagging the two words "Wells" and "Fargo" as an ORGANIZATION, the tag on both words should have the
            same tag_uuid in order to indicate they are both needed to form the single ORGANIZATION.  If a tag_uuid is provided, it is used
            on all tags created in this method.  This may result in multiple nodes or multiple feature values having the same tag_uuid.
            For example, if the selector provided results in more than one node being selected, each node would be tagged with the same tag_uuid.
            The same holds true if a content_re value is provided, node_only is set to False, and multiple matches are found for the content_re
            pattern.  In that case, each feature value would share the same UUID.
            If no tag_uuid is provided, a new uuid is generated for each tag instance.
              tag_uuid: str:  (Default value = None)
          confidence: The confidence in the tag (0-1)
          value: The value you wish to store with the tag, this allows you to provide text that isn't part of the content but represents the data you wish tagged
          use_match: If True (default) we will use match for regex matching, if False we will use search
          index: The index for the tag
          cell_index: The cell index for the tag
          group_uuid: The group uuid for the tag
          parent_group_uuid: The parent group uuid for the tag

        >>> document.content_node.tag('is_cheese')
        """

        if use_all_content and node_only is None:
            node_only = True
        elif node_only is None:
            node_only = False

        def get_tag_uuid(tag_uuid):
            if tag_uuid:
                return tag_uuid
            else:
                return str(uuid.uuid4())

        def tag_node_position(node_to_check, start, end, node_data, tag_uuid, offset=0, value=None):
            content_length = 0
            original_start = start
            original_end = end
            for part_idx, part in enumerate(node_to_check.get_content_parts()):
                if isinstance(part, str):
                    if len(part) > 0:
                        # It is just content
                        part_length = len(part)
                        if part_idx > 0:
                            end = end - len(separator)
                            content_length = content_length + len(separator)
                            offset = offset + len(separator)
                            start = 0 if start - len(separator) < 0 else start - len(separator)

                        if start < part_length and end < part_length:
                            node_to_check.add_feature('tag', tag_to_apply,
                                                      Tag(original_start, original_end,
                                                          part[start:end] if value is None else value,
                                                          data=node_data, uuid=tag_uuid, confidence=confidence,
                                                          index=index, parent_group_uuid=parent_group_uuid,
                                                          group_uuid=group_uuid, cell_index=cell_index))
                            return -1
                        elif start < part_length <= end:
                            node_to_check.add_feature('tag', tag_to_apply,
                                                      Tag(original_start,
                                                          content_length + part_length,
                                                          value=part[start:] if value is None else value,
                                                          data=node_data, uuid=tag_uuid, confidence=confidence,
                                                          index=index, parent_group_uuid=parent_group_uuid,
                                                          group_uuid=group_uuid, cell_index=cell_index))

                        end = end - part_length
                        content_length = content_length + part_length
                        offset = offset + part_length
                        start = 0 if start - part_length < 0 else start - part_length

                elif isinstance(part, int):
                    child_node = [child for child in node_to_check.get_children() if child.index == part][0]

                    if part_idx > 0:
                        end = end - len(separator)
                        content_length = content_length + len(separator)
                        offset = offset + len(separator)
                        start = 0 if start - len(separator) < 0 else start - len(separator)

                    result = tag_node_position(child_node, start, end, node_data, tag_uuid,
                                               offset=offset, value=value)

                    if result < 0 or (end - result) <= 0:
                        return -1
                    else:

                        offset = offset + result
                        end = end - result
                        start = 0 if start - result < 0 else start - result

                        content_length = content_length + result
                else:
                    raise Exception("Invalid part?")

            # We need to determine if we have missing children and add them to the end
            for child_idx, child_node in enumerate(node_to_check.get_children()):
                if child_node.index not in node_to_check.get_content_parts():

                    if content_length > 0:
                        end = end - len(separator)
                        content_length = content_length + len(separator)
                        offset = offset + len(separator)
                        start = 0 if start - len(separator) < 0 else start - len(separator)

                    result = tag_node_position(child_node, start, end, node_data, tag_uuid,
                                               offset=offset, value=value)

                    if result < 0 or (end - result) <= 0:
                        return -1
                    else:
                        offset = offset + result
                        end = end - result
                        start = 0 if start - result < 0 else start - result

                        content_length = content_length + result

            if len(node_to_check.get_all_content(strip=False)) != content_length:
                raise Exception(
                    f"There is a problem in the structure? (2) Length mismatch ({len(node_to_check.get_all_content(strip=False))} != {content_length})")

            return content_length

        if content_re:
            pattern = re.compile(content_re.replace(' ', '\s+') if use_all_content and not node_only else content_re)

        for node in self.select(selector):
            if fixed_position:
                tag_node_position(node, fixed_position[0], fixed_position[1], data, get_tag_uuid(tag_uuid), 0,
                                  value=value)

            else:
                if not content_re:
                    node.add_feature('tag', tag_to_apply,
                                     Tag(data=data, uuid=get_tag_uuid(tag_uuid), confidence=confidence, value=value,
                                         index=index, parent_group_uuid=parent_group_uuid, group_uuid=group_uuid,
                                         cell_index=cell_index))
                else:
                    if not use_all_content:
                        if node.content:
                            content = node.content
                        else:
                            content = None
                    else:
                        content = node.get_all_content(separator=separator,
                                                       strip=False) if not node_only else node.get_all_content(
                            separator=separator)

                    if content is not None:
                        if use_match:
                            matches = pattern.finditer(content)

                            if node_only:
                                if any(True for _ in matches):
                                    node.add_feature('tag', tag_to_apply,
                                                     Tag(data=data, uuid=get_tag_uuid(tag_uuid), confidence=confidence,
                                                         value=value, index=index, parent_group_uuid=parent_group_uuid,
                                                         group_uuid=group_uuid, cell_index=cell_index))
                            else:
                                if matches:
                                    for match in matches:
                                        start_offset = match.span()[0]
                                        end_offset = match.span()[1]
                                        tag_node_position(node, start_offset, end_offset, data, get_tag_uuid(tag_uuid),
                                                          value=value)

                        else:
                            search_match = pattern.search(content)
                            if search_match is not None:
                                start_offset = search_match.span()[0]
                                end_offset = search_match.span()[1]
                                tag_node_position(node, start_offset, end_offset, data, get_tag_uuid(tag_uuid),
                                                  value=value)

    def get_tags(self):
        """Returns a list of the names of the tags on the given node


        :return: A list of the tag name

        Args:

        Returns:

        >>> document.content_node.select('*').get_tags()
            ['is_cheese']
        """
        return [i.name for i in self.get_features_of_type("tag")]

    def get_tag_features(self):
        """Returns a list of the features that are tags on the given node


        :return: A list of the tag name

        Args:

        Returns:

        >>> document.content_node.select('*').get_tag_features()
            [ContentFeature()]
        """
        return [i for i in self.get_features_of_type("tag")]

    def get_tag_values(self, tag_name, include_children=False):
        """Get the values for a specific tag name

        Args:
          tag_name: tag name
          include_children: include the children of this node (Default value = False)

        Returns:
          a list of the tag values

        """
        values = []
        for tag in self.get_tag(tag_name):
            values.append(tag['value'])

        if include_children:
            for child in self.get_children():
                values.extend(child.get_tag_values(tag_name, include_children))

        return values

    def get_related_tag_values(self, tag_name: str, include_children: bool = False, value_separator: str = ' ',
                               tag_uuid=None):
        """Get the values for a specific tag name, grouped by uuid

        Args:
          tag_name (str): tag name
          include_children (bool): include the children of this node
          value_separator (str): the string to be used to join related tag values

        Returns:
          a list of the tag values

        """

        def group_tag_values(group_dict, feature_val, tag_uuid, tag_node):
            # we know the names of all these tags are the same, but we want to group them if they share the same uuid

            if feature_val['uuid'] != tag_uuid:
                return

            final_value = feature_val['value'] if 'value' in feature_val else None
            if final_value is None:
                final_value = tag_node.content

            if feature_val['uuid'] in value_groups.keys():
                # we've seen this UUID - add it's value to the group
                group_dict[feature_val['uuid']].append(final_value)
            else:
                # first occurrence
                group_dict[feature_val['uuid']] = [final_value]

        if include_children:
            tagged_nodes = self.document.get_tagged_nodes(tag_name, tag_uuid=tag_uuid)
        else:
            tagged_nodes = self.select('.')

        value_groups: Dict[str, Any] = {}
        for tag_node in tagged_nodes:
            tag_feature_vals = tag_node.get_feature_value('tag', tag_name)
            if tag_feature_vals:
                if not isinstance(tag_feature_vals, list):
                    tag_feature_vals = [tag_feature_vals]

                for v in tag_feature_vals:
                    group_tag_values(value_groups, v, tag_uuid, tag_node)

        value_strings = []
        for k in value_groups.keys():
            if value_groups[k] and len(value_groups[k]) > 0 and value_groups[k][0] is not None:
                value_strings.append(value_separator.join(value_groups[k]))

        return value_strings

    def get_related_tag_nodes(self, tag_name: str, everywhere: bool = False, tag_uuid=None):
        """Get the nodes for a specific tag name, grouped by uuid

        Args:
          tag_name (str): tag name
          everywhere (bool): include the children of this node
          tag_uuid (optional(str)): if set we will only get nodes related to this tag UUID

        Returns:
          a dictionary that groups nodes by tag UUID

        """
        if everywhere:
            tagged_nodes = self.document.get_tagged_nodes(tag_name, tag_uuid)
        else:
            tagged_nodes = [self]

        # We need to group these nodes together based on the TAG UUID

        node_groups = {}

        for tagged_node in tagged_nodes:
            tag_instances = tagged_node.get_tag(tag_name)

            for tag_instance in tag_instances:
                if tag_instance['uuid'] not in node_groups:
                    node_groups[tag_instance['uuid']] = [tagged_node]
                else:
                    node_groups[tag_instance['uuid']].append(tagged_node)

        return node_groups

    def get_tag(self, tag_name, tag_uuid=None):
        """Returns the value of a tag (a dictionary), this can be either a single value in a list [[start,end,value]] or if multiple parts of the
        content of this node match you can end up with a list of lists i.e. [[start1,end1,value1],[start2,end2,value2]]

        Args:
          tag_name: The name of the tag
          tag_uuid (Optional): Optionally you can also provide the tag UUID

        Returns:
          A list tagged location and values for this label in this node

        >>> document.content_node.select_first('//*[contentRegex(".*Cheese.*")]').get_tag('is_cheese')
            [0,10,'The Cheese Moved']
        """
        tag_details = self.get_feature_value('tag', tag_name)

        if tag_details is None:
            return []

        if not isinstance(tag_details, list):
            tag_details = [tag_details]

        final_result = []
        for tag_detail in tag_details:
            if 'uuid' in tag_detail and tag_uuid:
                if tag_detail['uuid'] == tag_uuid:
                    final_result.append(tag_detail)
            else:
                final_result.append(tag_detail)
        return final_result

    def get_all_tags(self):
        """Get the names of all tags that have been applied to this node or to its children.

        Args:

        Returns:
          list[str]: A list of the tag names belonging to this node and/or its children.

        >>> document.content_node.select_first('//*[contentRegex(".*Cheese.*")]').get_all_tags()
            ['is_cheese']
        """
        tags = []
        tags.extend(self.get_tags())
        for child in self.get_children():
            tags.extend(child.get_all_tags())
        return list(set(tags))

    def has_tags(self):
        """Determines if this node has any tags at all.

        Args:

        Returns:
          bool: True if node has any tags; else, False;

        >>> document.content_node.select_first('//*[contentRegex(".*Cheese.*")]').has_tags()
            True
        """
        return len([i.value for i in self.get_features_of_type("tag")]) > 0

    def has_tag(self, tag, include_children=False):
        """Determine if this node has a tag with the specified name.

        Args:
          tag(str): The name of the tag.
          include_children(bool): should we include child nodes

        Returns:
          bool: True if node has a tag by the specified name; else, False;

        >>> document.content_node.select_first('//*[contentRegex(".*Cheese.*")]').has_tag('is_cheese')
            True
            >>> document.content_node.select_first('//*[contentRegex(".*Cheese.*")]').has_tag('is_fish')
            False
        """
        for feature in self.get_features():
            if feature.feature_type == 'tag' and feature.name == tag:
                return True
        result = False
        if include_children:
            for child in self.get_children():
                if child.has_tag(tag, True):
                    result = True
        return result

    def is_first_child(self):
        """Determines if this node is the first child of its parent or has no parent.

        Args:

        Returns:
          bool: True if this node is the first child of its parent or if this node has no parent; else, False;

        """
        if not self.parent:
            return True
        else:
            return self.index == 0

    def is_last_child(self):
        """Determines if this node is the last child of its parent or has no parent.

        Returns:
          bool: True if this node is the last child of its parent or if this node has no parent; else, False;

        """

        if not self.get_parent():
            return True
        else:
            return self.index == self.get_parent().get_last_child_index()

    def get_last_child_index(self):
        """Returns the max index value for the children of this node. If the node has no children, returns None.

        Returns:
          int or None: The max index of the children of this node, or None if there are no children.

        """

        if not self.get_children():
            return None

        max_index = 0
        for child in self.get_children():
            if child.index > max_index:
                max_index = child.index

        return max_index

    def get_node_at_index(self, index):
        """Returns the child node at the specified index. If the specified index is outside the first (0), or
        last child's index, None is returned.

        Note:  documents allow for sparse representation and child nodes may not have consecutive index numbers.
        If there isn't a child node at the specfied index, a 'virtual' node will be returned.  This 'virtual' node
        will have the node type of its nearest sibling and will have an index value, but will have no features or content.

        Args:
          index (int): The index (zero-based) for the child node.

        Returns:
          ContentNode or None: Node at index, or None if the index is outside the boundaries of child nodes.

        """
        if self.get_children():

            if index < self.get_children()[0].index:
                virtual_node = self.document.create_node(node_type=self.get_children()[0].node_type, virtual=True,
                                                         parent=self,
                                                         index=index)
                return virtual_node

            last_child = None
            for child in self.get_children():
                if child.index < index:
                    last_child = child
                elif child.index == index:
                    return child
                else:
                    break

            if last_child:
                if last_child.index != index and index < self.get_children()[-1].index:
                    virtual_node = self.document.create_node(node_type=last_child.node_type, virtual=True, parent=self,
                                                             index=index)
                    return virtual_node
            else:
                return None
        else:
            return None

    def has_next_node(self, node_type_re=".*", skip_virtual=False):
        """Determine if this node has a next sibling that matches the type specified by the node_type_re regex.

        Args:
          node_type_re(str, optional, optional): The regular expression to match against the next sibling node's type; default is '.*'.
          skip_virtual(bool, optional, optional): Skip virtual nodes and return the next real node; default is False.

        Returns:
          bool: True if there is a next sibling node matching the specified type regex; else, False.

        """
        return self.next_node(node_type_re, skip_virtual=skip_virtual) is not None

    def has_previous_node(self, node_type_re=".*", skip_virtual=False):
        """Determine if this node has a previous sibling that matches the type specified by the node_type_re regex.

        Args:
          node_type_re(str, optional, optional): The regular expression to match against the previous sibling node's type; default is '.*'.
          skip_virtual(bool, optional, optional): Skip virtual nodes and return the next real node; default is False.

        Returns:
          bool: True if there is a previous sibling node matching the specified type regex; else, False.

        """
        return self.previous_node(node_type_re=node_type_re, skip_virtual=skip_virtual) is not None

    def next_node(self, node_type_re='.*', skip_virtual=False, has_no_content=True):
        """Returns the next sibling content node.

        Note:  This logic relies on node indexes.  Documents allow for sparse representation and child nodes may not have consecutive index numbers.
        Therefore, the next node might actually be a virtual node that is created to fill a gap in the document.  You can skip virtual nodes by setting the
        skip_virtual parameter to False.

        Args:
          node_type_re(str, optional, optional): The regular expression to match against the next sibling node's type; default is '.*'.
          skip_virtual(bool, optional, optional): Skip virtual nodes and return the next real node; default is False.
          has_no_content(bool, optional, optional): Allow a node that has no content to be returned; default is True.

        Returns:
          ContentNode or None: The next node or None, if no node exists

        """
        search_index = self.index + 1
        compiled_node_type_re = re.compile(node_type_re)

        while True:
            node = self.get_parent().get_node_at_index(search_index) if self.get_parent() else None

            if not node:
                return node

            if compiled_node_type_re.match(node.node_type) and (not skip_virtual or not node.virtual):
                if (not has_no_content and node.content) or has_no_content:
                    return node

            search_index += 1

    def previous_node(self, node_type_re='.*', skip_virtual=False, has_no_content=False, traverse=Traverse.SIBLING):
        """Returns the previous sibling content node.

        Note:  This logic relies on node indexes.  Documents allow for sparse representation and child nodes may not have consecutive index numbers.
        Therefore, the previous node might actually be a virtual node that is created to fill a gap in the document.  You can skip virtual nodes by setting the
        skip_virtual parameter to False.

        Args:
          node_type_re(str, optional, optional): The regular expression to match against the previous node's type; default is '.*'.
          skip_virtual(bool, optional, optional): Skip virtual nodes and return the next real node; default is False.
          has_no_content(bool, optional, optional): Allow a node that has no content to be returned; default is False.
          traverse(Traverse(enum), optional, optional): The transition you'd like to traverse (SIBLING, CHILDREN, PARENT, or ALL); default is Traverse.SIBLING.

        Returns:
          ContentNode or None: The previous node or None, if no node exists

        """

        # TODO: implement/differentiate traverse logic for CHILDREN and SIBLING
        if self.index == 0:
            if traverse == traverse.ALL or traverse == traverse.PARENT and self.get_parent():
                # Lets look for a previous node on the parent
                return self.get_parent().previous_node(node_type_re, skip_virtual, has_no_content, traverse)
            else:
                return None

        search_index = self.index - 1
        compiled_node_type_re = re.compile(node_type_re)

        while True:
            node = self.get_parent().get_node_at_index(search_index)

            if not node:
                return node

            if compiled_node_type_re.match(node.node_type) and (not skip_virtual or not node.virtual):
                if (not has_no_content) or (has_no_content and not node.content):
                    return node

            search_index -= 1


class ContentFeature(object):
    """A feature allows you to capture almost any additional data or metadata and associate it with a ContentNode"""

    def __init__(self, feature_type: str, name: str, value: Any, single: bool = True):
        self.feature_type: str = feature_type
        """The type of feature, a logical name to group feature types together (ie. spatial)"""
        self.name: str = name
        """The name of the feature (ie. bbox)"""
        self.value: Any = value
        """Description of the feature (Optional)"""
        self.single: bool = single
        """Determines whether the data for this feature is a single instance or an array, if you have added the same feature to the same node you will end up with multiple data elements in the content feature and the single flag will be false"""

    def __str__(self):
        return f"Feature [type='{self.feature_type}' name='{self.name}' value='{self.value}' single='{self.single}']"

    def to_dict(self):
        """Create a dictionary representing this ContentFeature's structure and content.
        Returns:
          dict: The properties of this ContentFeature structured as a dictionary.

        >>> node.to_dict()
        """
        return {'name': self.feature_type + ':' + self.name, 'value': self.value, 'single': self.single}

    def get_value(self):
        """Get the value from the feature. This method will handle the single flag

           Returns:
              The value of the feature
        """
        if self.single:
            return self.value[0]
        else:
            return self.value


@dataclasses.dataclass()
class SourceMetadata:
    """Class for keeping track of the original source information for a
    document

    Args:

    Returns:

    """
    original_filename: Optional[str] = None
    original_path: Optional[str] = None
    checksum: Optional[str] = None

    # The ID used for internal caching
    cid: Optional[str] = None
    last_modified: Optional[str] = None
    created: Optional[str] = None
    connector: Optional[str] = None
    mime_type: Optional[str] = None
    headers: Optional[Dict] = None

    # The UUID of the document that this document was derived from
    # noting that multiple documents coming from an original source
    lineage_document_uuid: Optional[str] = None

    # The UUID of the original first document
    source_document_uuid: Optional[str] = None

    # The UUID of the document in a PDF form (used for archiving and preview)
    pdf_document_uuid: Optional[str] = None

    @classmethod
    def from_dict(cls, env):
        """

        Args:
          env:

        Returns:

        """
        return cls(**{
            k: v for k, v in env.items()
            if k in inspect.signature(cls).parameters
        })


class ContentClassification(object):
    """A content classification captures information at the document level to track classification metadata"""

    def __init__(self, label: str, taxonomy: Optional[str] = None, selector: Optional[str] = None,
                 confidence: Optional[float] = None):
        self.label = label
        self.taxonomy = taxonomy
        self.selector = selector
        self.confidence = confidence

    def to_dict(self):
        return {"label": self.label, "taxonomy": self.taxonomy, "selector": self.selector,
                "confidence": self.confidence}

    @classmethod
    def from_dict(cls, dict_val):
        return ContentClassification(label=dict_val['label'], taxonomy=dict_val.get('taxonomy'),
                                     selector=dict_val.get('selector'), confidence=dict_val.get('confidence'))


class Document(object):
    """A Document is a collection of metadata and a set of content nodes."""

    PREVIOUS_VERSION: str = "1.0.0"
    CURRENT_VERSION: str = "4.0.1"

    def __str__(self):
        return f"kodexa://{self.uuid}"

    def __init__(self, metadata=None, content_node: ContentNode = None, source=None, ref: str = None,
                 kddb_path: str = None, delete_on_close=False):
        if metadata is None:
            metadata = DocumentMetadata()
        if source is None:
            source = SourceMetadata()

        # Mix-ins are going away - so we will allow people to turn them off as needed
        self.disable_mixin_methods = True

        self.delete_on_close = delete_on_close

        # The ref is not stored and is used when we have
        # initialized a document from a remote store and want
        # to keep track of that
        self.ref = ref

        self.metadata: DocumentMetadata = metadata
        """Metadata relating to the document"""
        self._content_node: Optional[ContentNode] = content_node
        """The root content node"""
        self.virtual: bool = False
        """Is the document virtual (deprecated)"""
        self._mixins: List[str] = []
        """A list of the mixins for this document"""
        self.uuid: str = str(uuid.uuid4())
        """The UUID of this document"""
        self.exceptions: List = []
        """A list of the exceptions on this document (deprecated)"""
        self.log: List[str] = []
        """A log for this document (deprecated)"""
        self.version = Document.CURRENT_VERSION
        """The version of the document"""
        self.source: SourceMetadata = source
        """Source metadata for this document"""
        self.labels: List[str] = []
        """A list of the document level labels for the document"""
        self.taxonomies: List[str] = []
        """A list of the taxonomy references for this document"""
        self.classes: List[ContentClassification] = []
        """A list of the content classifications associated at the document level"""

        self.add_mixin('core')

        # Start persistence layer
        from kodexa.model import PersistenceManager

        self._persistence_layer: Optional[PersistenceManager] = PersistenceManager(document=self,
                                                                                   filename=kddb_path,
                                                                                   delete_on_close=delete_on_close)
        self._persistence_layer.initialize()

    def get_persistence(self):
        return self._persistence_layer

    def get_all_tags(self):
        return self._persistence_layer.get_all_tags()

    def get_tagged_nodes(self, tag_name, tag_uuid=None):
        return self._persistence_layer.get_tagged_nodes(tag_name, tag_uuid)

    # def get_content_exceptions(self) -> List[ContentException]:
    #     return self._persistence_layer.get_content_exceptions()
    # 
    # def add_content_exception(self, content_exception: ContentException):
    #     self._persistence_layer.add_content_exception(content_exception)

    @property
    def content_node(self):
        """The root content Node"""
        return self._content_node

    @content_node.setter
    def content_node(self, value):
        value.index = 0
        if value != self._content_node and self._content_node is not None:
            self.get_persistence().remove_content_node(self._content_node)

        self._content_node = value
        if value is not None:
            self.get_persistence().add_content_node(self._content_node, None)

    def add_classification(self, label: str, taxonomy_ref: Optional[str] = None) -> ContentClassification:
        """Add a content classification to the document

        Args:
          label(str): the label
          taxonomy_ref(Optional[str]): the reference to the taxonomy

        Returns:
          the content classification created (or the matching one if it is already on the document)

        """
        content_classification = ContentClassification(label, taxonomy=taxonomy_ref)

        for existing_class in self.classes:
            if existing_class.label == content_classification.label:
                return existing_class

        self.classes.append(content_classification)
        return content_classification

    def add_label(self, label: str):
        """Add a label to the document

        Args:
          label: str Label to add
          label: str:

        Returns:
          the document

        """
        if label not in self.labels:
            self.labels.append(label)

        return self

    def remove_label(self, label: str):
        """Remove a label from the document

        Args:
          label: str Label to remove
          label: str:

        Returns:
          the document

        """
        self.labels.remove(label)
        return self

    @classmethod
    def from_text(cls, text, separator=None):
        """Creates a new Document from the text provided.

        Args:
          text: str  Text to be used as content on the Document's ContentNode(s)
          separator: str   If provided, this string will be used to split the text and the resulting text will be placed on children of the root ContentNode. (Default value = None)

        Returns:
          the document

        """
        new_document = Document()
        new_document.source.original_filename = f'text-{uuid.uuid4()}'
        new_document.content_node = new_document.create_node(node_type='text', index=0)
        if text:
            if separator:
                for s in text.split(separator):
                    new_document.content_node.add_child(new_document.create_node(node_type='text', content=s))
            else:
                new_document.content_node.content = text

        new_document.add_mixin('text')
        return new_document

    def get_root(self):
        """Get the root content node for the document (same as content_node)"""
        return self.content_node

    def to_kdxa(self, file_path: str):
        """Write the document to the kdxa format (msgpack) which can be
        used with the Kodexa platform

        Args:
          file_path: the path to the mdoc you wish to create
          file_path: str:

        Returns:

        >>> document.to_mdoc('my-document.kdxa')
        """
        with open(file_path, 'wb') as outfile:
            msgpack.pack(self.to_dict(), outfile, use_bin_type=True)

    @staticmethod
    def open_kddb(file_path):
        """
        Opens a Kodexa Document Database.

        This is the Kodexa V4 default way to store documents, it provides high-performance
        and also the ability to handle very large document objects

        :param file_path: The file path
        :return: The Document instance
        """
        return Document(kddb_path=file_path)

    def close(self):
        """
        Close the document and clean up the resources
        """
        self.get_persistence().close()

    def to_kddb(self, path=None):
        """
        Either write this document to a KDDB file or convert this document object structure into a KDDB and return a bytes-like object

        This is dependent on whether you provide a path to write to
        """

        if path is None:
            return self.get_persistence().get_bytes()
        else:
            with open(path, 'wb') as output_file:
                output_file.write(self.get_persistence().get_bytes())

    @staticmethod
    def from_kdxa(file_path):
        """Read an .kdxa file from the given file_path and

        Args:
          file_path: the path to the mdoc file

        Returns:

        >>> document = Document.from_kdxa('my-document.kdxa')
        """
        with open(file_path, 'rb') as data_file:
            data_loaded = msgpack.unpack(data_file, raw=False)
        return Document.from_dict(data_loaded)

    def to_msgpack(self):
        """Convert this document object structure into a message pack"""
        return msgpack.packb(self.to_dict(), use_bin_type=True)

    def to_json(self):
        """Create a JSON string representation of this Document.

        Args:

        Returns:
          str: The JSON formatted string representation of this Document.

        >>> document.to_json()
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)

    def to_dict(self):
        """Create a dictionary representing this Document's structure and content.

        Args:

        Returns:
          dict: A dictionary representation of this Document.

        >>> document.to_dict()
        """

        # We don't want to store the none values
        def clean_none_values(d):
            """

            Args:
              d:

            Returns:

            """
            clean = {}
            for k, v in d.items():
                if isinstance(v, dict):
                    nested = clean_none_values(v)
                    if len(nested.keys()) > 0:
                        clean[k] = nested
                elif v is not None:
                    clean[k] = v
            return clean

        return {'version': Document.CURRENT_VERSION, 'metadata': self.metadata,
                'content_node': self.content_node.to_dict() if self.content_node else None,
                'source': clean_none_values(dataclasses.asdict(self.source)),
                'mixins': self._mixins,
                'taxonomies': self.taxonomies,
                'classes': [content_class.to_dict() for content_class in self.classes],
                'exceptions': self.exceptions,
                'log': self.log,
                'labels': self.labels,
                'uuid': self.uuid}

    @staticmethod
    def from_dict(doc_dict):
        """Build a new Document from a dictionary.

        Args:
          dict: doc_dict: A dictionary representation of a Kodexa Document.
          doc_dict:

        Returns:
          Document: A complete Kodexa Document

        >>> Document.from_dict(doc_dict)
        """
        new_document = Document(DocumentMetadata(doc_dict['metadata']))
        for mixin in doc_dict['mixins']:
            registry.add_mixin_to_document(mixin, new_document)
        new_document.version = doc_dict['version'] if 'version' in doc_dict and doc_dict[
            'version'] else Document.PREVIOUS_VERSION  # some older docs don't have a version or it's None
        new_document.log = doc_dict['log'] if 'log' in doc_dict else []
        new_document.exceptions = doc_dict['exceptions'] if 'exceptions' in doc_dict else []
        new_document.uuid = doc_dict['uuid'] if 'uuid' in doc_dict else str(
            uuid.uuid5(uuid.NAMESPACE_DNS, 'kodexa.com'))

        if 'content_node' in doc_dict and doc_dict['content_node']:
            new_document.content_node = ContentNode.from_dict(new_document, doc_dict['content_node'])

        if 'source' in doc_dict and doc_dict['source']:
            new_document.source = SourceMetadata.from_dict(doc_dict['source'])
        if 'labels' in doc_dict and doc_dict['labels']:
            new_document.labels = doc_dict['labels']
        if 'taxomomies' in doc_dict and doc_dict['taxomomies']:
            new_document.labels = doc_dict['taxomomies']
        if 'classes' in doc_dict and doc_dict['classes']:
            new_document.classes = [ContentClassification.from_dict(content_class) for content_class in
                                    doc_dict['classes']]

        new_document.get_persistence().update_metadata()
        return new_document

    @staticmethod
    def from_json(json_string):
        """Create an instance of a Document from a JSON string.

        Args:
          str: json_string: A JSON string representation of a Kodexa Document
          json_string:

        Returns:
          Document: A complete Kodexa Document

        >>> Document.from_json(json_string)
        """
        return Document.from_dict(json.loads(json_string))

    @staticmethod
    def from_msgpack(bytes):
        """Create an instance of a Document from a message pack byte array.

        Args:
          bytes: bytes: A message pack byte array.

        Returns:
          Document: A complete Kodexa Document

        >>> Document.from_msgpack(open(os.path.join('news-doc.kdxa'), 'rb').read())
        """
        return Document.from_dict(msgpack.unpackb(bytes, raw=False))

    def get_mixins(self):
        """Get the list of mixins that have been enabled on this document."""
        return self._mixins

    def add_mixin(self, mixin):
        """Add the given mixin to this document,  this will apply the mixin to all the content nodes,
        and also register it with the document so that future invocations of create_node will ensure
        the node has the mixin appled.

        Args:
          mixin:

        Returns:

        >>> document.add_mixin('spatial')
        """
        registry.add_mixin_to_document(mixin, self)

    def create_node(self, node_type: str, content: Optional[str] = None, virtual: bool = False,
                    parent: ContentNode = None,
                    index: Optional[int] = None):
        """
        Creates a new node for the document.  The new node is not added to the document, but any mixins that have been
        applied to the document will also be available on the new node.

        Args:
          node_type (str): The type of node.
          content (str): The content for the node; defaults to None.
          virtual (bool): Indicates if this is a 'real' or 'virtual' node; default is False.  'Real' nodes contain
                          document content. 'Virtual' nodes are synthesized as necessary to fill gaps in between
                          non-consecutively indexed siblings.  Such indexing arises when document content is sparse.
          parent (ContentNode): The parent for this newly created node; default is None;
          index (Optional[int)): The index property to be set on this node; default is 0;

        Returns:
          ContentNode: This newly created node.

        >>> document.create_node(node_type='page')
            <kodexa.model.model.ContentNode object at 0x7f80605e53c8>
        """
        content_node = ContentNode(document=self, node_type=node_type, content=content,
                                   parent=parent, index=index, virtual=virtual)
        if parent is not None:
            parent.add_child(content_node, index)
        else:
            self.get_persistence().add_content_node(content_node, None)

        if content is not None and len(content_node.get_content_parts()) == 0:
            content_node.set_content_parts([content])

        return content_node

    @classmethod
    def from_kddb(cls, input, detached: bool = False):
        """
        Loads a document from a Kodexa Document Database (KDDB) file

        Args:

            input: if a string we will load the file at that path, if bytes we will create a temp file and
                    load the KDDB to it
            detached (bool): if reading from a file we will create a copy so we don't update in place

        :return: the document
        """
        if isinstance(input, str):
            if isinstance(input, str):
                document = Document(kddb_path=input)
            if detached:
                return Document.from_kddb(document.to_kddb())
            else:
                return document
        else:
            # We will assume the input is of byte type
            import tempfile
            from kodexa import KodexaPlatform
            fp = tempfile.NamedTemporaryFile(suffix='.kddb', delete=False, dir=KodexaPlatform.get_tempdir())
            fp.write(input)
            fp.close()
            return Document(kddb_path=fp.name, delete_on_close=True)

    @classmethod
    def from_file(cls, file, unpack: bool = False):
        """Creates a Document that has a 'file-handle' connector to the specified file.

        Args:
          file: file: The file to which the new Document is connected.
          unpack: bool:  (Default value = False)

        Returns:
          Document: A Document connected to the specified file.

        """
        if unpack:
            Document.from_kdxa(file)
        else:
            file_document = Document()
            file_document.metadata.connector = 'file-handle'
            file_document.metadata.connector_options.file = file
            file_document.source.connector = 'file-handle'
            file_document.source.original_filename = os.path.basename(file)
            file_document.source.original_path = file
            return file_document

    @classmethod
    def from_url(cls, url, headers=None):
        """Creates a Document that has a 'url' connector for the specified url.

        Args:
          str: url: The URL to which the new Document is connected.
          dict: headers: Headers that should be used when reading from the URL
          url:
          headers:  (Default value = None)

        Returns:
          Document: A Document connected to the specified URL with the specified headers (if any).

        """
        if headers is None:
            headers = {}
        url_document = Document()
        url_document.metadata.connector = 'url'
        url_document.metadata.connector_options.base_url = url
        url_document.metadata.connector_options.headers = headers
        url_document.source.connector = 'url'
        url_document.source.original_filename = url
        url_document.source.original_path = url
        url_document.source.headers = headers
        return url_document

    def select_first(self, selector, variables=None) -> Optional[ContentNode]:
        """Select and return the first child of this node that match the selector value.

        Args:
          selector (str): The selector (ie. //*)
          variables (dict, optional): A dictionary of variable name/value to use in substituion; defaults to None.  Dictionary keys should match a variable specified in the selector.

        Returns:
          Optional[ContentNode]: The first matching node or none

        >>> document.get_root().select_first('.')
           ContentNode

        >>> document.get_root().select_first('//*[hasTag($tagName)]', {"tagName": "div"})
           ContentNode
        """
        result = self.select(selector, variables)
        return result[0] if len(result) > 0 else None

    def select(self, selector: str, variables: Optional[dict] = None) -> List[ContentNode]:
        """Execute a selector on the root node and then return a list of the matching nodes.

        Args:
          selector (str): The selector (ie. //*)
          variables (Optional[dict): A dictionary of variable name/value to use in substituion; defaults to an empty dictionary.  Dictionary keys should match a variable specified in the selector.

        Returns:
          list[ContentNodes]: A list of the matching ContentNodes.  If no matches found, list is empty.

        >>> document.select('.')
           [ContentNode]
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

    def get_labels(self) -> List[str]:
        """

        Args:

        Returns:
          List[str]: list of associated labels

        """
        return self.labels


class DocumentStore(Store):
    """
    A document store supports storing, listing and retrieving Kodexa documents and document families
    """

    @abc.abstractmethod
    def get_ref(self) -> str:
        """
        Returns the reference (org-slug/store-slug:version)

        Returns:
            The reference of the document store (i.e. myorg/myslug:1.0.0)

        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_content_object_id(self, document_family: DocumentFamily, content_object_id: str) -> Optional[Document]:
        """Get a Document based on the ID of the ContentObject

        Args:
          document_family(DocumentFamily): The document family
          content_object_id(str): the ID of the ContentObject

        Returns:
          A document (or None if not found)

        """
        raise NotImplementedError

    @abc.abstractmethod
    def replace_content_object(self, document_family: DocumentFamily, content_object_id: str,
                               document: Document) -> Optional[DocumentFamily]:
        """Replace the document in a specific content object in a document family.

        Args:
          document_family (DocumentFamily): The document family
          content_object_id (str): the ID of the ContentObject
          document (Document): the document to replace the content object with

        Returns:
          The document family (or None if it wasn't found)

        """
        raise NotImplementedError

    @abc.abstractmethod
    def put_native(self, path: str, content):
        """
        Push content directly, this will create both a native object in the store and also a
        related Document that refers to it.

        :param path: the path where you want to put the native content
        :param content: the binary content for the native file
        :return: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_family(self, document_family_id: str) -> Optional[DocumentFamily]:
        """
        Returns a document family based on the ID

        Args:
            document_family_id (str): the ID of the document family

        Returns:
            The document family (or None if not found)

        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, path: str):
        """
        Delete the document family stored at the given path

        Args:
          path: the path to the content (ie. mymodel.dat)

        Returns:
          True if deleted, False if there was no file at the path

        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_related_document_to_family(self, document_family_id: str, transition: DocumentTransition,
                                       document: Document):
        """Add a document to a family as a new transition

        Args:
          document_family_id (str): the ID for the document family
          transition (DocumentTransition): the document transition
          document (Document): the document

        Returns:
          None

        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_document_by_content_object(self, document_family: DocumentFamily, content_object: ContentObject) -> \
            Optional[Document]:
        """
        Get a document for a given content object

        Args:
          document_family (DocumentFamily): the document family
          content_object  (ContentObject): the content object

        Returns:
          the Document (or None if not found)

        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_source_by_content_object(self, document_family: DocumentFamily, content_object: ContentObject) -> \
            Any:
        """
        Get the source for a given content object

        Args:
          document_family (DocumentFamily): the document family
          content_object  (ContentObject): the content object

        Returns:
          the source (or None if not found)

        """
        raise NotImplementedError

    def query(self, query: str = "*"):
        """

        Args:
          query (str):  The query (Default value = "*")

        Returns:

        """
        families = self.query_families(query)
        self._draw_table(families)

    @abc.abstractmethod
    def register_listener(self, listener):
        """Register a listener to this store.

        A store listener must have the method

            process_event(content_event:ContentEvent)

        Args:
          listener: the listener to register

        Returns:
          None

        """
        raise NotImplementedError

    def _draw_table(self, objects):
        """Internal method to draw a table

        Args:
          objects: return:

        Returns:

        """
        from rich.table import Table
        from rich import print

        table = Table(title="Listing Objects")

        cols = ['id', 'content_type', 'path']
        for col in cols:
            table.add_column(col)
        for object_dict in objects:
            row = []

            for col in cols:
                row.append(object_dict[col] if col in object_dict else '')
            table.add_row(*row)

        print(table)

    @abc.abstractmethod
    def query_families(self, query: str = "*", page: int = 1, page_size: int = 100) -> List[DocumentFamily]:
        """
        Query the document families

        Args:
          page (int): The page number
          page_size (int): The page size
          query (str): The query (Default is *)

        Returns:
            A list of matching document families

        """
        raise NotImplementedError

    @abc.abstractmethod
    def put(self, path: str, document: Document) -> DocumentFamily:
        """Puts a new document in the store with the given path.

        There mustn't be a family in the path, this method will create a new family based around the
        document

        Args:
          path (str): the path you wish to add the document in the store
          document (Document): the document
        Returns:
            A new document family

        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_family_by_path(self, path: str) -> Optional[DocumentFamily]:
        """
        Returns the document family (or None is not available) for a specific path in the store

        Args:
            path (str): the path within the store

        Returns:
            The document family, or None is no family exists at that path

        """
        raise NotImplementedError

    @abc.abstractmethod
    def count(self) -> int:
        """The number of document families in the store

        Returns:
            the count of families
        """
        raise NotImplementedError

    def accept(self, document: Document):
        """Determine if the store will accept this document.  This would typically mean that the store does
        not yet have a document at the derived family path

        Args:
          document (Document): the document to check

        Returns:
          True if there is no current family at derived path, False is there is one

        """
        return True

    def get_latest_document_in_family(self, document_family: DocumentFamily) -> Optional[Document]:
        """
        Returns the latest instance
        Args:
            document_family (DocumentFamily): The document family which we want the latest document in

        Returns:
            The last document to be stored in the family or None if there isn't one available

        """
        last_co = document_family.content_objects[-1]
        document = self.get_document_by_content_object(document_family, last_co)

        if document is not None:
            document.ref = f"{self.get_ref()}/{document_family.id}/{last_co.id}"

        return document


class ModelStore(Store):
    """A model store supports storing and retrieving of a ML models"""

    def get(self, path: str):
        """Returns the bytes object for the given path (or None is there nothing at that path)

        Args:
          path(str): the path to get content from

        Returns:
          Bytes or None is there is nothing at the path

        """
        pass

    def put(self, path: str, content: Any, replace=False) -> DocumentFamily:
        """

        Args:
          path (str): The path to put the content at
          content: The content to put in the store
          replace: Replace the object if it exists
        Returns:
          The document family that was created

        """
        pass

    def set_content_metadata(self, model_content_metadata: ModelContentMetadata):
        """
        Updates the model content metadata for the model store

        :param model_content_metadata: The metadata object
        """
        pass

    def get_content_metadata(self) -> ModelContentMetadata:
        """
        Gets the latest model content metadata for the model store

        :return: the model content metadata
        """
        pass

    def list_contents(self) -> List[str]:
        """
        Returns a list of the objects that have been uploaded into this model store

        :return: a list of the object names
        """
        pass


class ContentObjectReference:
    """ """

    def __init__(self, content_object: ContentObject, store: DocumentStore, document: Document,
                 document_family):
        self.content_object = content_object
        self.store = store
        self.document = document
        from kodexa.model import DocumentFamily
        self.document_family: DocumentFamily = document_family
