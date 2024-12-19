import dataclasses
import logging
import pathlib
import sqlite3
import tempfile
import time
import uuid
from typing import List, Optional

import msgpack

from kodexa.model import Document, ContentNode, SourceMetadata
from kodexa.model.model import (
    DocumentMetadata,
    ContentFeature,
    ContentException,
    ModelInsight, ProcessingStep,
)
from kodexa.model.objects import DocumentTaxonValidation

logger = logging.getLogger()

# Heavily used SQL
EXCEPTION_INSERT = "INSERT INTO content_exceptions (tag, message, exception_details, group_uuid, tag_uuid, exception_type, severity, node_uuid, exception_type_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
EXCEPTION_SELECT = "select tag, message, exception_details, group_uuid, tag_uuid, exception_type, severity, node_uuid, exception_type_id from content_exceptions"

MODEL_INSIGHT_INSERT = "INSERT INTO model_insights (model_insight) VALUES (?)"
MODEL_INSIGHT_SELECT = "select model_insight from model_insights"

FEATURE_INSERT = "INSERT INTO ft (id, cn_id, f_type, binary_value, single, tag_uuid) VALUES (?,?,?,?,?,?)"
FEATURE_DELETE = "DELETE FROM ft where cn_id=? and f_type=?"

CONTENT_NODE_INSERT = "INSERT INTO cn (pid, nt, idx) VALUES (?,?,?)"
CONTENT_NODE_UPDATE = "UPDATE cn set pid=?, nt=?, idx=? WHERE id=?"

CONTENT_NODE_PART_INSERT = (
    "INSERT INTO cnp (cn_id, pos, content, content_idx) VALUES (?,?,?,?)"
)
NOTE_TYPE_INSERT = "insert into n_type(name) values (?)"
NODE_TYPE_LOOKUP = "select id from n_type where name = ?"
FEATURE_TYPE_INSERT = "insert into f_type(name) values (?)"
FEATURE_TYPE_LOOKUP = "select id from f_type where name = ?"
METADATA_INSERT = "insert into metadata(id,metadata) values (1,?)"
METADATA_DELETE = "delete from metadata where id=1"

# Configuration constants
CACHE_SIZE = 10000  # Number of nodes to cache
BATCH_SIZE = 1000   # Size of batches for bulk operations
SLOW_QUERY_THRESHOLD = 1.0  # Seconds
MAX_CONNECTIONS = 5  # Maximum number of database connections

