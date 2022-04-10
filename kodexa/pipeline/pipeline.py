from __future__ import annotations

import inspect
import logging
import sys
import time
import traceback
import uuid
from collections import KeysView
from inspect import signature
from textwrap import dedent
from typing import List, Optional, Dict
from uuid import uuid4

import yaml

from kodexa.connectors import FolderConnector
from kodexa.connectors.connectors import get_caller_dir, DocumentStoreConnector
from kodexa.model import Document, Store, ContentObject
from kodexa.stores.stores import DocumentStore

logger = logging.getLogger()


def new_id():
    """ """
    return str(uuid.uuid4()).replace("-", "")


class InMemoryContentProvider:
    """A content provider is used to support getting content (documents or native) to
    and from the pipeline

    Args:

    Returns:

    """

    def __init__(self):
        self.content_objects = {}

    def get_content(self, content_object: ContentObject):
        """

        Args:
          content_object: ContentObject:

        Returns:

        """
        return self.content_objects[content_object.id]

    def put_content(self, content_object: ContentObject, content):
        """

        Args:
          content_object: ContentObject:
          content:

        Returns:

        """
        self.content_objects[content_object.id] = content


class InMemoryStoreProvider:
    """A store provider is used to support getting stores from the pipeline"""

    def __init__(self):
        self.stores = {}

    def put_store(self, name: str, store: Store):
        """

        Args:
          name: str:
          store: Store:

        Returns:

        """
        self.stores[name] = store

    def get_store(self, name):
        """

        Args:
          name:

        Returns:

        """
        return self.stores[name] if name in self.stores else None

    def get_store_names(self) -> KeysView:
        """ """
        return self.stores.keys()


class PipelineContext:
    """Pipeline context is created when you create a pipeline and it provides a way to access information about the
    pipeline that is running.  It can be made available to steps/functions so they can interact with it.

    It also provides access to the 'stores' that have been added to the pipeline

    Args:

    Returns:

    """

    def __init__(self, content_provider=None, store_provider=None,
                 existing_content_objects=None,
                 context=None, execution_id=None,
                 status_handler=None, cancellation_handler=None):
        if content_provider is None:
            content_provider = InMemoryContentProvider()
        if store_provider is None:
            store_provider = InMemoryStoreProvider()
        if context is None:
            context = {}
        if existing_content_objects is None:
            existing_content_objects = []

        self.execution_id = str(uuid4()) if execution_id is None else execution_id
        self.statistics: PipelineStatistics = PipelineStatistics()
        self.output_document: Optional[Document] = None
        self.content_objects: List[ContentObject] = existing_content_objects
        self.content_provider = content_provider
        self.context: Dict = context
        self.store_provider = store_provider
        self.stop_on_exception = True
        self.current_document = None
        self.document_family = None
        self.content_object = None
        self.document_store = None
        self.status_handler = status_handler
        self.cancellation_handler = cancellation_handler

    def update_status(self, status_message: str, status_full_message: Optional[str] = None):
        if self.status_handler is not None:
            self.status_handler(status_message, status_full_message)

    def is_cancelled(self) -> bool:
        if self.cancellation_handler is not None:
            return self.cancellation_handler()
        else:
            return False

    def get_context(self) -> Dict:
        """ """
        return self.context

    def get_content_objects(self) -> List[ContentObject]:
        """ """
        return self.content_objects

    def get_content(self, content_object: ContentObject):
        """

        Args:
          content_object: ContentObject:

        Returns:

        """
        self.content_provider.get_content(content_object)

    def put_content(self, content_object: ContentObject, content):
        """

        Args:
          content_object: ContentObject:
          content:

        Returns:

        """
        self.content_provider.put_content(content_object, content)

    def add_store(self, name: str, store):
        """Add a store with given name to the context

        Args:
          name: the name to refer to the store with
          store: the instance of the store
          name: str:

        Returns:

        """
        self.store_provider.put_store(name, store)

    def get_store_names(self) -> KeysView:
        """

        Args:

        Returns:
          :return: the list of store names

        """
        return self.store_provider.get_store_names()

    def set_current_document(self, current_document: Document):
        """Set the Document that is currently being processed in the pipeline

        Args:
          current_document: The current document
          current_document: Document:

        Returns:

        """
        self.current_document = current_document

    def get_current_document(self) -> Document:
        """Get the current document that is being processed in the pipeline

        :return: The current document, or None

        Args:

        Returns:

        """
        return self.current_document

    def set_output_document(self, output_document: Document):
        """Set the output document from the pipeline

        Args:
          output_document: the final output document from the pipeline
          output_document: Document:

        Returns:
          the final output document

        """
        self.output_document = output_document

    def get_store(self, name: str, default: Store = None) -> Store:
        """Get a store with given name from the context

        Args:
          name: the name to refer to the store with
          default: optionally the default to create the store as if it isn't there
          name: str:
          default: Store:  (Default value = None)

        Returns:
          the store, or None is not available

        """
        store = self.store_provider.get_store(name) if name in self.get_store_names() else None

        if not store and default:
            self.store_provider.put_store(name, default)
            default.set_pipeline_context(self)

        return self.store_provider.get_store(name)

    def merge_store(self, name, store):
        """
        Merge a store into the pipeline context

        Args:
          name:
          store:

        Returns:

        """
        if name not in self.get_store_names():
            logger.debug("New store, adding")
            self.add_store(name, store)
        else:
            logger.debug("Existing store, merging")
            self.get_store(name).merge(store)


