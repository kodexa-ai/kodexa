from __future__ import annotations

import inspect
import logging
import sys
import traceback
import uuid
from collections import KeysView
from enum import Enum
from inspect import signature
from io import StringIO
from textwrap import dedent
from typing import List, Optional, Dict
from uuid import uuid4

import yaml

from kodexa.connectors import FolderConnector
from kodexa.connectors.connectors import get_caller_dir
from kodexa.model import Document, Store


def new_id():
    return str(uuid.uuid4()).replace("-", "")


class ContentType(Enum):
    DOCUMENT = 'DOCUMENT'
    NATIVE = 'NATIVE'


class ContentObject:

    def __init__(self, name="untitled", id=new_id(), content_type=ContentType.DOCUMENT, tags=[], metadata={}):
        self.id = id
        self.name = name
        self.content_type = content_type
        self.tags = tags
        self.metadata = metadata


class InMemoryContentProvider:
    """
    A content provider is used to support getting content (documents or native) to
    and from the pipeline
    """

    def __init__(self):
        self.content_objects = {}

    def get_content(self, content_object: ContentObject):
        return self.content_objects[content_object.id]

    def put_content(self, content_object: ContentObject, content):
        self.content_objects[content_object.id] = content


class InMemoryStoreProvider:
    """
    A store provider is used to support getting stores from the pipeline
    """

    def __init__(self):
        self.stores = {}

    def put_store(self, name: str, store: Store):
        self.stores[name] = store

    def get_store(self, name):
        return self.stores[name] if name in self.stores else None

    def get_store_names(self) -> KeysView:
        return self.stores.keys()


class PipelineContext:
    """
    Pipeline context is created when you create a pipeline and it provides a way to access information about the
    pipeline that is running.  It can be made available to steps/functions so they can interact with it.

    It also provides access to the 'stores' that have been added to the pipeline
    """

    def __init__(self, content_provider=None, store_provider=None,
                 existing_content_objects=None,
                 context=None):
        if content_provider is None:
            content_provider = InMemoryContentProvider()
        if store_provider is None:
            store_provider = InMemoryStoreProvider()
        if context is None:
            context = {}
        if existing_content_objects is None:
            existing_content_objects = []
        self.transaction_id = str(uuid4())
        self.statistics: PipelineStatistics = PipelineStatistics()
        self.output_document: Optional[Document] = None
        self.content_objects: List[ContentObject] = existing_content_objects
        self.content_provider = content_provider
        self.context: Dict = context
        self.store_provider = store_provider
        self.stop_on_exception = True
        self.current_document = None

    def get_context(self) -> Dict:
        return self.context

    def get_content_objects(self) -> List[ContentObject]:
        return self.content_objects

    def get_content(self, content_object: ContentObject):
        self.content_provider.get_content(content_object)

    def put_content(self, content_object: ContentObject, content):
        self.content_provider.put_content(content_object, content)

    def add_store(self, name: str, store):
        """
        Add a store with given name to the context

        :param name: the name to refer to the store with
        :param store: the instance of the store
        """
        self.store_provider.put_store(name, store)

    def get_store_names(self) -> KeysView:
        """
        Return the list of store names in context

        :return: the list of store names
        """
        return self.store_provider.get_store_names()

    def set_current_document(self, current_document: Document):
        """
        Set the Document that is currently being processed in the pipeline

        :param current_document: The current document
        """
        self.current_document = current_document

    def get_current_document(self) -> Document:
        """
        Get the current document that is being processed in the pipeline

        :return: The current document, or None
        """
        return self.current_document

    def set_output_document(self, output_document: Document):
        """
        Set the output document from the pipeline

        :param output_document: the final output document from the pipeline
        :return: the final output document
        """
        self.output_document = output_document

    def get_store(self, name: str, default: Store = None) -> Store:
        """
        Get a store with given name from the context

        :param name: the name to refer to the store with
        :param default: optionally the default to create the store as if it isn't there
        :return: the store, or None is not available
        """
        store = self.store_provider.get_store(name) if name in self.get_store_names() else None

        if not store and default:
            self.store_provider.put_store(name, default)
            default.set_pipeline_context(self)

        return self.store_provider.get_store(name)

    def merge_store(self, name, store):
        if name not in self.get_store_names():
            self.add_store(name, store)
        else:
            self.get_store(name).merge(store)


