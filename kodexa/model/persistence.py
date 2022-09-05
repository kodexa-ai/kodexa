import dataclasses
import logging
import pathlib
import sqlite3
import tempfile
import uuid
from typing import List

import msgpack

from kodexa.model import Document, ContentNode, SourceMetadata
from kodexa.model.model import ContentClassification, DocumentMetadata, ContentFeature, ContentException

logger = logging.getLogger()

# Heavily used SQL
EXCEPTION_INSERT = "INSERT INTO content_exceptions (tag, message, exception_details, group_uuid, tag_uuid, exception_type, severity, node_uuid) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
EXCEPTION_SELECT = "select tag, message, exception_details, group_uuid, tag_uuid, exception_type, severity, node_uuid from content_exceptions"

FEATURE_INSERT = "INSERT INTO ft (id, cn_id, f_type, binary_value, single, tag_uuid) VALUES (?,?,?,?,?,?)"
FEATURE_DELETE = "DELETE FROM ft where cn_id=? and f_type=?"

CONTENT_NODE_INSERT = "INSERT INTO cn (pid, nt, idx) VALUES (?,?,?)"
CONTENT_NODE_UPDATE = "UPDATE cn set pid=?, nt=?, idx=? WHERE id=?"

CONTENT_NODE_PART_INSERT = "INSERT INTO cnp (cn_id, pos, content, content_idx) VALUES (?,?,?,?)"
NOTE_TYPE_INSERT = "insert into n_type(name) values (?)"
NODE_TYPE_LOOKUP = "select id from n_type where name = ?"
FEATURE_TYPE_INSERT = "insert into f_type(name) values (?)"
FEATURE_TYPE_LOOKUP = "select id from f_type where name = ?"
METADATA_INSERT = "insert into metadata(id,metadata) values (1,?)"
METADATA_DELETE = "delete from metadata where id=1"


