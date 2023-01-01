---
title: First Steps
---

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

# Saving a Document (Filesystem)

A document can be saved to a file, or to a store. In this example we will save the document to a
local file. By default the document will be saved in the Kodexa format, which is a SQLite database.

```python
document.to_kddb('my-document.kddb')
```

Note: By convention we store Kodexa documents in files with the extension .kddb (Kodexa Document Database)

# Loading a Document (Filesystem)

A document can be loaded from a file, or from a store. In this example we will load the document from a
local file. By default the document will be loaded from the Kodexa format, which is a SQLite database.

```python
document = Document.from_kddb('my-document.kddb')
```

## Detached Documents

When a document is loaded from a file by default any changes you make are then made to the file immediately. This is
useful for many use cases, but sometimes you want to make changes to a document without affecting the original file.

For example, you may want to make changes to a document, but not save them until you are sure that they are correct.

To do this you can load the document in detached mode.

```python
document = Document.from_kddb('my-document.kddb', detached=True)
```