# Creating a Document

Typically one of the first steps in Kodexa is create a new document. For this example, lets
assume that we have a document in PDF form.

We can simply create the document, referencing the PDF file.

```python
from kodexa import Document

document = Document.from_file('my-document.pdf')
```

This step doesn't parse the document, or open the PDF at all. However, it is an important first step
in understanding how Kodexa works. At this point we will a have an empty document, with a reference
to the PDF file.

In fact we can tell that it is empty by simply counting the number of nodes in the document.

```python
assert print(len(document.select('//*'))) == 0
```

However, metadata has been added to the new document to allow Kodexa to understand where it can
find the original document. 

```python
document.source
```