class PipelineStep:
    """
    The representation of a step within a step, which captures both the step itself and
    also the details around the step's use.

    It is internally used by the Pipeline and is not a public API
    """

    def __init__(self, step, enabled=False, condition=None, name=None):
        self.step = step
        self.name = name
        self.condition = condition
        self.enabled = enabled

        if callable(self.step):
            logging.info(f"Adding new step function {step.__name__} to pipeline {self.name}")
            self.name = step.__name__
        else:
            logging.info(f"Adding new step {step.get_name()} to pipeline {self.name}")

    def to_dict(self):
        try:
            if callable(self.step):
                metadata = {
                    'function': self.step.__name__,
                    'script': dedent(inspect.getsource(self.step))
                }
            else:
                metadata = self.step.to_dict()
            metadata['name'] = self.name
            metadata['condition'] = self.condition
            metadata['enabled'] = self.enabled
            return metadata
        except AttributeError as e:
            raise Exception("All steps must implement to_dict() for deployment", e)

    def execute(self, context, document):
        if self.will_execute(context, document):
            try:

                context.set_current_document(document)

                if not callable(self.step):
                    logging.info(f"Starting step {self.step.get_name()}")

                    if len(signature(self.step.process).parameters) == 1:
                        return self.step.process(document)
                    else:
                        return self.step.process(document, context)
                else:
                    logging.info(f"Starting step function {self.step.__name__}")

                    if len(signature(self.step).parameters) == 1:
                        return self.step(document)
                    else:
                        return self.step(document, context)
            except:
                tt, value, tb = sys.exc_info()
                document.exceptions.append({
                    "step": self.step.__name__ if callable(self.step) else self.step.get_name(),
                    "traceback": traceback.format_exception(tt, value, tb)
                })
                if context.stop_on_exception:
                    raise
                else:
                    return document
        else:
            return document

    def will_execute(self, context, document):
        if not self.enabled:
            return False

        if self.condition:
            from simpleeval import simple_eval
            return bool(
                simple_eval(self.condition, names={'document': document, 'step': self}))

        return True


