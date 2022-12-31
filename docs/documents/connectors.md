# What is a Connector?

A connector is a way to go from a Kodexa Document instance and get the original source for the content.

For example, if you have a PDF document, you can use the local filesystem connector to allow you to get the original PDF
file. This is useful if you want to do something like OCR the document, or if you want to do something like extract the text
from the PDF.

Working with the source can be done any any point of processing in a Kodexa document, for example you might want
a step in the pipeline to parse a PDF, and a later step to get the original PDF file to look for table using computer vision.

:include-meta: {bulletListType: "Steps", differentColors: true}

* Parse PDF
* Layout Analysis
* Table Identification (Computer Vision)

# How is Connector implemented?

A connector implement a single static method, `get_source` which takes a document and returns the bytes of the 
original content.

Lets take a look at a very simple source:

```python
from kodexa import Document

class LocalFilesystemConnector:
    
    @staticmethod
    def get_source(document: Document) -> bytes:
        return open(document.source, 'rb').read()
```