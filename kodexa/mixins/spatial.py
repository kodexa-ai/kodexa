import json
from uuid import uuid4

from kodexa.mixins.util import add_method_to_node


def set_statistics(self, statistics):
    """
    Set the spatial statistics for this node

        >>> document.content_node.find(type_re='page').set_statistics(NodeStatistics())

    :param statistics: the statistics object

    """
    self.add_feature("spatial", "statistics", statistics)


def get_statistics(self):
    """
    Get the spatial statistics for this node

        >>> document.content_node.find(type_re='page').get_statistics()
        <kodexa.spatial.NodeStatistics object at 0x7f80605e53c8>

    :return: the statistics object (or None if not set)


    """
    return self.get_feature_value("spatial", "statistics")


def set_bbox(self, bbox):
    """
    Set the bounding box for the node, this is structured as:

    [x1,y1,x2,y2]

        >>> document.content_node.find(type_re='page').set_bbox([10,20,50,100])

    :param bbox: the bounding box array

    """
    self.set_feature("spatial", "bbox", bbox)


def get_bbox(self):
    """
    Get the bounding box for the node, this is structured as:

    [x1,y1,x2,y2]

        >>> document.content_node.find(type_re='page').get_bbox()
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


def collapse(self, type_re):
    """
    Will collapse the given type, this will remove this type from the hierarchy.

    :param type_re: the type that you will collapse
    :return:
    """
    for node in self.findall(type_re=type_re):
        pass


def set_rotate(self, rotate):
    """
    Set the rotate of the node

        >>> document.content_node.find(type_re='page').set_rotate(90)

    :param rotate the rotation of the node

    """
    self.add_feature("spatial", "rotate", rotate)


def get_rotate(self):
    """
    Get the rotate of the node

        >>> document.content_node.find(type_re='page').get_rotate()
        90

    :return: the rotation of the node


    """
    return self.get_feature_value("spatial", "rotate")


def get_x(self):
    """
    Get the X position of the node

        >>> document.content_node.find(type_re='page').get_x()
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

        >>> document.content_node.find(type_re='page').get_y()
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

        >>> document.content_node.find(type_re='page').get_width()
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

        >>> document.content_node.find(type_re='page').get_height()
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
    def get_renderer(document):
        return SpatialRender(document)

    @staticmethod
    def to_text(node):
        return f" spatial[x:{node.get_x()},y:{node.get_y()},w:{node.get_width()},h:{node.get_height()}] "

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
        add_method_to_node(collapse, node)


class SpatialRender:

    def __init__(self, document):
        self.document = document
        self.color_array = ['#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6',
                            '#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D',
                            '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A',
                            '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
                            '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC',
                            '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
                            '#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680',
                            '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
                            '#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3',
                            '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF']

    def to_text(self):
        self.node_to_text(self.document.content_node, 0)

    def render_node(self, node):
        div_id = "doc-" + str(uuid4())

        tag_row = ''
        tag_colours = {}
        for index, tag in enumerate(node.get_all_tags()):
            tag_row = tag_row + f'<span style="color: white; padding:8px; background-color:{self.color_array[index]}">{tag}</span>'
            tag_colours[tag] = self.color_array[index]
        tag_row = tag_row + ''
        html = """

 
  <h4>Spatial Document</h4>
  <canvas id='""" + div_id + """'></canvas> 
  <script id="script">

require.config({
    paths: {
        jq: 'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js?noext',
        jfabric: 'https://cdnjs.cloudflare.com/ajax/libs/fabric.js/3.4.0/fabric.js?noext',
        jtree: 'https://cdnjs.cloudflare.com/ajax/libs/jstree/3.3.8/jstree.min.js?noext'
    }
});

require(["jq","jfabric"], function(d3) {

    var canvas = new fabric.Canvas('""" + div_id + """');
    canvas.setHeight(700);
    canvas.setWidth(1000);

    getFeature = function(name, features) {
        finalFeature = null;
        features.forEach(function(feature) {
            if (feature.name === name) {
               finalFeature = feature;
            }
        });
        return finalFeature;
    }

    transformDocument = function (node, tag_colors) {
      var children = [];
      if (node.children) {
          node.children.forEach(function (child) {
            children.push(transformDocument(child, tag_colors))
          });
      }
      if (node.features.length>0) {
        bgColor = 'rgba(0,0,0,0)';
        bbox = [];
        tag_name = null;

        node.features.forEach(function(feature) {
            if (feature.name && feature.name.startsWith('tag:')) {
                bgColor = tag_colors[feature.name.split(':')[1]]
            }
            if (feature.name && feature.name == 'spatial:bbox') {
                bbox = feature.value[0]
            }
        });

        if (node.content) {   
            height = (bbox[3]-bbox[1])*.86; 
            var text = new fabric.Text(node.content, {
                                                            left: bbox[0],
                                                            top: 600 - bbox[1],
                                                            width: bbox[2]-bbox[0],
                                                            fontSize: height,
                                                            lockMovementX: true,
                                                            lockMovementY: true,
                                                            lockRotation: true,
                                                            backgroundColor: bgColor,
                                                            lockScalingFlip: true,
                                                            lockScalingX: true,
                                                            lockScalingY: true
                                                            });
            canvas.add(text);
        } else {
            if (bbox.length && bgColor != 'rgba(0,0,0,0)') {
                var rect = new fabric.Rect({
                                            left: bbox[0],
                                            top: 600 - bbox[1],
                                            width: bbox[2]-bbox[0],
                                            height: bbox[3]-bbox[1],
                                            fill: bgColor
                                            });
                canvas.add(rect);
                canvas.sendToBack(rect);
            } else {
            }
        }
      }
      return { id: node.uuid, text: node.content, children: children, data: { "features": node.features } }
    }

    $(function () {
        tag_colors = """ + json.dumps(tag_colours) + """;

        data = """ + str(node.to_json()) + """;
        rootNode = transformDocument(data,tag_colors)
    
    });
});
  
  </script>
  
        """
        html = html + tag_row
        return html

    def to_html(self):
        return self.render_node(self.document.content_node.children[0])

    def to_mimetype(self):
        return self.render_node_mimetype(self.document.content_node.children[0])

    def render_node_mimetype(self, node):
        tag_colors = {}
        for index, tag in enumerate(node.get_all_tags()):
            tag_colors[tag] = self.color_array[index]

        render_data = {'node_data': node.to_json(), 'tag_colors': tag_colors, }
        bundle = {}
        bundle['application/vnd.kodexa.spatial+json'] = render_data
        return bundle
