from kodexa import ContentNode


def overlaps_with(node, other_node):
    """
    Checks if the given node overlaps with another node.

    This function works with nodes on the same line. It checks if the x-coordinate of the first node
     is less than or equal to the sum of the x-coordinate and width of the second node, and if
     the sum of the x-coordinate and width of the first node is greater than or equal to the x-coordinate of the second node.

    Args:
        node (Node): The reference node.
        other_node (Node): The other node to check for overlap.

    Returns:
        bool: True if the nodes overlap, False otherwise.
    """
    # x1 <= xb and x2 >= xa
    return (
        node.get_x() <= other_node.get_x() + other_node.get_width()
        and node.get_x() + node.get_width() >= other_node.get_x()
    )


def width_of_overlap(node, other_node):
    """
    Calculates and returns the width of overlap between two nodes.

    This function checks if the two nodes overlap. If they do, it calculates the width
    of the overlap by finding the maximum x-coordinate of the two nodes and the minimum
    x-coordinate plus width of the two nodes. The width of the overlap is then calculated
    as the difference between these two values. If the nodes do not overlap, the function returns 0.0.

    Args:
        node (Node): The first node to check for overlap.
        other_node (Node): The second node to check for overlap.

    Returns:
        float: The width of the overlap between the two nodes. Returns 0.0 if there is no overlap.
    """
    if overlaps_with(node, other_node):
        # Nodes overlap
        x1 = max(node.get_x(), other_node.get_x())
        x2 = min(
            node.get_x() + node.get_width(), other_node.get_x() + other_node.get_width()
        )
        return x2 - x1
    else:
        return 0.0


def kdxa_nodes_overlap(
    kdxa_node1: ContentNode, kdxa_node2: ContentNode, overlap_percentage: float
):
    """
    Calculates whether the overlap between two nodes is greater than or equal to a specified percentage.

    Args:
        kdxa_node1 (ContentNode): The first node object, which should have a method get_bbox() that returns its bounding box.
        kdxa_node2 (ContentNode): The second node object, which should also have a method get_bbox() that returns its bounding box.
        overlap_percentage (float): The percentage of overlap to check for. This should be a float between 0 and 1, where 1 means 100% overlap.

    Returns:
        bool: True if the overlap on both the x and y axis is greater than or equal to the specified percentage, False otherwise.
    """
    node1_bbox = kdxa_node1.get_bbox()
    node2_bbox = kdxa_node2.get_bbox()

    return (
        percent_nodes_overlap(node1_bbox, node2_bbox, axis_overlap="x")
        >= overlap_percentage
        and percent_nodes_overlap(node1_bbox, node2_bbox, axis_overlap="y")
        >= overlap_percentage
    )


def percent_nodes_overlap(node1_bbox, node2_bbox, axis_overlap="y"):
    """
    Calculates the percentage of overlap between two nodes along a specified axis.

    This function takes in the bounding boxes of two nodes in the Kodexa world and calculates the percentage of overlap
    between them along a specified axis. The axis can be either 'x' or 'y'. If 'y' is given as the axis_overlap,
    the function calculates how much of the y2s and y1s overlap.

    Args:
        node1_bbox (list): The bounding box of the first node. It is a list of four numbers representing the coordinates of the bounding box.
        node2_bbox (list): The bounding box of the second node. It is a list of four numbers representing the coordinates of the bounding box.
        axis_overlap (str): The axis along which the overlap is to be calculated. It can be either 'x' or 'y'.

    Returns:
        float: The percentage of overlap between the two nodes along the specified axis. If there is no overlap, the function returns 0.0.
    """
    # These are the bboxes in the Kodexa world
    # line1 is the reference and line2 is the line to check
    # Returns % overlap based on the axis given
    # If y is given as axis_overlap, calculates how much of the y2s and y1s overlap
    line1_width = node1_bbox[2] - node1_bbox[0]
    line2_width = node2_bbox[2] - node2_bbox[0]

    line1_height = node1_bbox[3] - node1_bbox[1]
    line2_height = node2_bbox[3] - node2_bbox[1]

    ref_width_height = (
        min(line1_width, line2_width)
        if axis_overlap == "x"
        else min(line1_height, line2_height)
    )
    index1 = 0 if axis_overlap == "x" else 1
    index2 = 2 if axis_overlap == "x" else 3

    if (
        node1_bbox[index1]
        <= node2_bbox[index1]
        <= node1_bbox[index2]
        <= node2_bbox[index2]
    ):
        return (node1_bbox[index2] - node2_bbox[index1]) / ref_width_height

    elif (
        node2_bbox[index1]
        <= node1_bbox[index1]
        <= node2_bbox[index2]
        <= node1_bbox[index2]
    ):
        return (node2_bbox[index2] - node1_bbox[index1]) / ref_width_height

    elif (
        node2_bbox[index1]
        <= node1_bbox[index1]
        <= node1_bbox[index2]
        <= node2_bbox[index2]
    ):
        return 1.0

    elif (
        node1_bbox[index1]
        <= node2_bbox[index1]
        <= node2_bbox[index2]
        <= node1_bbox[index2]
    ):
        return 1.0
    else:
        # No overlap
        return 0.0


def update_overlap_bbox(bbox1, bbox2):
    """
    This function updates the overlapping bounding boxes.

    Args:
        bbox1 (list): The first bounding box, represented as a list of four integers.
        bbox2 (list): The second bounding box, represented as a list of four integers.

    Returns:
        list: A list of four integers representing the updated bounding box.
    """
    return [
        min(bbox1[0], bbox2[0]),
        min(bbox1[1], bbox2[1]),
        max(bbox1[2], bbox2[2]),
        max(bbox1[3], bbox2[3]),
    ]
