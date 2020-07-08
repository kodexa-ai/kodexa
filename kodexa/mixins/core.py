class CoreMixin:

    @staticmethod
    def get_name():
        return "core"

    @staticmethod
    def get_renderer(document):
        return None

    @staticmethod
    def apply_to(node):
        # all functions have been moved to ContentNode
        pass
