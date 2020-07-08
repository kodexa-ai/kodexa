"""
Mix-ins
-------

Mix-ins are an effective way to add helper functionality to Documents and ContentNode's based on the underlying
features.
"""
from .core import CoreMixin
from .navigation import NavigationMixin
from .registry import get_mixin, get_renderers, add_mixin, apply_to_node, add_mixin_to_document, \
    add_mixins_to_document_node
from .spatial import SpatialMixin
from .util import add_method_to_node
