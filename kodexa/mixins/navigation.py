import re

from kodexa.mixins.util import add_method_to_node



class NavigationMixin:

    @staticmethod
    def get_name():
        return "navigation"

    @staticmethod
    def get_renderer(document):
        return None

    @staticmethod
    def to_text(self):
        return None

    @staticmethod
    def get_dependencies():
        return ['core']

    @staticmethod
    def apply_to(node):
        pass