def monitor_performance(func):
    """Performance monitoring decorator"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        if duration > SLOW_QUERY_THRESHOLD:
            logger.warning(f"Slow operation detected: {func.__name__}, duration: {duration}s")
        return result
    return wrapper

class SqliteDocumentPersistence(object):
    """
    The Sqlite persistence engine to support large scale documents (part of the V4 Kodexa Document Architecture)

    Attributes:
        document (Document): The document to be persisted.
        filename (str): The name of the file where the document is stored.
        delete_on_close (bool): If True, the file will be deleted when the connection is closed.
    """

    """
    The Sqlite persistence engine to support large scale documents (part of the V4 Kodexa Document Architecture)
    """

    def __init__(self, document: Document, filename: str = None, delete_on_close=False, inmemory=False, persistence_manager=None):
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

            new_file, filename = tempfile.mkstemp(
                suffix=".kddb", dir=KodexaPlatform.get_tempdir()
            )
            self.is_tmp = True

        self.current_filename = filename

        if inmemory:
            self.inmemory=True
            self.connection = self.create_in_memory_database(filename)
        else:
            self.inmemory=False
            self.connection = sqlite3.connect(filename)

        self.cursor = self.connection.cursor()
        self.cursor.execute("PRAGMA journal_mode=OFF")
        self.cursor.execute("PRAGMA temp_store=MEMORY")
        self.cursor.execute("PRAGMA mmap_size=30000000000")
        self.cursor.execute("PRAGMA cache_size=10000")
        self.cursor.execute("PRAGMA page_size=4096")

        try:
            # We need to populate node_type_id_by_name
            for n_type in self.cursor.execute("select id,name from n_type"):
                self.node_types[n_type[0]] = n_type[1]
                self.node_type_id_by_name[n_type[1]] = n_type[0]
        except:
            pass

    def create_in_memory_database(self, disk_db_path: str):
        # Connect to the in-memory database
        mem_conn = sqlite3.connect(':memory:')
        mem_cursor = mem_conn.cursor()

        # Connect to the database on disk
        disk_conn = sqlite3.connect(disk_db_path)
        disk_cursor = disk_conn.cursor()

        # Load the contents of the disk database into memory
        disk_cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
        tables = disk_cursor.fetchall()
        for table_name, create_table_sql in tables:
            if "sqlite" in table_name:
                continue

            # Create the table structure in the in-memory database
            mem_cursor.execute(create_table_sql)

            # Populate the table with data from the disk database
            disk_cursor.execute(f"SELECT * FROM {table_name}")
            rows = disk_cursor.fetchall()
            for row in rows:
                placeholders = ', '.join('?' * len(row))
                mem_cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", row)

        # Commit changes and close disk connection
        mem_conn.commit()
        disk_conn.close()

        return mem_conn

    @monitor_performance
    def get_all_tags(self):
        """
        Retrieves all tags from the document.

        Returns:
            list: A list of all tags in the document.
        """
        features = []
        for feature in self.cursor.execute(
                "select name from f_type where name like 'tag:%'"
        ).fetchall():
            features.append(feature[0].split(":")[1])

        return features

    @monitor_performance
    def update_features(self, node):
        """
        Updates the features of a given node in the document.

        Args:
            node (Node): The node whose features are to be updated.
        """

        next_feature_id = self.get_max_feature_id()
        all_features = []
        for feature in node.get_features():
            binary_value = sqlite3.Binary(
                msgpack.packb(feature.value, use_bin_type=True)
            )

            tag_uuid = None
            if feature.feature_type == "tag" and "uuid" in feature.value[0]:
                tag_uuid = feature.value[0]["uuid"]

            all_features.append(
                [
                    next_feature_id,
                    node.uuid,
                    self.get_feature_type_id(feature),
                    binary_value,
                    feature.single,
                    tag_uuid,
                ]
            )

            next_feature_id = next_feature_id + 1

        self.cursor.execute("DELETE FROM ft where cn_id=?", [node.uuid])
        self.cursor.executemany(FEATURE_INSERT, all_features)

    @monitor_performance
    def update_node(self, node):
        """
        Updates a given node in the document.

        Args:
            node (Node): The node to be updated.
        """
        self.cursor.execute(
            "update cn set idx=?, pid=? where id=?",
            [node.index, node._parent_uuid, node.uuid],
        )

    @monitor_performance
    def get_content_nodes(self, node_type, parent_node: ContentNode, include_children):
        """
        Retrieves content nodes from the document based on the given parameters.

        Args:
            node_type (str): The type of the node to be retrieved.
            parent_node (ContentNode): The parent node of the nodes to be retrieved.
            include_children (bool): If True, child nodes will also be retrieved.

        Returns:
            list: A list of content nodes that match the given parameters.
        """
        nodes = []
        if not self.connection.in_transaction:
            self.cursor.execute("BEGIN TRANSACTION")
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
                    results = self.cursor.execute(
                        query,
                        [
                            parent_node.uuid,
                            parent_node.get_parent().uuid
                            if parent_node.get_parent()
                            else None,
                            next(
                                key
                                for key, value in self.node_types.items()
                                if value == parent_node.get_node_type()
                            ),
                            parent_node.index,
                            f"{parent_node.index}".zfill(6),
                        ],
                    ).fetchall()
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
                    results = self.cursor.execute(
                        query,
                        [
                            parent_node.uuid,
                            parent_node.get_parent().uuid
                            if parent_node.get_parent()
                            else None,
                            next(
                                key
                                for key, value in self.node_types.items()
                                if value == parent_node.get_node_type()
                            ),
                            parent_node.index,
                            f"{parent_node.index}".zfill(6),
                            next(
                                key
                                for key, value in self.node_types.items()
                                if value == node_type
                            ),
                        ],
                    ).fetchall()
                except StopIteration:
                    self.connection.commit()
                    return []
        else:
            query = "select id, pid, nt, idx from cn where pid=? and nt=? order by idx"
            try:
                results = self.cursor.execute(
                    query,
                    [
                        parent_node.uuid,
                        next(
                            key
                            for key, value in self.node_types.items()
                            if value == node_type
                        ),
                    ],
                ).fetchall()
            except StopIteration:
                self.connection.commit()
                return []

        for raw_node in list(results):
            nodes.append(self.__build_node(raw_node))

        self.connection.commit()

        return nodes

    def initialize(self):
        """
        Initializes the SqliteDocumentPersistence object by either building a new database or loading an existing one.
        """
        if self.is_new:
            self.__build_db()
        else:
            self.__load_document()

    def close(self):
        """
        Closes the connection to the database. If delete_on_close is True, the file will also be deleted.
        """
        if self.is_tmp or self.delete_on_close:
            pathlib.Path(self.current_filename).unlink()
        else:
            self.cursor.close()
            self.connection.close()

    @monitor_performance
    def get_max_feature_id(self):
        """
        Retrieves the maximum feature id from the document.

        Returns:
            int: The maximum feature id.
        """
        max_id = self.cursor.execute("select max(id) from ft").fetchone()
        if max_id[0] is None:
            return 1

        return max_id[0] + 1

    def __build_db(self):
        """
        Builds a new database for the document.
        """
        self.cursor.execute(
            "CREATE TABLE metadata (id integer primary key, metadata text)"
        )
        self.cursor.execute(
            "CREATE TABLE cn (id integer primary key, nt INTEGER, pid INTEGER, idx INTEGER)"
        )
        self.cursor.execute(
            "CREATE TABLE cnp (id integer primary key, cn_id INTEGER, pos integer, content text, content_idx integer)"
        )

        self.cursor.execute("CREATE TABLE n_type (id integer primary key, name text)")
        self.cursor.execute("CREATE TABLE f_type (id integer primary key, name text)")
        self.cursor.execute(
            """CREATE TABLE ft
                                    (
                                        id           integer primary key,
                                        cn_id        integer,
                                        f_type       INTEGER,
                                        binary_value blob,
                                        single       integer,
                                        tag_uuid     text
                                    )"""
        )

        self.cursor.execute("CREATE UNIQUE INDEX n_type_uk ON n_type(name);")
        self.cursor.execute("CREATE UNIQUE INDEX f_type_uk ON f_type(name);")
        self.cursor.execute("CREATE INDEX cn_perf ON cn(nt);")
        self.cursor.execute("CREATE INDEX cn_perf2 ON cn(pid);")
        self.cursor.execute("CREATE INDEX cnp_perf ON cnp(cn_id, pos);")
        self.cursor.execute("CREATE INDEX f_perf ON ft(cn_id);")
        self.cursor.execute("CREATE INDEX f_perf2 ON ft(tag_uuid);")
        self.cursor.execute(
            """CREATE TABLE content_exceptions
                                    (
                                        id           integer primary key,
                                        tag          text,
                                        message      text,
                                        exception_details text,
                                        group_uuid   text,
                                        tag_uuid     text,
                                        exception_type text,
                                        exception_type_id text,
                                        severity     text,
                                        node_uuid    text
                                    )"""
        )
        self.cursor.execute(
            "CREATE TABLE model_insights (id integer primary key,model_insight text);"
        )
        self.document.version = "6.0.0"

        self.__update_metadata()

    @monitor_performance
    def content_node_count(self):
        """
        Counts the number of content nodes in the document.

        Returns:
            int: The number of content nodes in the document.
        """
        self.cursor.execute("select * from cn").fetchall()

    @monitor_performance
    def get_feature_type_id(self, feature):
        """
        Retrieves the id of a given feature.

        Args:
            feature (Feature): The feature whose id is to be retrieved.

        Returns:
            int: The id of the feature.
        """
        return self.__resolve_f_type(feature)

    def __resolve_f_type(self, feature):
        """
        Resolves the feature type of a given feature.

        Args:
            feature (Feature): The feature whose feature type is to be resolved.

        Returns:
            int: The id of the feature type.
        """
        feature_type_name = feature.feature_type + ":" + feature.name

        if feature_type_name in self.feature_type_id_by_name:
            return self.feature_type_id_by_name[feature_type_name]

        result = self.cursor.execute(
            FEATURE_TYPE_LOOKUP, [feature_type_name]
        ).fetchone()
        if result is None:
            new_feature_type_name_id = self.cursor.execute(
                FEATURE_TYPE_INSERT, [feature_type_name]
            ).lastrowid
            self.feature_type_names[new_feature_type_name_id] = feature_type_name
            self.feature_type_id_by_name[feature_type_name] = new_feature_type_name_id
            return new_feature_type_name_id

        return result[0]

    def __resolve_n_type(self, n_type):
        """
        Resolves the node type of a given node.

        Args:
            n_type (str): The node type to be resolved.

        Returns:
            int: The id of the node type.
        """
        if n_type in self.node_type_id_by_name:
            return self.node_type_id_by_name[n_type]
        result = self.cursor.execute(NODE_TYPE_LOOKUP, [n_type]).fetchone()
        if result is None:
            new_type_id = self.cursor.execute(NOTE_TYPE_INSERT, [n_type]).lastrowid
            self.node_types[new_type_id] = n_type
            self.node_type_id_by_name[n_type] = new_type_id
            return new_type_id

        return result[0]

    @monitor_performance
    def __insert_node(self, node: ContentNode, parent, execute=True):
        """
        Inserts a node into the document.

        Args:
            node (ContentNode): The node to be inserted.
            parent (Node): The parent node of the node to be inserted.
            execute (bool, optional): If True, the node will be inserted immediately. Defaults to True.

        Returns:
            tuple: A tuple containing the values of the node and its parts.
        """

        if node.index is None:
            node.index = 0

        if parent:
            node._parent_uuid = parent.uuid

        if node.uuid:
            # Delete the existing node
            cn_values = [
                node._parent_uuid,
                self.__resolve_n_type(node.node_type),
                node.index,
                node.uuid,
            ]

            # Make sure we load the content parts if we haven't
            node.get_content_parts()

            if execute:
                self.cursor.execute("DELETE FROM cn where id=?", [node.uuid])
                self.cursor.execute(
                    "INSERT INTO cn (pid, nt, idx, id) VALUES (?,?,?,?)", cn_values
                )
                self.cursor.execute("DELETE FROM cnp where cn_id=?", [node.uuid])

            cn_parts_values = []
            for idx, part in enumerate(node.get_content_parts()):
                cn_parts_values.append(
                    [
                        node.uuid,
                        idx,
                        part if isinstance(part, str) else None,
                        part if not isinstance(part, str) else None,
                    ]
                )

            if execute:
                self.cursor.executemany(CONTENT_NODE_PART_INSERT, cn_parts_values)

            return ([cn_values], cn_parts_values)

        raise Exception("Node must have a UUID?")

    def __clean_none_values(self, d):
        """
        Cleans a dictionary by removing keys with None values.

        Args:
            d (dict): The dictionary to be cleaned.

        Returns:
            dict: The cleaned dictionary.
        """
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
        """
        Updates the metadata of the document.
        """
        document_metadata = {
            "version": Document.CURRENT_VERSION,
            "metadata": self.document.metadata,
            "source": self.__clean_none_values(
                dataclasses.asdict(self.document.source)
            ),
            "mixins": self.document.get_mixins(),
            "labels": self.document.labels,
            "uuid": self.document.uuid,
        }
        self.cursor.execute(METADATA_DELETE)
        self.cursor.execute(
            METADATA_INSERT,
            [sqlite3.Binary(msgpack.packb(document_metadata, use_bin_type=True))],
        )

    def __load_document(self):
        """
        Loads an existing document from the database.
        """
        for n_type in self.cursor.execute("select id,name from n_type"):
            self.node_types[n_type[0]] = n_type[1]
        for f_type in self.cursor.execute("select id,name from f_type"):
            self.feature_type_names[f_type[0]] = f_type[1]

        metadata = msgpack.unpackb(
            self.cursor.execute("select * from metadata").fetchone()[1]
        )
        self.document.metadata = DocumentMetadata(metadata["metadata"])
        self.document.version = (
            metadata["version"]
            if "version" in metadata and metadata["version"]
            else Document.PREVIOUS_VERSION
        )
        # some older docs don't have a version or it's None

        self.uuid = (
            metadata["uuid"]
            if "uuid" in metadata
            else str(uuid.uuid5(uuid.NAMESPACE_DNS, "kodexa.com"))
        )
        if "source" in metadata and metadata["source"]:
            self.document.source = SourceMetadata.from_dict(metadata["source"])
        if "labels" in metadata and metadata["labels"]:
            self.document.labels = metadata["labels"]
        if "mixins" in metadata and metadata["mixins"]:
            self.document._mixins = metadata["mixins"]

        self.uuid = metadata.get("uuid")

        import semver

        root_node = self.cursor.execute(
            "select id, pid, nt, idx from cn where pid is null"
        ).fetchone()
        if root_node:
            self.document.content_node = self.__build_node(root_node)

        if semver.compare(self.document.version, "4.0.1") < 0:
            # We need to migrate this to a 4.0.1 document
            self.cursor.execute(
                """CREATE TABLE ft
                                    (
                                        id           integer primary key,
                                        cn_id        integer,
                                        f_type       INTEGER,
                                        binary_value blob,
                                        single       integer,
                                        tag_uuid     text
                                    )"""
            )
            self.cursor.execute(
                "insert into ft select f.id, f.cn_id, f.f_type, fv.binary_value, fv.single, null from f, f_value fv where fv.id = f.fvalue_id"
            )
            # we will create a new feature table
            self.cursor.execute("drop table f")
            self.cursor.execute("drop table f_value")
            self.cursor.execute("CREATE INDEX f_perf ON ft(cn_id);")
            self.cursor.execute("CREATE INDEX f_perf2 ON ft(tag_uuid);")

        # We always run this
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS content_exceptions
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
                                    )"""
        )
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS model_insights
                                    (
                                        id           integer primary key,
                                        model_insight text
                                    )"""
        )

        if semver.compare(self.document.version, "6.0.0") < 0:
            from sqlite3 import OperationalError

            try:
                self.cursor.execute(
                    "ALTER TABLE content_exceptions ADD COLUMN exception_type_id text"
                )
            except OperationalError:
                logger.info("exception_type_id column already exists")
                pass
        self.document.version = "6.0.0"
        self.update_metadata()

    def get_content_parts(self, new_node):
        """
        Retrieves the content parts of a given node.

        Args:
            new_node (Node): The node whose content parts are to be retrieved.

        Returns:
            list: A list of the content parts of the node.
        """
        content_parts = self.cursor.execute(
            "select cn_id, pos, content, content_idx from cnp where cn_id = ? order by pos",
            [new_node.uuid],
        ).fetchall()

        parts = []
        for content_part in content_parts:
            if content_part[3] is None:
                parts.append(content_part[2])
            else:
                parts.append(content_part[3])
        return parts

    def __build_node(self, node_row):
        """
        Builds a node from a given row of the database.

        Args:
            node_row (tuple): A tuple containing the values of the node.

        Returns:
            Node: The built node.
        """
        new_node = ContentNode(
            self.document,
            self.node_types[node_row[2]],
            parent=self.get_node(node_row[1]),
        )
        new_node.uuid = node_row[0]
        new_node.index = node_row[3]
        return new_node

    def add_content_node(self, node, parent, execute=True):
        """
        Adds a content node to the document.

        Args:
            node (Node): The node to be added.
            parent (Node): The parent node of the node to be added.
            execute (bool, optional): If True, the node will be added immediately. Defaults to True.

        Returns:
            tuple: A tuple containing the values of the node and its parts.
        """
        return self.__insert_node(node, parent, execute)

    def remove_feature(self, node, feature_type, name):
        """
        Removes a feature from a given node.

        Args:
            node (Node): The node from which the feature is to be removed.
            feature_type (str): The type of the feature to be removed.
            name (str): The name of the feature to be removed.
        """

        feature = ContentFeature(feature_type, name, None)
        f_values = [node.uuid, self.__resolve_f_type(feature)]
        self.cursor.execute(FEATURE_DELETE, f_values)

    def get_children(self, content_node):
        """
        Retrieves the children of a given node.

        Args:
            content_node (ContentNode): The node whose children are to be retrieved.

        Returns:
            list: A list of the children of the node.
        """

        # We need to get the child nodes
        children = []
        for child_node in self.cursor.execute(
                "select id, pid, nt, idx from cn where pid = ? order by idx",
                [content_node.uuid],
        ).fetchall():
            children.append(self.__build_node(child_node))
        return children

    def get_child_ids(self, content_node):
        """
        Retrieves the ids of the children of a given node.

        Args:
            content_node (ContentNode): The node whose children's ids are to be retrieved.

        Returns:
            list: A list of the ids of the children of the node.
        """

        # We need to get the child nodes
        children = []
        for child_node in self.cursor.execute(
                "select id, pid, nt, idx from cn where pid = ? order by idx",
                [content_node.uuid],
        ).fetchall():
            children.append(child_node[0])
        return children

    def get_node(self, node_id):
        """
        Retrieves a node by its id.

        Args:
            node_id (int): The id of the node to be retrieved.

        Returns:
            Node: The node with the given id.
        """
        node_row = self.cursor.execute(
            "select id, pid, nt, idx from cn where id = ?", [node_id]
        ).fetchone()
        if node_row:
            return self.__build_node(node_row)

        return None

    def get_parent(self, content_node):
        """
        Retrieves the parent of a given node.

        Args:
            content_node (ContentNode): The node whose parent is to be retrieved.

        Returns:
            Node: The parent of the node.
        """

        parent = self.cursor.execute(
            "select pid from cn where id = ?", [content_node.uuid]
        ).fetchone()
        if parent:
            return self.get_node(parent[0])

        return None

    def update_metadata(self):
        """
        Updates the metadata of the document.
        """
        self.__update_metadata()

    def __rebuild_from_document(self):
        """
        Rebuilds the database from the document.
        """
        self.cursor.execute("DELETE FROM cn")
        self.cursor.execute("DELETE FROM cnp")
        self.cursor.execute("DELETE FROM ft")

        self.__update_metadata()
        if self.document.content_node:
            self.__insert_node(self.document.content_node, None)

    def sync(self):
        """
        Synchronizes the database with the document.
        """
        self.__update_metadata()
        self.cursor.execute("pragma optimize")
        self.connection.commit()
        self.cursor.execute("VACUUM")
        self.cursor = self.connection.cursor()
        self.cursor.execute("PRAGMA journal_mode=OFF")
        self.cursor.execute("PRAGMA temp_store=MEMORY")
        self.cursor.execute("PRAGMA mmap_size=30000000000")
        self.cursor.execute("PRAGMA cache_size=10000")
        self.cursor.execute("PRAGMA page_size=4096")

    def dump_in_memory_db_to_file(self):
        # Connect to a new or existing database file
        disk_conn = sqlite3.connect(self.current_filename)

        # Use the backup API to copy the in-memory database to the disk file
        with disk_conn:
            self.connection.backup(disk_conn)

        # Close the file-based database connection
        disk_conn.close()

    def get_bytes(self):
        """
        Retrieves the document as bytes.

        Returns:
            bytes: The document as bytes.
        """
        self.sync()

        if self.inmemory:
            self.dump_in_memory_db_to_file()

        with open(self.current_filename, "rb") as f:
            return f.read()

    def get_features(self, node):
        """
        Retrieves the features of a given node.

        Args:
            node (Node): The node whose features are to be retrieved.

        Returns:
            list: A list of the features of the node.
        """
        # We need to get the features back

        features = []
        for feature in self.cursor.execute(
                "select id, cn_id, f_type, binary_value, single from ft where cn_id = ?",
                [node.uuid],
        ).fetchall():
            feature_type_name = self.feature_type_names[feature[2]]
            single = feature[4] == 1
            value = msgpack.unpackb(feature[3])
            features.append(
                ContentFeature(
                    feature_type_name.split(":")[0],
                    feature_type_name.split(":")[1],
                    value,
                    single=single,
                )
            )

        return features

    def update_content_parts(self, node, content_parts):
        """
        Updates the content parts of a given node.

        Args:
            node (Node): The node whose content parts are to be updated.
            content_parts (list): The new content parts of the node.
        """
        self.cursor.execute("delete from cnp where cn_id=?", [node.uuid])

        all_parts = []
        for idx, part in enumerate(content_parts):
            all_parts.append(
                [
                    node.uuid,
                    idx,
                    part if isinstance(part, str) else None,
                    part if not isinstance(part, str) else None,
                ]
            )
        self.cursor.executemany(CONTENT_NODE_PART_INSERT, all_parts)

    def remove_content_node(self, node):
        """
        Removes a node from the document.

        Args:
            node (Node): The node to be removed.
        """

        def get_all_node_ids(node):
            """
            This function recursively traverses a node tree, collecting the ids of all non-virtual nodes.
            """
            all_node_ids = []
            if not node.virtual:
                all_node_ids.append(node.uuid)  # Append the uuid directly, not as a list
                for child in node.get_children():
                    all_node_ids.extend(get_all_node_ids(child))
            return all_node_ids

        all_child_ids = get_all_node_ids(node)
        parameter_tuples = [(id,) for id in all_child_ids]  # Prepare the parameters as tuples

        # Assuming `self.cursor` is part of a larger transaction management system
        try:
            self.cursor.executemany("delete from cnp where cn_id=?", parameter_tuples)
            self.cursor.executemany("delete from cn where id=?", parameter_tuples)
            self.cursor.executemany("delete from ft where cn_id=?", parameter_tuples)
            self.connection.commit()  # Commit the transaction if part of one
            return all_child_ids
        except Exception as e:
            self.connection.rollback()  # Rollback in case of error
            logger.error(f"An error occurred: {e}")

    def remove_all_features(self, node):
        """
        Removes all features from a given node.

        Args:
            node (Node): The node from which all features are to be removed.
        """
        self.cursor.execute("delete from ft where cn_id=?", [node.uuid])

    def remove_all_features_by_id(self, node_id):
        """
        Removes all features from a node by its id.

        Args:
            node_id (int): The id of the node from which all features are to be removed.
        """
        self.cursor.execute("delete from ft where cn_id=?", [node_id])

    def get_next_node_id(self):
        """
        Retrieves the next node id from the document.

        Returns:
            int: The next node id.
        """
        next_id = self.cursor.execute("select max(id) from cn").fetchone()
        if next_id[0] is None:
            return 1

        return next_id[0] + 1

    def get_tagged_nodes(self, tag, tag_uuid=None):
        """
        Retrieves nodes with a given tag.

        Args:
            tag (str): The tag of the nodes to be retrieved.
            tag_uuid (str, optional): The uuid of the tag. Defaults to None.

        Returns:
            list: A list of nodes with the given tag.
        """
        content_nodes = []
        if tag_uuid is None:
            query = f"select distinct(cn_id) from ft where f_type in (select id from f_type where name like 'tag:{tag}')"
        else:
            query = f"select distinct(cn_id) from ft where f_type in (select id from f_type where name like 'tag:{tag}') and tag_uuid = '{tag_uuid}'"
        for content_node_ids in self.cursor.execute(query).fetchall():
            content_nodes.append(self.get_node(content_node_ids[0]))

        return content_nodes

    def add_model_insight(self, model_insights: ModelInsight):
        """
        Adds a model insight to the document.

        Args:
            model_insights (ModelInsight): The model insight to be added.
        """
        self.cursor.execute(MODEL_INSIGHT_INSERT, [model_insights.json()])

    def get_model_insights(self) -> List[ModelInsight]:
        """
        Retrieves all model insights from the document.

        Returns:
            list: A list of all model insights in the document.
        """
        model_insights = []
        for model_insight in self.cursor.execute(MODEL_INSIGHT_SELECT).fetchall():
            model_insights.append(ModelInsight.parse_raw(model_insight[0]))

        return model_insights

    def add_exception(self, exception: ContentException):
        """
        Adds an exception to the document.

        Args:
            exception (ContentException): The exception to be added.
        """
        # Add an exception to the exception table
        self.cursor.execute(
            EXCEPTION_INSERT,
            [
                exception.tag,
                exception.message,
                exception.exception_details,
                exception.group_uuid,
                exception.tag_uuid,
                exception.exception_type,
                exception.severity,
                exception.node_uuid,
                exception.exception_type_id,
            ],
        )

    def get_exceptions(self) -> List[ContentException]:
        """
        Retrieves all exceptions from the document.

        Returns:
            list: A list of all exceptions in the document.
        """
        exceptions = []
        for exception in self.cursor.execute(EXCEPTION_SELECT).fetchall():
            exceptions.append(
                ContentException(
                    tag=exception[0],
                    message=exception[1],
                    exception_details=exception[2],
                    group_uuid=exception[3],
                    tag_uuid=exception[4],
                    exception_type=exception[5],
                    severity=exception[6],
                    node_uuid=exception[7],
                    exception_type_id=exception[8],
                )
            )
        return exceptions

    def replace_exceptions(self, exceptions: List[ContentException]):
        """
        Replaces all exceptions in the document with a given list of exceptions.

        Args:
            exceptions (list): The new list of exceptions.
        """
        self.cursor.execute("delete from content_exceptions")
        for exception in exceptions:
            self.add_exception(exception)

    def clear_model_insights(self):
        """
        Clears all model insights from the document.
        """
        self.cursor.execute("delete from model_insights")

    def get_all_tagged_nodes(self):
        """
        Retrieves all nodes with tags from the document.

        Returns:
            list: A list of all nodes with tags in the document.
        """
        content_nodes = []
        query = "select distinct(cn_id) from ft where f_type in (select id from f_type where name like 'tag:%')"
        for content_node_ids in self.cursor.execute(query).fetchall():
            content_nodes.append(self.get_node(content_node_ids[0]))

        return content_nodes

    def get_nodes_by_type(self, node_type):
        """
        Retrieves nodes of a given type from the document.

        Args:
            node_type (str): The type of the nodes to be retrieved.

        Returns:
            list: A list of nodes of the given type.
        """
        content_nodes = []

        node_type_id = self.node_type_id_by_name.get(node_type)

        query = "select id, pid, nt, idx from cn where nt = ? order by idx"
        for content_node in self.cursor.execute(query, [node_type_id]).fetchall():
            content_nodes.append(self.__build_node(content_node))

        return content_nodes

    def __ensure_validations_table_exists(self):
        """
        Ensure the 'validations' table exists in the database.
        Creates the table if it does not exist and initializes it with an empty list.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS validations (
                obj BLOB
            )
        """)

        # Check if the table has any rows, if not, insert an initial empty row
        result = self.cursor.execute("SELECT COUNT(*) FROM validations").fetchone()
        if result[0] == 0:
            self.cursor.execute("INSERT INTO validations (obj) VALUES (?)", [sqlite3.Binary(msgpack.packb([]))])

    def set_validations(self, validations: List[DocumentTaxonValidation]):
        """
        Sets the validations for the document.

        Args:
            validations (List[DocumentTaxonValidation]): The validations to store.
        """
        self.__ensure_validations_table_exists()
        serialized_data = sqlite3.Binary(msgpack.packb([v.model_dump(by_alias=True) for v in validations]))
        self.cursor.execute("UPDATE validations SET obj = ? WHERE rowid = 1", [serialized_data])
        self.connection.commit()

    def get_validations(self) -> List[DocumentTaxonValidation]:
        """
        Gets the validations associated with this document.

        Returns:
            List[DocumentTaxonValidation]: The list of validations stored in the validations table.
        """
        self.__ensure_validations_table_exists()
        result = self.cursor.execute("SELECT obj FROM validations WHERE rowid = 1").fetchone()
        if result and result[0]:
            return [DocumentTaxonValidation.model_validate(v) for v in msgpack.unpackb(result[0])]
        return []

    def set_external_data(self, external_data: dict, key: str = "default"):
        """
        Sets the external data for the document for a specific key.

        Args:
            external_data (dict): The external data to store, must be JSON serializable.
            key (str): The key to store the data under, defaults to "default"
        """
        self.__ensure_ed_table_exists()
        serialized_data = sqlite3.Binary(msgpack.packb(external_data))
        self.cursor.execute("DELETE FROM ed WHERE key = ?", [key])
        self.cursor.execute("INSERT INTO ed (key, obj) VALUES (?, ?)", [key, serialized_data])
        self.connection.commit()

    def get_external_data(self, key: str = "default") -> dict:
        """
        Gets the external data associated with this document for a specific key.

        Args:
            key (str): The key to retrieve data for, defaults to "default"

        Returns:
            dict: The external data stored in the ed table for the given key.
        """
        self.__ensure_ed_table_exists()
        result = self.cursor.execute("SELECT obj FROM ed WHERE key = ?", [key]).fetchone()
        if result and result[0]:
            return msgpack.unpackb(result[0])
        return {}

    def get_external_data_keys(self) -> List[str]:
        """
        Gets all keys under which external data is stored.

        Returns:
            List[str]: A list of all keys that have external data stored.
        """
        self.__ensure_ed_table_exists()
        results = self.cursor.execute("SELECT key FROM ed").fetchall()
        return [row[0] for row in results]

    def __ensure_ed_table_exists(self):
        """
        Ensure the 'ed' table exists in the database.
        Creates the table if it does not exist.
        """
        # First check if the old table exists and has key column
        old_table = self.cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='ed'
        """).fetchone()

        if old_table:
            # Check if table has key column
            table_info = self.cursor.execute("PRAGMA table_info(ed)").fetchall()
            has_key_column = any(col[1] == 'key' for col in table_info)

            if not has_key_column:
                # Get the old data and drop the table
                data = self.cursor.execute("SELECT obj FROM ed").fetchone()
                self.cursor.execute("DROP TABLE ed")

                # Create new table with key column
                self.cursor.execute("""
                    CREATE TABLE ed (
                        key TEXT PRIMARY KEY,
                        obj BLOB
                    )
                """)

                # If there was data in the old table, insert it with default key
                if data:
                    self.cursor.execute("INSERT INTO ed (key, obj) VALUES (?, ?)",
                                      ["default", data[0]])
            else:
                # Table exists and has key column - do nothing
                return
        else:
            # Create new table if it doesn't exist
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS ed (
                    key TEXT PRIMARY KEY,
                    obj BLOB
                )
            """)

            # Check if default key exists, if not insert empty data
            result = self.cursor.execute("SELECT COUNT(*) FROM ed WHERE key = 'default'").fetchone()
            if result[0] == 0:
                self.cursor.execute("INSERT INTO ed (key, obj) VALUES (?, ?)",
                                  ["default", sqlite3.Binary(msgpack.packb({}))])

    def __ensure_steps_table_exists(self):
        """
        Ensure the 'steps' table exists in the database.
        Creates the table if it does not exist.
        """
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS steps (
                    obj BLOB
                )
            """)

        # Check if the table has any rows, if not, insert an initial empty row
        result = self.cursor.execute("SELECT COUNT(*) FROM steps").fetchone()
        if result[0] == 0:
            self.cursor.execute("INSERT INTO steps (obj) VALUES (?)", [sqlite3.Binary(msgpack.packb([]))])

    def set_steps(self, steps: List[ProcessingStep]):
        """
        Sets the processing steps for the document.

        Args:
            steps (List[ProcessingStep]): A list of ProcessingStep objects to store.
        """
        self.__ensure_steps_table_exists()
        serialized_steps = [step.to_dict() for step in steps]
        packed_data = sqlite3.Binary(msgpack.packb(serialized_steps))
        self.cursor.execute("UPDATE steps SET obj = ? WHERE rowid = 1", [packed_data])
        self.connection.commit()

    def get_steps(self) -> List[ProcessingStep]:
        """
        Gets the processing steps associated with this document.

        Returns:
            List[ProcessingStep]: A list of ProcessingStep objects.
        """
        self.__ensure_steps_table_exists()
        result = self.cursor.execute("SELECT obj FROM steps WHERE rowid = 1").fetchone()
        if result and result[0]:
            unpacked_data = msgpack.unpackb(result[0])
            return [ProcessingStep(**step) for step in unpacked_data]
        return []


