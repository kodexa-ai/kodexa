import numpy as np
from kodexa import Document
from kodexa.spatial.bbox_common import percent_nodes_overlap

KDXA_BBOX_KEY = "kodexa_bbox"


def create_page_node_keep_azure_lines(
    document, page_node, azure_page, overlap_percentage=0.6
):
    """
    This function creates a page node and keeps azure lines. It first creates a node with the content area as the parent node.
    Then it sets the bounding box of the page node with the width and height of the azure page. It then checks all the lines identified
    by Form Recognizer and creates a line node for each line. It also sets the bounding box of the line node. It then checks if the
    azure nodes overlap. If they do, it adds the word to the line words and included words. It then creates a word node for each word
    in the line words and sets the bounding box and content parts of the word node.

    Args:
        document (obj): The document object.
        page_node (obj): The page node object.
        azure_page (dict): The azure page dictionary.
        overlap_percentage (float, optional): The overlap percentage. Defaults to 0.6.

    Returns:
        bool: Returns False if there is no issue.
    """
    page_node = document.create_node("content-area", parent=page_node)
    page_node.set_bbox([0, 0, azure_page["width"], azure_page["height"]])

    # Now check all the lines identified by Form Recognizer
    all_words = get_azure_page_words(azure_page)

    included_words = []
    word_index = 0
    for line_index, line in enumerate(azure_page["lines"]):
        # Create the line and set bbox
        line_node = document.create_node("line", parent=page_node)
        line_node.set_bbox(convert_azure_bbox(line, azure_page))
        line_words = []
        while True and word_index < len(all_words):
            if azure_kdxa_nodes_overlap(
                all_words[word_index], line_node, azure_page, overlap_percentage
            ):
                line_words.append(all_words[word_index])
                included_words.append(all_words[word_index])
                word_index += 1
            else:
                break

        for word in line_words:
            word_node = document.create_node("word", parent=line_node)
            word_node.set_bbox(convert_azure_bbox(word, azure_page))
            word_node.set_content_parts([word["content"]])

    # No issue
    return False


def create_kddb_from_azure(azure_data, keep_azure_lines=True, overlap_percentage=0.6):
    """
    This function creates a kddb document from Azure data.

    Args:
        azure_data (dict): A dictionary of the json data returned by Azure.
        keep_azure_lines (bool, optional): If set to False, the lines returned will match how Kodexa put lines together.
            Default is True - keeping how Azure creates lines.
        overlap_percentage (float, optional): The percentage of overlap for nodes to be considered on the same line (from 0.0 to 1.0).
            Default is 0.6.

    Returns:
        Document: A kddb document with the content nodes. If an issue is found during the creation of the document, None is returned.
    """
    # This restores the lines provided by Azure (not matching Kodexa)
    if not azure_data:
        return None

    # Create an empty document
    document = Document()
    root_node = document.create_node("root")

    for page_index, azure_page in enumerate(azure_data["analyzeResult"]["pages"]):
        page_node = document.create_node("page", parent=root_node)
        page_node.set_bbox([0, 0, azure_page["width"], azure_page["height"]])
        if "angle" in azure_page.keys() and azure_page["angle"] is not None:
            page_node.add_feature("page", "angle", azure_page["angle"])

        # Create the kddb document (keeping Azure lines or matching them with Kodexa lines)
        issue_found = (
            create_page_node_keep_azure_lines(
                document, page_node, azure_page, overlap_percentage=overlap_percentage
            )
            if keep_azure_lines
            else create_page_node_line_up_kodexa(document, page_node, azure_page)
        )

        if issue_found:
            return None

    document.content_node = root_node
    document.add_mixin("spatial")

    return document


