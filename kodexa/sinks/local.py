from kodexa import Document
from kodexa.stores.stores import DocumentStore


class DocumentStoreSink:
    """A sink that writes to the underlying store"""

    def __init__(self, document_store: DocumentStore):
        self.document_store = document_store

    @staticmethod
    def get_name():
        """ """
        return "Store Sink"

    def sink(self, document: Document):
        """

        Args:
          document: Document: 

        Returns:

        """
        if document.source.original_path is not None and document.source.original_filename is not None:
            self.document_store.put(document.source.original_path + "/" + document.source.original_filename, document)
        else:
            self.document_store.put(document.uuid, document)

    def accept(self, document: Document):
        """

        Args:
          document: Document: 

        Returns:

        """
        return self.document_store.accept(document)


class FolderSink:
    """A folder sink that stores the documents in KDXA format"""

    def __init__(self, path=None):
        self.path = "./" if path is None else path + "/"

    @staticmethod
    def get_name():
        """ """
        return "Folder"

    def accept(self, document: Document):
        """

        Args:
          document: Document: 

        Returns:

        """
        return True

    def sink(self, document: Document):
        """Adds the document to the sink

        Args:
          document: document to add
          document: Document: 

        Returns:

        """
        file_name = document.source.original_filename \
            if document.source.original_filename is not None else document.uuid
        document.to_kdxa(self.path + file_name + ".kdxa")
