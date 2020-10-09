from kodexa import Document


class FolderSink:
    """
    A folder sink that stores the documents in KDXA format
    """

    def __init__(self, path=None):
        self.path = "./" if path is None else path + "/"

    @staticmethod
    def get_name():
        return "Folder"

    def sink(self, document: Document):
        """
        Adds the document to the sink

        :param document: document to add
        """
        file_name = document.source.original_filename \
            if document.source.original_filename is not None else document.uuid
        document.to_kdxa(self.path + file_name + ".kdxa")
