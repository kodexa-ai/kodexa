import dataclasses
import hashlib
import pathlib
import sqlite3
import tempfile
import uuid

import msgpack

from kodexa.model import Document, ContentNode, SourceMetadata
from kodexa.model.model import ContentClassification, DocumentMetadata

# Heavily used SQL

FEATURE_INSERT = "INSERT INTO f (cn_id, f_type, fvalue_id) VALUES (?,?,?)"
CONTENT_NODE_INSERT = "INSERT INTO cn (pid, nt, idx) VALUES (?,?,?)"
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

        is_new = True
        if filename is not None:
            self.is_tmp = False
            path = pathlib.Path(filename)
            if path.exists():
                # At this point we need to load the db
                is_new = False
        else:
            new_file, filename = tempfile.mkstemp()
            self.is_tmp = True

        self.current_filename = filename
        self.connection = sqlite3.connect(filename)
        self.connection.execute("PRAGMA journal_mode=OFF")

        if is_new:
            self.__build_db()
        else:
            self.__load_document()

    def close(self):
        if self.is_tmp or self.delete_on_close:
            pathlib.Path(self.current_filename).unlink()

    def __build_db(self):
        cursor = self.connection.cursor()
        cursor.execute("CREATE TABLE version (id integer primary key, version text)")
        cursor.execute("CREATE TABLE metadata (id integer primary key, metadata text)")
        cursor.execute("CREATE TABLE cn (id integer primary key, nt INTEGER, pid INTEGER, idx INTEGER)")
        cursor.execute(
            "CREATE TABLE cnp (id integer primary key, cn_id INTEGER, pos integer, content text, content_idx integer)")

        cursor.execute("CREATE TABLE n_type (id integer primary key, name text)")
        cursor.execute("CREATE TABLE f_type (id integer primary key, name text)")
        cursor.execute(
            "CREATE TABLE f_value (id integer primary key, hash integer, binary_value blob, single integer)")
        cursor.execute(
            "CREATE TABLE f (id integer primary key, cn_id integer, f_type INTEGER, fvalue_id integer)")

        cursor.execute("CREATE UNIQUE INDEX n_type_uk ON n_type(name);")
        cursor.execute("CREATE UNIQUE INDEX f_type_uk ON f_type(name);")
        cursor.execute("CREATE INDEX cn_perf ON cn(nt);")
        cursor.execute("CREATE INDEX cn_perf2 ON cn(pid);")
        cursor.execute("CREATE INDEX cnp_perf ON cnp(cn_id, pos);")
        cursor.execute("CREATE INDEX f_perf ON cnp(cn_id);")
        cursor.execute("CREATE INDEX f_value_hash ON f_value(hash);")

        self.__update_metadata(cursor)

        if self.document.content_node:
            self.__insert_node(self.document.content_node, cursor)

        self.connection.commit()

        cursor.close()

    def content_node_count(self):
        cursor = self.connection.cursor()
        cursor.execute("select * from cn").fetchall()

    def __resolve_f_type(self, feature, cursor):
        feature_type_name = feature.feature_type + ":" + feature.name
        result = cursor.execute(FEATURE_TYPE_LOOKUP, [feature_type_name]).fetchone()
        if result is None:
            return cursor.execute(FEATURE_TYPE_INSERT, [feature_type_name]).lastrowid
        return result[0]

    def __resolve_n_type(self, n_type, cursor):
        result = cursor.execute(NODE_TYPE_LOOKUP, [n_type]).fetchone()
        if result is None:
            return cursor.execute(NOTE_TYPE_INSERT, [n_type]).lastrowid
        return result[0]

    def __resolve_feature_value(self, feature, cursor):
        binary_value = sqlite3.Binary(msgpack.packb(feature.value, use_bin_type=True))
        hash_value = int(hashlib.sha1(binary_value).hexdigest(), 16) % (10 ** 8)
        result = cursor.execute(FEATURE_VALUE_LOOKUP, [hash_value]).fetchone()
        new_row = [binary_value, hash_value, feature.single]

        if result is None:
            fvalue_id = cursor.execute(FEATURE_VALUE_INSERT, new_row).lastrowid
        else:
            fvalue_id = result[0]
        return fvalue_id

    def __insert_node(self, node: ContentNode, cursor):
        cn_values = [node.parent.uuid if node.parent else None,
                     self.__resolve_n_type(node.node_type, cursor), node.index]
        node.uuid = cursor.execute(CONTENT_NODE_INSERT, cn_values).lastrowid

        if node.content_parts is None or (node.content is not None and len(node.content_parts) == 0):
            cn_parts_values = [node.uuid, 0, node.content, None]
            cursor.execute(CONTENT_NODE_PART_INSERT, cn_parts_values)
        else:
            for idx, part in enumerate(node.content_parts):
                cn_parts_values = [node.uuid, idx, part if isinstance(part, str) else None,
                                   part if not isinstance(part, str) else None]
                cursor.execute(CONTENT_NODE_PART_INSERT, cn_parts_values)

        # Work through the features
        for feature in node.get_features():
            f_values = [node.uuid, self.__resolve_f_type(feature, cursor),
                        self.__resolve_feature_value(feature, cursor)]
            feature.uuid = cursor.execute(FEATURE_INSERT,
                                          f_values).lastrowid

        for child in node.children:
            self.__insert_node(child, cursor)

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

    def __update_metadata(self, cursor):
        document_metadata = {'version': Document.CURRENT_VERSION, 'metadata': self.document.metadata.to_dict(),
                             'source': self.__clean_none_values(dataclasses.asdict(self.document.source)),
                             'mixins': self.document.get_mixins(),
                             'taxonomies': self.document.taxonomies,
                             'classes': [content_class.to_dict() for content_class in self.document.classes],
                             'labels': self.document.labels,
                             'uuid': self.document.uuid}
        cursor.execute(VERSION_DELETE)
        cursor.execute(VERSION_INSERT)
        cursor.execute(METADATA_DELETE)
        cursor.execute(METADATA_INSERT, [sqlite3.Binary(msgpack.packb(document_metadata, use_bin_type=True))])

    def __load_document(self):
        cursor = self.connection.cursor()
        for n_type in cursor.execute("select id,name from n_type"):
            self.node_types[n_type[0]] = n_type[1]
        for f_type in cursor.execute("select id,name from f_type"):
            self.feature_type_names[f_type[0]] = f_type[1]

        metadata = msgpack.unpackb(cursor.execute("select * from metadata").fetchone()[1])
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

        root_node = cursor.execute("select id, pid, nt, idx from cn where pid is null").fetchone()
        if root_node:
            self.document.content_node = self.__build_node(
                root_node,
                cursor)
        cursor.close()

    def __build_node(self, node_row, cursor):
        new_node = ContentNode(self.document, self.node_types[node_row[2]])
        new_node.uuid = node_row[0]
        new_node.index = node_row[3]

        content_parts = cursor.execute("select cn_id, pos, content, content_idx from cnp where cn_id = ? order by pos",
                                       [new_node.uuid]).fetchall()

        content = ""
        for content_part in content_parts:
            if content_part[3] is None:
                content = content + content_part[2]
                new_node.content_parts.append(content_part[2])
            else:
                new_node.content_parts.append(content_part[3])

        new_node.content = content

        # We need to get the features back
        for feature in cursor.execute("select id, cn_id, f_type, fvalue_id from f where cn_id = ?",
                                      [new_node.uuid]).fetchall():
            feature_type_name = self.feature_type_names[feature[2]]
            f_value = cursor.execute("select binary_value, single from f_value where id = ?", [feature[3]]).fetchone()
            new_node.add_feature(feature_type_name.split(':')[0], feature_type_name.split(':')[1],
                                 value=msgpack.unpackb(f_value[0]), single=f_value[1] == 1, serialized=True)

        # We need to get the child nodes
        for child_node in cursor.execute("select id, pid, nt, idx from cn where pid = ?", [new_node.uuid]).fetchall():
            new_node.add_child(self.__build_node(child_node, cursor))

        return new_node

    def __rebuild_from_document(self):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM cn")
        cursor.execute("DELETE FROM cnp")
        cursor.execute("DELETE FROM f")
        cursor.execute("DELETE FROM f_value")

        self.__update_metadata(cursor)
        if self.document.content_node:
            self.__insert_node(self.document.content_node, cursor)

        cursor.close()
        self.connection.commit()

    def get_bytes(self):

        # TODO we need to make this an option?
        self.__rebuild_from_document()

        with open(self.current_filename, 'rb') as f:
            return f.read()
