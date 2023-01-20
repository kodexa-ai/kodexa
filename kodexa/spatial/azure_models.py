import numpy as np
from kodexa import Document
from kodexa.spatial.bbox_common import percent_nodes_overlap

KDXA_BBOX_KEY = 'kodexa_bbox'


def create_page_node_keep_azure_lines(document, page_node, azure_page, overlap_percentage=0.6):
    page_node = document.create_node("content-area", parent=page_node)
    page_node.set_bbox([0, 0, azure_page['width'], azure_page['height']])

    # Now check all the lines identified by Form Recognizer
    all_words = get_azure_page_words(azure_page)

    included_words = []
    word_index = 0
    for line_index, line in enumerate(azure_page['lines']):
        # Create the line and set bbox
        line_node = document.create_node("line", parent=page_node)
        line_node.set_bbox(convert_azure_bbox(line, azure_page))
        line_words = []
        while True and word_index < len(all_words):
            if azure_kdxa_nodes_overlap(all_words[word_index], line_node, azure_page, overlap_percentage):
                line_words.append(all_words[word_index])
                included_words.append(all_words[word_index])
                word_index += 1
            else:
                break

        for word in line_words:
            word_node = document.create_node("word", parent=line_node)
            word_node.set_bbox(convert_azure_bbox(word, azure_page))
            word_node.set_content_parts([word['content']])

    # No issue
    return False


def create_kddb_from_azure(azure_data, keep_azure_lines=True, overlap_percentage=0.6):
    """

    :param azure_data: dictionary of the json data returned by Azure
    :param keep_azure_lines: If set to False, the lines returned will match how Kodexa put lines together.
    Default is True - keeping how Azure creates lines.
    :param overlap_percentage: the percentage of overlap for nodes to be considered on the same line (from 0.0 to 1.0)
    Default is 0.6.
    :return: kddb document with the content nodes
    """
    # This restores the lines provided by Azure (not matching Kodexa)
    if not azure_data:
        return None

    # Create an empty document
    document = Document()
    root_node = document.create_node("root")

    for page_index, azure_page in enumerate(azure_data['analyzeResult']['pages']):
        page_node = document.create_node("page", parent=root_node)
        page_node.set_bbox([0, 0, azure_page['width'], azure_page['height']])
        if 'angle' in azure_page.keys() and azure_page['angle'] is not None:
            page_node.add_feature('page', 'angle', azure_page['angle'])

        # Create the kddb document (keeping Azure lines or matching them with Kodexa lines)
        issue_found = create_page_node_keep_azure_lines(document, page_node, azure_page,
                                                        overlap_percentage=overlap_percentage) \
            if keep_azure_lines else create_page_node_line_up_kodexa(document, page_node, azure_page)

        if issue_found:
            return None

    document.content_node = root_node
    document.add_mixin('spatial')

    return document


def create_page_node_line_up_kodexa(document, page_node, azure_page):
    # Group Azure's OCR words into lines to match how Kodexa sees lines
    content_area_node = document.create_node("content-area", parent=page_node)
    content_area_node.set_bbox([0, 0, azure_page['width'], azure_page['height']])

    line_groups = group_azure_lines_to_kodexa_lines(azure_page)
    azure_page_words = get_azure_page_words(azure_page)
    already_added_azure_words = []

    for line_group_index, line_group in enumerate(line_groups):
        # Sort words in word_group based on x
        line_group = sorted(line_group, key=lambda d: d[KDXA_BBOX_KEY][0])

        # Create the line and set bbox
        line_node = document.create_node("line", parent=content_area_node)

        char_count = 0
        chars_total_width = 0.0

        for azure_line in line_group:
            # Now create a line for each line_group and get the words
            try:
                azure_line_words = azure_line['words']
            except KeyError:
                # The azure line does not contain the words in the metadata - so we have to find them
                azure_line_words = get_azure_line_words(azure_line, azure_page, azure_page_words,
                                                        already_added_azure_words)

            if not azure_line_words:
                continue

            for word in azure_line_words:
                word_node = document.create_node("word", parent=line_node)
                word_node.set_bbox(convert_azure_bbox(word, azure_page))

                if 'confidence' in word.keys():
                    word_node.add_feature('azure', 'confidence', word['confidence'])

                word_node.set_content_parts([word['content']])
                chars_total_width += word_node.get_width()
                char_count += len(word['content'])

        line_node.set_bbox_from_children()
        if char_count > 0:
            line_node.set_statistics({'updated_mean_width': chars_total_width / char_count})
        else:
            line_node.set_statistics({'updated_mean_width': 0.0})

    # This is a good kddb document (no issue)
    return False