class SimpleObjectCache(object):
    """
    A simple cache based on ID'd objects, where we will build ID's for new
    objects, store them and also a dirty flag so that it is easy to pull all
    dirty objects and store them as needed.
    """

    """
    A simple cache based on ID'd objects, where we will build ID's for new
    objects, store them and also a dirty flag so that it is easy to pull all
    dirty objects and store them as needed.
    """
    """
    A simple cache based on ID'd objects, where we will build ID's for new
    objects, store them and also a dirty flag so that it is easy to pull all
    dirty objects and store them as needed
    """

    def __init__(self):
        self.objs = {}
        self.next_id = 1
        self.dirty_objs = set()

    def get_obj(self, obj_id) -> Optional[ContentNode]:
        """
        Get the object with the given ID.

        Args:
            obj_id (int): The ID of the object.

        Returns:
            object: The object with the given ID if it exists, None otherwise.
        """
        if obj_id in self.objs:
            return self.objs[obj_id]

        return None

    def add_obj(self, obj: ContentNode):
        """
        Add an object to the cache.

        Args:
            obj (object): The object to add. If the object does not have a uuid, one will be assigned.
        """
        if obj.uuid is None:
            obj.uuid = self.next_id
            self.next_id += 1
        self.objs[obj.uuid] = obj
        self.dirty_objs.add(obj.uuid)

    def remove_obj(self, obj: ContentNode):
        """
        Remove an object from the cache.

        Args:
            obj (object): The object to remove.
        """
        if obj and obj.uuid in self.objs:
            self.objs.pop(obj.uuid)
            if obj.uuid in self.dirty_objs:
                self.dirty_objs.remove(obj.uuid)

    def get_dirty_objs(self) -> list[ContentNode]:
        """
        Get all dirty objects in the cache.

        Returns:
            list: A list of all dirty objects in the cache.
        """
        results = []
        for set_id in set(self.dirty_objs):
            node = self.get_obj(set_id)
            if node is not None:
                results.append(node)
        return results

    def undirty(self, obj):
        """
        Mark an object as not dirty.

        Args:
            obj (object): The object to mark as not dirty.
        """
        self.dirty_objs.remove(obj.uuid)


