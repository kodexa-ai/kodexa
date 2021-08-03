import dataclasses
import hashlib
import pathlib
import sqlite3
import tempfile
import uuid

import msgpack
from kodexa.model import Document, ContentNode, SourceMetadata
from kodexa.model.model import ContentClassification, DocumentMetadata, ContentFeature

# Heavily used SQL

FEATURE_INSERT = "INSERT INTO f (cn_id, f_type, fvalue_id) VALUES (?,?,?)"
FEATURE_DELETE = "DELETE FROM f where cn_id=? and f_type=?"

CONTENT_NODE_INSERT = "INSERT INTO cn (pid, nt, idx) VALUES (?,?,?)"
CONTENT_NODE_UPDATE = "UPDATE cn set pid=?, nt=?, idx=? WHERE id=?"

CONTENT_NODE_PART_INSERT = "INSERT INTO cnp (cn_id, pos, content, content_idx) VALUES (?,?,?,?)"
NOTE_TYPE_INSERT = "insert into n_type(name) values (?)"
NODE_TYPE_LOOKUP = "select id from n_type where name = ?"
FEATURE_VALUE_LOOKUP = "select id from f_value where hash=?"
FEATURE_VALUE_INSERT = "insert into f_value(binary_value, hash, single) values (?,?,?)"
FEATURE_TYPE_INSERT = "insert into f_type(name) values (?)"
FEATURE_TYPE_LOOKUP = "select id from f_type where name = ?"
METADATA_INSERT = "insert into metadata(id,metadata) values (1,?)"
METADATA_DELETE = "delete from metadata where id=1"
VERSION_INSERT = "insert into version(id,version) values (1,'4.0.0')"
VERSION_DELETE = "delete from version where id=1"


