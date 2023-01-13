def overlaps_with(node, other_node):
    """
    Returns True if this node overlaps with other_node (works with nodes on the same line)
    :param node: reference node
    :param other_node: the other node to check
    """
    # x1 <= xb and x2 >= xa
    return node.get_x() <= other_node.get_x() + other_node.get_width() and \
           node.get_x() + node.get_width() >= other_node.get_x()


def width_of_overlap(node, other_node):
    """
   Returns the width of overlap between this node and other_node
   Returns 0.0 if there is no overlap
   :param node: reference node
   :param other_node: the other node to check
   """
    if overlaps_with(node, other_node):
        # Nodes overlap
        x1 = max(node.get_x(), other_node.get_x())
        x2 = min(node.get_x() + node.get_width(), other_node.get_x() + other_node.get_width())
        return x2 - x1
    else:
        return 0.0


def kdxa_nodes_overlap(kdxa_node1, kdxa_node2, overlap_percentage):
    node1_bbox = kdxa_node1.get_bbox()
    node2_bbox = kdxa_node2.get_bbox()

    return percent_nodes_overlap(node1_bbox, node2_bbox, axis_overlap='x') >= overlap_percentage and \
           percent_nodes_overlap(node1_bbox, node2_bbox, axis_overlap='y') >= overlap_percentage


def percent_nodes_overlap(node1_bbox, node2_bbox, axis_overlap='y'):
    # These are the bboxes in the Kodexa world
    # line1 is the reference and line2 is the line to check
    # Returns % overlap based on the axis given
    # If y is given as axis_overlap, calculates how much of the y2s and y1s overlap
    line1_width = node1_bbox[2] - node1_bbox[0]
    line2_width = node2_bbox[2] - node2_bbox[0]

    line1_height = node1_bbox[3] - node1_bbox[1]
    line2_height = node2_bbox[3] - node2_bbox[1]

    ref_width_height = min(line1_width, line2_width) if axis_overlap == 'x' else min(line1_height, line2_height)
    index1 = 0 if axis_overlap == 'x' else 1
    index2 = 2 if axis_overlap == 'x' else 3

    if node1_bbox[index1] <= node2_bbox[index1] <= node1_bbox[index2] <= node2_bbox[index2]:
        return (node1_bbox[index2] - node2_bbox[index1]) / ref_width_height

    elif node2_bbox[index1] <= node1_bbox[index1] <= node2_bbox[index2] <= node1_bbox[index2]:
        return (node2_bbox[index2] - node1_bbox[index1]) / ref_width_height

    elif node2_bbox[index1] <= node1_bbox[index1] <= node1_bbox[index2] <= node2_bbox[index2]:
        return 1.0

    elif node1_bbox[index1] <= node2_bbox[index1] <= node2_bbox[index2] <= node1_bbox[index2]:
        return 1.0
    else:
        # No overlap
        return 0.0


def update_overlap_bbox(bbox1, bbox2):
    return [min(bbox1[0], bbox2[0]), min(bbox1[1], bbox2[1]),
            max(bbox1[2], bbox2[2]), max(bbox1[3], bbox2[3])]

