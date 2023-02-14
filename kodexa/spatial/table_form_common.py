import re

from kodexa import ContentNode
from kodexa.spatial.bbox_common import overlaps_with, width_of_overlap, percent_nodes_overlap
from typing import Optional, List, Dict, Tuple
import logging

logger = logging.getLogger()

OVERLAP_PERCENTAGE = 0.4
MIN_OVERLAP_PERCENTAGE_X = 0.2
MIN_OVERLAP_PERCENTAGE_Y = 0.4
COL_SPACE_MULTIPLIER = 2.0


def transform_line_to_columns(node, col_space_multiplier=3.0, col_marker_line=None,
                              use_graphical_nodes=False, graphic_slop=1.0):
    """
    Calculate the potential columns under this node and then transform the line to have
    a new set of nodes (type column).
    Note that this action will transform the document.

    :param node: The node that we want to transform to columns
    :param col_space_multiplier: Number of spaces between columns relative to the mean width of
    the characters on the page. Default is 3.0.
    :param col_marker_line: Line that dictates the positions of the columns. Default is None - which means the columns
    will be identified based on the spatial values of the nodes.
    :param use_graphical_nodes: If set to True, the graphical figures (lines and rects)
    that are identified on the page will be used to identify the columns of the table. Default is False.
    :param graphic_slop: The value of the slop allowed in lining up the nodes.
    Default is 1.0 which means it is +/- 1.0 of the mean character width of the line.
    This is only checked when use_graphical_nodes is set to True.

    """

    if node.node_type != 'line':
        return

    if node.get_children()[0].node_type == 'column':
        # This line has already been transformed to columns
        return

    # Grab graphic elements on the page
    page = node.select_first('parent::page')

    line_words = node.get_children().copy()
    mean_width = node.get_statistics()['updated_mean_width']

    # If col_markers is not None, use it to identify the words that belong to a column.
    # We identify the spaces by checking the overlap in the spaces
    insert_empty_col = False
    if col_marker_line:
        col_markers = col_marker_line.get_children().copy()
        column_words_index = []
        for cm_idx, cm in enumerate(list(col_markers)[0:-1]):
            # We are checking where the spaces overlap
            cm_bbox = cm.get_bbox()
            next_cm_bbox = col_markers[cm_idx + 1].get_bbox()

            # Identify the spaces that overlap and that the x2 of the word is after the next column_markers x
            gap_index_list = [i for i in range(1, len(line_words))
                              if (line_words[i - 1].get_bbox()[2] <= next_cm_bbox[0] < line_words[i].get_bbox()[2] and
                                  line_words[i].get_x() >= cm_bbox[2])]

            if len(gap_index_list) > 0:
                column_words_index.append(max(gap_index_list))
            else:
                # Identify the words that overlap - this is true for those columns that are 'inserted'
                # The 'overlap' should be 100% (meaning the words - with text - should be fully overlapping
                # with the empty-text column
                word_index_list = [i + 1 for i in range(0, len(line_words)) if
                                   (cm.get_all_content() == '' and cm_bbox[0] <= line_words[i].get_x() <
                                    line_words[i].get_bbox()[2] <= cm_bbox[2]) or
                                   (len(cm.get_all_content()) > 0 and
                                    (overlaps_with(line_words[i], cm) or
                                     line_words[i].get_bbox()[2] < next_cm_bbox[0]))]

                if len(word_index_list) > 0:
                    column_words_index.append(max(word_index_list))

    else:
        column_words_index = []

        for i in range(1, len(line_words)):
            is_break = False

            if use_graphical_nodes:
                is_break = check_graphical_nodes_break(page, graphic_slop, mean_width, line_words, i)

            elif line_words[i].get_x() - (line_words[i - 1].get_x() + line_words[i - 1].get_width()) >= \
                    col_space_multiplier * mean_width:
                is_break = True

            if is_break:
                column_words_index.append(i)

    # Insert 0 as the first index for column words; and len(node.words) as last
    column_words_index.insert(len(column_words_index), len(line_words))
    if 0 not in column_words_index:
        column_words_index.insert(0, 0)

    num_columns = 0
    new_columns = []
    for c_idx, n_idx in zip(column_words_index[:-1], column_words_index[1:]):
        column_words = []

        for i in range(c_idx, n_idx):
            column_words.append(line_words[i])

        # Create a new Column if there are column words
        if len(column_words) > 0:
            column_node = create_column_node_from_words(node.document, node, column_words)
            column_node.set_bbox_from_children()
            num_columns += 1
            new_columns.append(column_node)

    node.adopt_children(new_columns, replace=True)