def create_page_node_line_up_kodexa(document, page_node, azure_page):
    """
    This function creates a page node line up for a Kodexa document using Azure's OCR words.
    It groups Azure's OCR words into lines to match how Kodexa sees lines.
    It also sets the bounding box for the content area node and line node.
    It creates a word node for each word in the Azure line words and sets the bounding box for each word node.
    It also adds a feature for the word node if the word has a confidence key.
    It sets the content parts for the word node and calculates the total width of the characters and the count of characters.
    It sets the statistics for the line node based on the calculated total width and count of characters.

    Args:
        document (Document): The Kodexa document.
        page_node (Node): The page node in the Kodexa document.
        azure_page (dict): The Azure page containing the OCR words.

    Returns:
        bool: Returns False indicating that the document is a good kddb document with no issue.
    """
    # Group Azure's OCR words into lines to match how Kodexa sees lines
    content_area_node = document.create_node("content-area", parent=page_node)
    content_area_node.set_bbox([0, 0, azure_page["width"], azure_page["height"]])

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
                azure_line_words = azure_line["words"]
            except KeyError:
                # The azure line does not contain the words in the metadata - so we have to find them
                azure_line_words = get_azure_line_words(
                    azure_line, azure_page, azure_page_words, already_added_azure_words
                )

            if not azure_line_words:
                continue

            for word in azure_line_words:
                word_node = document.create_node("word", parent=line_node)
                word_node.set_bbox(convert_azure_bbox(word, azure_page))

                if "confidence" in word.keys():
                    word_node.add_feature("azure", "confidence", word["confidence"])

                word_node.set_content_parts([word["content"]])
                chars_total_width += word_node.get_width()
                char_count += len(word["content"])

        line_node.set_bbox_from_children()
        if char_count > 0:
            line_node.set_statistics(
                {"updated_mean_width": chars_total_width / char_count}
            )
        else:
            line_node.set_statistics({"updated_mean_width": 0.0})

    # This is a good kddb document (no issue)
    return False


def get_azure_line_words(
    azure_line, azure_page, azure_page_words, already_added_azure_words
):
    """
    This function is used to get the words from a line in Azure. It checks if the words overlap with the Azure line and
    page, and if they have not been added before.

    Args:
        azure_line (dict): The Azure line to get words from.
        azure_page (dict): The Azure page that contains the line.
        azure_page_words (list): The list of words in the Azure page.
        already_added_azure_words (list): The list of words that have already been added.

    Returns:
        list: A list of words from the Azure line that overlap with the Azure page and have not been added before.

    Raises:
        IndexError: An error occurred when trying to access the first element of an empty list.
    """
    azure_line_words = []
    word_texts = azure_line["content"].split()
    for wt in word_texts:
        try:
            word = [
                w
                for w in azure_page_words
                if w["content"] == wt
                and azure_nodes_overlap(w, azure_line, azure_page)
                and w not in already_added_azure_words
            ][0]
        except IndexError:
            print("Issue with converting Azure lines to Kodexa lines")
            continue

        # Add this word as it has already been found
        already_added_azure_words.append(word)

        # line words to return
        azure_line_words.append(word)

    return azure_line_words


def get_azure_page_words(azure_page):
    """
    This function extracts the words from a given Azure page. If the page already contains a 'words' key,
    it directly assigns the value to 'page_words'. If not, it iterates over the 'lines' key, extends the 'page_words'
    list with the words in each line, and assigns the 'text' value to the 'content' key for each word.

    Args:
        azure_page (dict): A dictionary representing an Azure page. It should contain either a 'words' key with a list of words as its value, or a 'lines' key with a list of lines, each containing a 'words' key with a list of words as its value.

    Returns:
        list: A list of words extracted from the Azure page. Each word is represented as a dictionary with a 'content' key.
    """
    if "words" in azure_page.keys():
        page_words = azure_page["words"]
    else:
        page_lines = azure_page["lines"]
        page_words = []
        [page_words.extend(pl["words"]) for pl in page_lines]
        for pw in page_words:
            pw["content"] = pw["text"]

    return page_words