class Pipeline:
    """
    A pipeline represents a way to bring together parts of the kodexa framework to solve a specific problem.

    When you create a Pipeline you must provide the connector that will be used to source the documents.

        >>> pipeline = Pipeline(FolderConnector(path='/tmp/', file_filter='example.pdf'))

    :param connector: the connector that will be the starting point for the pipeline
    :param name: the name of the pipeline (default 'Default')
    :param stop_on_exception: Should the pipeline raise exceptions and stop (default True)
    :param logging_level: The logging level of the pipeline (default INFO)
    """
    context: PipelineContext

    def __init__(self, connector, name="Default", stop_on_exception=True, logging_level=logging.INFO):
        logging.info(f"Initializing a new pipeline {name}")

        if isinstance(connector, Document):
            self.connector = [connector]
        else:
            self.connector = connector

        self.steps: List[PipelineStep] = []
        self.sink = None
        self.name = name
        self.context: PipelineContext = PipelineContext()
        self.context.stop_on_exception = stop_on_exception
        self.logging_level = logging_level

    def add_store(self, name, store):
        """
        Add the store to the pipeline so that it is available to the pipeline

            >>> pipeline = Pipeline(FolderConnector(path='/tmp/', file_filter='example.pdf'))
            >>> pipeline.add_store("test-store", InMemoryObjectStore())

        :param name: the name of the store (to refer to it)
        :param store: the store that should be added
        """
        self.context.add_store(name, store)

        return self

    def add_step(self, step, name=None, enabled=True, condition=None):
        """
        Add the given step to the current pipeline

            >>> pipeline = Pipeline(FolderConnector(path='/tmp/', file_filter='example.pdf'))
            >>> pipeline.add_step(ExampleStep())

        Note that it is also possible to add a function as a step, for example

            >>> def my_function(doc):
            >>>      doc.metadata.fishstick = 'foo'
            >>>      return doc
            >>> pipeline.add_step(my_function)

        :param step: the step to add
        :param name: the name to use to describe the step (default None)
        :param enabled: is the step enabled (default True)
        :param condition: condition to evaluate before executing the step (default None)
        """
        self.steps.append(PipelineStep(step=step, name=name, enabled=enabled, condition=condition))

        return self

    def set_sink(self, sink):
        """
        Set the sink you wish to use, note that it will replace any currently assigned
        sink

            >>> pipeline = Pipeline(FolderConnector(path='/tmp/', file_filter='example.pdf'))
            >>> pipeline.set_sink(ExampleSink())

        :param sink: the sink for the pipeline
        """
        logging.info(f"Setting sink {sink.get_name()} on {self.name}")
        self.sink = sink

        return self

    def to_yaml(self):
        """
        Will return the YAML representation of any actions that support conversion to YAML

        The YAML representation for RemoteAction's can be used for metadata only pipelines in the Kodexa Platform

        :return: YAML representation
        """

        configuration_steps = []

        for step in self.steps:

            try:
                configuration_steps.append(step.to_dict())
            except:
                pass

        return yaml.dump(configuration_steps)

    def run(self):
        """
        Run the current pipeline, note that you must have a sink in place to allow the pipeline to run

            >>> pipeline = Pipeline(FolderConnector(path='/tmp/', file_filter='example.pdf'))
            >>> pipeline.set_sink(ExampleSink())
            >>> pipeline.run()

        :return: The context from the run
        """
        self.context.statistics = PipelineStatistics()
        logging.info(f"Starting pipeline {self.name}")
        for document in self.connector:

            log_stream = StringIO()
            logging.basicConfig(stream=log_stream, level=self.logging_level)
            logging.info(f"Processing {document}")
            for step in self.steps:
                document = step.execute(self.context, document)

            if self.sink:
                logging.info(f"Writing to sink {self.sink.get_name()}")
                try:
                    self.sink.sink(document)
                except:
                    if document:
                        document.exceptions.append({
                            "step": self.sink.get_name(),
                            "exception": sys.exc_info()[0]
                        })
                    if self.context.stop_on_exception:
                        raise

            if document:
                document.log = log_stream.getvalue()

            self.context.statistics.processed_document(document)
            self.context.output_document = document

        logging.info(f"Completed pipeline {self.name}")

        return self.context

    @staticmethod
    def from_url(url, headers=None):
        """
        Build a new pipeline with the input being a document created from the given URL

        :param url: The URL ie. https://www.google.com
        :param headers: A dictionary of headers
        :return: A new instance of a pipeline
        """
        return Pipeline(Document.from_url(url, headers))

    @staticmethod
    def from_file(file_path: str) -> Pipeline:
        """
        Create a new pipeline using a file path as a source
        :param file_path: The path to the file
        :return: A new pipeline
        :rtype: Pipeline
        """
        return Pipeline(Document.from_file(file_path))

    @staticmethod
    def from_text(text: str) -> Pipeline:
        """
        Build a new pipeline and provide text as the basic to create a document

        :param text: Text to use to create document
        :return: A new pipeline
        :rtype: Pipeline
        """
        return Pipeline(Document.from_text(text))

    @staticmethod
    def from_folder(folder_path: str, filename_filter: str = "*", recursive: bool = False, relative: bool = False,
                    caller_path: str = get_caller_dir(), *args, **kwargs) -> Pipeline:
        """
        Create a pipeline that will run against a set of local files from a folder

        :param folder_path: The folder path
        :param filename_filter: The filter for filename (i.e. *.pdf)
        :param recursive: Should we look recursively in sub-directories (default False)
        :param relative: Is the folder path relative to the caller (default False)
        :param caller_path: The caller path (defaults to trying to work this out from the stack)
        :return: A new pipeline
        :rtype: Pipeline
        """
        return Pipeline(FolderConnector(folder_path, filename_filter, recursive, relative, caller_path))


class PipelineStatistics:
    """
    A set of statistics for the processed document

    documents_processed
    document_exceptions
    """

    def __init__(self):
        self.documents_processed = 0
        self.document_exceptions = 0

    def processed_document(self, document):
        """
        Update statistics based on this document completing processing

        :param document: the document that has been processed
        """
        self.documents_processed += 1

        if document.exceptions:
            self.document_exceptions += 1