def check_graphical_nodes_break(node, graphic_slop, mean_width, line_words, i):
    is_break = False
    graphical_nodes = node.select('//rect | //figure-line')

    x1 = (line_words[i - 1].get_x() + line_words[i - 1].get_width()) - (graphic_slop * mean_width)
    x2 = (line_words[i].get_x()) + (graphic_slop * mean_width)
    for node in graphical_nodes:

        # if line_words[i].get_y() + line_words[i].get_height() - (graphic_slop * mean_width) \
        #         <= node.get_y() + node.get_height() and \
        #         line_words[i].get_y() >= node.get_y() + (graphic_slop * mean_width):

        if x1 < node.get_bbox()[0] < x2:
            is_break = True
            original_bbox = line_words[i].get_bbox()
            original_bbox = [node.get_bbox()[0], original_bbox[1], original_bbox[2], original_bbox[3]]
            line_words[i].set_bbox(original_bbox)

            previous_bbox = line_words[i - 1].get_bbox()
            previous_bbox = [previous_bbox[0], previous_bbox[1], node.get_bbox()[0] - 0.01,
                             previous_bbox[3]]
            line_words[i - 1].set_bbox(previous_bbox)
        if x1 < node.get_bbox()[2] < x2:
            is_break = True
            original_bbox = line_words[i].get_bbox()
            original_bbox = [node.get_bbox()[2], original_bbox[1], original_bbox[2], original_bbox[3]]
            line_words[i].set_bbox(original_bbox)

            previous_bbox = line_words[i - 1].get_bbox()
            previous_bbox = [previous_bbox[0], previous_bbox[1], node.get_bbox()[2] - 0.01,
                             previous_bbox[3]]
            line_words[i - 1].set_bbox(previous_bbox)

    return is_break


def create_column_node_from_words(document, line, column_words):
    column_node = document.create_node(node_type='column')

    cw_first_bbox = column_words[0].get_bbox()
    cw_last_bbox = column_words[-1].get_bbox()
    column_node.set_bbox([cw_first_bbox[0], cw_first_bbox[1],
                          cw_last_bbox[2], cw_first_bbox[3]])

    column_node.adopt_children(column_words, replace=True)

    return column_node


def to_table(node, tag_name,
             col_space_multiplier=3.0, col_marker_line=None,
             insert_col_before=False, insert_col_after=False, insert_col_index=None,
             use_graphical_nodes=False, graphic_slop=1.0):
    """
    Uses a tag name to convert matching child nodes into tables
    If col_marker_line is given, it will be used to identify the number of columns
    in the table, with the col_space_multiplier.

    Note that this transforms the document - adding 'columns' as children of 'lines'.

    :param tag_name: The tag name used for the table rows
    :param col_space_multiplier: Number of spaces between columns relative to the mean width of
    the characters on the page. Default is 3.0.
    :param col_marker_line: Line that dictates the positions of the columns. Default is None - which means the columns
    will be identified based on the spatial values of the nodes.
    :param insert_col_before: If set to True, the code will insert an empty column header (col 0)
    based on col_marker_line. Default is False.
    :param insert_col_after: If set to True, the code will append an empty column header (last column)
    based on col_marker_line. Default is False.
    :param insert_col_index: Index where an empty column will be inserted in col_marker_line. Default is None.
    :param use_graphical_nodes: If set to True, th e graphical figures (lines and rects) that are identified on
    the page will be used to identify the columns of the table. Default is False.
    :param graphic_slop: The value of the slop allowed in lining up the nodes. Default is 1.0 which means it is
    +/- 1.0 of the mean character width of the line. This is only checked when use_graphical_nodes is set to True.
    """

    selector_str = "//*[hasTag('" + tag_name + "')]"
    transform_lines_to_table(node, tag_name, node.select(selector_str), col_space_multiplier=col_space_multiplier,
                             col_marker_line=col_marker_line, insert_col_before=insert_col_before,
                             insert_col_after=insert_col_after, insert_col_index=insert_col_index,
                             use_graphical_nodes=use_graphical_nodes, graphic_slop=graphic_slop)