def get_azure_next_line(
    document_lines, ref_line, direction="right", overlap_percentage=0.6
):
    """
    Finds the next line in a given direction from a reference line in a document.

    This function searches for the next line in a document from a reference line in a specified direction.
    The direction can be 'right', 'left', 'down', 'up', or 'up_left'. The function returns the next line
    if it exists, otherwise it returns None.

    Args:
        document_lines (list): A list of lines in the document.
        ref_line (str): The reference line from which to find the next line.
        direction (str, optional): The direction in which to find the next line. Defaults to 'right'.
        overlap_percentage (float, optional): The minimum percentage of overlap required to consider a line as the next line. Defaults to 0.6.

    Returns:
        str or None: The next line in the specified direction from the reference line if it exists, otherwise None.

    Raises:
        ValueError: If the direction is not one of 'right', 'left', 'down', 'up', or 'up_left'.
    """
    if ref_line not in document_lines:
        return None

    ref_bbox = ref_line.get_bbox()
    possible_lines = document_lines[
        max(document_lines.index(ref_line) - 25, 0): min(
            document_lines.index(ref_line) + 25, len(document_lines)
        )
    ]

    if direction == "right":
        # Get all the lines to the right of the cell, where the y overlaps; and sort according to x
        right_lines = [
            right_line
            for right_line in possible_lines
            if right_line.get_bbox()[0] >= ref_bbox[2]
            and percent_nodes_overlap(ref_bbox, right_line.get_bbox(), "y")
            >= overlap_percentage
        ]

        if not right_lines:
            return None

        # Sort by x (increasing)
        sorted_next_right_lines = [right_lines[0]]
        [
            sorted_next_right_lines.insert(0, right_line)
            for right_line in right_lines
            if right_line.get_bbox()[0] < sorted_next_right_lines[0].get_bbox()[0]
        ]

        return sorted_next_right_lines[0]

    elif direction == "left":
        # Get all the lines to the left of the cell, where the y overlaps; and sort according to x2 (decreasing)
        left_lines = [
            left_line
            for left_line in possible_lines
            if left_line.get_bbox()[2] <= ref_bbox[0]
            and percent_nodes_overlap(ref_bbox, left_line.get_bbox(), "y")
            >= overlap_percentage
        ]

        if not left_lines:
            return None

        # Sort by x (decreasing)
        sorted_next_left_lines = [left_lines[0]]
        [
            sorted_next_left_lines.insert(0, left_line)
            for left_line in left_lines
            if left_line.get_bbox()[0] > sorted_next_left_lines[0].get_bbox()[0]
        ]

        return sorted_next_left_lines[0]

    elif direction == "down":
        # Get all the lines below of the cell, where the x overlaps; and sort according to y
        down_lines = [
            down_line
            for down_line in possible_lines
            if down_line.get_bbox()[3] <= ref_bbox[1]
            and percent_nodes_overlap(ref_bbox, down_line.get_bbox(), "x")
            >= overlap_percentage
        ]

        if not down_lines:
            return None

        # Sort by y (increasing since 0 is at the bottom of the page)
        sorted_next_down_lines = [down_lines[0]]
        [
            sorted_next_down_lines.insert(0, down_line)
            for down_line in down_lines
            if down_line.get_bbox()[1] > sorted_next_down_lines[0].get_bbox()[1]
        ]

        return sorted_next_down_lines[0]

    elif direction == "up":
        # Get all the lines above of the cell, where the x overlaps; and sort according to y
        up_lines = [
            up_line
            for up_line in possible_lines
            if up_line.get_bbox()[1] >= ref_bbox[3]
            and percent_nodes_overlap(ref_bbox, up_line.get_bbox(), "x")
            >= overlap_percentage
        ]

        if not up_lines:
            return None

        # Sort by y (decreasing since 0 is at the bottom of the page)
        sorted_next_up_lines = [up_lines[0]]
        [
            sorted_next_up_lines.insert(0, up_line)
            for up_line in up_lines
            if up_line.get_bbox()[1] < sorted_next_up_lines[0].get_bbox()[1]
        ]

        return sorted_next_up_lines[0]

    elif direction == "up_left":
        # Get all the lines above of the cell, where the x is to the left of the cell
        up_left_lines = [
            up_line
            for up_line in possible_lines
            if up_line.get_bbox()[1] >= ref_bbox[3]
            and ref_bbox[2] > up_line.get_x()
            and ref_bbox[0] - up_line.get_bbox()[2] <= 0.75
        ]

        if not up_left_lines:
            return None

        # Sort by y (decreasing since 0 is at the bottom of the page)
        sorted_next_up_left_lines = [up_left_lines[0]]
        [
            sorted_next_up_left_lines.insert(0, up_left_line)
            for up_left_line in up_left_lines
            if up_left_line.get_bbox()[1] < sorted_next_up_left_lines[0].get_bbox()[1]
        ]

        return sorted_next_up_left_lines[0]

    return None