class PipelineStep:
    """The representation of a step within a step, which captures both the step itself and
    also the details around the step's use.

    It is internally used by the Pipeline and is not a public API
    """

    def __init__(self, step, name=None, options=None, attach_source=False,
                 step_type='ACTION'):
        if options is None:
            options = {}
        self.step = step
        self.name = name
        self.options = options
        self.step_type = step_type

        if str(type(self.step)) == "<class 'type'>":
            logger.info(f"Adding new step class {step.__name__} to pipeline")
            self.step = step
        elif callable(self.step):
            logger.info(f"Adding new step function {step.__name__} to pipeline")
            self.name = step.__name__
        elif isinstance(self.step, str):
            logger.info(f"Adding new remote step {step} to pipeline")
            from kodexa import RemoteStep
            self.step = RemoteStep(step, step_type=step_type, options=options, attach_source=attach_source)
        else:
            logger.info(f"Adding new step {type(step)} to pipeline")

    def to_dict(self):
        """ """
        try:
            if str(type(self.step)) == "<class 'type'>":
                raise Exception("You can not yet deploy a pipeline with a class instance style step")
            elif isinstance(self.step, str):
                return {
                    'ref': self.step,
                    'options': self.options
                }
            elif callable(self.step):
                metadata = {
                    'function': self.step.__name__,
                    'script': dedent(inspect.getsource(self.step))
                }
            else:
                metadata = self.step.to_dict()

            metadata['name'] = self.name
            metadata['stepType'] = self.step_type
            return metadata
        except AttributeError as e:
            raise Exception("All steps must implement to_dict() for deployment", e)

    def execute(self, context, document):

        start = time.perf_counter()
        try:

            context.set_current_document(document)
            logger.info(f"Starting step")
            if str(type(self.step)) == "<class 'type'>":

                logger.info(f"Starting step based on class {self.step}")

                # We need to handle the parameterization
                import copy

                option_copy = copy.deepcopy(self.options)
                step_instance = self.step(**option_copy)
                if len(signature(step_instance.process).parameters) == 1:
                    result_document = step_instance.process(document)
                else:
                    result_document = step_instance.process(document, context)

            elif not callable(self.step):
                logger.info(f"Starting step {type(self.step)}")

                if len(signature(self.step.process).parameters) == 1:
                    result_document = self.step.process(document)
                else:
                    result_document = self.step.process(document, context)
            else:
                logger.info(f"Starting step function {self.step.__name__}")

                if len(signature(self.step).parameters) == 1:
                    result_document = self.step(document)
                else:
                    result_document = self.step(document, context)

            end = time.perf_counter()
            logger.info(f"Step completed (f{end - start:0.4f}s)")

            return result_document
        except:
            logger.warning("Step failed")
            tt, value, tb = sys.exc_info()
            document.exceptions.append({
                "step": self.step.__name__ if callable(self.step) else type(self.step),
                "traceback": traceback.format_exception(tt, value, tb)
            })
            if context.stop_on_exception:
                raise
            else:
                return document


class LabelStep(object):
    """A simple step for handling the labelling for a document"""

    def __init__(self, label: str, remove=False):
        self.label = label
        self.remove = remove

    def process(self, document: Document):
        """

        Args:
          document: Document:

        Returns:

        """
        if self.remove:
            document.remove_label(self.label)
        else:
            document.add_label(self.label)
        return document


class PipelineStore:
    """ """

    def __init__(self, name: str, store: Store, extracted_labelled: bool = False):
        self.name = name
        self.store = store
        self.extract_labelled = extracted_labelled

    def extract(self, document):
        """

        Args:
          document:

        Returns:

        """
        # TODO implement
        pass


