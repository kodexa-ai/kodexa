import errno
import logging
from typing import Dict, cast

from kodexa import PipelineContext, TableDataStore, Document, ContentNode

logger = logging.getLogger('kodexa.testing')


def print_data_table(context: PipelineContext, store_name: str):
    """
    A small helper to support working with a store in a test

    :param context:
    :param store_name:
    :return:
    """
    if store_name in context.get_store_names():
        print(f"\n{store_name}\n")
        data_table = cast(TableDataStore, context.get_store(store_name))
        from texttable import Texttable
        table = Texttable(max_width=1000).header(data_table.columns)
        table.add_rows(data_table.rows, header=False)
        print(table.draw() + "\n")
    else:
        print(f"\n{store_name} - MISSING\n")


def snapshot_store(context: PipelineContext, store_name: str, filename: str):
    """
    Capture the data in a store to a JSON file so that we can use it later
    to compare the data (usually in a test)

    :param context: the pipeline context
    :param store_name: the name of the store
    :param filename: the name of the file to snapshot the store to
    """
    import json
    logger.warning('Snapshotting store')
    with open(filename, 'w') as f:
        json.dump(context.get_store(store_name).to_dict(), f)


def simplify_node(node: ContentNode):
    return {
        "index": node.index,
        "node_type": node.node_type,
        "features": [feature.to_dict() for feature in node.get_features()],
        "content": node.content,
        "content_parts": node.content_parts,
        "children": [simplify_node(child_node) for child_node in node.children]
    }


def simplify_document(document: Document) -> Dict:
    return {
        "content_node": simplify_node(document.get_root())
    }


def compare_document(document: Document, filename: str, throw_exception=True):
    from os import path
    import json
    import os

    try:
        os.makedirs('test_snapshots')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    filename = "test_snapshots/" + filename

    if not path.exists(filename):
        with open(filename, 'w') as f:
            simplified_document = simplify_document(document)
            json.dump(simplified_document, f)

        logger.warning("WARNING!!! Creating snapshot file")
        raise Exception("Creating snapshot, invalid test")

    with open(filename) as f:
        snapshot_document = json.load(f)

    target_document = json.loads(json.dumps(simplify_document(document)))

    from deepdiff import DeepDiff
    diff = DeepDiff(snapshot_document, target_document, ignore_order=False)

    if bool(diff) and throw_exception:
        print(diff)
        raise Exception('Document does not match')

    return diff


def compare_store(context: PipelineContext, store_name: str, filename: str, throw_exception=True):
    """
    Compare a store in the provided pipeline context to the store that has been snapshot

    :param context: the pipeline context containing the store to compare
    :param store_name: the name of the store
    :param filename: the filename of the
    :param throw_exception: throw an exception if there is a mismatch
    """

    from os import path

    import os
    try:
        os.makedirs('test_snapshots')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    filename = "test_snapshots/" + filename

    if not path.exists(filename):
        snapshot_store(context, store_name, filename)
        logger.warning("WARNING!!! Creating snapshot file")
        raise Exception("Creating snapshot, invalid test")

    import json

    # A list of the descriptions of issues
    issues = []

    target_table_store: TableDataStore = cast(TableDataStore, context.get_store(store_name))

    if target_table_store is None:
        print(f"Store {store_name} doesn't exist in the pipeline context")
        return False

    with open(filename) as f:
        snapshot_table_store = TableDataStore.from_dict(json.load(f))

    row_match = len(target_table_store.rows) == len(snapshot_table_store.rows)

    if not row_match:
        issues.append(
            f"Number of rows don't match {len(target_table_store.rows)} is target vs {len(snapshot_table_store.rows)} in snapshot")
    else:
        for row_idx, row in enumerate(target_table_store.rows):
            for cell_idx, cell in enumerate(row):
                if snapshot_table_store.rows[row_idx][cell_idx] != target_table_store.rows[row_idx][cell_idx]:
                    issues.append(
                        f"Row {row_idx} cell {cell_idx} doesn't match - should be [{snapshot_table_store.rows[row_idx][cell_idx]}] but is [{target_table_store.rows[row_idx][cell_idx]}]")

    col_match = len(target_table_store.columns) == len(snapshot_table_store.columns)

    if not col_match:
        issues.append(
            f"Number of columns don't match {len(target_table_store.columns)} is target vs {len(snapshot_table_store.columns)} in snapshot")
    else:
        for col_idx, col in enumerate(target_table_store.columns):
            if snapshot_table_store.columns[col_idx] != col:
                issues.append(
                    f"Column name at index {col_idx} doesn't match - should be [{snapshot_table_store.columns[col_idx]}] but is [{col}]")

    if len(issues) > 0 and throw_exception:
        raise Exception("\n".join(issues))

    for issue in issues:
        print(issue)

    return len(issues) == 0