def transform_lines_to_table(node, tag_name, table_lines,
                             col_space_multiplier=3.0, col_marker_line=None,
                             insert_col_before=False, insert_col_after=False,
                             insert_col_index=None,
                             use_graphical_nodes=False, graphic_slop=10):
    """
    Transforms each line into columns first and then groups them according to their positions.
    Note that this transforms the document.

    :param tag_name: The tag name used for the table rows
    :param table_lines: The lines that will be transformed into table
    :param col_space_multiplier: Number of spaces between columns relative to the mean width of
    the characters on the page. Default is 3.0.
    :param col_marker_line: Line that dictates the positions of the columns. Default is None - which means the columns
    will be identified based on the spatial values of the nodes.
    :param insert_col_before: If set to True, the code will insert an empty column header (col 0)
    based on col_marker_line. Default is False.
    :param insert_col_after: If set to True, the code will append an empty column header (last column)
    based on col_marker_line. Default is False.
    :param insert_col_index: Index where an empty column will be inserted in col_marker_line. Default is None.
    :param use_graphical_nodes: If set to True, th e graphical figures (lines and rects) that are identified on
    the page will be used to identify the columns of the table. Default is False.
    :param graphic_slop: The value of the slop allowed in lining up the nodes. Default is 1.0 which means it is
    +/- 1.0 of the mean character width of the line. This is only checked when use_graphical_nodes is set to True.
    """
    if len(table_lines) == 0:
        return

    # If col_marker_line is given, identify the column positions from this line
    if col_marker_line:
        transform_line_to_columns(col_marker_line, col_space_multiplier,
                                  use_graphical_nodes=use_graphical_nodes,
                                  graphic_slop=graphic_slop)

        if insert_col_before or insert_col_after or insert_col_index is not None:
            # Insert an empty column in col_marker_line
            insert_col_before_or_after(col_marker_line, insert_col_before, insert_col_after,
                                       insert_col_index, col_space_multiplier, use_graphical_nodes)

    # Check first if the line is not transformed to columns yet
    if table_lines[0].get_children()[0].node_type == 'word':
        transform_line_to_columns(table_lines[0], col_space_multiplier, col_marker_line,
                                  use_graphical_nodes=use_graphical_nodes,
                                  graphic_slop=graphic_slop)

    table = [] if col_marker_line else [table_lines[0].get_children().copy()]

    line_start_index = 0 if col_marker_line else 1
    for line in table_lines[line_start_index:]:
        # Check first if the line is not transformed to columns yet
        if line.get_children()[0].node_type == 'word':
            transform_line_to_columns(line, col_space_multiplier, col_marker_line,
                                      use_graphical_nodes=use_graphical_nodes,
                                      graphic_slop=graphic_slop)

        # Align the columns of this line with the rest from the table
        if col_marker_line:
            temp_line_columns = adjust_col_marker_line_columns(line, col_marker_line)
        else:
            temp_line_columns = adjust_table_line_columns(line, table, col_space_multiplier)
        table.append(temp_line_columns)

    # Update the bbox of each column nodes based on min_x1 and max_x2 for each column
    # If there is/are inserted columns in col_marker_line, we should only get the x1 and x2 of those columns with text
    min_x1_list = []
    max_x2_list = []
    for col_idx in range(len(table[0])):
        x1_list = [row[col_idx].get_bbox()[0] for row in table if len(row[col_idx].get_all_content()) > 0]
        x2_list = [row[col_idx].get_bbox()[2] for row in table if len(row[col_idx].get_all_content()) > 0]

        min_x1_list.append(min(x1_list) if x1_list else
                           col_marker_line.get_children()[col_idx].get_bbox()[0] if
                           col_marker_line and len(col_marker_line.get_children()) > col_idx else None)
        max_x2_list.append(max(x2_list) if x2_list else
                           col_marker_line.get_children()[col_idx].get_bbox()[2] if
                           col_marker_line and len(col_marker_line.get_children()) > col_idx else None)

        # Remove None if any
        min_x1_list = [x1 for x1 in min_x1_list if x1 is not None]
        max_x2_list = [x2 for x2 in max_x2_list if x2 is not None]

    # Need to add these table columns as children of each column line
    for row_index, table_row in enumerate(table):
        for col_idx, col in enumerate(table_row):
            # Tag each column
            col.tag(f"{tag_name}/col{col_idx}")
            col.set_bbox([min_x1_list[col_idx] if len(min_x1_list) > col_idx else col.get_bbox()[0],
                          col.get_bbox()[1],
                          max_x2_list[col_idx] if len(max_x2_list) > col_idx else col.get_bbox()[2],
                          col.get_bbox()[3]])

        table_line = table_lines[row_index]
        table_line.adopt_children(table_row, replace=True)