class SqliteDocumentPersistence(object):
    """
    The Sqlite persistence engine to support large scale documents (part of the V4 Kodexa Document Architecture)
    """

    def __init__(self, document: Document, filename: str = None, delete_on_close=False):
        self.document = document

        self.node_types = {}
        self.node_type_id_by_name = {}
        self.feature_type_id_by_name = {}
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
            from kodexa import KodexaPlatform
            new_file, filename = tempfile.mkstemp(suffix='.kddb', dir=KodexaPlatform.get_tempdir())
            self.is_tmp = True

        self.current_filename = filename

        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()
        self.cursor.execute("PRAGMA journal_mode=OFF")
        self.cursor.execute("pragma temp_store = memory")
        self.cursor.execute("pragma mmap_size = 30000000000")

    def get_all_tags(self):
        "select * from cn where id in (select cn_id from ft where f_type in (select id from f_type where name like 'tag:%'))"
        features = []
        for feature in self.cursor.execute(
                "select name from f_type where name like 'tag:%'").fetchall():
            features.append(feature[0].split(':')[1])

        return features

    def update_features(self, node):

        next_feature_id = self.get_max_feature_id()
        all_features = []
        for feature in node.get_features():
            binary_value = sqlite3.Binary(msgpack.packb(feature.value, use_bin_type=True))

            tag_uuid = None
            if feature.feature_type == 'tag' and 'uuid' in feature.value[0]:
                tag_uuid = feature.value[0]['uuid']

            all_features.append(
                [next_feature_id, node.uuid, self.get_feature_type_id(feature),
                 binary_value, feature.single, tag_uuid])

            next_feature_id = next_feature_id + 1

        self.cursor.execute("DELETE FROM ft where cn_id=?", [node.uuid])
        self.cursor.executemany(FEATURE_INSERT, all_features)

    def update_node(self, node):
        self.cursor.execute('update cn set idx=?, pid=? where id=?',
                            [node.index, node._parent_uuid,
                             node.uuid])

    def get_content_nodes(self, node_type, parent_node: ContentNode, include_children):
        nodes = []

        results = []
        if include_children:

            if node_type == "*":
                query = """
                            with recursive
                            parent_node(id, pid, nt, idx, path) AS (
                                VALUES (?,?,?,?,?)
                                UNION ALL
                                SELECT cns.id, cns.pid, cns.nt, cns.idx, parent_node.path || substr('0000000' || cns.idx, -6, 6) 
                                FROM cn cns, parent_node
                                WHERE parent_node.id = cns.pid  
                            )
                            SELECT id, pid, nt, idx, path from parent_node order by path
                            """

                try:
                    results = self.cursor.execute(query,
                                                  [parent_node.uuid,
                                                   parent_node.get_parent().uuid if parent_node.get_parent() else None,
                                                   next(key for key, value in self.node_types.items() if
                                                        value == parent_node.get_node_type()),
                                                   parent_node.index, f"{parent_node.index}".zfill(6)]).fetchall()
                except StopIteration:
                    return []
            else:
                query = """
                                with recursive
                                parent_node(id, pid, nt, idx, path) AS (
                                    VALUES (?,?,?,?,?)
                                    UNION ALL
                                    SELECT cns.id, cns.pid, cns.nt, cns.idx, parent_node.path || substr('000000' || cns.idx, -6, 6) 
                                    FROM cn cns, parent_node
                                    WHERE parent_node.id = cns.pid  
                                )
                                SELECT id, pid, nt, idx, path from parent_node where nt=? order by path
                                """

                try:
                    results = self.cursor.execute(query,
                                                  [parent_node.uuid,
                                                   parent_node.get_parent().uuid if parent_node.get_parent() else None,
                                                   next(key for key, value in self.node_types.items() if
                                                        value == parent_node.get_node_type()),
                                                   parent_node.index,
                                                   f"{parent_node.index}".zfill(6),
                                                   next(key for key, value in self.node_types.items() if
                                                        value == node_type)]).fetchall()
                except StopIteration:
                    return []
        else:
            query = "select id, pid, nt, idx from cn where pid=? and nt=? order by idx"
            try:
                results = self.cursor.execute(query,
                                              [parent_node.uuid, next(key for key, value in self.node_types.items() if
                                                                      value == node_type)]).fetchall()
            except StopIteration:
                return []

        for raw_node in list(results):
            nodes.append(self.__build_node(raw_node))

        return nodes

    def initialize(self):
        if self.is_new:
            self.__build_db()
        else:
            self.__load_document()

    def close(self):
        if self.is_tmp or self.delete_on_close:
            self.cursor.close()
            self.connection.close()
            pathlib.Path(self.current_filename).unlink()

    def get_max_feature_id(self):
        max_id = self.cursor.execute("select max(id) from ft").fetchone()
        if max_id[0] is None:
            return 1

        return max_id[0] + 1

    def __build_db(self):
        self.cursor.execute("CREATE TABLE metadata (id integer primary key, metadata text)")
        self.cursor.execute("CREATE TABLE cn (id integer primary key, nt INTEGER, pid INTEGER, idx INTEGER)")
        self.cursor.execute(
            "CREATE TABLE cnp (id integer primary key, cn_id INTEGER, pos integer, content text, content_idx integer)")

        self.cursor.execute("CREATE TABLE n_type (id integer primary key, name text)")
        self.cursor.execute("CREATE TABLE f_type (id integer primary key, name text)")
        self.cursor.execute("""CREATE TABLE ft
                                    (
                                        id           integer primary key,
                                        cn_id        integer,
                                        f_type       INTEGER,
                                        binary_value blob,
                                        single       integer,
                                        tag_uuid     text
                                    )""")

        self.cursor.execute("CREATE UNIQUE INDEX n_type_uk ON n_type(name);")
        self.cursor.execute("CREATE UNIQUE INDEX f_type_uk ON f_type(name);")
        self.cursor.execute("CREATE INDEX cn_perf ON cn(nt);")
        self.cursor.execute("CREATE INDEX cn_perf2 ON cn(pid);")
        self.cursor.execute("CREATE INDEX cnp_perf ON cnp(cn_id, pos);")
        self.cursor.execute("CREATE INDEX f_perf ON ft(cn_id);")
        self.cursor.execute("CREATE INDEX f_perf2 ON ft(tag_uuid);")
        self.cursor.execute("""CREATE TABLE content_exceptions
                                    (
                                        id           integer primary key,
                                        tag          text,
                                        message      text,
                                        exception_details text,
                                        group_uuid   text,
                                        tag_uuid     text,
                                        exception_type text,
                                        severity     text,
                                        node_uuid    text
                                    )""")
        self.document.version = "4.0.2"

        self.__update_metadata()

    def content_node_count(self):
        self.cursor.execute("select * from cn").fetchall()

    def get_feature_type_id(self, feature):
        return self.__resolve_f_type(feature)

    def __resolve_f_type(self, feature):
        feature_type_name = feature.feature_type + ":" + feature.name

        if feature_type_name in self.feature_type_id_by_name:
            return self.feature_type_id_by_name[feature_type_name]

        result = self.cursor.execute(FEATURE_TYPE_LOOKUP, [feature_type_name]).fetchone()
        if result is None:
            new_feature_type_name_id = self.cursor.execute(FEATURE_TYPE_INSERT, [feature_type_name]).lastrowid
            self.feature_type_names[new_feature_type_name_id] = feature_type_name
            self.feature_type_id_by_name[feature_type_name] = new_feature_type_name_id
            return new_feature_type_name_id

        return result[0]

    def __resolve_n_type(self, n_type):
        if n_type in self.node_type_id_by_name:
            return self.node_type_id_by_name[n_type]
        result = self.cursor.execute(NODE_TYPE_LOOKUP, [n_type]).fetchone()
        if result is None:
            new_type_id = self.cursor.execute(NOTE_TYPE_INSERT, [n_type]).lastrowid
            self.node_types[new_type_id] = n_type
            self.node_type_id_by_name[n_type] = new_type_id
            return new_type_id

        return result[0]

    def __insert_node(self, node: ContentNode, parent, execute=True):

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

            if execute:
                self.cursor.execute("DELETE FROM cn where id=?", [node.uuid])
                self.cursor.execute("INSERT INTO cn (pid, nt, idx, id) VALUES (?,?,?,?)", cn_values)
                self.cursor.execute("DELETE FROM cnp where cn_id=?", [node.uuid])

            cn_parts_values = []
            for idx, part in enumerate(node.get_content_parts()):
                cn_parts_values.append([node.uuid, idx, part if isinstance(part, str) else None,
                                        part if not isinstance(part, str) else None])

            if execute:
                self.cursor.executemany(CONTENT_NODE_PART_INSERT, cn_parts_values)

            return ([cn_values], cn_parts_values)

        raise Exception("Node must have a UUID?")

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
        self.cursor.execute(METADATA_DELETE)
        self.cursor.execute(METADATA_INSERT, [sqlite3.Binary(msgpack.packb(document_metadata, use_bin_type=True))])

    def __load_document(self):
        for n_type in self.cursor.execute("select id,name from n_type"):
            self.node_types[n_type[0]] = n_type[1]
        for f_type in self.cursor.execute("select id,name from f_type"):
            self.feature_type_names[f_type[0]] = f_type[1]

        metadata = msgpack.unpackb(self.cursor.execute("select * from metadata").fetchone()[1])
        self.document.metadata = DocumentMetadata(metadata['metadata'])
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

        if self.document.version != '4.0.1' and self.document.version != '4.0.2':
            # We need to migrate this to a 4.0.1 document
            self.cursor.execute("""CREATE TABLE ft
                                    (
                                        id           integer primary key,
                                        cn_id        integer,
                                        f_type       INTEGER,
                                        binary_value blob,
                                        single       integer,
                                        tag_uuid     text
                                    )""")
            self.cursor.execute(
                "insert into ft select f.id, f.cn_id, f.f_type, fv.binary_value, fv.single, null from f, f_value fv where fv.id = f.fvalue_id")
            # we will create a new feature table
            self.cursor.execute("drop table f")
            self.cursor.execute("drop table f_value")
            self.cursor.execute("CREATE INDEX f_perf ON ft(cn_id);")
            self.cursor.execute("CREATE INDEX f_perf2 ON ft(tag_uuid);")
            self.document.version = "4.0.1"
            self.update_metadata()

        if self.document.version == '4.0.1':
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS content_exceptions
                                    (
                                        id           integer primary key,
                                        tag          text,
                                        message      text,
                                        exception_details text,
                                        group_uuid   text,
                                        tag_uuid     text,
                                        exception_type text,
                                        severity     text,
                                        node_uuid    text
                                    )""")
            self.document.version = "4.0.2"
            self.update_metadata()

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

    def add_content_node(self, node, parent, execute=True):
        return self.__insert_node(node, parent, execute)

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

    def get_child_ids(self, content_node):

        # We need to get the child nodes
        children = []
        for child_node in self.cursor.execute("select id, pid, nt, idx from cn where pid = ? order by idx",
                                              [content_node.uuid]).fetchall():
            children.append(child_node[0])
        return children

    def get_node(self, node_id):
        node_row = self.cursor.execute("select id, pid, nt, idx from cn where id = ?", [node_id]).fetchone()
        if node_row:
            return self.__build_node(node_row)

        return None

    def get_parent(self, content_node):

        parent = self.cursor.execute("select pid from cn where id = ?", [content_node.uuid]).fetchone()
        if parent:
            return self.get_node(parent[0])

        return None

    def update_metadata(self):
        self.__update_metadata()

    def __rebuild_from_document(self):
        self.cursor.execute("DELETE FROM cn")
        self.cursor.execute("DELETE FROM cnp")
        self.cursor.execute("DELETE FROM ft")

        self.__update_metadata()
        if self.document.content_node:
            self.__insert_node(self.document.content_node, None)

    def sync(self):
        self.__update_metadata()
        self.cursor.execute("pragma optimize")
        self.connection.commit()
        self.cursor.execute("VACUUM")
        self.connection.close()

        self.connection = sqlite3.connect(self.current_filename)
        self.cursor = self.connection.cursor()
        self.cursor.execute("PRAGMA journal_mode=OFF")
        self.cursor.execute("pragma temp_store = memory")
        self.cursor.execute("pragma mmap_size = 30000000000")

    def get_bytes(self):
        self.sync()
        with open(self.current_filename, 'rb') as f:
            return f.read()

    def get_features(self, node):
        # We need to get the features back

        features = []
        for feature in self.cursor.execute("select id, cn_id, f_type, binary_value, single from ft where cn_id = ?",
                                           [node.uuid]).fetchall():
            feature_type_name = self.feature_type_names[feature[2]]
            single = feature[4] == 1
            value = msgpack.unpackb(feature[3])
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

    def remove_content_node(self, node):
        def get_all_node_ids(node):
            all_node_ids = []
            if not node.virtual:
                all_node_ids.append([node.uuid])
                for child in node.get_children():
                    all_node_ids.extend(get_all_node_ids(child))

            return all_node_ids

        all_child_ids = get_all_node_ids(node)

        self.cursor.executemany("delete from cnp where cn_id=?", all_child_ids)
        self.cursor.executemany("delete from cn where id=?", all_child_ids)
        self.cursor.executemany("delete from ft where cn_id=?", all_child_ids)

    def remove_all_features(self, node):
        self.cursor.execute("delete from ft where cn_id=?", [node.uuid])

    def remove_all_features_by_id(self, node_id):
        self.cursor.execute("delete from ft where cn_id=?", [node_id])

    def get_next_node_id(self):
        next_id = self.cursor.execute("select max(id) from cn").fetchone()
        if next_id[0] is None:
            return 1

        return next_id[0] + 1

    def get_tagged_nodes(self, tag, tag_uuid=None):
        content_nodes = []
        if tag_uuid is None:
            query = f"select cn_id from ft where f_type in (select id from f_type where name like 'tag:{tag}')"
        else:
            query = f"select cn_id from ft where f_type in (select id from f_type where name like 'tag:{tag}') and tag_uuid = '{tag_uuid}'"
        for content_node_ids in self.cursor.execute(
                query).fetchall():
            content_nodes.append(self.get_node(content_node_ids[0]))

        return content_nodes

    def add_exception(self, exception: ContentException):
        # Add an exception to the exception table
        self.cursor.execute(EXCEPTION_INSERT,
                            [exception.tag, exception.message, exception.exception_details, exception.group_uuid,
                             exception.tag_uuid, exception.exception_type, exception.severity, exception.node_uuid])

    def get_exceptions(self) -> List[ContentException]:
        exceptions = []
        for exception in self.cursor.execute(EXCEPTION_SELECT).fetchall():
            exceptions.append(ContentException(tag=exception[0], message=exception[1], exception_details=exception[2],
                                               group_uuid=exception[3], tag_uuid=exception[4],
                                               exception_type=exception[5],
                                               severity=exception[6], node_uuid=exception[7]))
        return exceptions

    def replace_exceptions(self, exceptions: List[ContentException]):
        self.cursor.execute("delete from content_exceptions")
        for exception in exceptions:
            self.add_exception(exception)


class SimpleObjectCache(object):
    """
    A simple cache based on ID'd objects, where we will build ID's for new
    objects, store them and also a dirty flag so that it is easy to pull all
    dirty objects and store them as needed
    """

    def __init__(self):
        self.objs = {}
        self.next_id = 1
        self.dirty_objs = set()

    def get_obj(self, obj_id):
        if obj_id in self.objs:
            return self.objs[obj_id]

        return None

    def add_obj(self, obj):
        if obj.uuid is None:
            obj.uuid = self.next_id
            self.next_id += 1
        self.objs[obj.uuid] = obj
        self.dirty_objs.add(obj.uuid)

    def remove_obj(self, obj):
        if obj.uuid in self.objs:
            self.objs.pop(obj.uuid)
            if obj.uuid in self.dirty_objs:
                self.dirty_objs.remove(obj.uuid)

    def get_dirty_objs(self):
        results = []
        for set_id in set(self.dirty_objs):
            node = self.get_obj(set_id)
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
        self.child_id_cache = {}
        self.feature_cache = {}
        self.content_parts_cache = {}
        self.node_parent_cache = {}

        self._underlying_persistence = SqliteDocumentPersistence(document, filename, delete_on_close)

    def add_exception(self, exception: ContentException):
        self._underlying_persistence.add_exception(exception)

    def get_exceptions(self) -> List[ContentException]:
        return self._underlying_persistence.get_exceptions()

    def replace_exceptions(self, exceptions: List[ContentException]):
        self._underlying_persistence.replace_exceptions(exceptions)

    def get_all_tags(self):
        return self._underlying_persistence.get_all_tags()

    def get_tagged_nodes(self, tag, tag_uuid=None):
        self.flush_cache()
        return self._underlying_persistence.get_tagged_nodes(tag, tag_uuid)

    def initialize(self):
        self._underlying_persistence.initialize()

        self.node_cache.next_id = self._underlying_persistence.get_next_node_id()

    def get_parent(self, node):
        if node.uuid in self.node_parent_cache:
            return self.node_cache.get_obj(self.node_parent_cache[node.uuid])

        return self._underlying_persistence.get_parent(node)

    def close(self):
        self._underlying_persistence.close()

    def flush_cache(self):
        all_node_ids = []
        all_nodes = []
        all_content_parts = []
        all_features = []
        node_id_with_features = []

        logger.debug("Merging cache to persistence")
        dirty_nodes = self.node_cache.get_dirty_objs()

        logger.debug(f"Identified {len(dirty_nodes)} nodes to update")

        next_feature_id = self._underlying_persistence.get_max_feature_id()
        for node in dirty_nodes:
            if not node.virtual:
                all_node_ids.append([node.uuid])
                node_obj, content_parts = self._underlying_persistence.add_content_node(node, None, execute=False)
                all_nodes.extend(node_obj)
                all_content_parts.extend(content_parts)
                if node.uuid in self.feature_cache:

                    if node.uuid in self.feature_cache:
                        node_id_with_features.append([node.uuid])

                    for feature in self.feature_cache[node.uuid]:
                        binary_value = sqlite3.Binary(msgpack.packb(feature.value, use_bin_type=True))

                        tag_uuid = None
                        if feature.feature_type == 'tag' and 'uuid' in feature.value[0]:
                            tag_uuid = feature.value[0]['uuid']

                        all_features.append(
                            [next_feature_id, node.uuid, self._underlying_persistence.get_feature_type_id(feature),
                             binary_value, feature.single, tag_uuid])
                        next_feature_id = next_feature_id + 1

                self.node_cache.undirty(node)

        logger.debug(f"Writing {len(all_node_ids)} nodes")
        self._underlying_persistence.cursor.executemany("DELETE FROM cn where id=?", all_node_ids)
        self._underlying_persistence.cursor.executemany("DELETE FROM ft where cn_id=?", node_id_with_features)
        self._underlying_persistence.cursor.executemany("INSERT INTO cn (pid, nt, idx, id) VALUES (?,?,?,?)", all_nodes)
        self._underlying_persistence.cursor.executemany("DELETE FROM cnp where cn_id=?", all_node_ids)
        logger.debug(f"Writing {len(all_content_parts)} content parts")

        self._underlying_persistence.cursor.executemany(CONTENT_NODE_PART_INSERT, all_content_parts)

        logger.debug(f"Writing {len(all_features)} features")
        self._underlying_persistence.cursor.executemany(FEATURE_INSERT, all_features)

    def get_content_nodes(self, node_type, parent_node, include_children):
        return self._underlying_persistence.get_content_nodes(node_type, parent_node, include_children)

    def get_bytes(self):
        self.flush_cache()
        self._underlying_persistence.sync()
        return self._underlying_persistence.get_bytes()

    def update_metadata(self):
        self._underlying_persistence.update_metadata()

    def add_content_node(self, node, parent):

        if node.index is None:
            node.index = 0

        if parent:
            node._parent_uuid = parent.uuid
            self.node_cache.add_obj(parent)

        self.node_cache.add_obj(node)

        update_child_cache = False

        if node.uuid not in self.node_parent_cache:
            self.node_parent_cache[node.uuid] = node._parent_uuid
            update_child_cache = True

        if node.uuid in self.node_parent_cache and node._parent_uuid != self.node_parent_cache[node.uuid]:
            # Remove from the old parent
            self.child_id_cache[self.node_parent_cache[node.uuid]].remove(node.uuid)
            self.child_cache[self.node_parent_cache[node.uuid]].remove(node)
            # Add to the new parent
            self.node_parent_cache[node.uuid] = node._parent_uuid
            update_child_cache = True

        if update_child_cache:

            if node._parent_uuid not in self.child_cache:
                self.child_cache[node._parent_uuid] = [node]
                self.child_id_cache[node._parent_uuid] = set([node.uuid])
            else:
                if node.uuid not in self.child_id_cache[node._parent_uuid]:
                    self.child_id_cache[node._parent_uuid].add(node.uuid)
                    current_children = self.child_cache[node._parent_uuid]
                    if len(current_children) == 0 or node.index >= current_children[-1].index:
                        self.child_cache[node._parent_uuid].append(node)
                    else:
                        self.child_cache[node._parent_uuid].append(node)
                        self.child_cache[node._parent_uuid] = sorted(self.child_cache[node._parent_uuid],
                                                                     key=lambda x: x.index)

    def get_node(self, node_id):

        node = self.node_cache.get_obj(node_id)
        if node is None:
            node = self._underlying_persistence.get_node(node_id)
            if node is not None:
                self.node_cache.add_obj(node)
                if node._parent_uuid:
                    self.node_parent_cache[node.uuid] = node._parent_uuid
                    if node._parent_uuid not in self.child_id_cache:
                        self.get_node(node._parent_uuid)

        return node

    def remove_content_node(self, node):

        self.node_cache.remove_obj(node)

        if node.uuid in self.node_parent_cache:
            self.child_cache[self.node_parent_cache[node.uuid]].remove(node)
            self.child_id_cache[self.node_parent_cache[node.uuid]].remove(node.uuid)
            del self.node_parent_cache[node.uuid]

        self.content_parts_cache.pop(node.uuid, None)
        self.feature_cache.pop(node.uuid, None)

        self._underlying_persistence.remove_content_node(node)

    def get_children(self, node):
        if node.uuid not in self.child_id_cache:
            child_ids = self._underlying_persistence.get_child_ids(node)
        else:
            child_ids = self.child_id_cache[node.uuid]

        if node.uuid not in self.child_cache:
            new_children = []

            for child_id in child_ids:
                child_node = self.node_cache.get_obj(child_id)

                if child_node is not None:
                    new_children.append(child_node)
                else:
                    new_children.append(self.get_node(child_id))

            self.child_cache[node.uuid] = sorted(new_children, key=lambda x: x.index)
            self.child_id_cache[node.uuid] = set(child_ids)

        return self.child_cache[node.uuid]

    def update_node(self, node):
        # We need to also update the parent
        self.node_parent_cache[node.uuid] = node._parent_uuid

        self._underlying_persistence.update_node(node)

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
        self._underlying_persistence.remove_feature(node, feature_type, name)
        new_features = [i for i in features if not (i.feature_type == feature_type and i.name == name)]
        self.feature_cache[node.uuid] = new_features
        self.node_cache.add_obj(node)

    def get_features(self, node):

        if node.uuid not in self.feature_cache:
            features = self._underlying_persistence.get_features(node)
            self.feature_cache[node.uuid] = features

        return self.feature_cache[node.uuid]

    def add_feature(self, node, feature):

        if node.uuid not in self.feature_cache:
            features = self._underlying_persistence.get_features(node)
            self.feature_cache[node.uuid] = features

        self.node_cache.add_obj(node)
        self.feature_cache[node.uuid].append(feature)