def get_azure_line_words(azure_line, azure_page, azure_page_words, already_added_azure_words):
    azure_line_words = []
    word_texts = azure_line['content'].split()
    for wt in word_texts:
        try:
            word = [w for w in azure_page_words if w['content'] == wt and
                    azure_nodes_overlap(w, azure_line, azure_page) and w not in already_added_azure_words][0]
        except IndexError:
            print('Issue with converting Azure lines to Kodexa lines')
            continue

        # Add this word as it has already been found
        already_added_azure_words.append(word)

        # line words to return
        azure_line_words.append(word)

    return azure_line_words


def get_azure_page_words(azure_page):
    if 'words' in azure_page.keys():
        page_words = azure_page['words']
    else:
        page_lines = azure_page['lines']
        page_words = []
        [page_words.extend(pl['words']) for pl in page_lines]
        for pw in page_words:
            pw['content'] = pw['text']

    return page_words


def get_azure_next_line(document_lines, ref_line, direction='right', overlap_percentage=0.6):
    if ref_line not in document_lines:
        return None

    ref_bbox = ref_line.get_bbox()
    possible_lines = document_lines[max(document_lines.index(ref_line) - 25, 0):
                                    min(document_lines.index(ref_line) + 25, len(document_lines))]

    if direction == 'right':
        # Get all the lines to the right of the cell, where the y overlaps; and sort according to x
        right_lines = [right_line for right_line in possible_lines
                       if right_line.get_bbox()[0] >= ref_bbox[2] and
                       percent_nodes_overlap(ref_bbox, right_line.get_bbox(), 'y') >= overlap_percentage]

        if not right_lines:
            return None

        # Sort by x (increasing)
        sorted_next_right_lines = [right_lines[0]]
        [sorted_next_right_lines.insert(0, right_line) for right_line in right_lines
         if right_line.get_bbox()[0] < sorted_next_right_lines[0].get_bbox()[0]]

        return sorted_next_right_lines[0]

    elif direction == 'left':
        # Get all the lines to the left of the cell, where the y overlaps; and sort according to x2 (decreasing)
        left_lines = [left_line for left_line in possible_lines
                      if left_line.get_bbox()[2] <= ref_bbox[0] and
                      percent_nodes_overlap(ref_bbox, left_line.get_bbox(), 'y') >= overlap_percentage]

        if not left_lines:
            return None

        # Sort by x (decreasing)
        sorted_next_left_lines = [left_lines[0]]
        [sorted_next_left_lines.insert(0, left_line) for left_line in left_lines
         if left_line.get_bbox()[0] > sorted_next_left_lines[0].get_bbox()[0]]

        return sorted_next_left_lines[0]

    elif direction == 'down':
        # Get all the lines below of the cell, where the x overlaps; and sort according to y
        down_lines = [down_line for down_line in possible_lines if
                      down_line.get_bbox()[3] <= ref_bbox[1] and
                      percent_nodes_overlap(ref_bbox, down_line.get_bbox(), 'x') >= overlap_percentage]

        if not down_lines:
            return None

        # Sort by y (increasing since 0 is at the bottom of the page)
        sorted_next_down_lines = [down_lines[0]]
        [sorted_next_down_lines.insert(0, down_line) for down_line in down_lines
         if down_line.get_bbox()[1] > sorted_next_down_lines[0].get_bbox()[1]]

        return sorted_next_down_lines[0]

    elif direction == 'up':
        # Get all the lines above of the cell, where the x overlaps; and sort according to y
        up_lines = [up_line for up_line in possible_lines if
                    up_line.get_bbox()[1] >= ref_bbox[3] and
                    percent_nodes_overlap(ref_bbox, up_line.get_bbox(), 'x') >= overlap_percentage]

        if not up_lines:
            return None

        # Sort by y (decreasing since 0 is at the bottom of the page)
        sorted_next_up_lines = [up_lines[0]]
        [sorted_next_up_lines.insert(0, up_line) for up_line in up_lines
         if up_line.get_bbox()[1] < sorted_next_up_lines[0].get_bbox()[1]]

        return sorted_next_up_lines[0]

    return None