def insert_col_before_or_after(node, insert_col_before, insert_col_after, insert_col_index,
                               col_space_multiplier, use_graphical_nodes):
    # Insert (an) empty column/s in col_marker_line
    # insert_col_index is expected to be the index after column before/after is/are added

    new_columns = node.get_children()
    if insert_col_before:
        # First check if the empty column has already been inserted
        # Happens during the automatic table tagger (since the algo is run twice on the same document for testing)
        if not node.get_children()[0].get_all_content():
            return

        if use_graphical_nodes:
            # Adjust the column's x first
            graphical_nodes = [gn for gn in node.select('parent::page')[0].select('//rect | //figure-line')
                               if gn.get_bbox()[0] < node.get_x()]

            # Get the line with the max x from graphical_nodes
            max_x = max([gn.get_bbox()[0] for gn in graphical_nodes])
            first_col_node = node.get_children()[0]
            first_col_node.set_bbox([max_x, node.get_y(), first_col_node.get_bbox()[2], node.get_bbox()[3]])
            node.set_bbox([max_x, node.get_y(), node.get_bbox()[2], node.get_bbox()[3]])

        new_x2 = node.get_x() - 0.01 if use_graphical_nodes \
            else node.get_x() - col_space_multiplier * node.get_statistics()['updated_mean_width']
        column_node = node.document.create_node(node_type='column')
        column_node.set_bbox([0.0, node.get_y(), new_x2, node.get_bbox()[3]])
        new_columns.insert(0, column_node)

    if insert_col_after:
        if not node.get_children()[-1].get_all_content():
            return

        if use_graphical_nodes:
            # Adjust the column's x first
            graphical_nodes = [gn for gn in node.select('parent::page')[0].select('//rect | //figure-line')
                               if gn.get_bbox()[0] > node.get_bbox()[2]]

            # Get the line with the max x from graphical_nodes
            min_x = min([gn.get_bbox()[0] for gn in graphical_nodes])
            last_col_node = node.get_children()[-1]
            last_col_node.set_bbox([last_col_node.get_x(), node.get_y(), min_x, node.get_bbox()[3]])
            node.set_bbox([node.get_x(), node.get_y(), last_col_node.get_bbox()[2], node.get_bbox()[3]])

        # New bbox is from last node's x + page's width
        new_x1 = node.get_bbox()[2] + 0.01 if use_graphical_nodes \
            else node.get_bbox()[2] + col_space_multiplier * node.get_statistics()['updated_mean_width']
        column_node = node.document.create_node(node_type='column')
        column_node.set_bbox([new_x1, node.get_y(),
                              node.select_first('parent::page').get_bbox()[2], node.get_bbox()[3]])
        new_columns.append(column_node)

    if insert_col_index is not None and 0 < insert_col_index < len(new_columns) - 1:
        # First check if the empty column has already been inserted
        # Happens during the automatic table tagger (since the algo is run twice on the same document for testing)
        if not node.get_children()[insert_col_index].get_all_content():
            return

        # New bbox is +/- col_cpace_multiplier from the columns before and after
        bbox_before = node.get_children()[insert_col_index - 1].get_bbox()
        bbox_after = node.get_children()[insert_col_index].get_bbox()
        x1 = bbox_before[2]
        x2 = bbox_after[0]
        new_x1 = x1 + col_space_multiplier * node.get_statistics()['updated_mean_width']
        new_x2 = x2 - col_space_multiplier * node.get_statistics()['updated_mean_width']
        column_node = node.document.create_node(node_type='column')
        column_node.set_bbox([new_x1, node.get_y(),
                              new_x2, node.get_bbox()[3]])

        new_columns.insert(insert_col_index, column_node)

    node.adopt_children(new_columns, replace=True)
    node.set_bbox_from_children()


