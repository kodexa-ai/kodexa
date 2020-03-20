"""
Mix-ins
-------

Mix-ins are an effective way to add helper functionality to Documents and ContentNode's based on the underlying
features.
"""
from .core import CoreMixin, FindDirection
from .navigation import NavigationMixin
from .registry import *
from .spatial import SpatialMixin, SpatialRender
from .util import add_method_to_node