def group_azure_lines_to_kodexa_lines(page):
    # Group the azure lines into Kodexa lines
    # Each line group is a list of lines
    page_lines = page['lines']
    if not page_lines:
        return []

    # Convert Azure lines into Kodexa lines
    line_heights = []
    char_widths = []

    for page_line in page_lines:
        page_line[KDXA_BBOX_KEY] = convert_azure_bbox(page_line, page)
        page_line['content'] = page_line['content'] if 'content' in page_line.keys() \
            else page_line['text'] if 'text' in page_line.keys() else None

    # heights = np.array([page_line[KDXA_BBOX_KEY][3] - page_line[KDXA_BBOX_KEY][1] for page_line in page_lines])
    # stdev_height = np.std(heights)
    #
    # # Get the lines with height above the standard deviation
    # lines_to_separate = [page_lines[i] for i in range(len(line_heights)) if line_heights[i] >= stdev_height]
    lines_to_separate = []
    # # Initialize line_groups
    # line_groups = [[line] for line in lines_to_separate]
    line_groups = []

    # Sort the remaining page_lines by y1
    lines_to_sort = sorted([page_line for page_line in page_lines if page_line not in lines_to_separate],
                           key=lambda d: d[KDXA_BBOX_KEY][1], reverse=True)

    line_groups.extend(check_azure_line_group(lines_to_sort))

    # Need to sort the line_groups based on y
    line_groups.sort(key=lambda line_group: [line[KDXA_BBOX_KEY][1] for line in line_group], reverse=True)
    return line_groups


def get_bbox_of_line_group(line_group):
    if not line_group:
        return None

    # Gets the bounding box of the line_group
    x1_values = [line[KDXA_BBOX_KEY][0] for line in line_group]
    y1_values = [line[KDXA_BBOX_KEY][1] for line in line_group]
    x2_values = [line[KDXA_BBOX_KEY][2] for line in line_group]
    y2_values = [line[KDXA_BBOX_KEY][3] for line in line_group]

    return [min(x1_values), min(y1_values), max(x2_values), max(y2_values)]


def page_line_overlaps_with_line_group(page_line_dict, line_group, next_line_group,
                                       axis_overlap='y', min_overlap_percentage_y=0.4):
    page_line_dict_bbox = page_line_dict[KDXA_BBOX_KEY]
    # line_group_bbox = get_bbox_of_line_group(line_group)
    # next_line_group_bbox = get_bbox_of_line_group(next_line_group)
    line_group_bbox = line_group[-1][KDXA_BBOX_KEY]
    next_line_group_bbox = next_line_group[-1][KDXA_BBOX_KEY] if next_line_group else None

    if next_line_group:
        # Check if page_line_dict overlaps with both line_group and next_line_group
        # If it does, only return true if the overlap is more for line_group than next_line_group
        line_group_overlap = percent_nodes_overlap(page_line_dict_bbox, line_group_bbox, axis_overlap=axis_overlap)
        next_line_group_overlap = percent_nodes_overlap(page_line_dict_bbox, next_line_group_bbox,
                                                        axis_overlap=axis_overlap)
        if line_group_overlap >= min_overlap_percentage_y and \
                next_line_group_overlap >= min_overlap_percentage_y and \
                node_heights_are_valid(page_line_dict_bbox, line_group) and \
                node_heights_are_valid(page_line_dict_bbox, next_line_group):
            return page_line_dict[KDXA_BBOX_KEY][0] - line_group_bbox[0] < \
                page_line_dict[KDXA_BBOX_KEY][0] - next_line_group_bbox[0]
        elif line_group_overlap >= min_overlap_percentage_y and \
                node_heights_are_valid(page_line_dict_bbox, line_group):
            return True
        else:
            return False
    else:
        return percent_nodes_overlap(page_line_dict_bbox, line_group_bbox, axis_overlap=axis_overlap) \
            >= min_overlap_percentage_y and \
            node_heights_are_valid(page_line_dict_bbox, line_group)


def node_heights_are_valid(new_bbox, line_group):
    # The font size/height of the nodes should be within 60% of each other
    # Get the min_height and max_height of each line
    # return True
    height_values = [line[KDXA_BBOX_KEY][3] - line[KDXA_BBOX_KEY][1] for line in line_group]
    min_height = min(height_values)
    max_height = max(height_values)
    new_height = new_bbox[3] - new_bbox[1]
    return min(new_height, min_height) / max(new_height, min_height) >= 0.55 or \
        min(new_height, max_height) / max(new_height, max_height) >= 0.55


