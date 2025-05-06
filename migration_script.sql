-- Migration script to convert old schema to new kddb format
-- This script will migrate data from the old tables to the new "kddb_" prefixed tables

PRAGMA foreign_keys = OFF;
BEGIN TRANSACTION;

-- Check if we need to migrate
SELECT CASE 
    WHEN EXISTS(SELECT 1 FROM sqlite_master WHERE type='table' AND name='cn') 
    AND NOT EXISTS(SELECT 1 FROM kddb_content_nodes LIMIT 1)
    THEN 1 ELSE 0 END AS should_migrate;

-- Create temporary mapping table
CREATE TEMP TABLE IF NOT EXISTS temp_do_mapping (
    cn_id INTEGER PRIMARY KEY,
    do_id INTEGER
);

-- Migrate node types (n_type → kddb_node_types)
INSERT OR IGNORE INTO kddb_node_types (name)
SELECT name FROM n_type;

-- Migrate feature types (f_type → kddb_feature_types)
INSERT OR IGNORE INTO kddb_feature_types (name)
SELECT name FROM f_type;

-- Create temporary table for node hierarchy
CREATE TEMP TABLE node_levels (
    id INTEGER PRIMARY KEY,
    pid INTEGER,
    level INTEGER
);

-- First insert root nodes (level 0)
INSERT INTO node_levels (id, pid, level)
SELECT id, pid, 0
FROM cn
WHERE pid IS NULL;

-- Insert level 1 nodes
INSERT INTO node_levels (id, pid, level)
SELECT c.id, c.pid, 1
FROM cn c
JOIN node_levels p ON c.pid = p.id
WHERE p.level = 0;

-- Insert level 2 nodes
INSERT INTO node_levels (id, pid, level)
SELECT c.id, c.pid, 2
FROM cn c
JOIN node_levels p ON c.pid = p.id
WHERE p.level = 1;

-- Insert level 3 nodes
INSERT INTO node_levels (id, pid, level)
SELECT c.id, c.pid, 3
FROM cn c
JOIN node_levels p ON c.pid = p.id
WHERE p.level = 2;

-- Insert level 4 nodes
INSERT INTO node_levels (id, pid, level)
SELECT c.id, c.pid, 4
FROM cn c
JOIN node_levels p ON c.pid = p.id
WHERE p.level = 3;

-- Insert level 5 nodes
INSERT INTO node_levels (id, pid, level)
SELECT c.id, c.pid, 5
FROM cn c
JOIN node_levels p ON c.pid = p.id
WHERE p.level = 4;

-- Create an index to speed up lookups
CREATE INDEX node_levels_idx ON node_levels(level, id, pid);

-- First create all data objects in a single operation
INSERT INTO kddb_data_objects (idx, deleted, created, modified)
SELECT cn.idx, 0, datetime('now'), datetime('now')
FROM cn;

-- Store mapping between content node IDs and data object IDs
INSERT INTO temp_do_mapping (cn_id, do_id)
SELECT cn.id, rowid
FROM cn;

-- Update root node parent IDs
UPDATE kddb_data_objects
SET parent_id = NULL
WHERE id IN (
    SELECT do_map.do_id
    FROM node_levels nl
    JOIN temp_do_mapping do_map ON nl.id = do_map.cn_id
    WHERE nl.level = 0
);

-- Update child node parent references
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

-- Migrate content nodes
INSERT INTO kddb_content_nodes (id, data_object_id, node_type, created, modified)
SELECT cn.id, do_map.do_id, nt.name, datetime('now'), datetime('now')
FROM cn
JOIN temp_do_mapping do_map ON cn.id = do_map.cn_id
JOIN n_type nt ON cn.nt = nt.id;

-- Migrate content node parts
INSERT INTO kddb_content_node_parts (content_node_id, pos, content, content_idx)
SELECT cn_id, pos, content, content_idx
FROM cnp;

-- Migrate features
INSERT INTO kddb_features (feature_type_id, content_node_id, data_object_id, single, tag_uuid)
SELECT ft.f_type, ft.cn_id, do_map.do_id, ft.single, ft.tag_uuid
FROM ft
JOIN temp_do_mapping do_map ON ft.cn_id = do_map.cn_id;

-- Migrate feature binary data
INSERT INTO kddb_feature_blob (feature_id, binary_value)
SELECT id, binary_value
FROM ft
WHERE binary_value IS NOT NULL;

-- Migrate metadata if it exists
INSERT OR IGNORE INTO kddb_metadata (id, metadata)
SELECT id, metadata FROM metadata
WHERE EXISTS(SELECT 1 FROM metadata);

-- Clean up temporary tables
DROP TABLE IF EXISTS temp_do_mapping;
DROP TABLE IF EXISTS node_levels;

-- Update sequences to avoid primary key conflicts (only if sqlite_sequence exists)
UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM kddb_content_nodes) 
WHERE name = 'kddb_content_nodes'
AND EXISTS(SELECT 1 FROM sqlite_master WHERE type='table' AND name='sqlite_sequence');

UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM kddb_content_node_parts) 
WHERE name = 'kddb_content_node_parts'
AND EXISTS(SELECT 1 FROM sqlite_master WHERE type='table' AND name='sqlite_sequence');

UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM kddb_data_objects) 
WHERE name = 'kddb_data_objects'
AND EXISTS(SELECT 1 FROM sqlite_master WHERE type='table' AND name='sqlite_sequence');

UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM kddb_features) 
WHERE name = 'kddb_features'
AND EXISTS(SELECT 1 FROM sqlite_master WHERE type='table' AND name='sqlite_sequence');

UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM kddb_feature_blob) 
WHERE name = 'kddb_feature_blob'
AND EXISTS(SELECT 1 FROM sqlite_master WHERE type='table' AND name='sqlite_sequence');

PRAGMA foreign_keys = ON;
COMMIT; 