import dataclasses
import json
import logging
import pathlib
import sqlite3
import tempfile
import time
import uuid
from typing import List, Optional

import msgpack

from kodexa.model.model import Document, ContentNode, SourceMetadata, ContentFeature, Tag
from kodexa.model.model import (
    DocumentMetadata,
    ContentException,
    ModelInsight, ProcessingStep,
)
from kodexa.model.objects import DocumentTaxonValidation

logger = logging.getLogger()

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
    using Peewee ORM
    """

    def __init__(self, document: Document, filename: str = None, delete_on_close=False, inmemory=False, persistence_manager=None):
        self.document = document
        self.delete_on_close = delete_on_close
        self.is_tmp = False
        self.inmemory = inmemory
        self.filename = filename
        
        if filename is not None:
            self.is_new = not pathlib.Path(filename).exists()
            self.is_tmp = False
            # Create a temporary copy of the file to work with
            from kodexa import KodexaPlatform
            _, newfile = tempfile.mkstemp(suffix=".kddb", dir=KodexaPlatform.get_tempdir())
            if not self.is_new:
                import shutil
                shutil.copy2(filename, newfile)
            filename = newfile
            print(f"Using temporary file: {filename}")
        else:
            from kodexa import KodexaPlatform
            new_file, filename = tempfile.mkstemp(suffix=".kddb", dir=KodexaPlatform.get_tempdir())
            self.is_tmp = True
            self.is_new = True
        
        self.current_filename = filename
        
        from kodexa.model.persistence_models import initialize_database, database
        initialize_database(filename if not inmemory else ':memory:')
        
        self.connection = database
        self.node_type_cache = {}
        self.feature_type_cache = {}

        self.__convert_old_db()

    def initialize(self):
        """
        Initializes the SqliteDocumentPersistence object by either building a new database or loading an existing one.
        """
        if self.is_new:
            self.__build_db()
        else:
            self.__load_document()

    def __check_for_updates(self):
        """
        Checks for updates to the database schema.
        """
        # Check if we have a table called kddb_metadata
        if not self.connection.table_exists('kddb_metadata'):
            # We are going to assume this is the old database and we need to convert it
            print("Converting old database format to new kddb format...")
            self.__convert_old_db()
        
    def __convert_old_db(self):
        """
        Converts the old database to the new database.
        """
        logging.info("Converting old database format to new kddb format...")
        
        # Turn off foreign key constraints during migration
        self.connection.execute_sql("PRAGMA foreign_keys = OFF;")
        
        try:
            with self.connection.atomic():
                # Check if migration is needed
                cursor = self.connection.execute_sql("""
                    SELECT CASE 
                        WHEN EXISTS(SELECT 1 FROM sqlite_master WHERE type='table' AND name='cn') 
                        AND NOT EXISTS(SELECT 1 FROM kddb_content_nodes LIMIT 1)
                        THEN 1 ELSE 0 END AS should_migrate;
                """)
                should_migrate = cursor.fetchone()[0]
                
                if not should_migrate:
                    logging.info("Migration not needed or already done.")
                    return
                
                logging.info("Starting database migration...")
                
                # Create temporary mapping table
                self.connection.execute_sql("""
                    CREATE TEMP TABLE IF NOT EXISTS temp_do_mapping (
                        cn_id INTEGER PRIMARY KEY,
                        do_id INTEGER
                    );
                """)
                
                # Migrate node types (n_type → kddb_node_types)
                self.connection.execute_sql("""
                    INSERT OR IGNORE INTO kddb_node_types (name)
                    SELECT name FROM n_type;
                """)
                
                # Populate the node_type_cache with all node types
                from kodexa.model.persistence_models import NodeType
                for node_type in NodeType.select():
                    self.node_type_cache[node_type.name] = node_type.name
                
                # Migrate feature types (f_type → kddb_feature_types)
                self.connection.execute_sql("""
                    INSERT OR IGNORE INTO kddb_feature_types (name)
                    SELECT name FROM f_type;
                """)
                
                # Create temporary table for node hierarchy
                self.connection.execute_sql("""
                    CREATE TEMP TABLE node_levels (
                        id INTEGER PRIMARY KEY,
                        pid INTEGER,
                        level INTEGER
                    );
                """)
                
                # Insert nodes at each level
                self.connection.execute_sql("""
                    -- First insert root nodes (level 0)
                    INSERT INTO node_levels (id, pid, level)
                    SELECT id, pid, 0
                    FROM cn
                    WHERE pid IS NULL;
                """)
                
                self.connection.execute_sql("""
                    -- Insert level 1 nodes
                    INSERT INTO node_levels (id, pid, level)
                    SELECT c.id, c.pid, 1
                    FROM cn c
                    JOIN node_levels p ON c.pid = p.id
                    WHERE p.level = 0;
                """)
                
                self.connection.execute_sql("""
                    -- Insert level 2 nodes
                    INSERT INTO node_levels (id, pid, level)
                    SELECT c.id, c.pid, 2
                    FROM cn c
                    JOIN node_levels p ON c.pid = p.id
                    WHERE p.level = 1;
                """)
                
                self.connection.execute_sql("""
                    -- Insert level 3 nodes
                    INSERT INTO node_levels (id, pid, level)
                    SELECT c.id, c.pid, 3
                    FROM cn c
                    JOIN node_levels p ON c.pid = p.id
                    WHERE p.level = 2;
                """)
                
                self.connection.execute_sql("""
                    -- Insert level 4 nodes
                    INSERT INTO node_levels (id, pid, level)
                    SELECT c.id, c.pid, 4
                    FROM cn c
                    JOIN node_levels p ON c.pid = p.id
                    WHERE p.level = 3;
                """)
                
                self.connection.execute_sql("""
                    -- Insert level 5 nodes
                    INSERT INTO node_levels (id, pid, level)
                    SELECT c.id, c.pid, 5
                    FROM cn c
                    JOIN node_levels p ON c.pid = p.id
                    WHERE p.level = 4;
                """)
                
                # Create index for faster lookups
                self.connection.execute_sql("""
                    CREATE INDEX node_levels_idx ON node_levels(level, id, pid);
                """)

                # Migrate content nodes
                self.connection.execute_sql("""
                    INSERT INTO kddb_content_nodes (id, parent_id, node_type, content, created, modified, "index")
                    SELECT cn.id, cn.pid, nt.name, CASE WHEN cnp.content IS NOT NULL THEN cnp.content ELSE NULL END, 
                           datetime('now'), datetime('now'), cn.idx
                    FROM cn
                    JOIN n_type nt ON cn.nt = nt.id
                    LEFT JOIN cnp ON cn.id = cnp.cn_id AND cnp.pos = 0;
                """)
                
                # Make sure the content field exists in kddb_content_nodes
                cursor = self.connection.execute_sql("""
                    PRAGMA table_info(kddb_content_nodes);
                """)
                columns = [column[1] for column in cursor.fetchall()]
                
                if 'content' not in columns:
                    self.connection.execute_sql("""
                        ALTER TABLE kddb_content_nodes ADD COLUMN content TEXT;
                    """)
                    
                    # Update content from content parts
                    self.connection.execute_sql("""
                        UPDATE kddb_content_nodes 
                        SET content = (
                            SELECT cnp.content 
                            FROM kddb_content_node_parts cnp 
                            WHERE cnp.content_node_id = kddb_content_nodes.id 
                            AND cnp.pos = 0 
                            AND cnp.content IS NOT NULL
                            LIMIT 1
                        );
                    """)
                
                # Make sure the index field exists in kddb_content_nodes
                if 'index' not in columns:
                    self.connection.execute_sql("""
                        ALTER TABLE kddb_content_nodes ADD COLUMN "index" INTEGER;
                    """)
                    
                    # Update index values if possible (e.g., from data object idx)
                    self.connection.execute_sql("""
                        UPDATE kddb_content_nodes 
                        SET "index" = (
                            SELECT do.idx 
                            FROM kddb_data_objects do 
                            WHERE do.id = kddb_content_nodes.data_object_id
                            LIMIT 1
                        );
                    """)
                
                # Migrate content node parts
                self.connection.execute_sql("""
                    INSERT INTO kddb_content_node_parts (content_node_id, pos, content, content_idx)
                    SELECT cn_id, pos, content, content_idx
                    FROM cnp;
                """)
                
                # Migrate features
                self.connection.execute_sql("""
                    INSERT INTO kddb_features (id, feature_type_id)
                    SELECT ft.id, ft.f_type
                    FROM ft;
                """)

                # Populate the new ContentNodeFeatureLink table
                self.connection.execute_sql("""
                    INSERT INTO kddb_content_node_feature_links (content_node_id, feature_id)
                    SELECT ft.cn_id, ft.id
                    FROM ft
                    WHERE ft.cn_id IS NOT NULL;
                """)
                
                # Migrate feature binary data
                self.connection.execute_sql("""
                    INSERT INTO kddb_feature_blob (feature_id, binary_value)
                    SELECT id, binary_value
                    FROM ft
                    WHERE binary_value IS NOT NULL;
                """)
                
                # Migrate metadata if it exists
                self.connection.execute_sql("""
                    INSERT OR IGNORE INTO kddb_metadata (id, metadata)
                    SELECT id, metadata FROM metadata
                    WHERE EXISTS(SELECT 1 FROM metadata);
                """)
                
                # Convert existing metadata from JSON text to msgpack blob if needed
                try:
                    metadata_record = self.connection.execute_sql("SELECT id, metadata FROM kddb_metadata").fetchone()
                    if metadata_record and metadata_record[1]:
                        # Check if metadata is a JSON string (text) that needs conversion
                        try:
                            # Try to decode as text - if this works, it's the old JSON format
                            metadata_text = metadata_record[1].decode('utf-8')
                            metadata_dict = json.loads(metadata_text)
                            
                            # Convert to msgpack blob
                            metadata_blob = msgpack.packb(metadata_dict, use_bin_type=True)
                            
                            # Update the record with the blob
                            self.connection.execute_sql(
                                "UPDATE kddb_metadata SET metadata = ? WHERE id = ?",
                                (metadata_blob, metadata_record[0])
                            )
                            logging.info("Converted metadata from JSON to msgpack blob format")
                        except (UnicodeDecodeError, json.JSONDecodeError):
                            # If this fails, it's probably already in the new format
                            logging.info("Metadata is already in the msgpack blob format")
                except Exception as e:
                    logging.warning(f"Error converting metadata: {e}")
                
                # Migrate external data if the old table exists
                try:
                    # Check if old external_data table exists
                    cursor = self.connection.execute_sql("""
                        SELECT CASE 
                            WHEN EXISTS(SELECT 1 FROM sqlite_master WHERE type='table' AND name='external_data') 
                            THEN 1 ELSE 0 END AS table_exists;
                    """)
                    external_data_exists = cursor.fetchone()[0]
                    
                    if external_data_exists:
                        logging.info("Migrating external data from old format...")
                        
                        # Create kddb_external_data table if it doesn't exist
                        self.connection.execute_sql("""
                            CREATE TABLE IF NOT EXISTS kddb_external_data (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                taxonomy_id INTEGER,
                                key TEXT NOT NULL,
                                data BLOB,
                                FOREIGN KEY (taxonomy_id) REFERENCES kddb_taxonomies (id)
                            );
                        """)
                        
                        # Get all entries from the old external_data table
                        cursor = self.connection.execute_sql("SELECT key, data FROM external_data")
                        entries = cursor.fetchall()
                        
                        for key, data in entries:
                            # Check if data is a JSON string that needs conversion
                            try:
                                # Try to decode as text - if this works, it's the old JSON format
                                data_text = data.decode('utf-8')
                                data_dict = json.loads(data_text)
                                
                                # Convert to msgpack blob
                                data_blob = msgpack.packb(data_dict, use_bin_type=True)
                                
                                # Insert into the new table
                                self.connection.execute_sql(
                                    "INSERT INTO kddb_external_data (taxonomy_id, key, data) VALUES (?, ?, ?)",
                                    (None, key, data_blob)
                                )
                                logging.info(f"Migrated external data for key: {key}")
                            except (UnicodeDecodeError, json.JSONDecodeError, AttributeError):
                                # If data is None or already binary, pack it directly
                                if data is not None:
                                    data_blob = msgpack.packb(data, use_bin_type=True)
                                    # Insert into the new table
                                    self.connection.execute_sql(
                                        "INSERT INTO kddb_external_data (taxonomy_id, key, data) VALUES (?, ?, ?)",
                                        (None, key, data_blob)
                                    )
                                    logging.info(f"Migrated external data for key: {key} (already in binary format)")
                except Exception as e:
                    logging.warning(f"Error migrating external data: {e}")
                    import traceback
                    logging.warning(traceback.format_exc())
                
                # Clean up temporary tables
                self.connection.execute_sql("DROP TABLE IF EXISTS temp_do_mapping;")
                self.connection.execute_sql("DROP TABLE IF EXISTS node_levels;")
                
                # Check if sqlite_sequence exists before updating it
                cursor = self.connection.execute_sql("SELECT name FROM sqlite_master WHERE type='table' AND name='sqlite_sequence';")
                if cursor.fetchone():
                    # Update sequence values
                    self.connection.execute_sql("""
                        UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM kddb_content_nodes) 
                        WHERE name = 'kddb_content_nodes'
                    """)
                    
                    self.connection.execute_sql("""
                        UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM kddb_content_node_parts) 
                        WHERE name = 'kddb_content_node_parts'
                    """)
                    
                    self.connection.execute_sql("""
                        UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM kddb_data_objects) 
                        WHERE name = 'kddb_data_objects'
                    """)
                    
                    self.connection.execute_sql("""
                        UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM kddb_features) 
                        WHERE name = 'kddb_features'
                    """)
                    
                    self.connection.execute_sql("""
                        UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM kddb_feature_blob) 
                        WHERE name = 'kddb_feature_blob'
                    """)
                
                logging.info("Database migration completed successfully.")
        
        except Exception as e:
            logging.error(f"Error during database migration: {e}")
            raise
        
        finally:
            # Turn foreign key constraints back on
            self.connection.execute_sql("PRAGMA foreign_keys = ON;")

    def __build_db(self):
        """
        Builds a new database for the document using Peewee models.
        """
        from kodexa.model.persistence_models import Metadata
        import uuid as uuid_lib
        
        # Store document metadata
        document_metadata = {
            "version": Document.CURRENT_VERSION,
            "metadata": self.document.metadata,
            "source": self.__clean_none_values(dataclasses.asdict(self.document.source)),
            "mixins": self.document.get_mixins(),
            "labels": getattr(self.document, 'labels', []),
            "uuid": getattr(self.document, 'uuid', str(uuid_lib.uuid4())),
        }
        
        Metadata.create(id=1, metadata=msgpack.packb(document_metadata, use_bin_type=True))
        self.document.version = "6.0.0"

    def __clean_none_values(self, d):
        """
        Cleans a dictionary by removing keys with None values.
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

    def __load_document(self):
        """
        Loads an existing document from the database using Peewee models.
        """
        from kodexa.model.persistence_models import Metadata, NodeType, FeatureType
        
        # Load node types and feature types into cache
        for node_type in NodeType.select():
            self.node_type_cache[node_type.id] = node_type.name
            self.node_type_cache[node_type.name] = node_type.name  # Add name mapping for direct string reference
            
        for feature_type in FeatureType.select():
            self.feature_type_cache[feature_type.id] = feature_type.name
            
        # Load document metadata
        metadata_record = Metadata.get_or_none(Metadata.id == 1)
        if metadata_record:
            metadata = None
            # Try loading with msgpack first
            try:
                metadata = msgpack.unpackb(metadata_record.metadata)
            except Exception as e:
                # Fallback: try if it's JSON in a text field (backward compatibility)
                try:
                    metadata_text = metadata_record.metadata.decode('utf-8')
                    metadata = json.loads(metadata_text)
                    
                    # If loaded successfully as JSON, convert to msgpack format for next load
                    logging.info("Converting JSON metadata to msgpack format")
                    Metadata.delete().where(Metadata.id == 1).execute()
                    Metadata.create(id=1, metadata=msgpack.packb(metadata, use_bin_type=True))
                except Exception as inner_e:
                    logging.error(f"Failed to load metadata: {e}, Fallback error: {inner_e}")
            
            if metadata:
                self.document.metadata = DocumentMetadata(metadata["metadata"])
                self.document.version = metadata.get("version", Document.PREVIOUS_VERSION)
                
                self.id = metadata.get("uuid", str(uuid.uuid5(uuid.NAMESPACE_DNS, "kodexa.com")))
                
                if "source" in metadata and metadata["source"]:
                    self.document.source = SourceMetadata.from_dict(metadata["source"])
                if "labels" in metadata and metadata["labels"]:
                    self.document.labels = metadata["labels"]
                if "mixins" in metadata and metadata["mixins"]:
                    self.document._mixins = metadata["mixins"]
            
            # Load root node
            from kodexa.model.persistence_models import ContentNode as PeeweeContentNode
            
            root_content_node = PeeweeContentNode.get_or_none(PeeweeContentNode.parent == None)
            if root_content_node:
                self.document.content_node = self.__build_node(root_content_node)
        
        # Ensure we're on the latest version
        self.document.version = "6.0.0"
        self.update_metadata()

    def __build_node(self, peewee_node):
        """
        Builds a ContentNode from a Peewee ContentNode model.
        """
        from kodexa.model.persistence_models import ContentNode as PeeweeContentNode
        
        parent_node = None 
        if peewee_node.parent_id:
            parent_node = self.get_node(peewee_node.parent_id)

        # Handle either ID or direct node_type string reference
        node_type = peewee_node.node_type
        if node_type in self.node_type_cache:
            node_type = self.node_type_cache[node_type]
        else:
            # Add to cache for future reference
            self.node_type_cache[node_type] = node_type

        new_node = ContentNode(
            document=self.document,
            node_type=node_type,
            content=peewee_node.content,
            parent=parent_node,
            index=peewee_node.index
        )
        new_node.id = peewee_node.id

        return new_node

    def close(self):
        """
        Closes the connection to the database. If delete_on_close is True, the file will also be deleted.
        """
        from kodexa.model.persistence_models import close_database
        
        close_database()
        
        if self.is_tmp or self.delete_on_close:
            pathlib.Path(self.current_filename).unlink()

    def update_metadata(self):
        """
        Updates the metadata of the document.
        """
        from kodexa.model.persistence_models import Metadata
        import uuid as uuid_lib
        
        document_metadata = {
            "version": Document.CURRENT_VERSION,
            "metadata": self.document.metadata,
            "source": self.__clean_none_values(dataclasses.asdict(self.document.source)),
            "mixins": self.document.get_mixins(),
            "labels": getattr(self.document, 'labels', []),
            "uuid": getattr(self.document, 'uuid', str(uuid_lib.uuid4())),
        }
        
        # Delete existing metadata and create new
        Metadata.delete().where(Metadata.id == 1).execute()
        Metadata.create(id=1, metadata=msgpack.packb(document_metadata, use_bin_type=True))

    def get_node(self, node_id):
        """
        Retrieves a node by its id.
        """
        from kodexa.model.persistence_models import ContentNode as PeeweeContentNode
        
        peewee_node = PeeweeContentNode.get_or_none(PeeweeContentNode.id == node_id)
        if peewee_node:
            return self.__build_node(peewee_node)
        return None

    def get_parent(self, content_node: ContentNode):
        """
        Retrieves the parent of a given node.
        """
        from kodexa.model.persistence_models import ContentNode as PeeweeContentNode, DataObject
        self.get_node(content_node._parent_id)
        
    def get_children(self, content_node: ContentNode):
        """
        Retrieves the children of a given node.
        """
        from kodexa.model.persistence_models import ContentNode as PeeweeContentNode
        
        children = []
        peewee_node = PeeweeContentNode.get_or_none(PeeweeContentNode.id == content_node.id)
        if peewee_node:
            # Get child nodes directly through parent relationship
            child_nodes = PeeweeContentNode.select().where(
                PeeweeContentNode.parent == peewee_node
            ).order_by(PeeweeContentNode.index)
            
            # If any child nodes have data_object still set, verify they're not deleted
            for child_node in child_nodes:
                children.append(self.__build_node(child_node))
        
        return children

    def get_child_ids(self, content_node):
        """
        Retrieves the ids of the children of a given node.
        """
        from kodexa.model.persistence_models import ContentNode as PeeweeContentNode
        
        children = []
        peewee_node = PeeweeContentNode.get_or_none(PeeweeContentNode.id == content_node.id)
        if peewee_node:
            # Get child nodes directly through parent relationship
            child_nodes = PeeweeContentNode.select().where(
                PeeweeContentNode.parent == peewee_node
            )
            
            # If any child nodes have data_object still set, verify they're not deleted
            for child_node in child_nodes:
                children.append(child_node.id)
                
        return children

    def add_content_node(self, node: ContentNode, parent: Optional[ContentNode] = None, execute=True):
        """
        Adds a content node to the document.
        """
        from kodexa.model.persistence_models import ContentNode as PeeweeContentNode
        from kodexa.model.persistence_models import ContentNodePart as PeeweeContentNodePart
        
        with self.connection.atomic():
            # Get parent node if provided
            parent_node = None
            if parent and parent.id:
                parent_node = PeeweeContentNode.get_or_none(PeeweeContentNode.id == parent.id)

                if parent_node is None:
                    raise ValueError(f"Parent node {parent.id} not found")

            if parent and parent.id is None:
                raise ValueError("Parent node ID is required to add a content node")
            
            if node.id is None:
            
                # Create ContentNode with parent relationship
                peewee_node = PeeweeContentNode.create(
                    node_type=node.node_type,
                    parent=parent_node,
                    content=node.content,
                    index=node.index
                )

                # Create ContentNodePart entries
                for idx, part in enumerate(node.get_content_parts()):
                    PeeweeContentNodePart.create(
                        content_node=peewee_node.id,
                        pos=idx,
                        content=part if isinstance(part, str) else None,
                        content_idx=part if not isinstance(part, str) else None
                    )
                
                
                # Set the UUID to the new node's ID
                node.id = peewee_node.id

            else:
                peewee_node = PeeweeContentNode.get_or_none(PeeweeContentNode.id == node.id)

                if peewee_node.parent is None or peewee_node.parent.id != parent.id:
                    peewee_node.parent = parent_node
                    peewee_node.save()
                    if parent_node:
                        node._parent_id = parent_node.id
                    else:
                        node._parent_id = None

            if parent and node.id is None:
                node._parent_id = parent.id
            
            return node

    def get_content_parts(self, node):
        """
        Retrieves the content parts of a given node.
        """
        from kodexa.model.persistence_models import ContentNodePart as PeeweeContentNodePart
        
        parts = []
        if node.id:
            peewee_parts = PeeweeContentNodePart.select().where(
                PeeweeContentNodePart.content_node == node.id
            ).order_by(PeeweeContentNodePart.pos)
            
            for part in peewee_parts:
                if part.content_idx is None:
                    parts.append(part.content)
                else:
                    parts.append(part.content_idx)
                    
        return parts

    def update_content_parts(self, node: ContentNode, content_parts: List[str | int]):
        """
        Updates the content parts of a given node.
        """
        from kodexa.model.persistence_models import ContentNodePart as PeeweeContentNodePart
        
        # Ensure node has an id before updating content parts
        if node.id is None:
            return
            
        with self.connection.atomic():
            # Delete existing parts
            PeeweeContentNodePart.delete().where(PeeweeContentNodePart.content_node == node.id).execute()
            
            # Create new parts
            for idx, part in enumerate(content_parts):
                PeeweeContentNodePart.create(
                    content_node=node.id,
                    pos=idx,
                    content=part if isinstance(part, str) else None,
                    content_idx=part if not isinstance(part, str) else None
                )

    def get_features(self, node: ContentNode) -> List[ContentFeature]:
        from kodexa.model.persistence_models import Feature as PeeweeFeature, FeatureBlob, FeatureType
        from kodexa.model.persistence_models import FeatureTag, FeatureBBox 
        from kodexa.model.persistence_models import ContentNodeFeatureLink
        
        content_features_list: List[ContentFeature] = []
        if node.id:
            peewee_feature_instances = (PeeweeFeature.select()
                               .join(ContentNodeFeatureLink, on=(PeeweeFeature.id == ContentNodeFeatureLink.feature_id))
                               .where(ContentNodeFeatureLink.content_node_id == node.id))
            
            for pf_instance in peewee_feature_instances:
                db_feature_type = FeatureType.get_by_id(pf_instance.feature_type_id)
                feature_type_name = db_feature_type.name
                
                feature_parts = feature_type_name.split(":", 1)
                feature_type_str = feature_parts[0] 
                feature_name_str = feature_parts[1] if len(feature_parts) > 1 else ""

                value_list = []
                if feature_type_str == 'tag':
                    tag_records = FeatureTag.select().where(FeatureTag.feature_id == pf_instance.id) # Use feature_id
                    for tag_record in tag_records:
                        tag_data_dict = {
                            'start': tag_record.start_pos, 'end': tag_record.end_pos,
                            'value': tag_record.tag_value, 'uuid': tag_record.uuid,
                            'data': msgpack.unpackb(tag_record.data) if tag_record.data else None,
                            'confidence': tag_record.confidence, 'group_uuid': tag_record.group_uuid,
                            'parent_group_uuid': tag_record.parent_group_uuid,
                            'cell_index': tag_record.cell_index, 'index': tag_record.index,
                            'note': tag_record.note, 'status': tag_record.status,
                            'owner_uri': tag_record.owner_uri,
                            'is_dirty': bool(tag_record.is_dirty) if tag_record.is_dirty is not None else None
                        }
                        value_list.append(Tag(**tag_data_dict))
                elif feature_type_str == 'spatial' and feature_name_str == 'bbox':
                    bbox_records = FeatureBBox.select().where(FeatureBBox.feature_id == pf_instance.id) # Use feature_id
                    for bbox_record in bbox_records:
                        value_list.append([bbox_record.x1, bbox_record.y1, bbox_record.x2, bbox_record.y2])
                else:
                    blob_records = FeatureBlob.select().where(FeatureBlob.feature_id == pf_instance.id) # Use feature_id
                    for blob_record in blob_records:
                        if blob_record.binary_value is not None:
                            value_list.append(msgpack.unpackb(blob_record.binary_value))
                        else:
                            value_list.append(None)
                
                content_features_list.append(
                    ContentFeature( # This is the ContentFeature from kodexa.model
                        feature_type_str,
                        feature_name_str,
                        value_list 
                    )
                )
                
        return content_features_list

    def add_feature(self, node: ContentNode, feature: ContentFeature, replace=False):
        if node.id is None:
            raise ValueError("Node ID is required to add a feature")

        from kodexa.model.persistence_models import Feature as PeeweeFeature, FeatureBlob, FeatureType
        from kodexa.model.persistence_models import FeatureTag, FeatureBBox # Added FeatureBBox
        from kodexa.model.persistence_models import ContentNodeFeatureLink
        
        with self.connection.atomic():
            feature_type_name = f"{feature.feature_type}:{feature.name}"
            db_feature_type, _ = FeatureType.get_or_create(name=feature_type_name)
            
            peewee_feature = (PeeweeFeature.select()
                             .join(ContentNodeFeatureLink, on=(PeeweeFeature.id == ContentNodeFeatureLink.feature_id))
                             .where((ContentNodeFeatureLink.content_node_id == node.id) &
                                    (PeeweeFeature.feature_type_id == db_feature_type.id))
                             .first())

            if not peewee_feature:
                peewee_feature = PeeweeFeature.create(feature_type=db_feature_type)
                ContentNodeFeatureLink.create(content_node_id=node.id, feature_id=peewee_feature.id)
            
            if replace:
                FeatureTag.delete().where(FeatureTag.feature_id == peewee_feature.id).execute()
                FeatureBBox.delete().where(FeatureBBox.feature_id == peewee_feature.id).execute()
                FeatureBlob.delete().where(FeatureBlob.feature_id == peewee_feature.id).execute()

            # Legacy handling for spatial bbox, check if the value is a list of 4 numbers, if so wrap in list
            if feature.feature_type == 'spatial' and feature.name == 'bbox':
                if isinstance(feature.value, list) and len(feature.value) == 4 and all(isinstance(coord, (int, float)) for coord in feature.value):
                    feature.value = [feature.value]

            for item_value in feature.value: # feature.value is always a list
                if feature.feature_type == 'tag':
                    if not isinstance(item_value, Tag):
                        raise ValueError(f"Expected Tag object for feature type 'tag', got {type(item_value)}")
                    tag_obj: Tag = item_value
                    FeatureTag.create(
                        feature=peewee_feature,
                        tag_value=tag_obj.value, start_pos=tag_obj.start, end_pos=tag_obj.end, uuid=tag_obj.uuid,
                        data=msgpack.packb(tag_obj.data, use_bin_type=True) if tag_obj.data is not None else None,
                        confidence=tag_obj.confidence, group_uuid=tag_obj.group_uuid,
                        parent_group_uuid=tag_obj.parent_group_uuid, cell_index=tag_obj.cell_index,
                        index=tag_obj.index, note=tag_obj.note, status=tag_obj.status,
                        owner_uri=tag_obj.owner_uri, is_dirty=1 if tag_obj.is_dirty else 0
                    )
                elif feature.feature_type == 'spatial' and feature.name == 'bbox':
                    if not (isinstance(item_value, list) and len(item_value) == 4 and all(isinstance(coord, (int, float)) for coord in item_value)):
                         raise ValueError(f"Expected a list of 4 numeric coordinates for 'spatial:bbox', got {item_value}")
                    FeatureBBox.create(
                        feature=peewee_feature,
                        x1=item_value[0], y1=item_value[1], x2=item_value[2], y2=item_value[3]
                    )
                else: 
                    FeatureBlob.create(
                        feature=peewee_feature,
                        binary_value=msgpack.packb(item_value, use_bin_type=True) if item_value is not None else None
                    )

    def remove_feature(self, node, feature_type, name):
        """
        Removes a feature from a given node.
        """
        from kodexa.model.persistence_models import Feature as PeeweeFeature, FeatureBlob, FeatureType, FeatureTag, FeatureBBox, ContentNodeFeatureLink
        
        feature_type_name = f"{feature_type}:{name}"
        
        # Find the feature type
        peewee_feature_type = FeatureType.get_or_none(FeatureType.name == feature_type_name)
        if peewee_feature_type:
            # Find features with this type linked to this node
            features_query = (PeeweeFeature.select()
                              .join(ContentNodeFeatureLink, on=(PeeweeFeature.id == ContentNodeFeatureLink.feature))
                              .where(ContentNodeFeatureLink.content_node == node.id,
                                     PeeweeFeature.feature_type == peewee_feature_type))
            
            feature_ids_to_delete = [f.id for f in features_query]

            if feature_ids_to_delete:
                with self.connection.atomic():
                    # Delete feature tags
                    FeatureTag.delete().where(FeatureTag.feature_id.in_(feature_ids_to_delete)).execute()
                    
                    # Delete feature bboxes
                    FeatureBBox.delete().where(FeatureBBox.feature_id.in_(feature_ids_to_delete)).execute()
                    
                    # Delete feature blobs
                    FeatureBlob.delete().where(FeatureBlob.feature_id.in_(feature_ids_to_delete)).execute()

                    # Delete links between content node and features
                    ContentNodeFeatureLink.delete().where(
                        ContentNodeFeatureLink.content_node == node.id, # Use node.id for FK object
                        ContentNodeFeatureLink.feature_id.in_(feature_ids_to_delete)
                    ).execute()
                
                    # Now delete the features themselves
                    PeeweeFeature.delete().where(PeeweeFeature.id.in_(feature_ids_to_delete)).execute()

    def remove_all_features(self, node):
        """
        Removes all features from a given node.
        """
        from kodexa.model.persistence_models import Feature as PeeweeFeature, FeatureBlob, FeatureTag, FeatureBBox, ContentNodeFeatureLink
        
        # Find all features linked to this node
        features_query = (PeeweeFeature.select()
                          .join(ContentNodeFeatureLink, on=(PeeweeFeature.id == ContentNodeFeatureLink.feature))
                          .where(ContentNodeFeatureLink.content_node == node.id)) # Use node.id for FK object
        
        feature_ids_to_delete = [f.id for f in features_query]

        if feature_ids_to_delete:
            with self.connection.atomic():
                # Delete feature tags
                FeatureTag.delete().where(FeatureTag.feature_id.in_(feature_ids_to_delete)).execute()
                
                # Delete feature bboxes
                FeatureBBox.delete().where(FeatureBBox.feature_id.in_(feature_ids_to_delete)).execute()
                
                # Delete feature blobs
                FeatureBlob.delete().where(FeatureBlob.feature_id.in_(feature_ids_to_delete)).execute()

                # Delete links between content node and features
                ContentNodeFeatureLink.delete().where(
                    ContentNodeFeatureLink.content_node == node.id, # Use node.id for FK object
                    ContentNodeFeatureLink.feature_id.in_(feature_ids_to_delete)
                ).execute()
            
                # Now delete the features themselves
                PeeweeFeature.delete().where(PeeweeFeature.id.in_(feature_ids_to_delete)).execute()

    def remove_all_features_by_id(self, node_id):
        """
        Removes all features from a node by its id.
        """
        self.remove_all_features(ContentNode(self.document, "", uuid=node_id))

    def remove_content_node(self, node):
        """
        Removes a node and all its children from the document.
        """
        from kodexa.model.persistence_models import ContentNode as PeeweeContentNode
        from kodexa.model.persistence_models import ContentNodePart as PeeweeContentNodePart
        
        def get_all_node_ids(node):
            """
            This function recursively traverses a node tree, collecting the ids of all non-virtual nodes.
            """
            all_node_ids = []
            if not node.virtual:
                all_node_ids.append(node.id)
                for child in node.get_children():
                    all_node_ids.extend(get_all_node_ids(child))
            return all_node_ids
        
        all_child_ids = get_all_node_ids(node)
        
        try:
            with self.connection.atomic():
                # Batch remove features
                for node_id in all_child_ids:
                    self.remove_all_features_by_id(node_id)
                
                # Batch remove content parts
                PeeweeContentNodePart.delete().where(
                    PeeweeContentNodePart.content_node.in_(all_child_ids)
                ).execute()
                
                # Remove the content nodes
                PeeweeContentNode.delete().where(
                    PeeweeContentNode.id.in_(all_child_ids)
                ).execute()
                
                return all_child_ids
            
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Error removing content node: {e}")
            return []

    def update_node(self, node: ContentNode):
        """
        Updates a given node in the document.
        """
        from kodexa.model.persistence_models import ContentNode as PeeweeContentNode
        
        try:
            peewee_node = PeeweeContentNode.get_or_none(PeeweeContentNode.id == node.id)
            # Update the peewee_node to match the node
            if peewee_node is not None:
                # Update node properties
                peewee_node.node_type = node.node_type
                peewee_node.content = node.content
                peewee_node.index = node.index
                peewee_node.save()
                
                # Update content parts
                self.update_content_parts(node, node.get_content_parts())
                
                logger.debug(f"Successfully updated node {node.id}")
        except Exception as e:
            logger.error(f"Failed to update node: {e}")

    def get_nodes_by_type(self, node_type):
        """
        Retrieves nodes of a given type from the document.
        """
        from kodexa.model.persistence_models import ContentNode as PeeweeContentNode
        
        content_nodes = []
        
        try:
            # Get all nodes of the specified type
            peewee_nodes = PeeweeContentNode.select().where(
                PeeweeContentNode.node_type == node_type
            )
            
            # Build content nodes
            for peewee_node in peewee_nodes:
                content_nodes.append(self.__build_node(peewee_node))
            
        except Exception as e:
            logger.error(f"Error retrieving nodes by type: {e}")
        
        return content_nodes

    def get_content_nodes(self, node_type, parent_node, include_children):
        """
        Retrieves content nodes from the document based on the given parameters.
        """
        from kodexa.model.persistence_models import ContentNode as PeeweeContentNode
        
        nodes = []
        
        try:
            with self.connection.atomic():
                # Find the parent node
                parent_peewee_node = PeeweeContentNode.get_or_none(PeeweeContentNode.id == parent_node.id)
                if include_children:
                    # For now, use a recursive function to get all descendants
                    def get_all_descendants(node_id):
                        descendants = []
                        # Get direct children
                        children = list(PeeweeContentNode.select().where(
                            PeeweeContentNode.parent_id == node_id
                        ))
                        
                        # Add children to descendants
                        for child in children:
                            descendants.append(child)
                            # Recursively get children's descendants
                            descendants.extend(get_all_descendants(child.id))
                            
                        return descendants
                    
                    # Get all descendants of parent node
                    if parent_peewee_node is not None:
                        all_nodes = get_all_descendants(parent_peewee_node.id)
                    else:
                        if node_type == "*":
                            all_nodes = PeeweeContentNode.select()
                        else:
                            all_nodes = PeeweeContentNode.select().where(PeeweeContentNode.node_type == node_type)
                    
                    # Filter by node type if needed
                    if node_type != "*":
                        all_nodes = [n for n in all_nodes if n.node_type == node_type]
                    
                    # Sort by index and create ContentNodes
                    for peewee_node in sorted(all_nodes, key=lambda x: x.index or 0):
                        nodes.append(self.__build_node(peewee_node))
                else:
                    # Get direct children of parent node with specific node type
                    child_nodes = PeeweeContentNode.select().where(
                        PeeweeContentNode.parent_id == parent_peewee_node.id
                    )
                    
                    if node_type != "*":
                        child_nodes = child_nodes.where(PeeweeContentNode.node_type == node_type)
                    
                    # Sort by index
                    for child_node in sorted(list(child_nodes), key=lambda x: getattr(x, 'index', 0) or 0):
                        nodes.append(self.__build_node(child_node))
        except Exception as e:
            logger.error(f"Error getting content nodes: {e}")
            self.connection.rollback()
        
        return nodes

    def get_all_tags(self):
        """
        Retrieves all tags from the document.
        """
        from kodexa.model.persistence_models import FeatureType
        
        features = []
        tag_feature_types = FeatureType.select().where(FeatureType.name.startswith('tag:'))
        
        for feature_type in tag_feature_types:
            features.append(feature_type.name.split(":")[1])
        
        return features

    def get_tagged_nodes(self, tag, tag_uuid=None):
        """
        Retrieves nodes with a given tag.
        """
        from kodexa.model.persistence_models import Feature as PeeweeFeature, FeatureType
        from kodexa.model.persistence_models import ContentNode as PeeweeContentNode
        from kodexa.model.persistence_models import FeatureTag
        
        content_nodes = []
        tag_name = f"tag:{tag}"
        
        try:
            # Find the feature type for this tag
            feature_type = FeatureType.get_or_none(FeatureType.name == tag_name)
            if feature_type:
                # Query for features with this type
                feature_query = PeeweeFeature.select(PeeweeFeature.content_node).distinct().where(
                    PeeweeFeature.feature_type == feature_type
                )
                
                if tag_uuid:
                    # If we have a tag UUID, look for matching tags
                    matching_tags = FeatureTag.select(FeatureTag.feature).where(FeatureTag.uuid == tag_uuid)
                    matching_feature_ids = [tag.feature_id for tag in matching_tags]
                    
                    if matching_feature_ids:
                        feature_query = feature_query.where(PeeweeFeature.id.in_(matching_feature_ids))
                    else:
                        # Check for tag_uuid in the Feature table as well (older format)
                        feature_query = feature_query.where(PeeweeFeature.tag_uuid == tag_uuid)
                
                for feature in feature_query:
                    peewee_node = PeeweeContentNode.get_or_none(PeeweeContentNode.id == feature.content_node)
                    if peewee_node:
                        content_nodes.append(self.__build_node(peewee_node))
        
        except Exception as e:
            logger.error(f"Error retrieving tagged nodes: {e}")
        
        return content_nodes

    def get_all_tagged_nodes(self):
        """
        Retrieves all nodes with tags from the document.
        """
        from kodexa.model.persistence_models import Feature as PeeweeFeature, FeatureType
        from kodexa.model.persistence_models import ContentNode as PeeweeContentNode
        
        content_nodes = []
        
        try:
            # Find all tag feature types
            tag_feature_types = FeatureType.select().where(FeatureType.name.startswith('tag:'))
            if tag_feature_types:
                # Query for features with any tag type
                feature_query = PeeweeFeature.select(PeeweeFeature.content_node).distinct().where(
                    PeeweeFeature.feature_type.in_([ft.id for ft in tag_feature_types])
                )
                
                for feature in feature_query:
                    peewee_node = PeeweeContentNode.get_or_none(PeeweeContentNode.id == feature.content_node)
                    if peewee_node:
                        node = self.__build_node(peewee_node)
                        if node not in content_nodes:  # Avoid duplicates
                            content_nodes.append(node)
        except Exception as e:
            logger.error(f"Error retrieving all tagged nodes: {e}")
            
        return content_nodes

    def add_model_insight(self, model_insights: ModelInsight):
        """
        Adds a model insight to the document.
        """
        from kodexa.model.persistence_models import database
        
        with database.atomic():
            # Execute raw SQL since there's no dedicated model
            database.execute_sql(
                "INSERT INTO model_insights (model_insight) VALUES (?)",
                (model_insights.json(),)
            )

    def get_model_insights(self) -> List[ModelInsight]:
        """
        Retrieves all model insights from the document.
        """
        from kodexa.model.persistence_models import database
        
        model_insights = []
        cursor = database.execute_sql("SELECT model_insight FROM model_insights")
        
        for row in cursor.fetchall():
            model_insights.append(ModelInsight.model_validate_json(row[0]))
        
        return model_insights
    
    def clear_model_insights(self):
        """
        Clears all model insights from the document.
        """
        from kodexa.model.persistence_models import database
        
        with database.atomic():
            database.execute_sql("DELETE FROM model_insights")

    def add_exception(self, exception: ContentException):
        """
        Adds an exception to the document.
        """
        from kodexa.model.persistence_models import ContentException as PeeweeContentException
        
        with self.connection.atomic():
            PeeweeContentException.create(
                data_object=None,  # Remove data_object relationship
                message=exception.message,
                exception_details=exception.exception_details,
                exception_type=exception.exception_type,
                severity=exception.severity,
                path=None,  # Not in original model
                closing_comment=None,  # Not in original model
                open=True,  # Default to open
                node_uuid=exception.node_uuid,  # Store node_uuid directly
                exception_type_id=exception.exception_type_id  # Store exception_type_id
            )

    def get_exceptions(self) -> List[ContentException]:
        """
        Retrieves all exceptions from the document.
        """
        from kodexa.model.persistence_models import ContentException as PeeweeContentException
        
        exceptions = []
        peewee_exceptions = PeeweeContentException.select()
        
        for peewee_exception in peewee_exceptions:
            exceptions.append(
                ContentException(
                    tag=None,  # Not in Peewee model
                    message=peewee_exception.message,
                    exception_details=peewee_exception.exception_details,
                    group_uuid=None,  # Not in Peewee model
                    tag_uuid=None,  # Not in Peewee model
                    exception_type=peewee_exception.exception_type,
                    severity=peewee_exception.severity,
                    node_uuid=peewee_exception.node_uuid,  # Get node_uuid directly
                    exception_type_id=peewee_exception.exception_type_id  # Get exception_type_id
                )
            )
        
        return exceptions

    def replace_exceptions(self, exceptions: List[ContentException]):
        """
        Replaces all exceptions in the document with a given list of exceptions.
        """
        from kodexa.model.persistence_models import ContentException as PeeweeContentException
        
        with self.connection.atomic():
            PeeweeContentException.delete().execute()
            
            for exception in exceptions:
                self.add_exception(exception)

    def get_bytes(self):
        """
        Retrieves the document as bytes.
        """
        self.sync()
        
        if self.inmemory:
            # For in-memory DB, first save to disk using the sqlite3 backup API
            import sqlite3
            
            # Create a connection to the temporary file
            dest_conn = sqlite3.connect(self.current_filename)
            
            # Get the source connection from Peewee
            source_conn = self.connection.connection()
            
            # Back up the in-memory database to the file
            source_conn.backup(dest_conn)
            
            # Close the destination connection to ensure it's flushed to disk
            dest_conn.close()
        
        with open(self.current_filename, "rb") as f:
            return f.read()

    def sync(self):
        """
        Synchronizes the database with the document.
        """
        self.update_metadata()
        self.connection.commit()

    def debug_tags(self):
        """
        Debug method to print tag information from the database.
        """
        from kodexa.model.persistence_models import Feature as PeeweeFeature, FeatureType
        from kodexa.model.persistence_models import ContentNode as PeeweeContentNode
        from kodexa.model.persistence_models import FeatureTag, FeatureBlob
        
        try:
            # Log tag feature types
            tag_types = FeatureType.select().where(FeatureType.name.startswith('tag:'))
            print(f"Tag feature types: {[t.name for t in tag_types]}")
            
            # Log features with tag types
            for tag_type in tag_types:
                features = PeeweeFeature.select().where(PeeweeFeature.feature_type == tag_type)
                print(f"Features for tag type {tag_type.name}: {features.count()}")
                
                for feature in features:
                    print(f"Feature ID: {feature.id}, Content Node ID: {feature.content_node}")
                    
                    # Check for FeatureTags
                    tags = FeatureTag.select().where(FeatureTag.feature == feature)
                    print(f"Feature Tags: {tags.count()}")
                    
                    # Check for feature blob
                    blobs = FeatureBlob.select().where(FeatureBlob.feature == feature)
                    print(f"Feature Blobs: {blobs.count()}")
                    
                    if blobs.count() > 0:
                        blob = blobs.first()
                        blob_content = msgpack.unpackb(blob.binary_value)
                        print(f"Blob content: {blob_content}")
            
            # Log content nodes with features
            feature_count = PeeweeFeature.select().count()
            print(f"Total features in the database: {feature_count}")
            
            return True
        except Exception as e:
            print(f"Error in debug_tags: {e}")
            import traceback
            print(traceback.format_exc())
            return False

    def get_external_data(self, key="default") -> dict:
        """
        Get external data stored with the given key.
        
        Args:
            key: The key for the external data, defaults to "default"
            
        Returns:
            A dictionary of the external data
        """
        from kodexa.model.persistence_models import ExternalData
        
        try:
            external_data = ExternalData.get_or_none(ExternalData.key == key)
            if external_data:
                return msgpack.unpackb(external_data.data)
            return {}
        except Exception as e:
            logger.error(f"Error getting external data: {e}")
            return {}
            
    def get_external_data_keys(self) -> List[str]:
        """
        Get all keys used for external data.
        
        Returns:
            A list of keys used for external data
        """
        from kodexa.model.persistence_models import ExternalData
        
        try:
            keys = ExternalData.select(ExternalData.key).distinct()
            key_list = [k.key for k in keys]
            
            # Always include 'default' in the list of keys
            if 'default' not in key_list:
                key_list.insert(0, 'default')
                
            return key_list
        except Exception as e:
            logger.error(f"Error getting external data keys: {e}")
            return ['default']  # Return default key even on error
            
    def set_external_data(self, external_data: dict, key="default"):
        """
        Store external data with the given key.
        
        Args:
            external_data: A dictionary of data to store
            key: The key to store the data under, defaults to "default"
        """
        from kodexa.model.persistence_models import ExternalData
        
        try:
            with self.connection.atomic():
                # Delete any existing data with this key
                ExternalData.delete().where(ExternalData.key == key).execute()
                
                # Store the new data
                ExternalData.create(
                    taxonomy=None,  # Could be linked to taxonomy in the future
                    key=key,
                    data=msgpack.packb(external_data, use_bin_type=True)
                )
        except Exception as e:
            logger.error(f"Error setting external data: {e}")