def check_azure_line_group(original_line_group):
    # Confirms that the azure lines in this group do not overlap on the x-axis.
    # If they do, then we break down this line group into multiple groups
    if not original_line_group:
        return []

    # Sort the lines in original_line_group by x
    original_line_group = sorted(original_line_group, key=lambda d: d[KDXA_BBOX_KEY][0])

    line_groups = [[original_line_group[0]]]
    for azure_line in original_line_group[1:]:
        line_group_inserted = False
        for lg_index, line_group in enumerate(line_groups):
            # If the azure line does not x-overlap with this line group, check if they y-overlap (+/- 0.1)
            if (azure_line[KDXA_BBOX_KEY][0] >= line_group[-1][KDXA_BBOX_KEY][2] - 0.1 or
                azure_line[KDXA_BBOX_KEY][2] <= line_group[0][KDXA_BBOX_KEY][0] + 0.1) and \
                    page_line_overlaps_with_line_group(azure_line, line_group,
                                                       line_groups[lg_index + 1] if lg_index + 1 < len(line_groups)
                                                       else None):
                line_group.append(azure_line)
                line_group_inserted = True
                break

        if line_group_inserted:
            continue

        line_groups.append([azure_line])
        line_groups.sort(key=lambda line_group: [line[KDXA_BBOX_KEY][1] for line in line_group], reverse=True)

    return line_groups


def convert_azure_bbox(azure_obj, azure_page):
    # boundingBox has 8 points
    if 'boundingBox' in azure_obj:
        bbox_points = azure_obj['boundingBox']
    elif 'bounding_box' in azure_obj:
        bbox_points = azure_obj['bounding_box']
    elif 'polygon' in azure_obj:
        bbox_points = azure_obj['polygon']
    else:
        raise Exception('Could not find bounding box in azure object')

    if len(bbox_points) == 8:
        # The x and y are given as a flat data
        x_points = bbox_points[0::2]
        y_points = bbox_points[1::2]
    else:
        # The x and y area given as pairs
        x_points = [pt['x'] for pt in bbox_points]
        y_points = [pt['y'] for pt in bbox_points]

    # Convert these points based on the angle of the page
    if 'angle' in azure_page.keys() and azure_page['angle'] is not None:
        rotated_x_points = []
        rotated_y_points = []
        for (x, y) in [(x_points[index], y_points[index]) for index in range(len(x_points))]:
            rot_x, rot_y = rotate((x, y), (0, 0), azure_page['angle'])
            rotated_x_points.append(rot_x)
            rotated_y_points.append(rot_y)
        x_points = rotated_x_points
        y_points = rotated_y_points

    x1 = min(x_points)
    y1 = azure_page['height'] - max(y_points)
    x2 = max(x_points)
    y2 = azure_page['height'] - min(y_points)

    return [x1, y1, x2, y2]


def percent_azure_nodes_overlap(azure_node1, azure_node2, azure_page, axis_overlap='y'):
    kdxa_bbox1 = convert_azure_bbox(azure_node1, azure_page)
    kdxa_bbox2 = convert_azure_bbox(azure_node2, azure_page)

    return percent_nodes_overlap(kdxa_bbox1, kdxa_bbox2, axis_overlap=axis_overlap)


def azure_kdxa_nodes_overlap(azure_node1, kdxa_node2, azure_page, overlap_percentage=0.6):
    node1_bbox = convert_azure_bbox(azure_node1, azure_page)
    node2_bbox = kdxa_node2.get_bbox()

    return percent_nodes_overlap(node1_bbox, node2_bbox, axis_overlap='x') >= overlap_percentage and \
        percent_nodes_overlap(node1_bbox, node2_bbox, axis_overlap='y') >= overlap_percentage


def azure_nodes_overlap(azure_node1, azure_node2, azure_page, overlap_percentage=0.6):
    return percent_azure_nodes_overlap(azure_node1, azure_node2, azure_page, axis_overlap='x') >= overlap_percentage and \
        percent_azure_nodes_overlap(azure_node1, azure_node2, azure_page, axis_overlap='y') >= overlap_percentage


def rotate(point, origin, degrees):
    radians = np.deg2rad(degrees)
    x, y = point
    offset_x, offset_y = origin
    adjusted_x = (x - offset_x)
    adjusted_y = (y - offset_y)
    cos_rad = np.cos(radians)
    sin_rad = np.sin(radians)
    qx = offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y
    qy = offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y
    return qx, qy
