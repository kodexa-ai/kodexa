import json
import os
import uuid

import msgpack
from attrdict import AttrDict

from kodexa.mixins import registry
from kodexa.mixins.registry import get_mixin


class DocumentMetadata(dict):
    """
    A flexible dict based approach to capturing metadata for the document

    Sub-classes dict, and further allows attribute-like access to dictionary items.

        >>> d = DocumentMetadata({'a': 1})
        >>> d.a, d['a'], d.get('a')
        (1, 1, 1)
        >>> d.b = 2
        >>> d.b, d['b']
        (2, 2)
    """

    def __init__(self, *args, **kwargs):
        super(DocumentMetadata, self).__init__(*args, **kwargs)
        self.__dict__ = self


class ContentNode(object):
    """
    A Content Node identifies a section of the document containing logical
    grouping of information

    The node will have content and can include n number of features.

    You should always create a node using the Document create_node method to
    ensure that the correct mixins are applied.

        >>> new_page = document.create_node(type='page')
        <mango.model.model.ContentNode object at 0x7f80605e53c8>
        >>> current_content_node.add_child(new_page)

    or

        >>> new_page = document.create_node(type='page', content='This is page 1')
        <mango.model.model.ContentNode object at 0x7f80605e53c8>
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

    def to_text(self):
        """
        Convert this node  structure into a text representation,
        which can be useful when trying to review the structure.


            >>> node.to_text()
        """
        return DefaultDocumentRender(self.document).node_to_text(self, 0)

    def _repr_html_(self):
        return self.to_html()

    def to_html(self):
        return DocumentRender(self.document).render_node(self)

    def to_mimetype(self):
        return DocumentRender(self.document).render_node_mimetype(self)

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
            <mango.model.model.ContentNode object at 0x7f80605e53c8>
            >>> current_content_node.to_dict()
        """
        new_dict = {'type': self.type, 'content': self.content, 'content_parts': self.content_parts, 'features': [],
                    'index': self.index, 'children': []}
        for feature in self.get_features():
            new_dict['features'].append(feature.to_dict())

        for child in self.children:
            new_dict['children'].append(child.to_dict())
        return new_dict

    @staticmethod
    def from_dict(document, content_node_dict):
        new_content_node = document.create_node(type=content_node_dict['type'], content=content_node_dict[
            'content'] if 'content' in content_node_dict else None)

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
            <mango.model.model.ContentNode object at 0x7f80605e53c8>
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
           <mango.model.model.ContentNode object at 0x7f80605e53c8>
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
           <mango.model.model.ContentNode object at 0x7f80605e53c8>
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
           <mango.model.model.ContentNode object at 0x7f80605e53c8>
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
        self.default_renderer = DefaultDocumentRender(document)

    def to_text(self):
        return self.default_renderer.node_to_text(self.document.content_node, 0)

    def to_html(self):
        print(self.get_mixin_renderer())
        return self.get_mixin_renderer().to_html()

    def get_mixin_renderer(self):
        renderer_dict = registry.get_renderers(self.document)
        if renderer_dict:
            return next(iter(renderer_dict.values()))
        else:
            return self.default_renderer

    def render_node(self, node):
        return self.get_mixin_renderer().render_node(node)

    def to_mimetype(self):
        return self.get_mixin_renderer().to_mimetype()

    def render_node_mimetype(self, node):
        return self.get_mixin_renderer().render_node_mimetype(node)


class DefaultDocumentRender:

    def __init__(self, document):
        self.document = document

    def to_text(self):
        return self.node_to_text(self.document.content_node, 0)

    def to_html(self):
        return f"<h3>Document {self.document}</h3>"

    def render_node(self, node):
        out_list = []
        self.get_node_text_format(node, 0, out_list)
        return f"<h3>Content Node</h3><p>{self.node_to_text(node, 0)}"

    def node_to_text(self, node, level):
        out_list = []
        self.get_node_text_format(node, level, out_list)
        return os.linesep.join(out_list)

    def get_node_text_format(self, node, level, out_list):
        out_list.append("{}[type:{}]{}".format(" " * (4 * level), node.type, self.mixins_to_text(node)))

        if node.content_parts:
            print("Content Parts:")
            out_list.append("{}{}".format(" " * (4 * level), self.get_content_parts(node)))

        print("Content:")
        out_list.append("{}{}".format(" " * (4 * level), node.content))

        for child in node.get_children():
            self.get_node_text_format(child, level + 1, out_list)

    def get_content_parts(self, node):
        result = ""
        for part in node.content_parts:
            if isinstance(part, str):
                result = result + part
            # else:
            #     result = result + "#c" + str(part)

        return result

    def mixins_to_text(self, node):
        display = ""
        for mixin in self.document.get_mixins():
            if get_mixin(mixin):
                text = get_mixin(mixin).to_text(node)
                if text:
                    display = display + get_mixin(mixin).to_text(node)

        return display

    def to_mimetype(self):
        out_list = []
        self.get_node_text_format(self.document.content_node, 0, out_list)
        return self.prepare_mimetype_data('document', tuple(out_list))

    def render_node_mimetype(self, node):
        out_list = []
        self.get_node_text_format(node, 0, out_list)
        return self.prepare_mimetype_data('content_node', tuple(out_list))

    def prepare_mimetype_data(self, data_type, data_list):
        render_data = {'data_type': data_type, 'data': tuple(data_list)}
        bundle = {}
        bundle['application/vnd.mango.document+json'] = render_data
        return bundle


class Document(object):
    """
    A Document is a collection of metadata and a set of content nodes.
    """

    def __str__(self):
        return f"MDocument {self.uuid} {self.metadata}"

    def __init__(self, metadata: DocumentMetadata, content_node: ContentNode = None):
        self.metadata: DocumentMetadata = metadata
        self.content_node: ContentNode = content_node
        self.virtual: bool = False
        self._mixins = []
        self.uuid: str = str(uuid.uuid5(uuid.NAMESPACE_DNS, 'kodexa.com'))
        self.exceptions = []
        self.log = []
        self.version = "1.0.0"

        # Make sure we apply all the mixins
        registry.apply_to_document(self)

    def get_root(self):
        """
        Get the root content node for the document (same as content_node)


            >>> node = document.get_node()
        """
        return self.content_node

    def to_text(self):
        """
        Convert this document object structure into a text representation,
        which can be useful when trying to review the structure.


            >>> document.to_text()
        """
        return DocumentRender(self).to_text()

    def to_mdoc(self, file_path):
        """
        Write the document to the mdoc format (msgpack) which can be
        used with the Kodexa platform

            >>> document.to_mdoc('my-document.mdoc')

        :param file_path: the path to the mdoc you wish to create
        """
        with open(file_path, 'wb') as outfile:
            msgpack.pack(self.to_dict(), outfile, use_bin_type=True)

    @staticmethod
    def from_mdoc(file_path):
        """
        Read an mdoc file from the given file_path and

            >>> document = Document.from_mdoc('my-document.mdoc')

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

    def to_mimetype(self):
        return DocumentRender(self).to_mimetype()

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
        return Document.from_dict(json.loads(json_string, object_hook=AttrDict))

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

    def create_node(self, type=type, content=None, virtual=False, parent=None, index=0):
        """
        Creates a new node for the document, this doesn't add the node to the document however
        it does ensure that any mixins that have been applied to the document will also be
        available on the new node

            >>> document.create_node(type='page')
            <mango.model.model.ContentNode object at 0x7f80605e53c8>
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