def group_azure_lines_to_kodexa_lines(page):
    """
    This function groups Azure lines into Kodexa lines. It first checks if the page contains any lines. If not, it returns an empty list.
    If there are lines, it converts Azure lines into Kodexa lines. It then sorts the remaining page lines by y1 and extends the line groups
    with the result of the check_azure_line_group function applied to the sorted lines. Finally, it sorts the line groups based on y and
    returns the sorted line groups.

    Args:
        page (dict): A dictionary representing a page. It should contain a key "lines" which maps to a list of lines. Each line is a
        dictionary that should contain the keys "content" or "text".

    Returns:
        list: A list of line groups. Each line group is a list of lines. Each line is a dictionary that contains the keys "content" or
        "text" and a key KDXA_BBOX_KEY which maps to a list of four numbers representing the bounding box of the line.
    """
    # Group the azure lines into Kodexa lines
    # Each line group is a list of lines
    page_lines = page["lines"]
    if not page_lines:
        return []

    # Convert Azure lines into Kodexa lines
    for page_line in page_lines:
        page_line[KDXA_BBOX_KEY] = convert_azure_bbox(page_line, page)
        page_line["content"] = (
            page_line["content"]
            if "content" in page_line.keys()
            else page_line["text"]
            if "text" in page_line.keys()
            else None
        )

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
    lines_to_sort = sorted(
        [page_line for page_line in page_lines if page_line not in lines_to_separate],
        key=lambda d: d[KDXA_BBOX_KEY][1],
        reverse=True,
    )

    line_groups.extend(check_azure_line_group(lines_to_sort))

    # Need to sort the line_groups based on y
    line_groups.sort(
        key=lambda line_group: [line[KDXA_BBOX_KEY][1] for line in line_group],
        reverse=True,
    )
    return line_groups


def get_bbox_of_line_group(line_group):
    """
    This function calculates and returns the bounding box of a given line group. If the line group is empty, the function returns None.

    Args:
        line_group (list): A list of lines where each line is a dictionary containing the key 'KDXA_BBOX_KEY' which
        maps to a list of four integers representing the bounding box of the line.

    Returns:
        list or None: A list of four values representing the bounding box of the line group. If the line group is empty, returns None.
    """
    if not line_group:
        return None

    # Gets the bounding box of the line_group
    x1_values = [line[KDXA_BBOX_KEY][0] for line in line_group]
    y1_values = [line[KDXA_BBOX_KEY][1] for line in line_group]
    x2_values = [line[KDXA_BBOX_KEY][2] for line in line_group]
    y2_values = [line[KDXA_BBOX_KEY][3] for line in line_group]

    return [min(x1_values), min(y1_values), max(x2_values), max(y2_values)]


def page_line_overlaps_with_line_group(
    page_line_dict,
    line_group,
    next_line_group,
    axis_overlap="y",
    min_overlap_percentage_y=0.4,
):
    """
    Checks if a page line overlaps with a line group. If the page line overlaps with both the line group and the next line group,
    it only returns true if the overlap is more for the line group than the next line group.

    Args:
        page_line_dict (dict): Dictionary containing page line data.
        line_group (list): List of lines in the current line group.
        next_line_group (list): List of lines in the next line group.
        axis_overlap (str, optional): Axis to check for overlap. Defaults to 'y'.
        min_overlap_percentage_y (float, optional): Minimum overlap percentage on the y-axis to consider valid. Defaults to 0.4.

    Returns:
        bool: True if the page line overlaps with the line group, False otherwise.
    """
    page_line_dict_bbox = page_line_dict[KDXA_BBOX_KEY]
    # line_group_bbox = get_bbox_of_line_group(line_group)
    # next_line_group_bbox = get_bbox_of_line_group(next_line_group)
    line_group_bbox = line_group[-1][KDXA_BBOX_KEY]
    next_line_group_bbox = (
        next_line_group[-1][KDXA_BBOX_KEY] if next_line_group else None
    )

    if next_line_group:
        # Check if page_line_dict overlaps with both line_group and next_line_group
        # If it does, only return true if the overlap is more for line_group than next_line_group
        line_group_overlap = percent_nodes_overlap(
            page_line_dict_bbox, line_group_bbox, axis_overlap=axis_overlap
        )
        next_line_group_overlap = percent_nodes_overlap(
            page_line_dict_bbox, next_line_group_bbox, axis_overlap=axis_overlap
        )
        if (
            line_group_overlap >= min_overlap_percentage_y
            and next_line_group_overlap >= min_overlap_percentage_y
            and node_heights_are_valid(page_line_dict_bbox, line_group)
            and node_heights_are_valid(page_line_dict_bbox, next_line_group)
        ):
            return (
                page_line_dict[KDXA_BBOX_KEY][0] - line_group_bbox[0]
                < page_line_dict[KDXA_BBOX_KEY][0] - next_line_group_bbox[0]
            )
        elif line_group_overlap >= min_overlap_percentage_y and node_heights_are_valid(
            page_line_dict_bbox, line_group
        ):
            return True
        else:
            return False
    else:
        return percent_nodes_overlap(
            page_line_dict_bbox, line_group_bbox, axis_overlap=axis_overlap
        ) >= min_overlap_percentage_y and node_heights_are_valid(
            page_line_dict_bbox, line_group
        )