class SqliteDocumentPersistence(object):
    """
    The Sqlite persistence engine to support large scale documents (part of the V4 Kodexa Document Architecture)
    """

    def __init__(self, document: Document, filename: str = None, delete_on_close=False):
        self.document = document

        self.node_types = {}
        self.feature_type_names = {}
        self.delete_on_close = delete_on_close

        import sqlite3

        self.is_new = True
        if filename is not None:
            self.is_tmp = False
            path = pathlib.Path(filename)
            if path.exists():
                # At this point we need to load the db
                self.is_new = False
        else:
            new_file, filename = tempfile.mkstemp()
            self.is_tmp = True

        self.current_filename = filename

        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()
        self.cursor.execute("PRAGMA journal_mode=WAL")
        self.cursor.execute("pragma synchronous = normal")
        self.cursor.execute("pragma temp_store = memory")
        self.cursor.execute("pragma mmap_size = 30000000000")

    def initialize(self):
        if self.is_new:
            self.__build_db()
        else:
            self.__load_document()

    def close(self):
        if self.is_tmp or self.delete_on_close:
            pathlib.Path(self.current_filename).unlink()

    def __build_db(self):
        self.cursor.execute("CREATE TABLE version (id integer primary key, version text)")
        self.cursor.execute("CREATE TABLE metadata (id integer primary key, metadata text)")
        self.cursor.execute("CREATE TABLE cn (id integer primary key, nt INTEGER, pid INTEGER, idx INTEGER)")
        self.cursor.execute(
            "CREATE TABLE cnp (id integer primary key, cn_id INTEGER, pos integer, content text, content_idx integer)")

        self.cursor.execute("CREATE TABLE n_type (id integer primary key, name text)")
        self.cursor.execute("CREATE TABLE f_type (id integer primary key, name text)")
        self.cursor.execute(
            "CREATE TABLE f_value (id integer primary key, hash integer, binary_value blob, single integer)")
        self.cursor.execute(
            "CREATE TABLE f (id integer primary key, cn_id integer, f_type INTEGER, fvalue_id integer)")

        self.cursor.execute("CREATE UNIQUE INDEX n_type_uk ON n_type(name);")
        self.cursor.execute("CREATE UNIQUE INDEX f_type_uk ON f_type(name);")
        self.cursor.execute("CREATE INDEX cn_perf ON cn(nt);")
        self.cursor.execute("CREATE INDEX cn_perf2 ON cn(pid);")
        self.cursor.execute("CREATE INDEX cnp_perf ON cnp(cn_id, pos);")
        self.cursor.execute("CREATE INDEX f_perf ON f(cn_id);")
        self.cursor.execute("CREATE INDEX f_value_hash ON f_value(hash);")

        self.__update_metadata()

    def content_node_count(self):
        self.cursor.execute("select * from cn").fetchall()

    def __resolve_f_type(self, feature):
        feature_type_name = feature.feature_type + ":" + feature.name
        result = self.cursor.execute(FEATURE_TYPE_LOOKUP, [feature_type_name]).fetchone()
        if result is None:
            new_feature_type_name_id = self.cursor.execute(FEATURE_TYPE_INSERT, [feature_type_name]).lastrowid
            self.feature_type_names[new_feature_type_name_id] = feature_type_name
            return new_feature_type_name_id

        return result[0]

    def __resolve_n_type(self, n_type):
        result = self.cursor.execute(NODE_TYPE_LOOKUP, [n_type]).fetchone()
        if result is None:
            new_type_id = self.cursor.execute(NOTE_TYPE_INSERT, [n_type]).lastrowid
            self.node_types[new_type_id] = n_type
            return new_type_id

        return result[0]

    def __resolve_feature_value(self, feature):
        binary_value = sqlite3.Binary(msgpack.packb(feature.value, use_bin_type=True))
        hash_value = int(hashlib.sha1(binary_value).hexdigest(), 16) % (10 ** 8)
        result = self.cursor.execute(FEATURE_VALUE_LOOKUP, [hash_value]).fetchone()
        new_row = [binary_value, hash_value, feature.single]

        if result is None:
            fvalue_id = self.cursor.execute(FEATURE_VALUE_INSERT, new_row).lastrowid
        else:
            fvalue_id = result[0]
        return fvalue_id

    def __insert_node(self, node: ContentNode, parent):

        if node.index is None:
            node.index = 0

        if parent:
            node._parent_uuid = parent.uuid

        if node.uuid:
            # Delete the existing node
            cn_values = [node._parent_uuid,
                         self.__resolve_n_type(node.node_type), node.index, node.uuid]

            # Make sure we load the content parts if we haven't
            node.get_content_parts()
            self.cursor.execute("DELETE FROM cn where id=?", [node.uuid])
            self.cursor.execute("INSERT INTO cn (pid, nt, idx, id) VALUES (?,?,?,?)", cn_values)
            self.cursor.execute("DELETE FROM cnp where cn_id=?", [node.uuid])

            cn_parts_values = []
            for idx, part in enumerate(node.get_content_parts()):
                cn_parts_values.append([node.uuid, idx, part if isinstance(part, str) else None,
                                        part if not isinstance(part, str) else None])

            self.cursor.executemany(CONTENT_NODE_PART_INSERT, cn_parts_values)

        else:
            cn_values = [parent.uuid if parent else None,
                         self.__resolve_n_type(node.node_type), node.index]
            node.uuid = self.cursor.execute(CONTENT_NODE_INSERT, cn_values).lastrowid

            cn_parts_values = []
            for idx, part in enumerate(node.get_content_parts()):
                cn_parts_values.append([node.uuid, idx, part if isinstance(part, str) else None,
                                        part if not isinstance(part, str) else None])

            self.cursor.executemany(CONTENT_NODE_PART_INSERT, cn_parts_values)

        # for child in node.get_children():
        #     child._parent = node
        #     child._parent_uuid = node.uuid
        #     self.__insert_node(child, node)

    def __clean_none_values(self, d):
        clean = {}
        for k, v in d.items():
            if isinstance(v, dict):
                nested = self.__clean_none_values(v)
                if len(nested.keys()) > 0:
                    clean[k] = nested
            elif v is not None:
                clean[k] = v
        return clean

    def __update_metadata(self):
        document_metadata = {'version': Document.CURRENT_VERSION,
                             'metadata': self.document.metadata.to_dict(),
                             'source': self.__clean_none_values(dataclasses.asdict(self.document.source)),
                             'mixins': self.document.get_mixins(),
                             'taxonomies': self.document.taxonomies,
                             'classes': [content_class.to_dict() for content_class in self.document.classes],
                             'labels': self.document.labels,
                             'uuid': self.document.uuid}
        self.cursor.execute(VERSION_DELETE)
        self.cursor.execute(VERSION_INSERT)
        self.cursor.execute(METADATA_DELETE)
        self.cursor.execute(METADATA_INSERT, [sqlite3.Binary(msgpack.packb(document_metadata, use_bin_type=True))])

    def __load_document(self):
        for n_type in self.cursor.execute("select id,name from n_type"):
            self.node_types[n_type[0]] = n_type[1]
        for f_type in self.cursor.execute("select id,name from f_type"):
            self.feature_type_names[f_type[0]] = f_type[1]

        metadata = msgpack.unpackb(self.cursor.execute("select * from metadata").fetchone()[1])
        self.document.metadata = DocumentMetadata(metadata['metadata'])
        for mixin in metadata['mixins']:
            from kodexa.mixins import registry
            registry.add_mixin_to_document(mixin, self.document)
        self.document.version = metadata['version'] if 'version' in metadata and metadata[
            'version'] else Document.PREVIOUS_VERSION  # some older docs don't have a version or it's None

        self.uuid = metadata['uuid'] if 'uuid' in metadata else str(
            uuid.uuid5(uuid.NAMESPACE_DNS, 'kodexa.com'))
        if 'source' in metadata and metadata['source']:
            self.document.source = SourceMetadata.from_dict(metadata['source'])
        if 'labels' in metadata and metadata['labels']:
            self.document.labels = metadata['labels']
        if 'taxomomies' in metadata and metadata['taxomomies']:
            self.document.taxonomies = metadata['taxomomies']
        if 'classes' in metadata and metadata['classes']:
            self.document.classes = [ContentClassification.from_dict(content_class) for content_class in
                                     metadata['classes']]
        self.uuid = metadata.get('uuid')

        root_node = self.cursor.execute("select id, pid, nt, idx from cn where pid is null").fetchone()
        if root_node:
            self.document.content_node = self.__build_node(
                root_node)

    def get_content_parts(self, new_node):
        content_parts = self.cursor.execute(
            "select cn_id, pos, content, content_idx from cnp where cn_id = ? order by pos",
            [new_node.uuid]).fetchall()

        parts = []
        for content_part in content_parts:
            if content_part[3] is None:
                parts.append(content_part[2])
            else:
                parts.append(content_part[3])
        return parts

    def __build_node(self, node_row):
        new_node = ContentNode(self.document, self.node_types[node_row[2]], parent=self.get_node(node_row[1]))
        new_node.uuid = node_row[0]
        new_node.index = node_row[3]
        return new_node

    def add_content_node(self, node, parent):
        self.__insert_node(node, parent)

    def add_feature(self, node, feature):
        f_values = [node.uuid, self.__resolve_f_type(feature),
                    self.__resolve_feature_value(feature)]
        self.cursor.execute(FEATURE_INSERT, f_values)

    def remove_feature(self, node, feature_type, name):

        feature = ContentFeature(feature_type, name, None)
        f_values = [node.uuid, self.__resolve_f_type(feature)]
        self.cursor.execute(FEATURE_DELETE, f_values)

    def get_children(self, content_node):

        # We need to get the child nodes
        children = []
        for child_node in self.cursor.execute("select id, pid, nt, idx from cn where pid = ? order by idx",
                                              [content_node.uuid]).fetchall():
            children.append(self.__build_node(child_node))
        return children

    def get_node(self, node_id):
        node_row = self.cursor.execute("select id, pid, nt, idx from cn where id = ?", [node_id]).fetchone()
        if node_row:
            return self.__build_node(node_row)
        else:
            return None

    def get_parent(self, content_node):

        parent = self.cursor.execute("select pid from cn where id = ?", [content_node.uuid]).fetchone()
        if parent:
            return self.__get_node(parent[0])
        else:
            return None

    def update_metadata(self):
        self.__update_metadata()

    def __rebuild_from_document(self):
        self.cursor.execute("DELETE FROM cn")
        self.cursor.execute("DELETE FROM cnp")
        self.cursor.execute("DELETE FROM f")
        self.cursor.execute("DELETE FROM f_value")

        self.__update_metadata()
        if self.document.content_node:
            self.__insert_node(self.document.content_node, None)

    def get_bytes(self):

        self.__update_metadata()
        self.cursor.execute("pragma optimize")
        self.connection.commit()
        self.connection.close()

        # We need to open/close the DB to get the WAL
        self.connection = sqlite3.connect(self.current_filename)
        self.connection.commit()
        self.connection.close()

        self.connection = sqlite3.connect(self.current_filename)
        self.connection.execute("pragma optimize")
        self.connection.close()

        self.connection = sqlite3.connect(self.current_filename)
        self.cursor = self.connection.cursor()
        self.cursor.execute("PRAGMA journal_mode=WAL")
        self.cursor.execute("pragma synchronous = normal")
        self.cursor.execute("pragma temp_store = memory")
        self.cursor.execute("pragma mmap_size = 30000000000")

        with open(self.current_filename, 'rb') as f:
            return f.read()

    def get_features(self, node):
        # We need to get the features back

        features = []
        for feature in self.cursor.execute("select id, cn_id, f_type, fvalue_id from f where cn_id = ?",
                                           [node.uuid]).fetchall():
            feature_type_name = self.feature_type_names[feature[2]]
            f_value = self.cursor.execute("select binary_value, single from f_value where id = ?",
                                          [feature[3]]).fetchone()

            single = f_value[1] == 1
            value = msgpack.unpackb(f_value[0])
            features.append(ContentFeature(feature_type_name.split(':')[0], feature_type_name.split(':')[1],
                                           value, single=single))

        return features

    def update_content_parts(self, node, content_parts):
        self.cursor.execute("delete from cnp where cn_id=?", [node.uuid])

        all_parts = []
        for idx, part in enumerate(content_parts):
            all_parts.append([node.uuid, idx, part if isinstance(part, str) else None,
                              part if not isinstance(part, str) else None])
        self.cursor.executemany(CONTENT_NODE_PART_INSERT, all_parts)

    def remove_content_node(self, child):
        self.cursor.execute("delete from cnp where cn_id=?", [child.uuid])
        self.cursor.execute("delete from cn where id=?", [child.uuid])

    def remove_all_features(self, node):
        self.cursor.execute("delete from f where cn_id=?", [node.uuid])

    def remove_all_features_by_id(self, node_id):
        self.cursor.execute("delete from f where cn_id=?", [node_id])

    def get_next_node_id(self):
        next_id = self.cursor.execute("select max(id) from cn").fetchone()
        if next_id[0] is None:
            return 1
        else:
            return next_id[0] + 1


