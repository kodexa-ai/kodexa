import os
import shutil
import logging
import sys
import sqlite3
from kodexa_document.model import Document
from kodexa_document.persistence import SqliteDocumentPersistence

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def analyze_database(db_path):
    """
    Analyze the database structure and content.
    """
    logger.info(f"Analyzing database: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    logger.info(f"Tables in the database: {[t[0] for t in tables]}")
    
    # Check counts in old tables
    old_tables = ['cn', 'cnp', 'n_type', 'f_type', 'ft', 'metadata']
    for table in old_tables:
        if table in [t[0] for t in tables]:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            logger.info(f"Count in old table {table}: {count}")
    
    # Check counts in new tables
    new_tables = ['kddb_data_objects', 'kddb_content_nodes', 'kddb_content_node_parts', 
                 'kddb_feature_types', 'kddb_features', 'kddb_feature_blob', 'kddb_node_types']
    for table in new_tables:
        if table in [t[0] for t in tables]:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            logger.info(f"Count in new table {table}: {count}")
    
    conn.close()

def migrate_database(db_path):
    """
    Explicitly run the migration script on the database.
    """
    logger.info(f"Running explicit migration on: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Read the migration SQL script
    with open('migration_script.sql', 'r') as f:
        migration_script = f.read()
    
    # Check if sqlite_sequence exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sqlite_sequence'")
    has_seq_table = cursor.fetchone() is not None
    
    # If it doesn't exist, remove the sqlite_sequence related statements
    if not has_seq_table:
        logger.info("sqlite_sequence table not found, modifying migration script...")
        lines = migration_script.split('\n')
        filtered_lines = []
        for line in lines:
            if 'sqlite_sequence' not in line:
                filtered_lines.append(line)
        migration_script = '\n'.join(filtered_lines)
    
    # Execute the migration script in small chunks to avoid errors
    try:
        # Split the script into statements
        statements = migration_script.split(';')
        
        for statement in statements:
            statement = statement.strip()
            if statement:
                try:
                    cursor.execute(statement)
                    conn.commit()
                except sqlite3.Error as e:
                    logger.error(f"Error executing statement: {statement}")
                    logger.error(f"Error message: {e}")
                    # Continue with next statement
        
        logger.info("Migration script executed successfully")
    except Exception as e:
        logger.error(f"Error executing migration script: {e}")
        conn.rollback()
    
    conn.close()

def execute_migration_manually(db_path):
    """
    Execute the migration manually, statement by statement.
    """
    logger.info(f"Executing manual migration on: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Turn off foreign keys
        cursor.execute("PRAGMA foreign_keys = OFF;")
        
        # Create temporary mapping table
        cursor.execute("""
            CREATE TEMP TABLE IF NOT EXISTS temp_do_mapping (
                cn_id INTEGER PRIMARY KEY,
                do_id INTEGER
            );
        """)
        
        # Migrate node types
        cursor.execute("""
            INSERT OR IGNORE INTO kddb_node_types (name)
            SELECT name FROM n_type;
        """)
        
        # Migrate feature types
        cursor.execute("""
            INSERT OR IGNORE INTO kddb_feature_types (name)
            SELECT name FROM f_type;
        """)
        
        # Create temporary table for node hierarchy
        cursor.execute("""
            CREATE TEMP TABLE node_levels (
                id INTEGER PRIMARY KEY,
                pid INTEGER,
                level INTEGER
            );
        """)
        
        # First insert root nodes (level 0)
        cursor.execute("""
            INSERT INTO node_levels (id, pid, level)
            SELECT id, pid, 0
            FROM cn
            WHERE pid IS NULL;
        """)
        
        # Insert level 1 nodes
        cursor.execute("""
            INSERT INTO node_levels (id, pid, level)
            SELECT c.id, c.pid, 1
            FROM cn c
            JOIN node_levels p ON c.pid = p.id
            WHERE p.level = 0;
        """)
        
        # Insert level 2+ nodes as needed
        cursor.execute("""
            INSERT INTO node_levels (id, pid, level)
            SELECT c.id, c.pid, 2
            FROM cn c
            JOIN node_levels p ON c.pid = p.id
            WHERE p.level = 1;
        """)
        
        # Create index for faster lookups
        cursor.execute("""
            CREATE INDEX node_levels_idx ON node_levels(level, id, pid);
        """)
        
        # First create all data objects in a single operation
        cursor.execute("""
            INSERT INTO kddb_data_objects (idx, deleted, created, modified)
            SELECT cn.idx, 0, datetime('now'), datetime('now')
            FROM cn;
        """)
        
        # Store mapping between content node IDs and data object IDs
        cursor.execute("""
            INSERT INTO temp_do_mapping (cn_id, do_id)
            SELECT cn.id, rowid
            FROM cn;
        """)
        
        # Update root node parent IDs
        cursor.execute("""
            UPDATE kddb_data_objects
            SET parent_id = NULL
            WHERE id IN (
                SELECT do_map.do_id
                FROM node_levels nl
                JOIN temp_do_mapping do_map ON nl.id = do_map.cn_id
                WHERE nl.level = 0
            );
        """)
        
        # Update child node parent references
        cursor.execute("""
            UPDATE kddb_data_objects
            SET parent_id = (
                SELECT parent_do.do_id
                FROM node_levels nl
                JOIN cn ON nl.id = cn.id
                JOIN temp_do_mapping parent_do ON cn.pid = parent_do.cn_id
                JOIN temp_do_mapping child_do ON cn.id = child_do.cn_id
                WHERE child_do.do_id = kddb_data_objects.id
                AND nl.level > 0
            );
        """)
        
        # Migrate content nodes
        cursor.execute("""
            INSERT INTO kddb_content_nodes (id, data_object_id, node_type, created, modified)
            SELECT cn.id, do_map.do_id, nt.name, datetime('now'), datetime('now')
            FROM cn
            JOIN temp_do_mapping do_map ON cn.id = do_map.cn_id
            JOIN n_type nt ON cn.nt = nt.id;
        """)
        
        # Migrate content node parts
        cursor.execute("""
            INSERT INTO kddb_content_node_parts (content_node_id, pos, content, content_idx)
            SELECT cn_id, pos, content, content_idx
            FROM cnp;
        """)
        
        # Migrate features
        cursor.execute("""
            INSERT INTO kddb_features (feature_type_id, content_node_id, data_object_id, single, tag_uuid)
            SELECT ft.f_type, ft.cn_id, do_map.do_id, ft.single, ft.tag_uuid
            FROM ft
            JOIN temp_do_mapping do_map ON ft.cn_id = do_map.cn_id;
        """)
        
        # Migrate feature binary data
        cursor.execute("""
            INSERT INTO kddb_feature_blob (feature_id, binary_value)
            SELECT id, binary_value
            FROM ft
            WHERE binary_value IS NOT NULL;
        """)
        
        # Migrate metadata if it exists
        cursor.execute("""
            INSERT OR IGNORE INTO kddb_metadata (id, metadata)
            SELECT id, metadata FROM metadata
            WHERE EXISTS(SELECT 1 FROM metadata);
        """)
        
        # Clean up temporary tables
        cursor.execute("DROP TABLE IF EXISTS temp_do_mapping;")
        cursor.execute("DROP TABLE IF EXISTS node_levels;")
        
        # Turn foreign keys back on
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        # Commit all changes
        conn.commit()
        
        logger.info("Manual migration executed successfully")
    except Exception as e:
        logger.error(f"Error executing manual migration: {e}")
        conn.rollback()
    finally:
        conn.close()

def test_migration(source_db, target_db=None, force_migration=True):
    """
    Test the migration from an old format database to the new kddb format.
    
    Args:
        source_db: Path to the source database file
        target_db: Path to the output database file (optional)
        force_migration: Whether to force migration using our script
    """
    if not os.path.exists(source_db):
        logger.error(f"Source database file {source_db} does not exist.")
        return False
    
    # Create a temporary copy of the database if target_db is not specified
    if target_db is None:
        target_db = source_db + ".new"
    
    # Copy the source database to the target location
    logger.info(f"Copying {source_db} to {target_db}")
    shutil.copy(source_db, target_db)
    
    # Analyze the database before migration
    logger.info("Database state before migration:")
    analyze_database(target_db)
    
    if force_migration:
        # First try with the migration script
        migrate_database(target_db)
        
        # Analyze the database after migration script
        logger.info("Database state after script migration:")
        analyze_database(target_db)
        
        # If the migration didn't work, try manual migration
        conn = sqlite3.connect(target_db)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM kddb_data_objects")
        count = cursor.fetchone()[0]
        conn.close()
        
        if count == 0:
            logger.info("Script migration didn't work, trying manual migration...")
            execute_migration_manually(target_db)
            
            # Analyze the database after manual migration
            logger.info("Database state after manual migration:")
            analyze_database(target_db)
    
    try:
        # Create a document object and point it to the copied database
        logger.info("Creating document from the database...")
        document = Document()
        
        # Initialize the persistence with the copied database
        persistence = SqliteDocumentPersistence(document, filename=target_db)
        
        # This will trigger automatic migration if needed
        logger.info("Initializing persistence (automatic migration will occur if needed)...")
        persistence.initialize()
        
        # Analyze the database after automatic migration
        logger.info("Database state after automatic migration:")
        analyze_database(target_db)
        
        # Print some statistics about the migrated document
        if document.content_node:
            logger.info(f"Root node type: {document.content_node.node_type}")
            children = document.content_node.get_children()
            logger.info(f"Number of child nodes: {len(children)}")
            
            # Print the structure of the document
            logger.info("Document structure:")
            def print_node(node, level=0):
                logger.info(f"{' ' * level}Node: {node.node_type} (ID: {node.id})")
                for child in node.get_children():
                    print_node(child, level + 2)
            
            print_node(document.content_node)
            
            # Check tags
            all_tags = persistence.get_all_tags()
            logger.info(f"Tags in document: {all_tags}")
            
            # Debug tag information
            logger.info("Running debug_tags to verify tag migration...")
            persistence.debug_tags()
        else:
            logger.warning("No content node found in the document after migration!")
        
        # Close the persistence to properly save changes
        persistence.close()
        
        logger.info(f"Migration completed. New database saved to {target_db}")
        return True
    
    except Exception as e:
        logger.error(f"Error during migration: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    # Get source database path from command line or use default
    source_db = sys.argv[1] if len(sys.argv) > 1 else "test_documents/fax2.kddb"
    
    # Get target database path from command line or use default
    target_db = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Determine whether to force migration
    force_migration = True if len(sys.argv) <= 3 or sys.argv[3].lower() != 'false' else False
    
    # Run the migration test
    success = test_migration(source_db, target_db, force_migration)
    
    if success:
        logger.info("Migration test completed successfully.")
    else:
        logger.error("Migration test failed.")
        sys.exit(1) 