class Pipeline:
    """A pipeline represents a way to bring together parts of the kodexa framework to solve a specific problem.

    When you create a Pipeline you must provide the connector that will be used to source the documents.

    Args:
      connector: the connector that will be the starting point for the pipeline
      name: the name of the pipeline (default 'Default')
      stop_on_exception: Should the pipeline raise exceptions and stop (default True)
      logging_level: The logging level of the pipeline (default INFO)

    Returns:

    >>> pipeline = Pipeline(FolderConnector(path='/tmp/', file_filter='example.pdf'))
    """
    context: PipelineContext

    def __init__(self, connector=None, name: str = "Default", stop_on_exception: bool = True,
                 logging_level=logger.info, apply_lineage: bool = True):
        logger.info(f"Initializing a new pipeline {name}")

        if isinstance(connector, Document):
            self.connector = [connector]
        else:
            self.connector = connector

        self.steps: List[PipelineStep] = []
        self.stores: List[PipelineStore] = []
        self.name = name
        self.stop_on_exception = stop_on_exception
        self.logging_level = logging_level
        self.apply_lineage = apply_lineage

    def add_store(self, name: str, store: Store, extracted_labelled=False):
        """Add the store to the pipeline so that it is available to the pipeline

        Args:
          name: the name of the store (to refer to it)
          store: the store that should be added
          extracted_labelled: at the end of the pipeline we will extract the labelled data
        to this store (Default value = False)
          name: str:
          store: Store:

        Returns:

        >>> pipeline = Pipeline(FolderConnector(path='/tmp/', file_filter='example.pdf'))
            >>> pipeline.add_store("test-store", TableDataStore())
        """
        self.stores.append(PipelineStore(name, store, extracted_labelled))
        return self

    def add_label(self, label: str, options=None, attach_source=False):
        """Adds a label to the document

        Args:
          label: label to add
          options: options to be passed to the step if it is a simplified remote action (Default value = None)
          attach_source: if step is simplified remote action this determines if we need to add the source (Default value = False)
          label: str:

        Returns:
          the pipeline

        """
        self.steps.append(
            PipelineStep(step=LabelStep(label), name=f"Add label {label}",
                         options=options,
                         attach_source=attach_source))
        return self

    def remove_label(self, label: str, options=None, attach_source=False):
        """Adds a label to the document

        Args:
          label: label to remove
          options: options to be passed to the step if it is a simplified remote action (Default value = None)
          attach_source: if step is simplified remote action this determines if we need to add the source (Default value = False)
          label: str: the label to add

        Returns:
          the pipeline

        """
        self.steps.append(
            PipelineStep(step=LabelStep(label, remove=True), name=f"Remove label {label}",
                         options=options,
                         attach_source=attach_source))
        return self

    def add_step(self, step, name=None, options=None, attach_source=False,
                 step_type='ACTION'):
        """Add the given step to the current pipeline


        Note that it is also possible to add a function as a step, for example


        If you are using remote actions on a server, or for deployment to a remote
        pipeline you can also use a shorthand

        Args:
          step: the step to add
          name: the name to use to describe the step (default None)
          options: options to be passed to the step if it is a simplified remote action (Default value = None)
          attach_source: if step is simplified remote action this determines if we need to add the source (Default value = False)
          step_type: the type of step to add, can either be an ACTION or MODEL
        Returns:
          the instance of the pipeline

        >>> pipeline = Pipeline(FolderConnector(path='/tmp/', file_filter='example.pdf'))
            >>> pipeline.add_step(ExampleStep())

            >>> def my_function(doc):
            >>>      doc.metadata.fishstick = 'foo'
            >>>      return doc
            >>> pipeline.add_step(my_function)

            >>> pipeline.add_step('kodexa/html-parser',options={'summarize':False})
        """
        if options is None:
            options = {}
        self.steps.append(PipelineStep(step=step, name=name, options=options,
                                       attach_source=attach_source,
                                       step_type=step_type))

        return self

    def to_yaml(self):
        """Will return the YAML representation of any actions that support conversion to YAML

        The YAML representation for RemoteAction's can be used for metadata only pipelines in the Kodexa Platform

        :return: YAML representation

        Args:

        Returns:

        """

        configuration_steps = []

        for step in self.steps:

            try:
                configuration_steps.append(step.to_dict())
            except:
                pass

        return yaml.dump(configuration_steps)

    def run(self, parameters=None):
        """Run the current pipeline, note that you must have a sink in place to allow the pipeline to run


        :return: The context from the run

        Args:
          parameters:  (Default value = None)

        Returns:

        >>> pipeline = Pipeline(FolderConnector(path='/tmp/', file_filter='example.pdf'))
            >>> pipeline.set_sink(ExampleSink())
            >>> pipeline.run()
        """
        if parameters is None:
            parameters = {}

        if self.connector is None:
            raise Exception("You can not run a pipeline that has no connector in place")

        self.context = PipelineContext()
        self.context.stop_on_exception = self.stop_on_exception

        for pipeline_store in self.stores:
            logger.info(f"Adding store {pipeline_store.name}")
            self.context.add_store(pipeline_store.name, pipeline_store.store)

        self.context.statistics = PipelineStatistics()
        self.context.parameters = parameters

        logger.info(f"Starting pipeline {self.name}")

        # Note that a connector can return either an instance of a
        # document or it can refer to a document in a store - this is
        # important since if the document comes from a store then we
        # also need to know the content object and also the document family
        # and the store itself - to provide richness to the action

        for connector_object in self.connector:

            from kodexa.model.model import ContentObjectReference
            if isinstance(connector_object, ContentObjectReference):
                document = connector_object.document
                self.context.document_store = connector_object.store
                self.context.content_object = connector_object.content_object
                self.context.document_family = connector_object.document_family
            else:
                # Otherwise assume it is a document
                document = connector_object
                self.context.document_store = None
                self.context.content_object = None
                self.context.document_family = None

            logger.info(f"Processing {document}")

            initial_source_metadata = document.source
            lineage_document_uuid = document.uuid

            for step in self.steps:
                document = step.execute(self.context, document)

            if document:

                document.source = initial_source_metadata
                if self.apply_lineage:
                    document.source.lineage_document_uuid = lineage_document_uuid
                else:
                    document.source.lineage_document_uuid = None

                self.context.statistics.processed_document(document)
                self.context.output_document = document

                # Determine if any of the stores will automatically extract the data
                for store in self.stores:
                    if store.extract_labelled:
                        store.extract(document)

            else:
                logger.warning("A step did not return a document?")

        logger.info(f"Completed pipeline {self.name}")

        return self.context

    @staticmethod
    def from_store(store: DocumentStore, subscription=None, *args, **kwargs):
        """Build a new pipeline with the input documents from a document store

        Args:
          store: DocumentStore The URL ie. https://www.google.com
          subscription: str The subscription query to use (Default value = None)
          store: DocumentStore:
          *args:
          **kwargs:

        Returns:
          A new instance of a pipeline

        """
        return Pipeline(DocumentStoreConnector(store, subscription), *args, **kwargs)

    @staticmethod
    def from_url(url, headers=None, *args, **kwargs):
        """Build a new pipeline with the input being a document created from the given URL

        Args:
          url: The URL ie. https://www.google.com
          headers: A dictionary of headers (Default value = None)
          *args:
          **kwargs:

        Returns:
          A new instance of a pipeline

        """
        return Pipeline(Document.from_url(url, headers), *args, **kwargs)

    @staticmethod
    def from_file(file_path: str, *args, **kwargs) -> Pipeline:
        """Create a new pipeline using a file path as a source

        Args:
          file_path: The path to the file
          file_path: str:
          *args:
          **kwargs:

        Returns:
          Pipeline: A new pipeline

        """
        return Pipeline(Document.from_file(file_path), *args, **kwargs)

    @staticmethod
    def from_text(text: str, *args, **kwargs) -> Pipeline:
        """Build a new pipeline and provide text as the basic to create a document

        Args:
          text: Text to use to create document
          text: str:
          *args:
          **kwargs:

        Returns:
          Pipeline: A new pipeline

        """
        return Pipeline(Document.from_text(text), *args, **kwargs)

    @staticmethod
    def from_folder(folder_path: str, filename_filter: str = "*", recursive: bool = False, relative: bool = False,
                    unpack=False, caller_path: str = get_caller_dir(), *args, **kwargs) -> Pipeline:
        """Create a pipeline that will run against a set of local files from a folder

        Args:
          folder_path: The folder path
          filename_filter: The filter for filename (i.e. *.pdf)
          recursive: Should we look recursively in sub-directories (default False)
          relative: Is the folder path relative to the caller (default False)
          caller_path: The caller path (defaults to trying to work this out from the stack)
          unpack: Treat the files in the folder as KDXA documents and unpack them using from_kdxa (default False)
          folder_path: str:
          filename_filter: str:  (Default value = "*")
          recursive: bool:  (Default value = False)
          relative: bool:  (Default value = False)
          caller_path: str:  (Default value = get_caller_dir())
          *args:
          **kwargs:

        Returns:
          Pipeline: A new pipeline

        """
        return Pipeline(FolderConnector(folder_path, filename_filter, recursive=recursive, relative=relative,
                                        caller_path=caller_path, unpack=unpack), *args, **kwargs)


class PipelineStatistics:
    """A set of statistics for the processed document

    documents_processed
    document_exceptions

    Args:

    Returns:

    """

    def __init__(self):
        self.documents_processed = 0
        self.document_exceptions = 0

    def processed_document(self, document):
        """Update statistics based on this document completing processing

        Args:
          document: the document that has been processed

        Returns:

        """
        self.documents_processed += 1

        if document and document.exceptions:
            self.document_exceptions += 1
