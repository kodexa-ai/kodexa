from peewee import *
import json
import datetime
import msgpack
from playhouse.sqlite_ext import JSONField, BlobField

database = SqliteDatabase(None)  # Will be initialized later with actual DB path


class BaseModel(Model):
    class Meta:
        database = database


class Taxonomy(BaseModel):
    id = AutoField()
    ref = TextField()

    class Meta:
        table_name = 'kddb_taxonomy'


class DataObject(BaseModel):
    id = AutoField()
    parent = ForeignKeyField('self', backref='children', null=True, column_name='parent_id')
    taxonomy = ForeignKeyField(Taxonomy, backref='data_objects', null=True, column_name='taxonomy_id')
    idx = IntegerField(null=True)
    path = TextField(null=True)
    group_uuid = TextField(null=True)
    cell_index = IntegerField(null=True)
    source_ordering = TextField(null=True)
    created = DateTimeField(default=datetime.datetime.now)
    modified = DateTimeField(default=datetime.datetime.now)
    lineage = JSONField(null=True)
    deleted = BooleanField(default=False)

    class Meta:
        table_name = 'kddb_data_objects'


class NodeType(BaseModel):
    id = AutoField()
    name = TextField()

    class Meta:
        table_name = 'kddb_node_types'


class ContentNode(BaseModel):
    id = AutoField()
    parent = ForeignKeyField('self', backref='children', null=True, column_name='parent_id')
    node_type = TextField()
    content = TextField(null=True)
    created = DateTimeField(default=datetime.datetime.now)
    modified = DateTimeField(default=datetime.datetime.now)
    index = IntegerField(null=True)

    class Meta:
        table_name = 'kddb_content_nodes'


class ContentNodePart(BaseModel):
    id = AutoField()
    content_node = ForeignKeyField(ContentNode, backref='parts', column_name='content_node_id')
    pos = IntegerField()
    content = TextField(null=True)
    content_idx = IntegerField(null=True)

    class Meta:
        table_name = 'kddb_content_node_parts'


class ContentException(BaseModel):
    id = AutoField()
    data_object = ForeignKeyField(DataObject, backref='content_exceptions', null=True, column_name='data_object_id')
    message = TextField(null=True)
    exception_details = TextField(null=True)
    exception_type = TextField(null=True)
    severity = TextField(null=True)
    path = TextField(null=True)
    closing_comment = TextField(null=True)
    open = BooleanField(default=True)
    node_uuid = TextField(null=True)
    exception_type_id = TextField(null=True)

    class Meta:
        table_name = 'kddb_content_exceptions'


class FeatureType(BaseModel):
    id = AutoField()
    name = TextField()

    class Meta:
        table_name = 'kddb_feature_types'


class Feature(BaseModel):
    id = AutoField()
    feature_type = ForeignKeyField(FeatureType, backref='features', column_name='feature_type_id')
    tag_uuid = TextField(null=True)

    class Meta:
        table_name = 'kddb_features'


class ContentNodeFeatureLink(BaseModel):
    id = AutoField()
    content_node = ForeignKeyField(ContentNode, backref='feature_links', column_name='content_node_id')
    feature = ForeignKeyField(Feature, backref='content_node_links', column_name='feature_id')

    class Meta:
        table_name = 'kddb_content_node_feature_links'
        indexes = (
            (('content_node_id', 'feature_id'), True),  # Ensure uniqueness of pairs
        )


class FeatureBlob(BaseModel):
    id = AutoField()
    feature = ForeignKeyField(Feature, backref='blobs', column_name='feature_id')
    binary_value = BlobField()

    class Meta:
        table_name = 'kddb_feature_blob'


class FeatureBBox(BaseModel):
    id = AutoField()
    feature = ForeignKeyField(Feature, backref='bboxes', column_name='feature_id')
    x1 = FloatField()
    y1 = FloatField()
    x2 = FloatField()
    y2 = FloatField()

    class Meta:
        table_name = 'kddb_feature_bbox'


class FeatureTag(BaseModel):
    id = AutoField()
    feature = ForeignKeyField(Feature, backref='tags', column_name='feature_id')
    tag_value = TextField(null=True)
    start_pos = IntegerField(null=True)
    end_pos = IntegerField(null=True)
    uuid = TextField(null=True)
    data = BlobField(null=True)
    confidence = FloatField(null=True)
    group_uuid = TextField(null=True)
    parent_group_uuid = TextField(null=True)
    cell_index = IntegerField(null=True)
    index = IntegerField(null=True)
    note = TextField(null=True)
    status = TextField(null=True)
    owner_uri = TextField(null=True)
    is_dirty = IntegerField(null=True)

    class Meta:
        table_name = 'kddb_feature_tag'


class DataAttribute(BaseModel):
    id = AutoField()
    data_object = ForeignKeyField(DataObject, backref='attributes', column_name='data_object_id')
    feature_tag = ForeignKeyField(FeatureTag, backref='data_attributes', null=True, column_name='feature_tag_id')
    tag = TextField(null=True)
    value = TextField(null=True)
    string_value = TextField(null=True)
    path = TextField(null=True)
    owner_uri = TextField(null=True)
    type_at_creation = TextField(null=True)
    decimal_value = FloatField(null=True)
    boolean_value = IntegerField(null=True)
    created = DateTimeField(default=datetime.datetime.now)
    modified = DateTimeField(default=datetime.datetime.now)
    confidence = FloatField(null=True)
    truncated = BooleanField(default=False)

    class Meta:
        table_name = 'kddb_data_attributes'