class PersistenceManager(object):
    """
    The persistence manager supports holding the document and only flushing objects to the persistence layer
    as needed. This is implemented to allow us to work with large complex documents in a performance centered way.

    Attributes:
        document (Document): The document to be managed.
        node_cache (SimpleObjectCache): Cache for nodes.
        child_cache (dict): Cache for child nodes.
        child_id_cache (dict): Cache for child node IDs.
        feature_cache (dict): Cache for features.
        content_parts_cache (dict): Cache for content parts.
        node_parent_cache (dict): Cache for node parents.
        _underlying_persistence (SqliteDocumentPersistence): The underlying persistence layer.
    """

    """
    The persistence manager supports holding the document and only flushing objects to the persistence layer
    as needed. This is implemented to allow us to work with large complex documents in a performance centered way.

    Attributes:
        document (Document): The document to be managed.
        node_cache (SimpleObjectCache): Cache for nodes.
        child_cache (dict): Cache for child nodes.
        child_id_cache (dict): Cache for child node IDs.
        feature_cache (dict): Cache for features.
        content_parts_cache (dict): Cache for content parts.
        node_parent_cache (dict): Cache for node parents.
        _underlying_persistence (SqliteDocumentPersistence): The underlying persistence layer.
    """
    """
    The persistence manager supports holding the document and only flushing objects to the persistence layer
    as needed.

    This is implemented to allow us to work with large complex documents in a performance centered way.
    """

    def __init__(self, document: Document, filename: str = None, delete_on_close=False, inmemory=False):
        self.document = document
        self.node_cache = SimpleObjectCache()
        self.child_cache = {}
        self.child_id_cache = {}
        self.feature_cache = {}
        self.content_parts_cache = {}
        self.node_parent_cache = {}

        self._underlying_persistence = SqliteDocumentPersistence(
            document, filename, delete_on_close, inmemory=inmemory, persistence_manager=self
        )

    def get_steps(self) -> list[ProcessingStep]:
        """
        Gets the processing steps for this document

        :return:
        """
        return self._underlying_persistence.get_steps()

    def set_steps(self, steps: list[ProcessingStep]):
        self._underlying_persistence.set_steps(steps)

    def set_validations(self, validations: list[DocumentTaxonValidation]):
        self._underlying_persistence.set_validations(validations)

    def get_validations(self) -> list[DocumentTaxonValidation]:
        return self._underlying_persistence.get_validations()

    def get_external_data(self, key="default") -> dict:
        """
        Gets the external data object associated with this document

        :return: dict of the external data
        """
        return self._underlying_persistence.get_external_data(key)

    def get_external_data_keys(self) -> List[str]:
        """
        Gets all keys under which external data is stored.

        Returns:
            List[str]: A list of all keys that have external data stored.
        """
        return self._underlying_persistence.get_external_data_keys()

    def set_external_data(self, external_data:dict, key="default"):
        """
        Sets the external data for this document

        :param external_data: dict representing the external data, must be JSON serializable
        :return:
        """
        self._underlying_persistence.set_external_data(external_data, key)

    def get_nodes_by_type(self, node_type: str) -> List[ContentNode]:
        """
        Retrieves all nodes of a given type from the underlying persistence layer.

        Args:
            node_type (str): The type of the nodes to be retrieved.

        Returns:
            List[ContentNode]: A list of all nodes of the given type.
        """
        return self._underlying_persistence.get_nodes_by_type(node_type)

    def get_node_by_uuid(self, uuid: int) -> ContentNode:
        """
        Retrieves a node by its uuid.

        Args:
            uuid (str): The uuid of the node to be retrieved.

        Returns:
            ContentNode: The node with the given uuid.
        """
        if self.node_cache.get_obj(uuid) is None:
            node = self._underlying_persistence.get_node(uuid)
            if node:
                self.node_cache.add_obj(node)
                return node

        return self.node_cache.get_obj(uuid) # return the cached version

    def add_model_insight(self, model_insight: ModelInsight):
        """
        Adds a model insight to the underlying persistence layer.

        Args:
            model_insight (ModelInsight): The model insight to be added.
        """
        self._underlying_persistence.add_model_insight(model_insight)

    def clear_model_insights(self):
        """
        Clears all model insights from the underlying persistence layer.
        """
        self._underlying_persistence.clear_model_insights()

    def get_model_insights(self) -> List[ModelInsight]:
        """
        Retrieves all model insights from the underlying persistence layer.

        Returns:
            List[ModelInsight]: A list of all model insights.
        """
        return self._underlying_persistence.get_model_insights()

    def add_exception(self, exception: ContentException):
        """
        Adds an exception to the underlying persistence layer.

        Args:
            exception (ContentException): The exception to be added.
        """
        self._underlying_persistence.add_exception(exception)

    def get_exceptions(self) -> List[ContentException]:
        """
        Retrieves all exceptions from the underlying persistence layer.

        Returns:
            List[ContentException]: A list of all exceptions.
        """
        return self._underlying_persistence.get_exceptions()

    def replace_exceptions(self, exceptions: List[ContentException]):
        """
        Replaces all exceptions in the underlying persistence layer with the provided list.

        Args:
            exceptions (List[ContentException]): The list of exceptions to replace with.
        """
        self._underlying_persistence.replace_exceptions(exceptions)

    def get_all_tags(self):
        """
        Retrieves all tags from the underlying persistence layer.

        Returns:
            List[str]: A list of all tags.
        """
        return self._underlying_persistence.get_all_tags()

    def get_tagged_nodes(self, tag, tag_uuid=None):
        """
        Retrieves all nodes tagged with the specified tag from the underlying persistence layer.

        Args:
            tag (str): The tag to filter nodes by.
            tag_uuid (str, optional): The UUID of the tag to filter nodes by. Defaults to None.

        Returns:
            List[Node]: A list of nodes tagged with the specified tag.
        """
        return self._underlying_persistence.get_tagged_nodes(tag, tag_uuid)

    def get_all_tagged_nodes(self):
        """
        Retrieves all tagged nodes from the underlying persistence layer.

        Returns:
            List[Node]: A list of all tagged nodes.
        """
        return self._underlying_persistence.get_all_tagged_nodes()

    def initialize(self):
        """
        Initializes the persistence manager by setting up the underlying persistence layer and node cache.
        """
        self._underlying_persistence.initialize()

        self.node_cache.next_id = self._underlying_persistence.get_next_node_id()

    def get_parent(self, node):
        """
        Retrieves the parent of the specified node.

        Args:
            node (Node): The node to get the parent of.

        Returns:
            Node: The parent of the specified node.
        """
        if node.uuid in self.node_parent_cache:
            return self.node_cache.get_obj(self.node_parent_cache[node.uuid])

        return self._underlying_persistence.get_parent(node)

    def close(self):
        """
        Closes the underlying persistence layer.
        """
        self._underlying_persistence.close()

    @monitor_performance
    def flush_cache(self):
        """
        Flushes the cache by merging it with the underlying persistence layer.
        """
        all_node_ids = []
        all_nodes = []
        all_content_parts = []
        all_features = []
        node_id_with_features = []
        dirty_nodes = self.node_cache.get_dirty_objs()

        if len(dirty_nodes) == 0:
            return

        if not self._underlying_persistence.connection.in_transaction:
            self._underlying_persistence.connection.execute("BEGIN TRANSACTION")

        next_feature_id = self._underlying_persistence.get_max_feature_id()
        for node in dirty_nodes:
            if not node.virtual:
                all_node_ids.append([node.uuid])
                node_obj, content_parts = self._underlying_persistence.add_content_node(
                    node, None, execute=False
                )
                all_nodes.extend(node_obj)
                all_content_parts.extend(content_parts)
                if node.uuid in self.feature_cache:
                    if node.uuid in self.feature_cache:
                        node_id_with_features.append([node.uuid])

                    for feature in self.feature_cache[node.uuid]:
                        binary_value = sqlite3.Binary(
                            msgpack.packb(feature.value, use_bin_type=True)
                        )

                        tag_uuid = None
                        if feature.feature_type == "tag" and "uuid" in feature.value[0]:
                            tag_uuid = feature.value[0]["uuid"]

                        all_features.append(
                            [
                                next_feature_id,
                                node.uuid,
                                self._underlying_persistence.get_feature_type_id(
                                    feature
                                ),
                                binary_value,
                                feature.single,
                                tag_uuid,
                            ]
                        )
                        next_feature_id = next_feature_id + 1

                self.node_cache.undirty(node)

        self._underlying_persistence.cursor.executemany(
            "DELETE FROM cn where id=?", all_node_ids
        )
        self._underlying_persistence.cursor.executemany(
            "DELETE FROM ft where cn_id=?", node_id_with_features
        )
        self._underlying_persistence.cursor.executemany(
            "INSERT INTO cn (pid, nt, idx, id) VALUES (?,?,?,?)", all_nodes
        )
        self._underlying_persistence.cursor.executemany(
            "DELETE FROM cnp where cn_id=?", all_node_ids
        )
        self._underlying_persistence.cursor.executemany(
            CONTENT_NODE_PART_INSERT, all_content_parts
        )
        self._underlying_persistence.cursor.executemany(FEATURE_INSERT, all_features)
        self._underlying_persistence.connection.commit()

    def get_content_nodes(self, node_type, parent_node, include_children):
        """
        Retrieves content nodes of the specified type and parent from the underlying persistence layer.

        Args:
            node_type (str): The type of nodes to retrieve.
            parent_node (Node): The parent node to filter nodes by.
            include_children (bool): Whether to include child nodes.

        Returns:
            List[Node]: A list of nodes that match the specified criteria.
        """
        return self._underlying_persistence.get_content_nodes(
            node_type, parent_node, include_children
        )

    def get_bytes(self):
        """
        Retrieves the bytes of the document from the underlying persistence layer.

        Returns:
            bytes: The bytes of the document.
        """
        self.flush_cache()
        self._underlying_persistence.sync()
        return self._underlying_persistence.get_bytes()

    def update_metadata(self):
        """
        Updates the metadata in the underlying persistence layer.
        """
        self._underlying_persistence.update_metadata()

    def add_content_node(self, node, parent):
        """
        Adds a content node to the cache and updates the child and parent caches accordingly.

        Args:
            node (Node): The node to be added.
            parent (Node): The parent of the node to be added.
        """

        if node.index is None:
            node.index = 0

        # Check if the node exists in the DB
        if node.uuid is None:
            node.uuid = self.node_cache.next_id
            self.node_cache.next_id += 1

        if self._underlying_persistence.get_node(node.uuid) is None:
            self._underlying_persistence.add_content_node(node, parent)

        if parent:
            node._parent_uuid = parent.uuid
            self.node_cache.add_obj(parent)

        self.node_cache.add_obj(node)

        update_child_cache = False

        if node.uuid not in self.node_parent_cache:
            self.node_parent_cache[node.uuid] = node._parent_uuid
            update_child_cache = True

        if (
                node.uuid in self.node_parent_cache
                and node._parent_uuid != self.node_parent_cache[node.uuid]
        ):
            # Remove from the old parent
            self.child_id_cache[self.node_parent_cache[node.uuid]].remove(node.uuid)
            self.child_cache[self.node_parent_cache[node.uuid]].remove(node)
            # Add to the new parent
            self.node_parent_cache[node.uuid] = node._parent_uuid
            update_child_cache = True

        if update_child_cache:
            if node._parent_uuid not in self.child_cache:
                self.child_cache[node._parent_uuid] = [node]
                self.child_id_cache[node._parent_uuid] = {node.uuid}
            else:
                if node.uuid not in self.child_id_cache[node._parent_uuid]:
                    self.child_id_cache[node._parent_uuid].add(node.uuid)
                    current_children = self.child_cache[node._parent_uuid]
                    if (
                            len(current_children) == 0
                            or node.index >= current_children[-1].index
                    ):
                        self.child_cache[node._parent_uuid].append(node)
                    else:
                        self.child_cache[node._parent_uuid].append(node)
                        self.child_cache[node._parent_uuid] = sorted(
                            self.child_cache[node._parent_uuid], key=lambda x: x.index
                        )

    def get_node(self, node_id):
        """
        Retrieves a node by its ID from the cache or the underlying persistence layer.

        Args:
            node_id (str): The ID of the node to retrieve.

        Returns:
            Node: The node with the specified ID.
        """

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
        """
        Removes a content node from the cache and the underlying persistence layer.

        Args:
            node (Node): The node to be removed.
        """

        self.node_cache.remove_obj(node)

        if node.uuid in self.node_parent_cache:
            try:
                self.child_cache[self.node_parent_cache[node.uuid]].remove(node)
            except ValueError:
                pass
            except KeyError:
                pass

            # We have a sitation where we seem to fail here?
            try:
                self.child_id_cache[self.node_parent_cache[node.uuid]].remove(node.uuid)
            except ValueError:
                pass
            except KeyError:
                pass
            del self.node_parent_cache[node.uuid]

        self.content_parts_cache.pop(node.uuid, None)
        self.feature_cache.pop(node.uuid, None)

        all_ids = self._underlying_persistence.remove_content_node(node)

        # remove all the ids from the cache
        for id in all_ids:
            tmp_node = self.node_cache.get_obj(id)
            if tmp_node is not None:
                self.node_cache.remove_obj(tmp_node)
            self.node_cache.dirty_objs.remove(id) if id in self.node_cache.dirty_objs else None

    def get_children(self, node):
        """
        Retrieves the children of the specified node from the cache or the underlying persistence layer.

        Args:
            node (Node): The node to get the children of.

        Returns:
            List[Node]: The children of the specified node.
        """
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
        """
        Updates a node in the cache and the underlying persistence layer.

        Args:
            node (Node): The node to be updated.
        """
        # We need to also update the parent
        self.node_parent_cache[node.uuid] = node._parent_uuid

        self._underlying_persistence.update_node(node)

    def update_content_parts(self, node, content_parts):
        """
        Updates the content parts of a node in the cache.

        Args:
            node (Node): The node to update the content parts of.
            content_parts (List[ContentPart]): The new content parts of the node.
        """
        self.content_parts_cache[node.uuid] = content_parts

    def get_content_parts(self, node):
        """
        Retrieves the content parts of a node from the cache or the underlying persistence layer.

        Args:
            node (Node): The node to get the content parts of.

        Returns:
            List[ContentPart]: The content parts of the node.
        """
        if node.uuid is None:
            return []

        cps = (
            self.content_parts_cache[node.uuid]
            if node.uuid in self.content_parts_cache
            else None
        )
        if cps is None:
            cps = self._underlying_persistence.get_content_parts(node)
            if cps is not None:
                self.content_parts_cache[node.uuid] = cps

        return cps

    def remove_feature(self, node, feature_type, name):
        """
        Removes a feature from a node in the cache and the underlying persistence layer.

        Args:
            node (Node): The node to remove the feature from.
            feature_type (str): The type of the feature to remove.
            name (str): The name of the feature to remove.
        """

        features = self.get_features(node)
        self._underlying_persistence.remove_feature(node, feature_type, name)
        new_features = [
            i
            for i in features
            if not (i.feature_type == feature_type and i.name == name)
        ]
        self.feature_cache[node.uuid] = new_features
        self.node_cache.add_obj(node)

    def get_features(self, node):
        """
        Retrieves the features of a node from the cache or the underlying persistence layer.

        Args:
            node (Node): The node to get the features of.

        Returns:
            List[Feature]: The features of the node.
        """

        if node.uuid not in self.feature_cache:
            features = self._underlying_persistence.get_features(node)
            self.feature_cache[node.uuid] = features

        return self.feature_cache[node.uuid]

    def add_feature(self, node, feature):
        """
        Adds a feature to a node in the cache and the underlying persistence layer.

        Args:
            node (Node): The node to add the feature to.
            feature (Feature): The feature to be added.
        """

        if node.uuid not in self.feature_cache:
            features = self._underlying_persistence.get_features(node)
            self.feature_cache[node.uuid] = features

        self.node_cache.add_obj(node)
        self.feature_cache[node.uuid].append(feature)
