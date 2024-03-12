from __future__ import annotations

import inspect
import logging
import time
import uuid
from inspect import signature
from textwrap import dedent
from typing import List, Optional, Dict
from uuid import uuid4

import yaml

from kodexa.connectors import FolderConnector
from kodexa.connectors.connectors import get_caller_dir
from kodexa.model import Document, ContentObject

logger = logging.getLogger()


def new_id():
    """
    Generates a new unique ID.

    Returns:
        str: A new unique ID generated using the UUID version 4 algorithm.
    """
    return str(uuid.uuid4()).replace("-", "")


class InMemoryContentProvider:
    """A class used to support getting content (documents or native) to
    and from the pipeline.

    Attributes:
        content_objects (dict): A dictionary to store content objects.
    """

    """A content provider is used to support getting content (documents or native) to
    and from the pipeline

    Args:

    Returns:

    """

    def __init__(self):
        self.content_objects = {}

    def get_content(self, content_object: ContentObject):
        """Method to get the content of a specific content object.

        Args:
            content_object (ContentObject): The content object whose content is to be fetched.

        Returns:
            content: The content of the specified content object.
        """
        return self.content_objects[content_object.id]

    def put_content(self, content_object: ContentObject, content):
        """Method to put the content of a specific content object.

        Args:
            content_object (ContentObject): The content object whose content is to be stored.
            content: The content to be stored.
        """
        self.content_objects[content_object.id] = content


class PipelineContext:
    """Pipeline context is created when you create a pipeline and it provides a way to access information about the
    pipeline that is running. It can be made available to steps/functions so they can interact with it.
    It also provides access to the 'stores' that have been added to the pipeline.

    Attributes:
        execution_id (str): Unique identifier for the execution.
        statistics (PipelineStatistics): Statistics related to the pipeline.
        output_document (Optional[Document]): The final output document from the pipeline.
        content_objects (List[ContentObject]): List of content objects.
        content_provider (InMemoryContentProvider): Provider for the content.
        context (Dict): Contextual information.
        stop_on_exception (bool): Flag to indicate whether to stop on exception.
        current_document (Document): The current document being processed in the pipeline.
        document_family (None): Not used.
        content_object (None): Not used.
        document_store (None): Not used.
        status_handler (function): Handler for status updates.
        cancellation_handler (function): Handler for cancellation requests.
    """

    """Pipeline context is created when you create a pipeline and it provides a way to access information about the
    pipeline that is running.  It can be made available to steps/functions so they can interact with it.

    It also provides access to the 'stores' that have been added to the pipeline

    Args:

    Returns:

    """

    def __init__(
        self,
        content_provider=None,
        existing_content_objects=None,
        context=None,
        execution_id=None,
        status_handler=None,
        cancellation_handler=None,
    ):
        if content_provider is None:
            content_provider = InMemoryContentProvider()
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
        self.stop_on_exception = True
        self.current_document = None
        self.document_family = None
        self.content_object = None
        self.document_store = None
        self.status_handler = status_handler
        self.cancellation_handler = cancellation_handler

    def update_status(
        self, status_message: str, status_full_message: Optional[str] = None
    ):
        """Updates the status of the pipeline.

        Args:
            status_message (str): The status message.
            status_full_message (str, optional): The full status message. Defaults to None.
        """
        if self.status_handler is not None:
            self.status_handler(status_message, status_full_message)

    def is_cancelled(self) -> bool:
        """Checks if the pipeline is cancelled.

        Returns:
            bool: True if the pipeline is cancelled, False otherwise.
        """
        if self.cancellation_handler is not None:
            return self.cancellation_handler()

        return False

    def get_context(self) -> Dict:
        """Gets the context of the pipeline.

        Returns:
            Dict: The context of the pipeline.
        """
        return self.context

    def get_content_objects(self) -> List[ContentObject]:
        """Gets the content objects of the pipeline.

        Returns:
            List[ContentObject]: The content objects of the pipeline.
        """
        return self.content_objects

    def get_content(self, content_object: ContentObject):
        """Gets the content of a content object.

        Args:
            content_object (ContentObject): The content object to get the content of.
        """
        self.content_provider.get_content(content_object)

    def put_content(self, content_object: ContentObject, content):
        """Puts content into a content object.

        Args:
            content_object (ContentObject): The content object to put the content into.
            content: The content to put into the content object.
        """
        self.content_provider.put_content(content_object, content)

    def set_current_document(self, current_document: Document):
        """Sets the current document being processed in the pipeline.

        Args:
            current_document (Document): The current document to set.
        """
        self.current_document = current_document

    def get_current_document(self) -> Document:
        """Gets the current document being processed in the pipeline.

        Returns:
            Document: The current document being processed in the pipeline.
        """
        return self.current_document

    def set_output_document(self, output_document: Document):
        """Sets the output document from the pipeline.

        Args:
            output_document (Document): The output document to set.
        """
        self.output_document = output_document


