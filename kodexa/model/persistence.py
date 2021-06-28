import dataclasses
import hashlib
import pathlib
import sqlite3

import msgpack

from kodexa.model import Document, ContentNode

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

    def __init__(self, document: Document, filename: str = None):
        self.document = document
        import sqlite3

        is_new = True
        if filename is not None:
            path = pathlib.Path(filename)
            if path.exists():
                # At this point we need to load the db
                is_new = False

                pass
        else:
            filename = ':memory:'

        self.current_filename = filename
        self.connection = sqlite3.connect(filename)

        if is_new:
            self.__build_db()

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
        cursor.execute("CREATE INDEX cnp_perf ON cnp(cn_id);")

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
        document_metadata = {'version': Document.CURRENT_VERSION, 'metadata': self.document.metadata,
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