def node_heights_are_valid(new_bbox, line_group):
    """
    This function checks if the font size/height of the nodes are within 60% of each other. It calculates the minimum
    and maximum height of each line and compares it with the new height.
    If the ratio of the minimum of new height and min_height to the maximum of new height and
    min_height is greater than or equal to 0.55, or the ratio of the minimum of new height and
    max_height to the maximum of new height and max_height is greater than or equal to 0.55, the function returns True.

    Args:
        new_bbox (list): A list representing the new bounding box.
        line_group (list): A list of lines.

    Returns:
        bool: True if the font size/height of the nodes are within 60% of each other, False otherwise.
    """
    # The font size/height of the nodes should be within 60% of each other
    # Get the min_height and max_height of each line
    # return True
    height_values = [
        line[KDXA_BBOX_KEY][3] - line[KDXA_BBOX_KEY][1] for line in line_group
    ]
    min_height = min(height_values)
    max_height = max(height_values)
    new_height = new_bbox[3] - new_bbox[1]
    return (
        min(new_height, min_height) / max(new_height, min_height) >= 0.55
        or min(new_height, max_height) / max(new_height, max_height) >= 0.55
    )


def check_azure_line_group(original_line_group):
    """
    This function checks if the azure lines in a given group overlap on the x-axis. If they do, the function breaks down
    the group into multiple groups.

    Args:
        original_line_group (list): A list of azure lines to be checked for overlap.

    Returns:
        list: A list of line groups where each group is a list of azure lines that do not overlap on the x-axis.

    Raises:
        None

    Note:
        The azure lines are sorted by x in the original_line_group. The function also checks for y-overlap (+/- 0.1).
    """
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
            if (
                azure_line[KDXA_BBOX_KEY][0] >= line_group[-1][KDXA_BBOX_KEY][2] - 0.1
                or azure_line[KDXA_BBOX_KEY][2] <= line_group[0][KDXA_BBOX_KEY][0] + 0.1
            ) and page_line_overlaps_with_line_group(
                azure_line,
                line_group,
                line_groups[lg_index + 1] if lg_index + 1 < len(line_groups) else None,
            ):
                line_group.append(azure_line)
                line_group_inserted = True
                break

        if line_group_inserted:
            continue

        line_groups.append([azure_line])
        line_groups.sort(
            key=lambda line_group: [line[KDXA_BBOX_KEY][1] for line in line_group],
            reverse=True,
        )

    return line_groups


def convert_azure_bbox(azure_obj, azure_page):
    """
    This function converts the bounding box coordinates from an Azure object to a standard format.

    Args:
        azure_obj (dict): The Azure object containing the bounding box information. This can be in the form of 'boundingBox',
                          'bounding_box', or 'polygon'.
        azure_page (dict): The Azure page object containing the page information such as 'angle' and 'height'.

    Raises:
        Exception: If no bounding box information can be found in the Azure object.

    Returns:
        list: A list of four elements representing the converted bounding box coordinates [x1, y1, x2, y2].
    """
    # boundingBox has 8 points
    if "boundingBox" in azure_obj:
        bbox_points = azure_obj["boundingBox"]
    elif "bounding_box" in azure_obj:
        bbox_points = azure_obj["bounding_box"]
    elif "polygon" in azure_obj:
        bbox_points = azure_obj["polygon"]
    else:
        raise Exception("Could not find bounding box in azure object")

    if len(bbox_points) == 8:
        # The x and y are given as a flat data
        x_points = bbox_points[0::2]
        y_points = bbox_points[1::2]
    else:
        # The x and y area given as pairs
        x_points = [pt["x"] for pt in bbox_points]
        y_points = [pt["y"] for pt in bbox_points]

    # Convert these points based on the angle of the page
    if "angle" in azure_page.keys() and azure_page["angle"] is not None:
        rotated_x_points = []
        rotated_y_points = []
        for x, y in [
            (x_points[index], y_points[index]) for index in range(len(x_points))
        ]:
            rot_x, rot_y = rotate((x, y), (0, 0), azure_page["angle"])
            rotated_x_points.append(rot_x)
            rotated_y_points.append(rot_y)
        x_points = rotated_x_points
        y_points = rotated_y_points

    x1 = min(x_points)
    y1 = azure_page["height"] - max(y_points)
    x2 = max(x_points)
    y2 = azure_page["height"] - min(y_points)

    return [x1, y1, x2, y2]


