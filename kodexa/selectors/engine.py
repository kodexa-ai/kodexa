from kodexa import selectors, ContentNode


class Selector:

    def __init__(self, path):
        self.path = path
        self.parsed_path = selectors.parse(path)

    def execute(self, content_node: ContentNode):
        return self.parsed_path.resolve(content_node)