def adjust_col_marker_line_columns(node, col_marker_line):
    # Check the other rows of the table if they align with the ref columns
    line_columns = node.get_children().copy()
    ref_columns = col_marker_line.get_children().copy()
    temp_line_columns = []
    ref_col_idx = 0

    if len(line_columns) == len(ref_columns):
        for line_index, line_col in enumerate(line_columns):
            ref_col = ref_columns[line_index]
            temp_line_columns.append(line_col)
            update_bbox_for_columns(ref_col, temp_line_columns[-1], update_col1=False)
        return temp_line_columns

    for line_col_idx, line_col in enumerate(line_columns):
        line_col_bbox = line_col.get_bbox()
        while ref_col_idx < len(ref_columns):
            ref_col = ref_columns[ref_col_idx]

            if (overlaps_with(line_col, ref_col) or line_col.get_x() < ref_col.get_x()) and \
                    ((ref_col_idx + 1 == len(ref_columns) or
                      (ref_col_idx + 1 < len(ref_columns) and (
                              not overlaps_with(line_col, ref_columns[ref_col_idx + 1]) or
                              width_of_overlap(line_col, ref_col) > width_of_overlap(line_col,
                                                                                     ref_columns[ref_col_idx + 1]))))):
                # If line_col overlaps with ref_col and line_col does not overlap with the next one
                temp_line_columns.append(line_col)
                update_bbox_for_columns(ref_col, temp_line_columns[-1], update_col1=False)
                ref_col_idx += 1
                break
            elif ref_col_idx + 1 < len(ref_columns) and \
                    not (overlaps_with(line_col, ref_columns[ref_col_idx + 1])) and \
                    line_col.get_x() + line_col.get_width() < ref_columns[ref_col_idx + 1].get_x():
                # If line_col does not overlap with the next ref_col but its x is less than the next ref_col's x,
                # then line_col lines up with ref_col
                temp_line_columns.append(line_col)
                update_bbox_for_columns(ref_col, temp_line_columns[-1], update_col1=False)
                ref_col_idx += 1
                break
            elif ref_col_idx == len(ref_columns) - 1 and \
                    line_col.get_x() > ref_columns[ref_col_idx].get_x() + ref_columns[ref_col_idx].get_width():
                # If line_col is after the last ref_col, then line_col lines up with ref_col
                temp_line_columns.append(line_col)
                update_bbox_for_columns(ref_col, temp_line_columns[-1], update_col1=False)
                ref_col_idx += 1
                break
            else:
                # Else, Insert an empty column node in temp_line_columns,
                # then check the next ref_col
                column_node = node.document.create_node(node_type='column')
                # Need to get the y values from this row
                ref_col_bbox = ref_col.get_bbox()
                column_node.set_bbox([ref_col_bbox[0], line_col_bbox[1],
                                      ref_col_bbox[2], line_col_bbox[3]])
                temp_line_columns.insert(ref_col_idx, column_node)
                ref_col_idx += 1

    while ref_col_idx < len(ref_columns):
        # Need to add columns since there are more columns in col_marker_line than this line
        ref_col = ref_columns[ref_col_idx]
        ref_col_bbox = ref_col.get_bbox()
        column_node = node.document.create_node(node_type='column')
        column_node.set_bbox([ref_col_bbox[0], line_col_bbox[1],
                              ref_col_bbox[2], line_col_bbox[3]])
        temp_line_columns.insert(ref_col_idx, column_node)
        ref_col_idx += 1

    return temp_line_columns