class PipelineStep:
    """The representation of a step within a step, which captures both the step itself and
    also the details around the step's use.

    It is internally used by the Pipeline and is not a public API

    Attributes:
        step: The step to be added to the pipeline.
        name (str, optional): The name of the step. Defaults to None.
        options (dict, optional): The options for the step. Defaults to None.
        attach_source (bool, optional): Whether to attach the source to the step. Defaults to False.
        step_type (str, optional): The type of the step. Defaults to 'ACTION'.
    """

    """The representation of a step within a step, which captures both the step itself and
    also the details around the step's use.

    It is internally used by the Pipeline and is not a public API
    """

    def __init__(
        self, step, name=None, options=None, attach_source=False, step_type="ACTION", conditional=None
    ):
        if options is None:
            options = {}
        self.step = step
        self.name = name
        self.options = options
        self.step_type = step_type
        self.conditional = conditional

        if str(type(self.step)) == "<class 'type'>":
            logger.info(f"Adding new step class {step.__name__} to pipeline")
            self.step = step
        elif callable(self.step):
            logger.info(f"Adding new step function {step.__name__} to pipeline")
            self.name = step.__name__
        elif isinstance(self.step, str):
            logger.info(f"Adding new remote step {step} to pipeline")
            from kodexa import RemoteStep

            self.step = RemoteStep(
                step, step_type=step_type,
                options=options,
                attach_source=attach_source,
                conditional=conditional
            )
        else:
            logger.info(f"Adding new step {type(step)} to pipeline")

    def to_dict(self):
        """Converts the PipelineStep to a dictionary.

        Raises:
            Exception: If the step is a class instance style step or if the step does not implement to_dict().

        Returns:
            dict: The PipelineStep as a dictionary.
        """
        try:
            if str(type(self.step)) == "<class 'type'>":
                raise Exception(
                    "You can not yet deploy a pipeline with a class instance style step"
                )
            if isinstance(self.step, str):
                return {"ref": self.step, "options": self.options}
            if callable(self.step):
                metadata = {
                    "function": self.step.__name__,
                    "script": dedent(inspect.getsource(self.step)),
                }
            else:
                metadata = self.step.to_dict()

            metadata["name"] = self.name
            metadata["stepType"] = self.step_type
            metadata["options"] = self.options
            metadata["conditional"] = self.conditional
            return metadata
        except AttributeError as e:
            raise Exception("All steps must implement to_dict() for deployment", e)

    def execute(self, context: PipelineContext, document: Document):
        """Executes the PipelineStep.

        Args:
            context: The context in which to execute the step.
            document: The document to process.

        Returns:
            The processed document.

        Raises:
            Exception: If the step fails and stop_on_exception is True.
        """

        start = time.perf_counter()
        # noinspection PyBroadException
        try:
            context.set_current_document(document)
            logger.info("Starting step")
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
        except Exception as e:
            logger.warning(f"Step failed [{e}]")
            if context.stop_on_exception:
                raise

            return document


