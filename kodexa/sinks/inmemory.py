class InMemoryDocumentSink:
    """
    An in-memory document sink can be used for testing where you want to capture a set of the documents as basic
    list in-memory and then access them
    """

    def __init__(self):
        self.documents = []

    @staticmethod
    def get_name():
        return "In-Memory Document"

    def sink(self, document):
        """
        Adds the document to the sink

        :param document: document to add
        """
        self.documents.append(document)

    def get_document(self, index):
        """
        Get document at given index

        :param index: index to get the document at
        """
        return self.documents[index]