def adjust_table_line_columns(node, table, col_space_multiplier):
    # Check the other rows of the table if they align with the ref columns
    line_columns = node.get_children().copy()
    ref_columns = table[0]
    temp_line_columns = []  # If there are ones to combine
    ref_col_idx = 0
    overlap_found = False
    mean_width = node.get_statistics()['updated_mean_width']

    for line_col_idx, line_col in enumerate(line_columns):
        line_col_bbox = line_col.get_bbox()
        while ref_col_idx < len(ref_columns):
            ref_col = ref_columns[ref_col_idx]

            if overlaps_with(line_col, ref_col) or \
                    abs(ref_col.get_x() - line_col.get_x()) <= col_space_multiplier * mean_width:
                # If line_col overlaps with ref_col or it is within the allowed col_space_multiplier
                # Check if there are already columns that overlap with this index
                if len(temp_line_columns) > ref_col_idx:
                    # Extend the x value to cover both nodes
                    column_node = temp_line_columns[ref_col_idx]
                    for child in line_col.get_children().copy():
                        column_node.add_child(child)

                    column_node_bbox = column_node.get_bbox()
                    column_node.set_bbox([column_node_bbox[0], column_node_bbox[1],
                                          line_col_bbox[2], line_col_bbox[3]])
                    temp_line_columns[ref_col_idx] = column_node
                    if ref_col_idx < len(ref_columns) - 1 and \
                            overlaps_with(column_node, ref_columns[ref_col_idx + 1]):
                        update_bbox_for_columns(ref_col, temp_line_columns[ref_col_idx], update_col1=False)
                    else:
                        update_bbox_for_columns(ref_col, temp_line_columns[ref_col_idx], update_col1=True)

                else:
                    temp_line_columns.append(line_col)
                    update_bbox_for_columns(ref_col, temp_line_columns[-1], update_col1=True)

                overlap_found = True
                break

            # Do not overlap
            elif line_col.get_x() < ref_col.get_x():
                # Check if the line_col's x is before ref_col's x
                # Insert an 'empty' column node in all the rows in the table,
                # then check the next line_col
                for row in table:
                    # Need to get the y values from this row
                    column_node = node.document.create_node(node_type='column')
                    row0_bbox = row[0].get_bbox()
                    column_node.set_bbox([line_col_bbox[0], row0_bbox[1],
                                          line_col_bbox[2], row0_bbox[3]])
                    row.insert(ref_col_idx, column_node)

                # Add the line_col to temp_line_columns
                temp_line_columns.append(line_col)

                # Updating ref_col_idx since we inserted a column
                ref_col_idx += 1
                overlap_found = False
                break

            # Check if the line_col's x is after ref_col's x + width
            elif line_col.get_x() > ref_col.get_x() + ref_col.get_width() + col_space_multiplier * mean_width:
                if ref_col_idx == len(ref_columns) - 1:
                    if overlap_found:
                        # These are extra columns
                        temp_line_columns.append(line_col)
                        # Append an empty column node to all the rows in the table
                        for row in table:
                            column_node = node.document.create_node(node_type='column')
                            # Need to get the y values from this row
                            row0_bbox = row[0].get_bbox()
                            column_node.set_bbox([line_col_bbox[0], row0_bbox[1],
                                                  line_col_bbox[2], row0_bbox[3]])
                            row.append(column_node)

                        ref_col_idx += 1
                        overlap_found = True
                        break

                    elif line_col_idx == len(line_columns) - 1:
                        # This is the last index, put line_col in the last index
                        temp_line_columns.append(line_col)

                        overlap_found = True
                        break

                    else:
                        # We will not break since we want to keep this line_col
                        # This is not the last col for line columns so we will just say overlap is found
                        # since we have already seen all the ref_cols
                        # Insert an empty column in temp_line_columns
                        column_node = node.document.create_node(node_type='column')
                        # Need to get the y values from this row
                        ref_col_bbox = ref_col.get_bbox()
                        column_node.set_bbox([ref_col_bbox[0], line_col_bbox[1],
                                              ref_col_bbox[2], line_col_bbox[3]])
                        temp_line_columns.insert(ref_col_idx, column_node)

                        overlap_found = True

                elif overlap_found:
                    # If overlap is found for ref_col, move on to the next ref_col
                    ref_col_idx += 1
                    overlap_found = False

                else:
                    # Else, Insert an empty column node in temp_line_columns,
                    # then check the next ref_col
                    column_node = node.document.create_node(node_type='column')
                    # Need to get the y values from this row
                    ref_col_bbox = ref_col.get_bbox()
                    column_node.set_bbox([ref_col_bbox[0], line_col_bbox[1],
                                          ref_col_bbox[2], line_col_bbox[3]])
                    ref_col_idx += 1
                    temp_line_columns.insert(ref_col_idx, column_node)
                    overlap_found = False

            # Append this column_node (with the right text) to temp_line_columns
            else:
                temp_line_columns.append(line_col)
                ref_col_idx += 1
                overlap_found = False

    for idx in range(len(ref_columns) - len(temp_line_columns)):
        # If there are less columns in the given line compared to the reference
        column_node = node.document.create_node(node_type='column')
        # Put a high x1 so it does not get read as a min
        # Put a low x2 so it does not get read as a max
        column_node.set_bbox([10000.00, line_col_bbox[1],
                              0.00, line_col_bbox[3]])
        temp_line_columns.append(column_node)

    return temp_line_columns


