from typing import List

from kodexa import Document


class InMemoryDocumentSink:
    """An in-memory document sink can be used for testing where you want to capture a set of the documents as basic
    list in-memory and then access them

    Args:

    Returns:

    """

    def __init__(self):
        self.documents: List[Document] = []

    @staticmethod
    def get_name():
        """ """
        return "In-Memory Document"

    def accept(self, document: Document):
        """Determines whether the store will accept this document
        
        This can be used to look at the metadata to determine if the sink already has
        the content and therefore doesn't need it again

        Args:
          document: return: True if the sink will accept the document
          document: Document: 

        Returns:
          True if the sink will accept the document

        """
        return True

    def sink(self, document: Document):
        """Adds the document to the sink

        Args:
          document: document to add
          document: Document: 

        Returns:

        """
        self.documents.append(document)

    def get_document(self, index: int) -> Document:
        """Get document at given index

        Args:
          index: index to get the document at
          index: int: 

        Returns:

        """
        return self.documents[index]
