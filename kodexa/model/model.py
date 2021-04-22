"""
The core model provides definitions for all the base objects in the Kodexa Content Model
"""
import abc
import dataclasses
import inspect
import itertools
import json
import os
import re
import uuid
from enum import Enum
from typing import Any, List, Optional

import msgpack
from addict import Dict

from kodexa.mixins import registry


class ContentType(Enum):
    """Types of content object that are supported"""
    DOCUMENT = 'DOCUMENT'
    NATIVE = 'NATIVE'


class ContentObject:
    """A ContentObject is a reference to a type of document, this can be either a native file (say a PDF etc) or it can be
    a Kodexa document.

    The content object allows us to capture metadata about the document or the native file without changing it
    """

    def __init__(self, name="untitled", id=None, content_type=ContentType.DOCUMENT, tags=None, metadata=None,
                 store_ref=None, labels=None, mixins=None):
        if labels is None:
            labels = []
        if metadata is None:
            metadata = {}
        if tags is None:
            tags = []
        if mixins is None:
            mixins = []
        from kodexa.pipeline import new_id
        self.id = new_id() if id is None else id
        """The unique ID for the content object"""
        self.name = name
        """The name/path of the content object"""
        self.content_type = content_type
        """The type of content the object refers to"""
        self.tags = tags
        """A list of the tags related to the object"""
        self.store_ref = store_ref
        """The reference to the store holding this content object"""
        self.metadata = metadata
        """A dictionary of the metadata"""
        self.labels = labels
        """A list of the labels related to the object"""
        self.path = name
        """.. deprecated::"""
        self.mixins = mixins
        """The mixins for this object"""
        self.classes: List[ContentClassification] = []
        """A list of the content classifications associated at the document level"""

    def to_dict(self):
        """Convert the content object to a dictionary

        :return: dictionary

        Args:

        Returns:

        """
        return {
            'id': self.id,
            'tags': self.tags,
            'labels': self.labels,
            'content_type': self.content_type.name,
            'metadata': self.metadata,
            'name': self.name,
            'store_ref': self.store_ref,
            'mixins': self.mixins,
            'classes': [content_class.to_dict() for content_class in self.classes],
        }

    @classmethod
    def from_dict(cls, co_dict):
        """Create a content object from a dictionary

        Args:
          co_dict (dict): The content object as a dictionary

        Returns:
          A content object
        """
        co = ContentObject(co_dict['path'] if 'path' in co_dict else None)
        co.id = co_dict['id']
        co.labels = co_dict['labels']
        co.metadata = co_dict['metadata']
        co.content_type = ContentType[co_dict['content_type']]
        co.mixins = co_dict['mixins']
        if 'classes' in co_dict and co_dict['classes']:
            co.classes = [ContentClassification.from_dict(content_class) for content_class in
                          co_dict['classes']]
        return co


class Store:
    """Base definition of a store in Kodexa (deprecated)"""

    def get_name(self):
        """ """
        pass

    def merge(self, other_store):
        """

        Args:
          other_store:

        Returns:

        """
        pass

    def to_dict(self):
        """ """
        pass

    def set_pipeline_context(self, pipeline_context):
        """

        Args:
          pipeline_context:

        Returns:

        """
        pass

    def count(self):
        """ """
        pass


class RemoteStore:
    """A remote store is one that refers to a Kodexa platform  instance"""

    def get_ref(self) -> str:
        """Get the reference to the store on the platform (i.e. kodexa/my-store:1.1.0)

        :return: The reference

        Args:

        Returns:

        """
        pass

    def delete_contents(self):
        """Delete the contents of the store"""
        from kodexa import KodexaPlatform
        import requests
        resp = requests.delete(
            f"{KodexaPlatform.get_url()}/api/stores/{self.get_ref().replace(':', '/')}/fs",
            headers={"x-access-token": KodexaPlatform.get_access_token()})

        if resp.status_code == 200:
            return resp.content
        else:
            msg = f"Unable to delete families {resp.text}, status : {resp.status_code}"
            raise Exception(msg)


