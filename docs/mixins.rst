Mix-Ins
-------

In this section we cover some of the included mix-ins and detail the functions that they add.

Core
^^^^

It is the core set of helpers that can be added to content nodes to allow for searching and tagging.

.. autofunction:: kodexa.mixins.core.tag

.. autofunction:: kodexa.mixins.core.tag_range

.. autofunction:: kodexa.mixins.core.get_all_content

.. autofunction:: kodexa.mixins.core.get_all_tags

.. autofunction:: kodexa.mixins.core.get_tag

.. autofunction:: kodexa.mixins.core.find

.. autofunction:: kodexa.mixins.core.findall

.. autofunction:: kodexa.mixins.core.find_with_feature_value

.. autofunction:: kodexa.mixins.core.findall_with_feature_value

.. autofunction:: kodexa.mixins.core.get_tags

.. autofunction:: kodexa.mixins.core.move_child_to_parent

.. autofunction:: kodexa.mixins.core.adopt_children

.. autofunction:: kodexa.mixins.core.remove_tag

.. autofunction:: kodexa.mixins.core.collect_nodes_to

.. autofunction:: kodexa.mixins.core.tag_nodes_to

.. autofunction:: kodexa.mixins.core.get_node_at_index

.. autofunction:: kodexa.mixins.core.has_next_node

.. autofunction:: kodexa.mixins.core.has_previous_node

.. autofunction:: kodexa.mixins.core.next_node

.. autofunction:: kodexa.mixins.core.previous_node

.. autofunction:: kodexa.mixins.core.get_last_child_index

.. autofunction:: kodexa.mixins.core.is_first_child

.. autofunction:: kodexa.mixins.core.is_last_child

Spatial
^^^^^^^

One of the core mix-ins is Spatial.  It is based on the concept of holding spatial information about the content nodes.

This spatial information can then be used by the mix-in's methods to allow you to both pull spatial information, but
also to query it.

.. autofunction:: kodexa.mixins.spatial.set_statistics

.. autofunction:: kodexa.mixins.spatial.get_statistics

.. autofunction:: kodexa.mixins.spatial.set_bbox

.. autofunction:: kodexa.mixins.spatial.get_bbox

.. autofunction:: kodexa.mixins.spatial.set_rotate

.. autofunction:: kodexa.mixins.spatial.get_rotate

.. autofunction:: kodexa.mixins.spatial.get_x

.. autofunction:: kodexa.mixins.spatial.get_y

.. autofunction:: kodexa.mixins.spatial.get_width

.. autofunction:: kodexa.mixins.spatial.get_height

.. autofunction:: kodexa.mixins.spatial.set_bbox_from_children

.. autofunction:: kodexa.mixins.spatial.collapse