class SimpleObjectCache(object):
    """
    A simple cache based on ID'd objects, where we will build ID's for new
    objects, store them and also a dirty flag so that it is easy to pull all
    dirty objects and store them as needed
    """

    def __init__(self):
        self.objs = {}
        self.next_id = 1
        self.dirty_objs = []

    def get_obj(self, id):
        if id in self.objs:
            return self.objs[id]
        else:
            return None

    def add_obj(self, obj):
        if obj.uuid is None:
            obj.uuid = self.next_id
            self.next_id += 1
        self.objs[obj.uuid] = obj
        self.dirty_objs.append(obj.uuid)

    def remove_obj(self, obj):
        if obj.uuid in self.objs:
            self.objs.pop(obj.uuid)
            self.dirty_objs.remove(obj.uuid)

    def get_dirty_objs(self):
        results = []
        for id in self.dirty_objs:
            node = self.get_obj(id)
            if node is not None:
                results.append(node)
        return results

    def undirty(self, obj):
        self.dirty_objs.remove(obj.uuid)


class PersistenceManager(object):
    """
    The persistence manager supports holding the document and only flushing objects to the persistence layer
    as needed.

    This is implemented to allow us to work with large complex documents in a performance centered way.
    """

    def __init__(self, document: Document, filename: str = None, delete_on_close=False):
        self.document = document
        self.node_cache = SimpleObjectCache()
        self.child_cache = {}
        self.feature_cache = {}
        self.content_parts_cache = {}
        self.node_parent_cache = {}

        self._underlying_persistence = SqliteDocumentPersistence(document, filename, delete_on_close)

    def initialize(self):
        self._underlying_persistence.initialize()

        self.node_cache.next_id = self._underlying_persistence.get_next_node_id()

    def close(self):
        self._underlying_persistence.close()

    def get_bytes(self):

        for node in self.node_cache.get_dirty_objs():
            if not node.virtual:
                self._underlying_persistence.add_content_node(node, None)
                self._underlying_persistence.remove_all_features(node)
                if node.uuid in self.feature_cache:
                    for feature in self.feature_cache[node.uuid]:
                        self._underlying_persistence.add_feature(node, feature)
                if node.uuid in self.content_parts_cache:
                    self._underlying_persistence.update_content_parts(node, self.content_parts_cache[node.uuid])
                self.node_cache.undirty(node)

        return self._underlying_persistence.get_bytes()

    def update_metadata(self):
        self._underlying_persistence.update_metadata()

    def add_content_node(self, node, parent):

        if node.index is None:
            node.index = 0

        if parent:
            node._parent_uuid = parent.uuid

        self.node_cache.add_obj(node)

        update_child_cache=False

        if node.uuid not in self.node_parent_cache:
            self.node_parent_cache[node.uuid] = node._parent_uuid
            update_child_cache=True

        if node.uuid in self.node_parent_cache and node._parent_uuid != self.node_parent_cache[node.uuid]:

            # Remove from the old parent
            self.child_cache[self.node_parent_cache[node.uuid]].remove(node)

            # Add to the new parent
            self.node_parent_cache[node.uuid] = node._parent_uuid
            update_child_cache=True

        if update_child_cache:

            if node._parent_uuid not in self.child_cache:
                self.child_cache[node._parent_uuid] = [node]
            else:
                if node not in self.child_cache[node._parent_uuid]:
                    self.child_cache[node._parent_uuid].append(node)
                    self.child_cache[node._parent_uuid] = sorted(self.child_cache[node._parent_uuid], key=lambda x: x.index)

    def get_node(self, node_id):

        node = self.node_cache.get_obj(node_id)
        if node is None:
            node = self._underlying_persistence.get_node(node_id)
            if node is not None:
                self.node_cache.add_obj(node)

        return node

    def remove_content_node(self, node):

        self.node_cache.remove_obj(node)

        if node._parent_uuid is not None:
            self.child_cache[node._parent_uuid].remove(node)

        self.content_parts_cache.pop(node.uuid, None)
        self.feature_cache.pop(node.uuid, None)

        self._underlying_persistence.remove_content_node(node)

    def get_children(self, node):
        if node.uuid not in self.child_cache:
            children = self._underlying_persistence.get_children(node)
            self.child_cache[node.uuid] = sorted(children, key=lambda x: x.index)
        return self.child_cache[node.uuid]

    def update_content_parts(self, node, content_parts):
        self.content_parts_cache[node.uuid] = content_parts

    def get_content_parts(self, node):
        if node.uuid is None:
            return []

        cps = self.content_parts_cache[node.uuid] if node.uuid in self.content_parts_cache else None
        if cps is None:
            cps = self._underlying_persistence.get_content_parts(node)
            if cps is not None:
                self.content_parts_cache[node.uuid] = cps

        return cps

    def remove_feature(self, node, feature_type, name):

        features = self.get_features(node)
        new_features = [i for i in features if not (i.feature_type == feature_type and i.name == name)]
        self.feature_cache[node.uuid] = new_features

    def get_features(self, node):

        if node.uuid not in self.feature_cache:
            features = self._underlying_persistence.get_features(node)
            self.feature_cache[node.uuid] = features

        return self.feature_cache[node.uuid]

    def add_feature(self, node, feature):

        if node.uuid not in self.feature_cache:
            features = self._underlying_persistence.get_features(node)
            self.feature_cache[node.uuid] = features

        self.feature_cache[node.uuid].append(feature)