class DocumentMetadata(Dict):
    """A flexible dict based approach to capturing metadata for the document"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Tag(Dict):
    """A tag represents the metadata for a label that is applies as a feature on a content node"""

    def __init__(self, start: Optional[int] = None, end: Optional[int] = None, value: Optional[str] = None,
                 uuid: Optional[str] = None, data: Any = None, *args, confidence: Optional[float] = None,
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
                 content_parts: Optional[List[Any]] = None):
        if content_parts is None:
            content_parts = []
        self.node_type: str = node_type
        """The node type (ie. line, page, cell etc)"""
        self.content: Optional[str] = content
        """The content of the node"""
        self.document: Document = document
        """The document that the node belongs to"""
        self.content_parts: List[Any] = content_parts
        """The children of the content node"""
        self.index: int = 0
        """The index of the content node"""
        self.uuid: str = str(uuid.uuid4())
        """The UUID of the content node"""
        self.virtual: bool = False
        """Is the node virtual (ie. it doesn't actually exist in the document)"""
        # Added for performance
        self._feature_map: Dict[str, ContentFeature] = {}

        self.parent: Optional[ContentNode] = None
        """The parent content node"""
        self.children: List[ContentNode] = []
        """The child content nodes of this content node"""

    def __str__(self):
        return f"ContentNode [node_type:{self.node_type}] ({len(self.get_features())} features, {len(self.children)} children) [" + str(
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
        """Build a new ContentNode from a dictionary representtion.

        Args:
          Document: document: The Kodexa document from which the new ContentNode will be created (not added).
          dict: content_node_dict: The dictionary-structured representation of a ContentNode.  This value will be unpacked into a ContentNode.
          document:
          content_node_dict: Dict:

        Returns:
          ContentNode: A ContentNode containing the unpacked values from the content_node_dict parameter.

        >>> ContentNode.from_dict(document, content_node_dict)
        """

        node_type = content_node_dict['type'] if document.version == Document.PREVIOUS_VERSION else content_node_dict[
            'node_type']

        new_content_node = document.create_node(node_type=node_type, content=content_node_dict[
            'content'] if 'content' in content_node_dict else None)
        if 'uuid' in content_node_dict:
            new_content_node.uuid = content_node_dict['uuid']

        if 'content_parts' in content_node_dict:
            new_content_node.content_parts = content_node_dict['content_parts']

        for dict_feature in content_node_dict['features']:

            feature_type = dict_feature['name'].split(':')[0]
            if feature_type == 'tag':
                new_content_node.add_feature(feature_type,
                                             dict_feature['name'].split(':')[1],
                                             dict_feature['value'], dict_feature['single'], True)
            else:

                # TODO we should convert to Tag?
                new_content_node.add_feature(feature_type,
                                             dict_feature['name'].split(':')[1],
                                             dict_feature['value'], dict_feature['single'], True)

        for dict_child in content_node_dict['children']:
            new_content_node.add_child(ContentNode.from_dict(document, dict_child), dict_child['index'])
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
        new_node = self.document.create_node(node_type=node_type)
        new_node.content = content
        self.add_child(new_node, index)
        return new_node

    def add_child(self, child, index=None):
        """Add a ContentNode as a child of this ContentNode

        Args:
          ContentNode: child: The node that will be added as a child of this node
          index(int, optional, optional): The index at which this child node should be added; defaults to None.  If None, index is set as the count of child node elements.
          child:

        Returns:

        >>> new_page = document.create_node(node_type='page')
            <kodexa.model.model.ContentNode object at 0x7f80605e53c8>
            >>> current_content_node.add_child(new_page)
        """
        if not index:
            child.index = len(self.children)
        else:
            child.index = index
        self.children.append(child)
        child.parent = self

    def get_children(self):
        """Returns a list of the children of this node.

        Args:

        Returns:
          list[ContentNode]: The list of child nodes for this ContentNode.

        >>> node.get_children()
        """
        return self.children

    def set_feature(self, feature_type, name, value):
        """Sets a feature for this ContentNode, replacing the value if a feature by this type and name already exists.

        Args:
          str: feature_type: The type of feature to be added to the node.
          str: name: The name of the feature.
          Any: value: The value of the feature.
          feature_type:
          name:
          value:

        Returns:
          ContentFeature: The feature that was added to this ContentNode

        >>> new_page = document.create_node(node_type='page')
           <kodexa.model.model.ContentNode object at 0x7f80605e53c8>
           >>> new_page.add_feature('pagination','pageNum',1)
        """
        self.remove_feature(feature_type, name)
        return self.add_feature(feature_type, name, value)

    def add_feature(self, feature_type, name, value, single=True, serialized=False):
        """Add a new feature to this ContentNode.

        Note: if a feature for this feature_type/name already exists, the new value will be added to the existing feature; therefore the feature value might become a list.

        Args:
          str: feature_type: The type of feature to be added to the node.
          str: name: The name of the feature.
          Any: value: The value of the feature.
          single(bool, optional, optional): Indicates that the value is singular, rather than a collection (ex: str vs list); defaults to True.
          serialized(bool, optional, optional): Indicates that the value is/is not already serialized; defaults to False.
          feature_type:
          name:
          value:

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

        Args:
          nodes: Optional[List[ContentNode]] a list of content nodes that are children to delete
          exclude_nodes: Optional[List[ContentNode]] a list of content node that are children not to delete
          nodes: Optional[List]:  (Default value = None)
          exclude_nodes: Optional[List]:  (Default value = None)

        Returns:

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
        """Gets the value for the given feature.

        Args:
          str: feature_type: The type of the feature.
          str: name: The name of the feature.
          feature_type:
          name:

        Returns:
          ContentFeature or None: The feature with the specified type & name.  If no feature is found, None is returned.

        >>> new_page.get_feature('pagination','pageNum')
           1
        """
        return self._feature_map[feature_type + ":" + name] if feature_type + ":" + name in self._feature_map else None

    def get_features_of_type(self, feature_type):
        """Get all features of a specific type.

        Args:
          str: feature_type: The type of the feature.
          feature_type:

        Returns:
          list[ContentFeature]: A list of feature with the specified type.  If no features are found, an empty list is returned.

        >>> new_page.get_features_of_type('my_type')
           []
        """
        return [i for i in self.get_features() if i.feature_type == feature_type]

    def has_feature(self, feature_type, name):
        """Determines if a feature with the given feature and name exists on this content node.

        Args:
          str: feature_type: The type of the feature.
          str: name: The name of the feature.
          feature_type:
          name:

        Returns:
          bool: True if the feature is present; else, False.

        >>> new_page.has_feature('pagination','pageNum')
           True
        """
        return feature_type + ":" + name in self._feature_map

    def get_features(self):
        """Get all features on this ContentNode.

        Args:

        Returns:
          list[ContentFeature]: A list of the features on this ContentNode.

        """
        return list(self._feature_map.values())

    def remove_feature(self, feature_type, name):
        """Removes the feature with the given name and type from this node.

        Args:
          str: feature_type: The type of the feature.
          str: name: The name of the feature.
          feature_type:
          name:

        Returns:

        >>> new_page.remove_feature('pagination','pageNum')
        """
        results = self.get_feature(feature_type, name)
        if results:
            del self._feature_map[feature_type + ":" + name]

    def get_feature_value(self, feature_type, name):
        """Get the value for a feature with the given name and type on this ContentNode.

        Args:
          str: feature_type: The type of the feature.
          str: name: The name of the feature.
          feature_type:
          name:

        Returns:
          Any or None: The value of the feature if it exists on this ContentNode otherwise, None.

        >>> new_page.get_feature_value('pagination','pageNum')
           1
        """
        feature = self.get_feature(feature_type, name)

        # Need to make sure we handle the idea of a single value for a feature
        return None if feature is None else feature.value[0] if feature.single else feature.value

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

    def select(self, selector, variables=None):
        """Select and return the child nodes of this node that match the selector value.


        or

        Args:
          str: selector: The selector (ie. //*)
          variables(dict, optional, optional): A dictionary of variable name/value to use in substituion; defaults to None.  Dictionary keys should match a variable specified in the selector.
          selector:

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
        parsed_selector = parse(selector)
        return parsed_selector.resolve(self, variables)

    def select_as_node(self, selector, variables=None):
        """Select and return the child nodes of this content node that match the selector value.
        Matching nodes will be returned as the children of a new proxy content node.

        Note this doesn't impact this content node's children.  They are not adopted by the proxy node,
        therefore their parents remain intact.


        or

        Args:
          str: selector: The selector (ie. //*)
          variables(dict, optional, optional): A dictionary of variable name/value to use in substituion; defaults to None.  Dictionary keys should match a variable specified in the selector.
          selector:

        Returns:
          ContentNode: A new proxy ContentNode with the matching (selected) nodes as its children.  If no matches are found, the list of children will be empty.

        >>> document.content_node.select_as_node('//line')
           ContentNode

        >>> document.get_root().select_as_node('//*[hasTag($tagName)]', {"tagName": "div"})
           ContentNode
        """
        new_node = self.document.create_node(node_type='result')
        new_node.children = self.select(selector, variables)
        return new_node

    def get_all_content(self, separator=" "):
        """Get this node's content, concatenated with all of its children's content.

        Args:
          separator(str, optional, optional): The separator to use in joining content together; defaults to " ".

        Returns:
          str: The complete content for this node concatenated with the content of all child nodes.

        >>> document.content_node.get_all_content()
            "This string is made up of multiple nodes"
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
        """This will move the target_child, which must be a child of the node, to a new parent.

        It will be added to the end of the parent

        Args:
          ContentNode: target_child: The child node that will be moved to a new parent node (target_parent).
          ContentNode: target_parent: The parent node that the target_child will be added to.  The target_child will be added at the end of the children collection.
          target_child:
          target_parent:

        Returns:

        >>> # Get first node of type 'line' from the first page
            >>> target_child = document.get_root().select('//page')[0].select('//line')[0]
            >>> # Get sixth node of type 'page'
            >>> target_parent = document.get_root().select('//page')[5]
            >>> # Move target_child (line) to the target_parent (sixth page)
            >>> document.get_root().move_child_to_parent(target_child, target_parent)
        """
        self.children.remove(target_child)
        target_parent.add_child(target_child)

    def adopt_children(self, children, replace=False):
        """This will take a list of content nodes and adopt them under this node, ensuring they are re-parented.

        Args:
          list: ContentNode] children: A list of ContentNodes that will be added to the end of this node's children collection
          bool: replace: If True, will remove all current children and replace them with the new list; defaults to True
          children:
          replace:  (Default value = False)

        Returns:

        >>> # select all nodes of type 'line', then the root node 'adopts' them
            >>> # and replaces all it's existing children with these 'line' nodes.
            >>> document.get_root().adopt_children(document.select('//line'), replace=True)
        """

        if replace:
            for child in self.children:
                child.parent = None
            self.children = []

        for child in children:
            self.add_child(child)

    def remove_tag(self, tag_name):
        """Remove a tag from this content node.

        Args:
          str: tag_name: The name of the tag that should be removed.
          tag_name:

        Returns:

        >>> document.get_root().remove_tag('foo')
        """
        self.remove_feature('tag', tag_name)

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
            existing_tag_values = node.get_feature_value('tag', existing_tag_name)
            if existing_tag_values:
                if type(existing_tag_values) == list:

                    # It's possible to have multiple features with the same tag name that also share the same uuid.
                    # If we DO have features with the same UUID, we need to make sure that their copies also share the same UUID.
                    sorted_tag_values = sorted(existing_tag_values, key=lambda k: k['uuid'])
                    previous_uuid = None
                    new_uuid = None
                    for val in sorted_tag_values:
                        if previous_uuid is None or previous_uuid != val['uuid']:
                            new_uuid = str(uuid.uuid4())

                        previous_uuid = val['uuid']
                        tag = Tag(start=val['start'], end=val['end'], value=val['value'], uuid=new_uuid,
                                  data=val['data'])
                        node.add_feature('tag', new_tag_name, tag)
                else:
                    tag = Tag(start=existing_tag_values['start'], end=existing_tag_values['end'],
                              value=existing_tag_values['value'], uuid=str(uuid.uuid4()),
                              data=existing_tag_values['data'])
                    node.add_feature('tag', new_tag_name, tag)

    def collect_nodes_to(self, end_node):
        """Get the the sibling nodes between the current node and the end_node.

        Args:
          ContentNode: end_node: The node to end at
          end_node:

        Returns:
          list[ContentNode]: A list of sibling nodes between this node and the end_node.

        >>> document.content_node.children[0].collect_nodes_to(end_node=document.content_node.children[5])
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
          ContentNode: end_node: The node to end with
          str: tag_to_apply: The tag name that will be applied to each node
          str: tag_uuid: The tag uuid used if you want to group them
          end_node:
          tag_to_apply:
          tag_uuid: str:  (Default value = None)

        Returns:

        >>> document.content_node.children[0].tag_nodes_to(document.content_node.children[5], tag_name='foo')
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

        Args:

        Returns:
          :return:

        """
        from anytree import RenderTree
        result = ""
        for pre, _, node in RenderTree(self):
            result = result + ("%s%s" % (pre, f"{node.content} ({node.node_type}) {node.get_tags()}\n"))
        return result

    def tag(self, tag_to_apply, selector=".", content_re=None,
            use_all_content=False, node_only=None,
            fixed_position=None, data=None, separator=" ", tag_uuid: str = None):
        """This will tag (see Feature Tagging) the expression groups identified by the regular expression.


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

        Returns:

        >>> document.content_node.tag('is_cheese')
        """

        if use_all_content and node_only is None:
            node_only = True
        elif node_only is None:
            node_only = False

        def get_tag_uuid(tag_uuid):
            """

            Args:
              tag_uuid:

            Returns:

            """
            if tag_uuid:
                return tag_uuid
            else:
                return str(uuid.uuid4())

        def tag_node_position(node_to_check, start, end, node_data, tag_uuid):
            """

            Args:
              node_to_check:
              start:
              end:
              node_data:
              tag_uuid:

            Returns:

            """

            content_length = 0

            # Make sure we have content on the node
            if node_to_check.content:
                if len(node_to_check.content) > 0:
                    if start < len(node_to_check.content) and end < len(node_to_check.content):
                        node_to_check.add_feature('tag', tag_to_apply,
                                                  Tag(start, end,
                                                      node_to_check.content[start:end],
                                                      data=node_data, uuid=tag_uuid))
                        return -1
                    elif start < len(node_to_check.content) <= end:
                        node_to_check.add_feature('tag', tag_to_apply,
                                                  Tag(start,
                                                      len(node_to_check.content),
                                                      value=node_to_check.content[start:],
                                                      data=node_data, uuid=tag_uuid))

                end = end - len(node_to_check.content) + len(separator)
                content_length = len(node_to_check.content) + len(separator)
                start = 0 if start - len(node_to_check.content) - len(separator) < 0 else start - len(
                    node_to_check.content) - len(separator)

            for child_node in node_to_check.children:
                result = tag_node_position(child_node, start, end, node_data, tag_uuid)
                content_length = content_length + result
                if result < 0 or (end - result) < 0:
                    return -1
                else:
                    end = end - result
                    start = 0 if start - result < 0 else start - result

            return content_length

        if content_re:
            pattern = re.compile(content_re)

        for node in self.select(selector):
            if fixed_position:
                tag_node_position(node, fixed_position[0], fixed_position[1], data, get_tag_uuid(tag_uuid))

            else:
                if not content_re:
                    node.add_feature('tag', tag_to_apply, Tag(data=data, uuid=get_tag_uuid(tag_uuid)))
                else:
                    if not use_all_content:
                        if node.content:
                            content = node.content
                        else:
                            content = None
                    else:
                        content = node.get_all_content(separator=separator)

                    if content is not None:
                        matches = pattern.finditer(content)

                        if node_only:
                            # If we are only tagging the node we
                            # simply need to know if there are any matches
                            if any(True for _ in matches):
                                node.add_feature('tag', tag_to_apply, Tag(data=data, uuid=get_tag_uuid(tag_uuid)))
                        else:
                            for match in matches:
                                start_offset = match.span()[0]
                                end_offset = match.span()[1]
                                tag_node_position(node, start_offset, end_offset, data, get_tag_uuid(tag_uuid))

    def get_tags(self):
        """Returns a list of the names of the tags on the given node


        :return: A list of the tag name

        Args:

        Returns:

        >>> document.content_node.select('*').get_tags()
            ['is_cheese']
        """
        return [i.name for i in self.get_features_of_type("tag")]

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
            values.append(tag.value)

        if include_children:
            for child in self.get_children():
                values.extend(child.get_tag_values(tag_name, include_children))

        return values

    def get_related_tag_values(self, tag_name: str, include_children: bool = False, value_separator: str = ' '):
        """Get the values for a specific tag name, grouped by uuid

        Args:
          tag_name: tag name
          include_children: include the children of this node
          value_separator: the string to be used to join related tag values
          tag_name: str:
          include_children: bool:  (Default value = False)
          value_separator: str:  (Default value = ' ')

        Returns:
          a list of the tag values

        """

        def group_tag_values(group_dict, feature_val):
            """

            Args:
              group_dict:
              feature_val:

            Returns:

            """
            # we know the names of all these tags are the same, but we want to group them if they share the same uuid
            if feature_val['uuid'] in value_groups.keys():
                # we've seen this UUID - add it's value to the group
                group_dict[feature_val['uuid']].append(feature_val['value'])
            else:
                # first occurrence
                group_dict[feature_val['uuid']] = [feature_val['value']]

        if include_children:
            tagged_nodes = self.select('//*[hasTag("' + tag_name + '")]')
        else:
            tagged_nodes = self.select('.')

        value_groups: Dict[str, Any] = {}
        for tag_node in tagged_nodes:
            tag_feature_vals = tag_node.get_feature_value('tag', tag_name)
            if tag_feature_vals:
                if not isinstance(tag_feature_vals, list):
                    tag_feature_vals = [tag_feature_vals]

                for v in tag_feature_vals:
                    group_tag_values(value_groups, v)

        value_strings = []
        for k in value_groups.keys():
            value_strings.append(value_separator.join(value_groups[k]))

        return value_strings

    def get_tag(self, tag_name):
        """Returns the value of a tag, this can be either a single list [start,end,value] or if multiple parts of the
        content of this node match you can end up with a list of lists i.e. [[start1,end1,value1],[start2,end2,value2]]

        Args:
          tag_name: The name of the tag

        Returns:
          A list tagged location and values for this label in this node

        >>> document.content_node.find(content_re='.*Cheese.*').get_tag('is_cheese')
            [0,10,'The Cheese Moved']
        """
        tag_details = self.get_feature_value('tag', tag_name)

        if tag_details is None:
            return []

        if isinstance(tag_details, list):
            return tag_details
        else:
            return [tag_details]

    def get_all_tags(self):
        """Get the names of all tags that have been applied to this node or to its children.

        Args:

        Returns:
          list[str]: A list of the tag names belonging to this node and/or its children.

        >>> document.content_node.find(content_re='.*Cheese.*').get_all_tags()
            ['is_cheese']
        """
        tags = []
        tags.extend(self.get_tags())
        for child in self.children:
            tags.extend(child.get_all_tags())
        return list(set(tags))

    def has_tags(self):
        """Determines if this node has any tags at all.

        Args:

        Returns:
          bool: True if node has any tags; else, False;

        >>> document.content_node.find(content_re='.*Cheese.*').has_tags()
            True
        """
        return len([i.value for i in self.get_features_of_type("tag")]) > 0

    def has_tag(self, tag):
        """Determine if this node has a tag with the specified name.

        Args:
          str: tag: The name of the tag.
          tag:

        Returns:
          bool: True if node has a tag by the specified name; else, False;

        >>> document.content_node.find(content_re='.*Cheese.*').has_tag('is_cheese')
            True
            >>> document.content_node.find(content_re='.*Cheese.*').has_tag('is_fish')
            False
        """
        for feature in self.get_features():
            if feature.feature_type == 'tag' and feature.name == tag:
                return True
        return False

    def find(self, content_re=".*", node_type_re=".*", direction=FindDirection.CHILDREN, tag_name=None, instance=1,
             tag_name_re=None, use_all_content=False):
        """Return a node related to this node (parent or child) that matches the content and/or node type specified by regular expressions.

        Args:
          content_re(str, optional, optional): The regular expression to match against the node's content; default is '.*'.
          node_type_re(str, optional, optional): The regular expression to match against the node's type; default is '.*'.
          direction(FindDirection(enum), optional, optional): The direction to search (CHILDREN or PARENT); default is FindDirection.CHILDREN.
          tag_name(str, optional, optional): The tag name that must exist on the node; default is None.
          instance(int, optional, optional): The instance of the matching node to return (may have multiple matches).  Value must be greater than zero; default is 1.
          tag_name_re(str, optional, optional): The regular expression that will match the tag_name that must exist on the node;  default is None.
          use_all_content(bool, optional, optional): Match content_re against the content of this node concatenated with the content of its child nodes; default is False.

        Returns:
          ContentNode or None.: Matching node (if found), or None.

        >>> document.get_root().find(content_re='.*Cheese.*',instance=2)
            <kodexa.model.model.ContentNode object at 0x7f80605e53c8>
        """
        results = self.findall(content_re, node_type_re, direction, tag_name, tag_name_re, use_all_content)
        if instance < 1 or len(results) < instance:
            return None
        else:
            return results[instance - 1]

    def find_with_feature_value(self, feature_type, feature_name, value, direction=FindDirection.CHILDREN, instance=1):
        """Return a node related to this node (parent or child) that has a specific feature type, feature name, and feature value.

        Args:
          str: feature_type: The feature type.
          str: feature_name: The feature name.
          Any: value: The feature value.
          direction(FindDirection(enum), optional, optional): The direction to search (CHILDREN or PARENT); default is FindDirection.CHILDREN.
          instance(int, optional, optional): The instance of the matching node to return (may have multiple matches).  Value must be greater than zero; default is 1.
          feature_type:
          feature_name:
          value:

        Returns:
          ContentNode or None: Matching node (if found), or None.

        >>> document.content_node.find_with_feature_value(feature_type='tag',feature_name='is_cheese',value=[1,10,'The Cheese has moved'])
            <kodexa.model.model.ContentNode object at 0x7f80605e53c8>
        """

        if instance < 1:
            return None
        else:
            return next(
                itertools.islice(self.findall_with_feature_value(feature_type, feature_name, value, direction),
                                 instance - 1, 1), None)

    def findall_with_feature_value(self, feature_type, feature_name, value, direction=FindDirection.CHILDREN):
        """Get all nodes related to this node (parents or children) that have a specific feature type, feature name, and feature value.

        Args:
          str: feature_type: The feature type.
          str: feature_name: The feature name.
          Any: value: The feature value.
          direction(FindDirection(enum), optional, optional): The direction to search (CHILDREN or PARENT); default is FindDirection.CHILDREN.
          feature_type:
          feature_name:
          value:

        Returns:
          list[ContentNode]: list of the matching content nodes

        >>> document.content_node.findall_with_feature_value(feature_type='tag',feature='is_cheese', value=[1,10,'The Cheese has moved'])
            [<kodexa.model.model.ContentNode object at 0x7f80605e53c8>]
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

        Args:

        Returns:
          bool: True if this node is the last child of its parent or if this node has no parent; else, False;

        """

        if not self.parent:
            return True
        else:
            return self.index == self.parent.get_last_child_index()

    def get_last_child_index(self):
        """Returns the max index value for the children of this node. If the node has no children, returns None.

        Args:

        Returns:
          int or None: The max index of the children of this node, or None if there are no children.

        """

        if not self.children:
            return None

        max_index = 0
        for child in self.children:
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
          int: index: The index (zero-based) for the child node.
          index:

        Returns:
          ContentNode or None: Node at index, or None if the index is outside the boundaries of child nodes.

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
            node = self.parent.get_node_at_index(search_index)

            if not node:
                return node

            if compiled_node_type_re.match(node.node_type) and (not skip_virtual or not node.virtual):
                if (not has_no_content and node.content) or (has_no_content):
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
        """Search for related nodes (child or parent) that match the content and/or type specified by regular expressions.

        Args:
          content_re(str, optional, optional): The regular expression to match against the node's content; default is '.*'.
          node_type_re(str, optional, optional): The regular expression to match against the node's type; default is '.*'.
          direction(FindDirection(enum), optional, optional): The direction to search (CHILDREN or PARENT); default is FindDirection.CHILDREN.
          tag_name(str, optional, optional): The tag name that must exist on the node; default is None.
          tag_name_re(str, optional, optional): The regular expression that will match the tag_name that must exist on the node;  default is None.
          use_all_content(bool, optional, optional): Match content_re against the content of this node concatenated with the content of its child nodes; default is False.

        Returns:
          list[ContentNode]: List of matching content nodes

        >>> document.content_node.findall(content_re='.*Cheese.*')
            [<kodexa.model.model.ContentNode object at 0x7f80605e53c8>,
            <kodexa.model.model.ContentNode object at 0x7f80605e53c8>]
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
        """Search for a node that matches on the value and or type using
        regular expressions using compiled expressions

        Args:
          value_re_compiled:
          node_type_re_compiled:
          direction:
          tag_name:
          tag_name_compiled:
          use_all_content:

        Returns:

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
    """A feature allows you to capture almost any additional data or metadata and associate it with a ContentNode"""

    def __init__(self, feature_type, name, value, description=None, single=True):
        self.feature_type = feature_type
        """The type of feature, a logical name to group feature types together (ie. spatial)"""
        self.name = name
        """The name of the feature (ie. bbox)"""
        self.value = value
        """A value of the feature, this can be any JSON serializable data object"""
        self.description = description
        """Description of the feature (Optional)"""
        self.single = single
        """Determines whether the data for this feature is a single instance or an array, if you have added the same feature to the same node you will end up with multiple data elements in the content feature and the single flag will be false"""

    def __str__(self):
        return f"Feature [type='{self.feature_type}' name='{self.name}' value='{self.value}' single='{self.single}']"

    def to_dict(self):
        """Create a dictionary representing this ContentFeature's structure and content.

        Args:

        Returns:
          dict: The properties of this ContentFeature structured as a dictionary.

        >>> node.to_dict()
        """
        return {'name': self.feature_type + ':' + self.name, 'value': self.value, 'single': self.single}


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
    CURRENT_VERSION: str = "2.0.0"

    def __str__(self):
        return f"kodexa://{self.uuid}"

    def __init__(self, metadata=None, content_node: ContentNode = None, source=None, ref: str = None):
        if metadata is None:
            metadata = DocumentMetadata()
        if source is None:
            source = SourceMetadata()

        # The ref is not stored and is used when we have
        # initialized a document from a remote store and want
        # to keep track of that
        self.ref = ref

        self.metadata: DocumentMetadata = metadata
        """Metadata relating to the document"""
        self.content_node: Optional[ContentNode] = content_node
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

        # Make sure we apply all the mixins
        registry.apply_to_document(self)

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
        new_document.content_node = new_document.create_node(node_type='text')
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
                    index: int = 0):
        """
        Creates a new node for the document.  The new node is not added to the document, but any mixins that have been
        applied to the document will also be available on the new node.

        Args:
          str: node_type: The type of node.
          str: content: The content for the node; defaults to None.
          bool: virtual: Indicates if this is a 'real' or 'virtual' node; default is False.  'Real' nodes contain document content.
        'Virtual' nodes are synthesized as necessary to fill gaps in between non-consecutively indexed siblings.  Such indexing arises when document content is sparse.
          ContentNode: parent: The parent for this newly created node; default is None;
          int: index: The index property to be set on this node; default is 0;
          node_type: str:
          content: Optional[str]:  (Default value = None)
          virtual: bool:  (Default value = False)
          parent: ContentNode:  (Default value = None)
          index: int:  (Default value = 0)

        Returns:
          ContentNode: This newly created node.

        >>> document.create_node(node_type='page')
            <kodexa.model.model.ContentNode object at 0x7f80605e53c8>
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
        url_document.metadata.connector_options.url = url
        url_document.metadata.connector_options.headers = headers
        url_document.source.connector = 'url'
        url_document.source.original_filename = url
        url_document.source.original_path = url
        url_document.source.headers = headers
        return url_document

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

    def select_as_node(self, selector, variables=None) -> ContentNode:
        """Execute a selector on the root node and then return new ContentNode with the results set as its children.

        Args:
          selector (str): The selector (ie. //*)
          variables (Optional[dict]): A dictionary of variable name/value to use in substituion; defaults to an empty dictionary.  Dictionary keys should match a variable specified in the selector.

        Returns:
          ContentNode: A new ContentNode.  All ContentNodes on this Document that match the selector value are added as the children for the returned ContentNode.

        >>> document.select('//line')
           ContentNode
        """
        if variables is None:
            variables = {}
        if self.content_node:
            return self.content_node.select_as_node(selector, variables)
        else:
            return self.create_node(node_type='results')

    def get_labels(self) -> List[str]:
        """

        Args:

        Returns:
          List[str]: list of associated labels

        """
        return self.labels


class TransitionType(Enum):
    """
    The type of transition
    """
    DERIVED = 'DERIVED'
    """A transition that derived a new document"""
    FRAGMENT = 'FRAGMENT'
    """A transition that placed a fragment of the document in another document"""


class BaseEvent:
    """
    The base for all events within Kodexa
    """
    pass


class ContentEventType(Enum):
    """
    The type of event that occurred on the content
    """
    NEW_OBJECT = 'NEW_OBJECT'
    DERIVED_DOCUMENT = 'DERIVED_DOCUMENT'


class ScheduledEvent(BaseEvent):
    """A scheduled event is sent to an assistant when a scheduled has been met"""

    type = "scheduled"

    @classmethod
    def from_dict(cls, event_dict: dict):
        return ScheduledEvent()

    def to_dict(self):
        return {
            'contentObject': self.content_object.to_dict(),
            'documentFamily': self.document_family.to_dict(),
            'eventType': self.event_type,
            'type': self.type
        }


class ContentEvent(BaseEvent):
    """A content event represents a change, update or deletion that has occurred in a document family
    in a store, and can be relayed for a reaction
    """

    type = "content"

    def __init__(self, content_object: ContentObject, event_type: ContentEventType, document_family):
        """
        Initialize a content event
        Args:
            content_object: the content object on which the event occurred
            event_type: the type of event
            document_family: the document family to which the object belongs
        """
        self.content_object = content_object
        """The content object that raised the event"""
        self.event_type = event_type
        """The event type"""
        self.document_family: DocumentFamily = document_family
        """The document family containing the content object"""

    @classmethod
    def from_dict(cls, event_dict: dict):
        return ContentEvent(ContentObject.from_dict(event_dict['contentObject']),
                            ContentEventType[event_dict['eventType']],
                            DocumentFamily.from_dict(event_dict['documentFamily']))

    def to_dict(self):
        return {
            'contentObject': self.content_object.to_dict(),
            'documentFamily': self.document_family.to_dict(),
            'eventType': self.event_type,
            'type': self.type
        }


class AssistantEvent(BaseEvent):
    type = "assistant"

    """
    A assistant event represents an interaction, usually from a user or an API, to evalute
    and respond to a document
    """

    def __init__(self, content_object: ContentObject, event_type: str):
        """
        Initialize a content event
        Args:
            content_object: the content object on which the event occurred
            event_type: the type of event
        """
        self.content_object = content_object
        """The assistant event"""
        self.event_type = event_type
        """The event type"""

    @classmethod
    def from_dict(cls, event_dict: dict):
        return AssistantEvent(ContentObject.from_dict(event_dict['contentObject']),
                              event_dict['eventType'])

    def to_dict(self):
        return {
            'contentObject': self.content_object.to_dict(),
            'eventType': self.event_type,
            'type': self.type
        }


class DocumentActor:
    """A document actor is something that can create a new document in a family and is
    part of the document transition
    """

    def __init__(self, actor_id: str, actor_type: str):
        """
        Initialize a document actor

        Args:
            actor_id: the ID of the actor (this typically has meaning within the scope of the actor type)
            actor_type: the type of actor
        """
        self.actor_id = actor_id
        """The ID of the actor (based on the type)"""
        self.actor_type = actor_type
        """The type of actor"""


class DocumentTransition:
    """
    A document transition represents a link between two documents and tries to capture the actor that was involved
    in the transition as well at the type of transition that exists
    """

    def __init__(self, transition_type: TransitionType, source_content_object_id: str,
                 destination_content_object_id: Optional[str] = None,
                 actor: Optional[DocumentActor] = None, execution_id: Optional[str] = None):
        """
        Create a document transition

        Args:
            transition_type:TransitionType: the type of transition
            source_content_object_id:str: the ID of the source content object
            destination_content_object_id:Optional[str] the ID of the destination content object
            actor (Optional[DocumentActor]): the actor (Defaults to None)
            execution_id (Optional[str]): the ID of the execution that created this transition
        """
        self.transition_type = transition_type
        """The type of transition"""
        self.source_content_object_id = source_content_object_id
        """The ID of the source content object"""
        self.destination_content_object_id = destination_content_object_id
        """The ID of the destination content object"""
        self.actor = actor
        """The actor in the transition"""
        self.execution_id = execution_id
        """The ID of the execution that created this transition"""

    @classmethod
    def from_dict(cls, transition_dict: dict):
        """
        Converts a dictionary from a REST call back into a DocumentTransition
        Args:
            transition_dict: Dictionary

        Returns: A document transition

        """
        transition = DocumentTransition(transition_dict['transitionType'], transition_dict['sourceContentObjectId'],
                                        transition_dict['destinationContentObjectId'],
                                        execution_id=transition_dict.get('executionId'))
        return transition

    def to_dict(self) -> dict:
        """
        Convert the transition to a dictionary to match REST API

        Returns:
            dictionary of transition
        """
        return {
            'transitionType': self.transition_type,
            'sourceContentObjectId': self.source_content_object_id,
            'destinationContentObjectId': self.destination_content_object_id,
            'executionId': self.execution_id
        }


class DocumentFamily:
    """A document family represents a collection of related documents which together represent different views of the same
    source material

    This approach allows parsed representations to he linked to native, derived representations, labelled etc all to be
    part of a family of content views that can be used together to understand the document and its content

    """

    def __init__(self, path: str, store_ref: str):
        """
        Creates a new document family at the given path and optionally with the
        document as its first entry

        Args:
            path (str): the path at which this document family exists (i.e. my-file.pdf)
            store_ref (str): the reference to the store holding this family
        """
        self.id: str = str(uuid.uuid4())
        """The ID of this document family"""
        self.transitions: List[DocumentTransition] = []
        """A list of the transitions within the document family"""
        self.content_objects: List[ContentObject] = []
        """A list of the content objects in the document family"""
        self.path = path
        """The path for this document family in the store (akin to a filename)"""
        self.store_ref = store_ref
        """The reference to the store containing the document family"""
        self.classes: List[ContentClassification] = []
        """The content classifications from the latest content object"""
        self.mixins: List[str] = []
        """The mixins from the latest content object"""
        self.labels: List[str] = []
        """The labels from the latest content object"""

    def add_document(self, document: Document, transition: Optional[DocumentTransition] = None) -> ContentEvent:
        """

        Args:
          document: Document:
          transition: DocumentTransition:  (Default value = None)

        Returns:
          A new content event
        """
        new_content_object = ContentObject()
        new_content_object.store_ref = self.store_ref
        new_content_object.content_type = ContentType.DOCUMENT
        new_content_object.metadata = document.metadata
        new_content_object.labels = document.labels
        new_content_object.mixins = document.get_mixins()

        self.content_objects.append(new_content_object)

        if transition is not None:
            transition.destination_content_object_id = new_content_object.id
            self.transitions.append(transition)

        new_event = ContentEvent(new_content_object, ContentEventType.NEW_OBJECT, self)
        return new_event

    def get_latest_content(self) -> ContentObject:
        """Returns the latest content object that we have in place

        Returns:
            The latest content object in the family
        """
        return self.content_objects[-1]

    def get_content_objects(self) -> List[ContentObject]:
        """Returns all the content objects in the family

        Returns:
            a list of the content objects


        """
        return self.content_objects

    def get_document_count(self) -> int:
        """
        Count of content objects in the family

        Returns:
          number of documents in the family

        """
        return len(self.content_objects)

    @classmethod
    def from_dict(cls, family_dict: dict):
        """
        Convert a dictionary from a REST call into the Document Family

        Args:
            param: the document family object as a dictionary

        Returns:
            An instance of the document family
        """
        document_family = DocumentFamily(family_dict['path'], family_dict['storeRef'])
        document_family.id = family_dict['id']
        document_family.content_objects = []

        if 'classes' in family_dict:
            for co_class in family_dict['classes']:
                document_family.classes.append(ContentClassification.from_dict(co_class))

        if 'labels' in family_dict:
            document_family.labels = family_dict['labels']
        else:
            document_family.labels = []

        if 'mixins' in family_dict:
            document_family.mixins = family_dict['mixins']
        else:
            document_family.mixins = []

        for co_dict in family_dict['contentObjects']:
            document_family.content_objects.append(ContentObject.from_dict(co_dict))
        for transition_dict in family_dict['transitions']:
            document_family.transitions.append(DocumentTransition.from_dict(transition_dict))
        return document_family

    def to_dict(self) -> dict:
        """
        Convert the document family to a dictionary to match REST API

        Returns:
            dictionary of document family
        """
        return {
            'id': self.id,
            'storeRef': self.store_ref,
            'path': self.path,
            'contentObjects': [co.to_dict() for co in self.content_objects],
            'transitions': [transition.to_dict() for transition in self.transitions]}


class DocumentStore:

    def __init__(self, store_type='DOCUMENT', store_purpose='OPERATIONAL'):
        self.store_type = store_type
        self.store_purpose = store_purpose

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
          document_family(DocumentFamily): The document family
          content_object_id(str): the ID of the ContentObject
          document(Document): the document to replace the content object with

        Returns:
          The document family (or None if it wasn't found)

        """
        raise NotImplementedError

    @abc.abstractmethod
    def put_native(self, path: str, content, force_replace=False):
        """
        Push content directly, this will create both a native object in the store and also a
        related Document that refers to it.

        :param path: the path where you want to put the native content
        :param content: the binary content for the native file
        :param force_replace: replace the content at this path completely
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
    def put(self, path: str, document: Document, force_replace: bool = False) -> DocumentFamily:
        """Puts a new document in the store with the given path.

        There mustn't be a family in the path, this method will create a new family based around the
        document

        Args:
          path (str): the path you wish to add the document in the store
          document (Document): the document
          force_replace (bool): Should we delete and replace the content at the path (Default False)

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


class ModelStore:
    """A model store supports storing and retrieving of a ML models"""

    def get(self, path: str):
        """Returns the bytes object for the given path (or None is there nothing at that path)

        Args:
          path(str): the path to get content from

        Returns:
          Bytes or None is there is nothing at the path

        """
        pass

    def put(self, path: str, content: Any, force_replace: bool = False):
        """

        Args:
          path (str): The path to put the content at
          content: The content to put in the store
          force_replace (bool): Replace the file stored at the path (Default false)
        Returns:

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