class DataException(BaseModel):
    id = AutoField()
    data_object = ForeignKeyField(DataObject, backref='data_exceptions', column_name='data_object_id')
    data_attribute = ForeignKeyField(DataAttribute, backref='exceptions', null=True, column_name='data_attribute_id')
    message = TextField(null=True)
    exception_details = TextField(null=True)
    group_uuid = TextField(null=True)
    tag_uuid = TextField(null=True)
    exception_type = TextField(null=True)
    severity = TextField(null=True)
    path = TextField(null=True)
    closing_comment = TextField(null=True)
    open = BooleanField(default=True)

    class Meta:
        table_name = 'kddb_data_exceptions'


class TagMetadata(BaseModel):
    id = AutoField()
    data_object = ForeignKeyField(DataObject, backref='tag_metadata', null=True, column_name='data_object_id')
    data_attribute = ForeignKeyField(DataAttribute, backref='tag_metadata', null=True, column_name='data_attribute_id')
    uuid = TextField(null=True)
    group_uuid = TextField(null=True)
    parent_group_uuid = TextField(null=True)
    start_pos = IntegerField(null=True)
    end_pos = IntegerField(null=True)
    confidence = FloatField(null=True)
    note = TextField(null=True)
    status = TextField(null=True)
    owner_uri = TextField(null=True)
    is_dirty = BooleanField(default=False)

    class Meta:
        table_name = 'kddb_tag_metadata'


class Metadata(BaseModel):
    id = AutoField()
    metadata = BlobField(null=True)

    class Meta:
        table_name = 'kddb_metadata'


class Step(BaseModel):
    obj = BlobField()

    class Meta:
        table_name = 'kddb_steps'
        primary_key = False  # No specific PK in schema


class ExternalData(BaseModel):
    id = AutoField()
    taxonomy = ForeignKeyField(Taxonomy, backref='external_data', null=True, column_name='taxonomy_id')
    key = TextField()
    data = BlobField()

    class Meta:
        table_name = 'kddb_external_data'


def initialize_database(db_path):
    """Initialize the database with the given path"""
    database.init(db_path)
    database.connect()
    
    # Create missing tables
    tables_to_create = []
    all_tables = [
        Taxonomy, DataObject, NodeType, ContentNode, ContentNodePart,
        ContentException, FeatureType, Feature, ContentNodeFeatureLink, FeatureBlob, FeatureBBox,
        FeatureTag, DataAttribute, DataException, TagMetadata, Metadata, Step,
        ExternalData
    ]
    
    for table in all_tables:
        if not database.table_exists(table._meta.table_name):
            tables_to_create.append(table)
    
    if tables_to_create:
        database.create_tables(tables_to_create)
    
    # Migrate ContentException table to add node_uuid and make data_object_id nullable
    if database.table_exists("kddb_content_exceptions"):
        # Check if node_uuid column exists
        cursor = database.execute_sql("PRAGMA table_info('kddb_content_exceptions')")
        columns = [column[1] for column in cursor.fetchall()]
        
        if "node_uuid" not in columns:
            # Add node_uuid column
            database.execute_sql("ALTER TABLE kddb_content_exceptions ADD COLUMN node_uuid TEXT")
            
        # Check if exception_type_id column exists
        if "exception_type_id" not in columns:
            # Add exception_type_id column
            database.execute_sql("ALTER TABLE kddb_content_exceptions ADD COLUMN exception_type_id TEXT")
        
        # Check if data_object_id has NOT NULL constraint
        cursor = database.execute_sql("PRAGMA table_info('kddb_content_exceptions')")
        has_not_null = False
        for column in cursor.fetchall():
            if column[1] == 'data_object_id' and column[3] == 1:  # column[3] is notnull flag
                has_not_null = True
                break
                
        if has_not_null:
            # We need to recreate the table to make data_object_id nullable
            # Execute each statement individually
            
            # Disable foreign keys
            database.execute_sql("PRAGMA foreign_keys=off")
            
            # Start transaction
            database.execute_sql("BEGIN TRANSACTION")
            
            # Create temporary table
            database.execute_sql("""
                CREATE TABLE kddb_content_exceptions_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data_object_id INTEGER,
                    message TEXT,
                    exception_details TEXT,
                    exception_type TEXT,
                    severity TEXT,
                    path TEXT,
                    closing_comment TEXT,
                    open BOOLEAN DEFAULT 1,
                    node_uuid TEXT,
                    exception_type_id TEXT,
                    FOREIGN KEY (data_object_id) REFERENCES kddb_data_objects (id)
                )
            """)
            
            # Copy data
            database.execute_sql("""
                INSERT INTO kddb_content_exceptions_new
                SELECT id, data_object_id, message, exception_details, exception_type, 
                       severity, path, closing_comment, open, node_uuid, exception_type_id
                FROM kddb_content_exceptions
            """)
            
            # Drop old table
            database.execute_sql("DROP TABLE kddb_content_exceptions")
            
            # Rename new table
            database.execute_sql("ALTER TABLE kddb_content_exceptions_new RENAME TO kddb_content_exceptions")
            
            # Commit transaction
            database.execute_sql("COMMIT")
            
            # Enable foreign keys
            database.execute_sql("PRAGMA foreign_keys=on")
    
def close_database():
    """Close the database connection"""
    if not database.is_closed():
        database.close()