class LabelStep(object):
    """A simple step for handling the labelling for a document"""

    """A simple step for handling the labelling for a document"""

    def __init__(self, label: str, remove=False):
        self.label = label
        self.remove = remove

    def process(self, document: Document):
        """
        Process the document by adding or removing the label.

        Args:
            document (Document): The document to be processed.

        Returns:
            Document: The processed document.
        """
        if self.remove:
            document.remove_label(self.label)
        else:
            document.add_label(self.label)
        return document


class Pipeline:
    """A pipeline represents a way to bring together parts of the kodexa framework to solve a specific problem.

    When you create a Pipeline you must provide the connector that will be used to source the documents.

    Args:
        connector: The connector that will be the starting point for the pipeline.
        name (str, optional): The name of the pipeline. Defaults to 'Default'.
        stop_on_exception (bool, optional): Should the pipeline raise exceptions and stop. Defaults to True.
        logging_level (optional): The logging level of the pipeline. Defaults to logger.info.
        apply_lineage (bool, optional): Apply lineage to the pipeline. Defaults to True.

    Attributes:
        context (PipelineContext): The context of the pipeline.
        connector: The connector that will be the starting point for the pipeline.
        steps (List[PipelineStep]): The steps of the pipeline.
        name (str): The name of the pipeline.
        stop_on_exception (bool): Should the pipeline raise exceptions and stop.
        logging_level: The logging level of the pipeline.
        apply_lineage (bool): Apply lineage to the pipeline.

    Examples:
        >>> pipeline = Pipeline(FolderConnector(path='/tmp/', file_filter='example.pdf'))
    """

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

    def __init__(
        self,
        connector=None,
        name: str = "Default",
        stop_on_exception: bool = True,
        logging_level=logger.info,
        apply_lineage: bool = True,
    ):
        logger.info(f"Initializing a new pipeline {name}")

        if isinstance(connector, Document):
            self.connector = [connector]
        else:
            self.connector = connector

        self.steps: List[PipelineStep] = []
        self.name = name
        self.stop_on_exception = stop_on_exception
        self.logging_level = logging_level
        self.apply_lineage = apply_lineage

    def add_label(self, label: str, options=None, attach_source=False):
        """Adds a label to the document.

        Args:
            label (str): Label to add.
            options (optional): Options to be passed to the step if it is a simplified remote action. Defaults to None.
            attach_source (bool, optional): If step is simplified remote action this determines if we need to add the source. Defaults to False.

        Returns:
            Pipeline: The pipeline.
        """
        self.steps.append(
            PipelineStep(
                step=LabelStep(label),
                name=f"Add label {label}",
                options=options,
                attach_source=attach_source,
            )
        )
        return self

    def remove_label(self, label: str, options=None, attach_source=False):
        """Removes a label from the document.

        Args:
            label (str): Label to remove.
            options (optional): Options to be passed to the step if it is a simplified remote action. Defaults to None.
            attach_source (bool, optional): If step is simplified remote action this determines if we need to add the source. Defaults to False.

        Returns:
            Pipeline: The pipeline.
        """
        self.steps.append(
            PipelineStep(
                step=LabelStep(label, remove=True),
                name=f"Remove label {label}",
                options=options,
                attach_source=attach_source,
            )
        )
        return self

    def add_step(
        self, step, name=None, options=None, attach_source=False, step_type="ACTION", conditional=None
    ):
        """Add the given step to the current pipeline.

        Args:
            step: The step to add.
            name (optional): The name to use to describe the step. Defaults to None.
            options (optional): Options to be passed to the step if it is a simplified remote action. Defaults to None.
            attach_source (bool, optional): If step is simplified remote action this determines if we need to add the source. Defaults to False.
            step_type (str, optional): The type of step to add, can either be an ACTION or MODEL. Defaults to 'ACTION'.
            conditional (str, optional): The conditional to use for the step. Defaults to None.
        Returns:
            Pipeline: The instance of the pipeline.
        """
        if options is None:
            options = {}
        self.steps.append(
            PipelineStep(
                step=step,
                name=name,
                options=options,
                attach_source=attach_source,
                step_type=step_type,
                conditional=conditional
            )
        )

        return self

    def to_yaml(self):
        """Will return the YAML representation of any actions that support conversion to YAML.

        The YAML representation for RemoteAction's can be used for metadata only pipelines in the Kodexa Platform.

        Returns:
            str: YAML representation.
        """

        configuration_steps = []

        for step in self.steps:
            # noinspection PyBroadException
            try:
                configuration_steps.append(step.to_dict())
            except Exception:
                pass

        return yaml.dump(configuration_steps)

    def run(self, parameters=None):
        """Run the current pipeline.

        Args:
            parameters (optional): Parameters for the pipeline. Defaults to None.

        Returns:
            PipelineContext: The context from the run.
        """
        if parameters is None:
            parameters = {}

        if self.connector is None:
            raise Exception("You can not run a pipeline that has no connector in place")

        self.context = PipelineContext()
        self.context.stop_on_exception = self.stop_on_exception

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

            else:
                logger.warning("A step did not return a document?")

        logger.info(f"Completed pipeline {self.name}")

        return self.context

    @staticmethod
    def from_url(url, headers=None, *args, **kwargs):
        """Build a new pipeline with the input being a document created from the given URL.

        Args:
            url (str): The URL ie. https://www.google.com.
            headers (dict, optional): A dictionary of headers. Defaults to None.

        Returns:
            Pipeline: A new instance of a pipeline.
        """
        return Pipeline(Document.from_url(url, headers), *args, **kwargs)

    @staticmethod
    def from_file(file_path: str, *args, **kwargs) -> Pipeline:
        """Create a new pipeline using a file path as a source.

        Args:
            file_path (str): The path to the file.

        Returns:
            Pipeline: A new pipeline.
        """
        return Pipeline(Document.from_file(file_path), *args, **kwargs)

    @staticmethod
    def from_text(text: str, *args, **kwargs) -> Pipeline:
        """Build a new pipeline and provide text as the basic to create a document.

        Args:
            text (str): Text to use to create document.

        Returns:
            Pipeline: A new pipeline.
        """
        return Pipeline(Document.from_text(text), *args, **kwargs)

    @staticmethod
    def from_folder(
        folder_path: str,
        filename_filter: str = "*",
        recursive: bool = False,
        relative: bool = False,
        unpack=False,
        caller_path: str = get_caller_dir(),
        *args,
        **kwargs,
    ) -> Pipeline:
        """Create a pipeline that will run against a set of local files from a folder.

        Args:
            folder_path (str): The folder path.
            filename_filter (str, optional): The filter for filename (i.e. *.pdf). Defaults to "*".
            recursive (bool, optional): Should we look recursively in sub-directories. Defaults to False.
            relative (bool, optional): Is the folder path relative to the caller. Defaults to False.
            caller_path (str, optional): The caller path (defaults to trying to work this out from the stack). Defaults to get_caller_dir().
            unpack (bool, optional): Treat the files in the folder as KDXA documents and unpack them using from_kdxa. Defaults to False.

        Returns:
            Pipeline: A new pipeline.
        """
        return Pipeline(
            FolderConnector(
                folder_path,
                filename_filter,
                recursive=recursive,
                relative=relative,
                caller_path=caller_path,
                unpack=unpack,
            ),
            *args,
            **kwargs,
        )


class PipelineStatistics:
    """A class to represent the statistics for the processed document.

    Attributes:
        documents_processed (int): The number of documents processed.
    """

    def __init__(self):
        self.documents_processed = 0

    def processed_document(self, document):
        """Updates statistics based on this document completing processing.

        Args:
            document (str): The document that has been processed.

        """
        self.documents_processed += 1
