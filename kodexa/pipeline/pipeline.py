import logging
import sys
import traceback
from inspect import signature
from io import StringIO
from uuid import uuid4

from kodexa import Document


class PipelineContext:
    """
    Pipeline context is created when you create a pipeline and it provides a way to access information about the
    pipeline that is running.  It can be made available to steps/functions so they can interact with it.

    It also provides access to the 'stores' that have been added to the pipeline
    """

    def __init__(self):
        self.transaction_id = str(uuid4())
        self.stores = {}
        self.statistics = PipelineStatistics()
        self.output_document = None

    def add_store(self, name, store):
        """
        Add a store with given name to the context

        :param name: the name to refer to the store with
        :param store: the instance of the store
        """
        self.stores[name] = store

    def get_store_names(self):
        """
        Return the list of store names in context

        :return: the list of store names
        """
        return list(self.stores.keys())

    def set_output_document(self, output_document):
        """
        Set the output document from the pipeline

        :param output_document: the final output document from the pipeline
        :return: the final output document
        """
        self.output_document = output_document

    def get_store(self, name, default=None):
        """
        Get a store with given name from the context

        :param name: the name to refer to the store with
        :param default: optionally the default to create the store as if it isn't there
        :return: the store, or None is not available
        """
        store = self.stores[name] if name in self.stores else None

        if not store and default:
            self.stores[name] = default

        return self.stores[name]


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

    def __init__(self, connector, name="Default", stop_on_exception=True, logging_level=logging.INFO):
        logging.info(f"Initializing a new pipeline {name}")

        if isinstance(connector, Document):
            self.connector = [connector]
        else:
            self.connector = connector

        self.steps = []
        self.sink = None
        self.name = name
        self.context = PipelineContext()
        self.stop_on_exception = stop_on_exception
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

    def add_step(self, step):
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
        """
        if callable(step):
            logging.info(f"Adding new step function {step.__name__} to pipeline {self.name}")
        else:
            logging.info(f"Adding new step {step.get_name()} to pipeline {self.name}")

        self.steps.append(step)

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
                try:
                    if not callable(step):
                        logging.info(f"Starting step {step.get_name()}")

                        if len(signature(step.process).parameters) == 1:
                            document = step.process(document)
                        else:
                            document = step.process(document, self.context)
                    else:
                        logging.info(f"Starting step function {step.__name__}")

                        if len(signature(step).parameters) == 1:
                            document = step(document)
                        else:
                            document = step(document, self.context)
                except:
                    tt, value, tb = sys.exc_info()
                    document.exceptions.append({
                        "step": step.__name__ if callable(step) else step.get_name(),
                        "traceback": traceback.format_exception(tt, value, tb)
                    })
                    if self.stop_on_exception:
                        raise

            if self.sink:
                logging.info(f"Writing to sink {self.sink.get_name()}")
                try:
                    self.sink.sink(document)
                except:
                    document.exceptions.append({
                        "step": self.sink.get_name(),
                        "exception": sys.exc_info()[0]
                    })
                    if self.stop_on_exception:
                        raise

            document.log = log_stream.getvalue()
            self.context.statistics.processed_document(document)

        logging.info(f"Completed pipeline {self.name}")

        return self.context


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