def update_bbox_for_columns(col1, col2, update_col1=True):
    """
    Updates the bounding box of the columns when lining them up in a table
    :param col1:  column 1
    :param col2: column 2
    :param update_col1: if set to False, only col2's bbox will be updated. Default is True.
    """
    # Set the bounding box to cover the min x1 and max x2
    min_x1 = min(col1.get_bbox()[0], col2.get_bbox()[0])
    max_x2 = max(col1.get_bbox()[2], col2.get_bbox()[2])

    if update_col1:
        col1_new_bbox = [min_x1, col1.get_bbox()[1], max_x2, col1.get_bbox()[3]]
        col1.set_bbox(col1_new_bbox)

    col2_new_bbox = [min_x1, col2.get_bbox()[1], max_x2, col2.get_bbox()[3]]
    col2.set_bbox(col2_new_bbox)


class DataMarker:
    data_marker_text: Optional[str] = ''
    data_marker_text_re: Optional[str] = ''
    data_marker_bbox: Optional[List[float]]
    data_value_bbox: Optional[List[float]]
    data_value_direction: Optional[str] = ''
    data_type: Optional[str] = ''


def get_data_marker_column_and_index(data_marker_line: ContentNode, data_marker: DataMarker):
    # Get column and column index where the data marker is and the column overlaps with the marker (x-axis)
    try:
        column_index = [col_idx for col_idx, column in enumerate(data_marker_line.select('//column'))
                        if re.match(f'(?i){data_marker.data_marker_text_re}', column.get_all_content()) and
                        percent_nodes_overlap(column.get_bbox(), data_marker.data_marker_bbox,
                                              axis_overlap='x') >= MIN_OVERLAP_PERCENTAGE_X][0]

    except IndexError:
        return None, None

    return data_marker_line.select('//column')[column_index], column_index


def data_marker_overlaps_with_target_marker(data_marker_line_bbox, data_word_bbox, target_data_marker: DataMarker,
                                            overlap_percentage=OVERLAP_PERCENTAGE):
    # Checks that data_marker_line overlaps with the bbox provided in the template
    template_data_marker_bbox = target_data_marker.data_marker_bbox
    template_data_value_bbox = target_data_marker.data_value_bbox
    return (percent_nodes_overlap(data_marker_line_bbox, template_data_marker_bbox, 'x') >= overlap_percentage
            and percent_nodes_overlap(data_word_bbox, template_data_value_bbox, 'x') >= overlap_percentage)


def get_column_below_or_above_data(data_marker_line: ContentNode, data_marker: DataMarker,
                                   target_lines: List[ContentNode],
                                   col_space_multiplier=2.0, column_direction='column_below'):
    data_marker_line_index = target_lines.index(data_marker_line)
    logger.info("get_column_below_or_above_data: %s", data_marker)

    # Can't get a next line
    if len(target_lines) <= data_marker_line_index:
        logger.info(f'No next line for data marker {data_marker.data_marker_text_re} in line {data_marker_line_index}')
        return None

    # Check if the next line overlaps with the y value of data_value_bbox)
    # Make the words as children again of this line
    for count in range(1, 4):
        if len(target_lines) <= data_marker_line_index + count:
            return None
        try:
            next_line = target_lines[data_marker_line_index + count] if column_direction == 'column_below' \
                else target_lines[data_marker_line_index - count]
        except IndexError:
            return None

        # Do not set col_marker_line since the line where the marker is does not guarantee the correct column markers
        [line.adopt_children(line.select('//word'), replace=True) for line in [data_marker_line, next_line]]
        [transform_line_to_columns(tl, col_space_multiplier=col_space_multiplier) for tl in
         [data_marker_line, next_line]]

        column, column_index = get_data_marker_column_and_index(data_marker_line, data_marker)
        if column_index is None:
            return None

        try:
            column_below = [col for col in next_line.select('//column')
                            if percent_nodes_overlap(column.get_bbox(), col.get_bbox(),
                                                     axis_overlap='x') >= 0.4][0]
        except IndexError:
            logger.info("No column below found")
            column_below = None

        if column and column_below and column_below.get_all_content() and \
                data_marker_overlaps_with_target_marker(column.get_bbox(), column_below.get_bbox(), data_marker):
            # This is the data found in the data_marker_line
            return column_below

    return None
