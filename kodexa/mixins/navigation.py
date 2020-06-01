class NavigationMixin:

    @staticmethod
    def get_name():
        return "navigation"

    @staticmethod
    def get_renderer(document):
        return None

    @staticmethod
    def get_dependencies():
        return ['core']

    @staticmethod
    def apply_to(node):
        pass
