import json
import re
import uuid

import msgpack
from addict import Dict

from kodexa.mixins import registry


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


class ContentNode(object):
    """
    A Content Node identifies a section of the document containing logical
    grouping of information

    The node will have content and can include n number of features.

    You should always create a node using the Document create_node method to
    ensure that the correct mixins are applied.

        >>> new_page = document.create_node(type='page')
        <kodexa.model.model.ContentNode object at 0x7f80605e53c8>
        >>> current_content_node.add_child(new_page)

    or

        >>> new_page = document.create_node(type='page', content='This is page 1')
        <kodexa.model.model.ContentNode object at 0x7f80605e53c8>
        >>> current_content_node.add_child(new_page)
    """

    def __init__(self, document, type, content="", content_parts=[]):
        self.type = type
        self.content = content
        self.document = document
        self.content_parts = content_parts
        self.parent = None
        self.children = []
        self.index = 0
        self.uuid = str(uuid.uuid4())

        # Added for performance
        self._feature_map = {}

    def __str__(self):
        return f"ContentNode [type:{self.type}] ({len(self.get_features())} features, {len(self.children)} children) [" + str(
            self.content) + "]"

    def _repr_html_(self):
        return self.to_html()

    def to_html(self):
        return DocumentRender(self.document).render_node(self)

    def to_json(self):
        """
        Convert this node structure into a JSON object


            >>> node.to_json()
        """
        return json.dumps(self.to_dict())

    def to_dict(self):
        """
        Convert the ContentNode, and all its children into a simple dictionary

            >>> new_page = document.create_node(type='page')
            <kodexa.model.model.ContentNode object at 0x7f80605e53c8>
            >>> current_content_node.to_dict()
        """
        new_dict = {'type': self.type, 'content': self.content, 'content_parts': self.content_parts, 'features': [],
                    'index': self.index, 'children': [], 'uuid': self.uuid}
        for feature in self.get_features():
            new_dict['features'].append(feature.to_dict())

        for child in self.children:
            new_dict['children'].append(child.to_dict())
        return new_dict

    @staticmethod
    def from_dict(document, content_node_dict):
        new_content_node = document.create_node(type=content_node_dict['type'], content=content_node_dict[
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

    def add_child(self, child, index=None):
        """
        Add a ContentNode as a child of this ContentNode

            >>> new_page = document.create_node(type='page')
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
        """
        Returns a list of the children of this node

           >>> new_page = document.create_node(type='page')
           <kodexa.model.model.ContentNode object at 0x7f80605e53c8>
           >>> new_page.get_children()
           []
        """
        return self.children

    def set_feature(self, feature_type, name, value):
        """
        Sets a feature to this ContentNode, replacing the value

        You will need to provide the feature type, the name of the feature
        and then the value.

        Note this will replace any matching feature (i.e. with the same type and name)

           >>> new_page = document.create_node(type='page')
           <kodexa.model.model.ContentNode object at 0x7f80605e53c8>
           >>> new_page.add_feature('pagination','pageNum',1)
        """
        self.remove_feature(feature_type, name)
        return self.add_feature(feature_type, name, value)

    def add_feature(self, feature_type, name, value, single=True, serialized=False):
        """
        Add a new feature to this ContentNode.

        You will need to provide the feature type, the name of the feature
        and then the value.

        Note this will add a value to an existing feature, therefore
        the feature value might switch to being a list

           >>> new_page = document.create_node(type='page')
           <kodexa.model.model.ContentNode object at 0x7f80605e53c8>
           >>> new_page.add_feature('pagination','pageNum',1)
        """
        if self.has_feature(feature_type, name):
            feature = self.get_feature(feature_type, name)
            if feature.single:
                feature.single = False
            feature.value.append(value)
            return feature
        else:
            # Make sure that we treat the value as list all the time
            new_feature = ContentFeature(feature_type, name,
                                         [value] if single and not serialized else value, single)
            self._feature_map[new_feature.feature_type + ":" + new_feature.name] = new_feature
            return new_feature

    def get_feature(self, feature_type, name):
        """
        Gets the value for the given feature.

        You will need to provide the type and name of the feature. If no
        feature is find you will get None

           >>> new_page.get_feature('pagination','pageNum')
           1

        """
        return self._feature_map[feature_type + ":" + name] if feature_type + ":" + name in self._feature_map else None

    def get_features_of_type(self, feature_type):
        """
        Return a list of all the features of a specific type

           >>> new_page.get_features_of_type('tag')
           []

        :returns: list of the tags

        """
        return [i for i in self.get_features() if i.feature_type == feature_type]

    def has_feature(self, feature_type, name):
        """
        Determines if the feature with the given name and type exists on this content node

        You will need to provide the type and name of the feature. If the feature is present
        it will return True, else it will return False

           >>> new_page.has_feature('pagination','pageNum')
           True

        :returns: True if the feature is present

        """
        return feature_type + ":" + name in self._feature_map

    def get_features(self):
        """
        Returns a list of the features on this content node

        :returns: a list of the features present
        """
        return list(self._feature_map.values())

    def remove_feature(self, feature_type, name):
        """
        Determines if the feature with the given name and type exists on this content node

        You will need to provide the type and name of the feature. If the feature is present
        it will return True, else it will return False

           >>> new_page.remove_feature('pagination','pageNum')


        """
        results = self.get_feature(feature_type, name)
        if results:
            del self._feature_map[feature_type + ":" + name]

    def get_feature_value(self, feature_type, name):
        """
        Returns the assigned value for a given feature

        You will need to provide the type and name of the feature. If the feature is present
        it will return the value otherwise it will return None.

           >>> new_page.get_feature_value('pagination','pageNum')
           1

        """
        feature = self.get_feature(feature_type, name)

        # Need to make sure we handle the idea of a single value for a feature
        return None if feature is None else feature.value[0] if feature.single else feature.value

    def get_content(self):
        """
        Returns the content of the node

           >>> new_page.get_content()
           "This is page one"

        """
        return self.content

    def get_type(self):
        """
        Returns the type of the node

           >>> new_page.get_content()
           "page"

        """
        return self.type

    def select(self, selector):
        """
        Execute a selector on this node and then return a list of the matching nodes

        >>> document.content_node.select('.')
           [ContentNode]

        :param selector: The selector (ie. //*)
        :return: A list of the matching content nodes
        """
        from kodexa.selectors import parse
        parsed_selector = parse(selector)
        return parsed_selector.resolve(self)

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

    def tag_nodes_to(self, end_node, tag_to_apply):
        """
        Tag all the nodes from this node to the end node with the given tag name

              >>> document.content_node.children[0].tag_nodes_to(document.content_node.children[5], tag_name='foo')

         :param end_node: The node to end with
         :param tag_to_apply: The tag name that will be applied to each node
         """
        [node.tag(tag_to_apply) for node in self.collect_nodes_to(end_node)]

    def tag_range(self, start_content_re, end_content_re, tag_to_apply, type_re='.*', use_all_content=False):
        """
        This will tag all the child nodes between the start and end content regular expressions

             >>> document.content_node.tag_range(start_content_re='.*Cheese.*', end_content_re='.*Fish.*', tag_to_apply='foo')

        :param start_content_re: The regular expression to match the starting child
        :param end_content_re: The regular expression to match the ending child
        :param tag_to_apply: The tag name that will be applied to the nodes in range
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
            [node.tag(tag_to_apply) for node in all_nodes[start_index:end_index]]

    def tag(self, tag_to_apply, selector=".", content_re=None,
            use_all_content=False, node_only=False,
            fixed_position=None, data=None):
        """
        This will tag (see Feature Tagging) the expression groups identified by the regular expression.

            >>> document.content_node.tag('is_cheese')

        :param tag_to_apply: the name of tag that will be applied to the node
        :param selector: The selector to identify the source nodes to work on (default . - the current node)
        :param content_re: the regular expression that you wish to use to tag, note that we will create a tag for each matching group
        :param use_all_content: apply the regular expression to the all_content (include content from child nodes)
        :param node_only: Ignore the matching groups and tag the whole node
        :param include_children: Include recurse into children and tag where matching
        :param fixed_position: use a fixed position, supplied as a tuple i.e. - (4,10) tag from position 4 to 10 (default None)
        :param data: Attach the a dictionary of data for the given tag
        """

        for node in self.select(selector):
            if fixed_position:
                self.add_feature('tag', tag_to_apply,
                                 Tag(fixed_position[0], fixed_position[1],
                                     self.content[fixed_position[0]:fixed_position[1]],
                                     data))
            else:
                if not content_re:
                    self.add_feature('tag', tag_to_apply, Tag(data=data))
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
                            self.add_feature('tag', tag_to_apply, Tag(data=data))
                        else:
                            for index, m in enumerate(match.groups()):
                                idx = index + 1
                                self.add_feature('tag', tag_to_apply,
                                                 Tag(match.start(idx), match.end(idx), match.group(idx), data=data))

    def get_tags(self):
        """
        Returns a list of the names of the tags on the given node

            >>> document.content_node.select('*').get_tags()
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
        return {'name': self.feature_type + ':' + self.name, 'value': self.value, 'single': self.single}


class DocumentRender:

    def __init__(self, document):
        self.document = document
        self.kodexa_render = KodexaRender()

    def to_html(self):
        return self.kodexa_render.build_html(self.document, self.document.content_node)

    def render_node(self, node):
        return self.kodexa_render.build_html(self.document, node)


class SourceMetadata(object):
    pass


class Document(object):
    """
    A Document is a collection of metadata and a set of content nodes.
    """

    def __str__(self):
        return f"kdxa//{self.uuid}/{self.metadata}"

    def __init__(self, metadata=None, content_node: ContentNode = None, source=SourceMetadata()):
        if metadata is None:
            metadata = DocumentMetadata()
        self.metadata: DocumentMetadata = metadata
        self.content_node: ContentNode = content_node
        self.virtual: bool = False
        self._mixins = []
        self.uuid: str = str(uuid.uuid5(uuid.NAMESPACE_DNS, 'kodexa.com'))
        self.exceptions = []
        self.log = []
        self.version = "1.0.0"
        self.add_mixin('core')
        self.source: SourceMetadata = source

        # Make sure we apply all the mixins
        registry.apply_to_document(self)

    @classmethod
    def from_text(cls, text):
        new_document = Document()
        new_document.content_node = new_document.create_node(type='text', content=text)
        new_document.add_mixin('text')
        return new_document

    def get_root(self):
        """
        Get the root content node for the document (same as content_node)


            >>> node = document.get_node()
        """
        return self.content_node

    def to_kdxa(self, file_path):
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
        Convert this document object structure into a JSON object


            >>> document.to_json()
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)

    def _repr_html_(self):
        return self.to_html()

    def to_html(self):
        return DocumentRender(self).to_html()

    def to_dict(self):
        """
        Convert this document object structure into a simple set of dictionaries


            >>> document.to_dict()
        """
        return {'version': self.version, 'metadata': self.metadata,
                'content_node': self.content_node.to_dict() if self.content_node else None,
                'mixins': self._mixins,
                'exceptions': self.exceptions,
                'log': self.log,
                'uuid': self.uuid}

    @staticmethod
    def from_dict(doc_dict):
        """
        Build a new document from a dictionary


            >>> Document.from_dict(doc_dict)
        """
        new_document = Document(DocumentMetadata(doc_dict['metadata']))
        for mixin in doc_dict['mixins']:
            registry.add_mixin_to_document(mixin, new_document)
        new_document.version = doc_dict['version'] if 'version' in doc_dict else '1.0.0'
        new_document.log = doc_dict['log'] if 'log' in doc_dict else []
        new_document.exceptions = doc_dict['exceptions'] if 'exceptions' in doc_dict else []
        new_document.uuid = doc_dict['uuid'] if 'uuid' in doc_dict else str(
            uuid.uuid5(uuid.NAMESPACE_DNS, 'kodexa.com'))
        if 'content_node' in doc_dict and doc_dict['content_node']:
            new_document.content_node = ContentNode.from_dict(new_document, doc_dict['content_node'])

        return new_document

    @staticmethod
    def from_json(json_string):
        """
        From a JSON string create an instance of a Document

            >>> document.from_json()
        """
        return Document.from_dict(json.loads(json_string))

    @staticmethod
    def from_msgpack(bytes):
        """
        From a message pack byte array create an instance of a Document

            >>> document.from_msgpack()
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

    def create_node(self, type: str = type, content: str = None, virtual: bool = False, parent: ContentNode = None,
                    index: int = 0):
        """
        Creates a new node for the document, this doesn't add the node to the document however
        it does ensure that any mixins that have been applied to the document will also be
        available on the new node

            >>> document.create_node(type='page')
            <kodexa.model.model.ContentNode object at 0x7f80605e53c8>
        """
        content_node = ContentNode(document=self, type=type, content=content)
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
        file_document = Document()
        file_document.metadata.connector = 'file-handle'
        file_document.metadata.connector_options.file = file
        return file_document

    @classmethod
    def from_url(cls, url, headers=None):
        if headers is None:
            headers = {}
        url_document = Document()
        url_document.metadata.connector = 'url'
        url_document.metadata.connector_options.url = url
        url_document.metadata.connector_options.headers = headers
        return url_document

    def select(self, selector):
        """
        Execute a selector on the root node and then return a list of the matching nodes

        >>> document.select('.')
           [ContentNode]

        :param selector: The selector (ie. //*)
        :return: A list of the matching content nodes
        """
        if self.content_node:
            return self.content_node.select(selector)
        else:
            return []


class KodexaRender:
    KODEXA_JS_URL = 'https://cdn.jsdelivr.net/npm/kodexajs/kodexa'

    """
    An implementation of a render that uses the KodexaJS
    library to render the document

    See https://github.com/kodexa-ai/kodexa.js
    """

    def build_node_html(self, node: ContentNode):
        self.build_html(node.document, node)

    def build_html(self, document: Document, node: ContentNode):
        render_uuid = str(uuid.uuid4())
        return """
  <div id='kodexa-div-""" + render_uuid + """'></div> 
  <script>

require.config({
    paths: {
        'kodexa-lib-""" + render_uuid + """': '""" + KodexaRender.KODEXA_JS_URL + """',
        'jquery': '//ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min'
    }
});

require(['kodexa-lib-""" + render_uuid + """','jquery'], function() {
    kodexa.fromMap(""" + document.to_json() + """).then(kdxaDocument => {
       let widget = kodexa.newDocumentWidget(kdxaDocument);
       widget.attach($('#kodexa-div-""" + render_uuid + """'))
       widget.render(""" + ("'" + node.uuid + "'" if node else "") + """);
    });
    
});
</script>
"""
