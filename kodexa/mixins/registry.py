from typing import Dict

from kodexa.mixins.core import CoreMixin
from kodexa.mixins.navigation import NavigationMixin
from kodexa.mixins.spatial import SpatialMixin

registered_mixins: Dict[str, object] = {}


def get_mixin(mixin):
    if mixin in registered_mixins:
        return registered_mixins[mixin]
    else:
        return None


def add_mixin(mixin):
    registered_mixins[mixin.get_name()] = mixin


def apply_to_node(mixin_name, node):
    if mixin_name in registered_mixins:
        registered_mixins[mixin_name].apply_to(node)

        # Apply to the children
        if node.get_children():
            for child in node.get_children():
                apply_to_node(mixin_name, child)


def apply_to_document(document):
    for mixin in document.get_mixins():
        add_mixin_to_document(mixin, document)


def add_mixins_to_document_node(document, node):
    for mixin in document.get_mixins():
        apply_to_node(mixin, node)


def add_mixin_to_document(mixin, document):
    if mixin not in document.get_mixins():
        document.get_mixins().append(mixin)

        if mixin not in registered_mixins:
            return

        if document.content_node:
            apply_to_node(mixin, document.content_node)

        # Include support for mix-in dependencies
        if hasattr(registered_mixins[mixin], 'get_dependencies') and callable(
                getattr(registered_mixins[mixin], 'get_dependencies')):
            for dependency_mixin in registered_mixins[mixin].get_dependencies():
                add_mixin_to_document(dependency_mixin, document)
    else:
        return


add_mixin(SpatialMixin())
add_mixin(CoreMixin())
add_mixin(NavigationMixin())


def get_renderers(document):
    renderers = {}
    for mixin in document.get_mixins():
        if mixin in registered_mixins:
            r = registered_mixins[mixin].get_renderer(document)
            if r:
                renderers[mixin] = r
    return renderers