def percent_azure_nodes_overlap(azure_node1, azure_node2, azure_page, axis_overlap="y"):
    """
    Calculates the percentage of overlap between two azure nodes along a specified axis.

    Args:
        azure_node1 (dict): The first azure node.
        azure_node2 (dict): The second azure node.
        azure_page (dict): The azure page containing the nodes.
        axis_overlap (str, optional): The axis along which to calculate overlap. Defaults to "y".

    Returns:
        float: The percentage of overlap between the two nodes.
    """
    kdxa_bbox1 = convert_azure_bbox(azure_node1, azure_page)
    kdxa_bbox2 = convert_azure_bbox(azure_node2, azure_page)

    return percent_nodes_overlap(kdxa_bbox1, kdxa_bbox2, axis_overlap=axis_overlap)


def azure_kdxa_nodes_overlap(
    azure_node1, kdxa_node2, azure_page, overlap_percentage=0.6
):
    """
    This function checks if the overlap between two nodes is greater than or equal to a specified percentage.

    Args:
        azure_node1 (dict): The first node from Azure.
        kdxa_node2 (object): The second node from KDXA.
        azure_page (dict): The page from Azure where the first node is located.
        overlap_percentage (float, optional): The minimum percentage of overlap. Defaults to 0.6.

    Returns:
        bool: True if the overlap in both x and y axis is greater than or equal to the overlap_percentage, False otherwise.
    """
    node1_bbox = convert_azure_bbox(azure_node1, azure_page)
    node2_bbox = kdxa_node2.get_bbox()

    return (
        percent_nodes_overlap(node1_bbox, node2_bbox, axis_overlap="x")
        >= overlap_percentage
        and percent_nodes_overlap(node1_bbox, node2_bbox, axis_overlap="y")
        >= overlap_percentage
    )


def azure_nodes_overlap(azure_node1, azure_node2, azure_page, overlap_percentage=0.6):
    """
    This function checks if two azure nodes overlap on a page by a certain percentage.

    Args:
        azure_node1 (object): The first azure node.
        azure_node2 (object): The second azure node.
        azure_page (object): The azure page where the nodes are located.
        overlap_percentage (float, optional): The percentage of overlap to check for. Defaults to 0.6.

    Returns:
        bool: True if the nodes overlap by the specified percentage on both x and y axis, False otherwise.
    """
    return (
        percent_azure_nodes_overlap(
            azure_node1, azure_node2, azure_page, axis_overlap="x"
        )
        >= overlap_percentage
        and percent_azure_nodes_overlap(
            azure_node1, azure_node2, azure_page, axis_overlap="y"
        )
        >= overlap_percentage
    )


def rotate(point, origin, degrees):
    """
    Rotates a point around a given origin.

    This function takes a point and an origin (both as tuples of x, y coordinates), and a number of degrees.
    It rotates the point around the origin by the given number of degrees, using the rotation matrix formula.

    Args:
        point (tuple): The x, y coordinates of the point to rotate.
        origin (tuple): The x, y coordinates of the point around which to rotate.
        degrees (float): The number of degrees by which to rotate the point.

    Returns:
        tuple: The x, y coordinates of the rotated point.
    """
    radians = np.deg2rad(degrees)
    x, y = point
    offset_x, offset_y = origin
    adjusted_x = x - offset_x
    adjusted_y = y - offset_y
    cos_rad = np.cos(radians)
    sin_rad = np.sin(radians)
    qx = offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y
    qy = offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y
    return qx, qy
