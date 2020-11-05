from typing import List

from kodexa import Document


class InMemoryDocumentSink:
    """
    An in-memory document sink can be used for testing where you want to capture a set of the documents as basic
    list in-memory and then access them
    """

    def __init__(self):
        self.documents: List[Document] = []

    @staticmethod
    def get_name():
        return "In-Memory Document"

    def accept(self, document: Document):
        """
        Determines whether the store will accept this document

        This can be used to look at the metadata to determine if the sink already has
        the content and therefore doesn't need it again

        :param document:
        :return: True if the sink will accept the document
        """
        return True

    def sink(self, document: Document):
        """
        Adds the document to the sink

        :param document: document to add
        """
        self.documents.append(document)

    def get_document(self, index: int) -> Document:
        """
        Get document at given index

        :param index: index to get the document at
        """
        return self.documents[index]
