from kodexa.mixins.util import add_method_to_node


def set_statistics(self, statistics):
    """
    Set the spatial statistics for this node

        >>> document.select.('//page')[0].set_statistics(NodeStatistics())

    :param statistics: the statistics object

    """
    self.add_feature("spatial", "statistics", statistics)


def get_statistics(self):
    """
    Get the spatial statistics for this node

        >>> document.select.('//page')[0].get_statistics()
        <kodexa.spatial.NodeStatistics object at 0x7f80605e53c8>

    :return: the statistics object (or None if not set)


    """
    return self.get_feature_value("spatial", "statistics")


def set_bbox(self, bbox):
    """
    Set the bounding box for the node, this is structured as:

    [x1,y1,x2,y2]

        >>> document.select.('//page')[0].set_bbox([10,20,50,100])

    :param bbox: the bounding box array

    """
    self.set_feature("spatial", "bbox", bbox)


def get_bbox(self):
    """
    Get the bounding box for the node, this is structured as:

    [x1,y1,x2,y2]

        >>> document.select.('//page')[0].get_bbox()
        [10,20,50,100]

    :return: the bounding box array


    """
    return self.get_feature_value("spatial", "bbox")


def set_bbox_from_children(self):
    """
    Set the bounding box for this node based on its children
    """

    x_min = None
    x_max = None
    y_min = None
    y_max = None

    for child in self.children:
        child_bbox = child.get_bbox()
        if child_bbox:
            if not x_min or x_min > child_bbox[0]:
                x_min = child_bbox[0]
            if not x_max or x_max < child_bbox[2]:
                x_max = child_bbox[2]
            if not y_min or y_min > child_bbox[1]:
                y_min = child_bbox[1]
            if not y_max or y_max < child_bbox[3]:
                y_max = child_bbox[3]

    if x_min:
        self.set_bbox([x_min, y_min, x_max, y_max])


def set_rotate(self, rotate):
    """
    Set the rotate of the node

        >>> document.select.('//page')[0].set_rotate(90)

    :param rotate the rotation of the node

    """
    self.add_feature("spatial", "rotate", rotate)


def get_rotate(self):
    """
    Get the rotate of the node

        >>> document.select.('//page')[0].get_rotate()
        90

    :return: the rotation of the node


    """
    return self.get_feature_value("spatial", "rotate")


def get_x(self):
    """
    Get the X position of the node

        >>> document.select.('//page')[0].get_x()
        10

    :return: the X position of the node


    """
    self_bbox = self.get_bbox()
    if self_bbox:
        return self_bbox[0]
    else:
        return None


def get_y(self):
    """
    Get the Y position of the node

        >>> document.select.('//page')[0].get_y()
        90

    :return: the Y position of the node
    """
    self_bbox = self.get_bbox()
    if self_bbox:
        return self_bbox[1]
    else:
        return None


def get_width(self):
    """
    Get the width of the node

        >>> document.select.('//page')[0].get_width()
        70

    :return: the width of the node
    """
    self_bbox = self.get_bbox()
    if self_bbox:
        return self_bbox[2] - self_bbox[0]
    else:
        return None


def get_height(self):
    """
    Get the height of the node

        >>> document.select.('//page')[0].get_height()
        40

    :return: the height of the node
    """
    self_bbox = self.get_bbox()
    if self_bbox:
        return self_bbox[3] - self_bbox[1]
    else:
        return None


class SpatialMixin:

    @staticmethod
    def get_name():
        return "spatial"

    @staticmethod
    def get_dependencies():
        return ['core']

    @staticmethod
    def apply_to(node):
        add_method_to_node(set_statistics, node)
        add_method_to_node(get_statistics, node)
        add_method_to_node(set_bbox, node)
        add_method_to_node(get_bbox, node)
        add_method_to_node(set_rotate, node)
        add_method_to_node(get_rotate, node)
        add_method_to_node(get_x, node)
        add_method_to_node(get_y, node)
        add_method_to_node(get_width, node)
        add_method_to_node(get_height, node)
        add_method_to_node(set_bbox_from_children, node)
