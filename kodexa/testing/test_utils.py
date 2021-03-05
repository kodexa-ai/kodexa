import errno
import importlib
import logging
from typing import List, cast

from addict import addict

from kodexa import Assistant, AssistantResponse, LocalDocumentStore
from kodexa import ContentEvent, ContentNode, Document, DocumentActor, DocumentTransition, PipelineContext, \
    TableDataStore, TransitionType
from kodexa.assistant.assistant import AssistantMetadata
from kodexa.model.model import AssistantEvent, ContentObjectReference, DocumentStore

logger = logging.getLogger('kodexa.testing')


def print_data_table(context: PipelineContext, store_name: str):
    """A small helper to support working with a store in a test

    Args:
      context: PipelineContext: The context for the pipeline
      store_name: str: The store name

    """
    if store_name in context.get_store_names():
        print(f"\n{store_name}\n")
        data_table = cast(TableDataStore, context.get_store(store_name))
        from texttable import Texttable
        table = Texttable(max_width=1000).header(data_table.columns)
        table.add_rows(data_table.rows, header=False)
        print(table.draw() + "\n")
    else:
        print(f"\n{store_name} - MISSING\n")


def snapshot_store(context: PipelineContext, store_name: str, filename: str):
    """Capture the data in a store to a JSON file so that we can use it later
    to compare the data (usually in a test)

    Args:
      context: the pipeline context
      store_name: the name of the store
      filename: the name of the file to snapshot the store to
      context: PipelineContext:
      store_name: str:
      filename: str:

    Returns:

    """
    import json
    logger.warning('Snapshotting store')
    with open(filename, 'w') as f:
        json.dump(context.get_store(store_name).to_dict(), f)


def simplify_node(node: ContentNode):
    """

    Args:
      node: ContentNode:

    Returns:

    """
    return {
        "index": node.index,
        "node_type": node.node_type,
        "features": [feature.to_dict() for feature in node.get_features()],
        "content": node.content,
        "content_parts": node.content_parts,
        "children": [simplify_node(child_node) for child_node in node.children]
    }


def simplify_document(document: Document) -> dict:
    """

    Args:
      document: Document:

    Returns:

    """
    return {
        "content_node": simplify_node(document.get_root())
    }


def compare_document(document: Document, filename: str, throw_exception=True):
    """

    Args:
      document: Document:
      filename: str:
      throw_exception:  (Default value = True)

    Returns:

    """
    from os import path
    import json
    import os

    try:
        os.makedirs('test_snapshots')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    filename = "test_snapshots/" + filename

    if not path.exists(filename):
        with open(filename, 'w') as f:
            simplified_document = simplify_document(document)
            json.dump(simplified_document, f)

        logger.warning("WARNING!!! Creating snapshot file")
        raise Exception("Creating snapshot, invalid test")

    with open(filename) as f:
        snapshot_document = json.load(f)

    target_document = json.loads(json.dumps(simplify_document(document)))

    from deepdiff import DeepDiff
    diff = DeepDiff(snapshot_document, target_document, ignore_order=False)

    if bool(diff) and throw_exception:
        print(diff)
        raise Exception('Document does not match')

    return diff


def compare_store(context: PipelineContext, store_name: str, filename: str, throw_exception=True):
    """Compare a store in the provided pipeline context to the store that has been snapshot

    Args:
      context: the pipeline context containing the store to compare
      store_name: the name of the store
      filename: the filename of the
      throw_exception: throw an exception if there is a mismatch (Default value = True)
      context: PipelineContext:
      store_name: str:
      filename: str:

    Returns:

    """

    from os import path

    import os
    try:
        os.makedirs('test_snapshots')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    filename = "test_snapshots/" + filename

    if not path.exists(filename):
        snapshot_store(context, store_name, filename)
        logger.warning("WARNING!!! Creating snapshot file")
        raise Exception("Creating snapshot, invalid test")

    import json

    # A list of the descriptions of issues
    issues = []

    target_table_store: TableDataStore = cast(TableDataStore, context.get_store(store_name))

    if target_table_store is None:
        print(f"Store {store_name} doesn't exist in the pipeline context")
        return False

    with open(filename) as f:
        snapshot_table_store = TableDataStore.from_dict(json.load(f))

    row_match = len(target_table_store.rows) == len(snapshot_table_store.rows)

    if not row_match:
        issues.append(
            f"Number of rows don't match {len(target_table_store.rows)} is target vs {len(snapshot_table_store.rows)} in snapshot")
    else:
        for row_idx, row in enumerate(target_table_store.rows):
            for cell_idx, cell in enumerate(row):
                if snapshot_table_store.rows[row_idx][cell_idx] != target_table_store.rows[row_idx][cell_idx]:
                    issues.append(
                        f"Row {row_idx} cell {cell_idx} doesn't match - should be [{snapshot_table_store.rows[row_idx][cell_idx]}] but is [{target_table_store.rows[row_idx][cell_idx]}]")

    col_match = len(target_table_store.columns) == len(snapshot_table_store.columns)

    if not col_match:
        issues.append(
            f"Number of columns don't match {len(target_table_store.columns)} is target vs {len(snapshot_table_store.columns)} in snapshot")
    else:
        for col_idx, col in enumerate(target_table_store.columns):
            if snapshot_table_store.columns[col_idx] != col:
                issues.append(
                    f"Column name at index {col_idx} doesn't match - should be [{snapshot_table_store.columns[col_idx]}] but is [{col}]")

    if len(issues) > 0 and throw_exception:
        raise Exception("\n".join(issues))

    for issue in issues:
        print(issue)

    return len(issues) == 0


class AssistantTestHarness:
    """
    A test harness to allow the testing of assistants in unit tests and offline for development

    >>> util = ExtensionPackUtil("../kodexa.yml")
    >>> harness = util.get_assistant("my-assistant", stores=[my_local_store])

    """

    def __init__(self, assistant: Assistant, stores: List[DocumentStore], kodexa_metadata_path: str,
                 metadata: AssistantMetadata):
        """
        Initialize the test harness

        Args:
            assistant: the instance of the assistant
            stores: the list of stores (usually LocalDocumentStore) that we will use to monitor for events
            kodexa_metadata_path (str): the path to the kodexa.yml (or kodexa.json)
            metadata (AssistantMetadata): the assistant metadata to use for this assistant
        """
        self.assistant = assistant
        self.stores = stores
        self.kodexa_metadata_path = kodexa_metadata_path
        self.metadata = metadata

        for store in self.stores:
            store.register_listener(self)

    def test_assistant_event(self, assistant_event: AssistantEvent):
        pass

    def process_event(self, event: ContentEvent):
        """The harness will take the content event and
        will pass it to the assistant - then we will
        take each of the pipelines and run the document
        through them in turn (note in the platform this might be in parallel)

        Args:
          event: ContentEvent: The event to process

        Returns:
          None

        """
        from kodexa import AssistantContext
        assistant_context = AssistantContext(self.metadata, self.kodexa_metadata_path, self.stores)

        response: AssistantResponse = self.assistant.process_event(event, assistant_context)

        # We need to get the document down
        store = self.get_store(event)

        for assistant_pipeline in response.pipelines:
            document = store.get_document_by_content_object(event.document_family, event.content_object)
            if document is not None:
                pipeline = assistant_pipeline.pipeline
                pipeline.connector = [
                    ContentObjectReference(content_object=event.content_object, document=document, store=store,
                                           document_family=event.document_family)]
                pipeline_context = pipeline.run()

                if pipeline_context.output_document is not None and assistant_pipeline.write_back_to_store:
                    # We need to build the transition between the old and the new
                    document_relationship = DocumentTransition(TransitionType.DERIVED, event.content_object.id, None,
                                                               DocumentActor("testing", "assistant"))

                    store.add_related_document_to_family(event.document_family.id, document_relationship,
                                                         pipeline_context.output_document)

        pass

    def register_local_document_store(self, store: LocalDocumentStore):
        """
        Register a local document store with this harness

        Args:
          store: LocalDocumentStore:

        Returns:

        """
        pass

    def get_store(self, event: ContentEvent) -> DocumentStore:
        """
        Get a document store for the event (based on the document family ID)

        Args:
          event: ContentEvent:

        Returns:
          The instance of the document store
        """
        for store in self.stores:
            if event.document_family.store_ref == store.get_ref():
                return store

        raise Exception(f"Unable to get store ref {event.document_family.store_ref}")


class OptionException(Exception):
    """
    An exception that is raised when there is a problem with a requests option
    """
    pass


class ExtensionPackUtil:
    """
    A utility that can be used to access an action defined in a kodexa.yml.

    This allows you to use the kodexa.yml in unit tests to ensure it matches your current action code

    >>> util = ExtensionPackUtil("../kodexa.yml")
    >>> pipeline = Pipeline()
    >>> pipeline.add_step(util.get_step("my-action",{"my-option": "cheese"}))
    >>> pipeline.run()

    """

    def __init__(self, file_path='kodexa.yml'):
        self.file_path = file_path

        if file_path.endswith('.yml'):
            import yaml

            with open(file_path, 'r') as stream:
                self.kodexa_metadata = addict.Dict(yaml.safe_load(stream))

        if file_path.endswith('.json'):
            import json

            with open(file_path, 'r') as stream:
                self.kodexa_metadata = addict.Dict(json.load(stream))

    def get_step(self, action_slug, options=None):
        """

        Args:
          action_slug (str): the slug to the action (ie. pdf-parser)
          options (dict):  the options for the action as a dictionary (Default value = None)

        Returns:

        """
        if options is None:
            options = {}

        for service in self.kodexa_metadata.services:
            if service.type == 'action' and service.slug == action_slug:
                # TODO We need to validate all the options

                if len(service.metadata.options) > 0:
                    option_names = []
                    for option in service.metadata.options:
                        option_names.append(option.name)
                        if option.name not in options and option.default is not None:
                            options[option.name] = option.default
                        if option.required and option.name not in options:
                            raise OptionException(f"Missing required option {option.name}")

                    for option_name in options.keys():
                        if option_name not in option_names:

                            # We need to determine if this is actually a group
                            is_group = False
                            for check_option in service.metadata.options:
                                if check_option['group'] is not None:
                                    if check_option['group']['name'] == option_name:
                                        is_group = True

                            if not is_group:
                                raise OptionException(f"Unexpected option {option_name}")

                # We need to create and return our action
                module = importlib.import_module(service.step.package)
                klass = getattr(module, service.step['class'])
                new_instance = klass(**options)

                # Since we will be using to access metadata we will need to
                # make sure we have a to_dict() that is able to convert this step properly

                import types

                def general_to_dict(self):
                    return {
                        'ref': f'./{action_slug}',
                        'options': options
                    }

                new_instance.to_dict = types.MethodType(general_to_dict, new_instance)
                return new_instance

        raise Exception("Unable to find the action " + action_slug)

    def get_assistant_test_harness(self, assistant_slug, assistant_metadata: AssistantMetadata, options=None,
                                   stores=None) -> AssistantTestHarness:
        """Provides a local test harness that can be used to validate the functionality
        of an assistant in a test case

        Args:
          assistant_slug (str): The slug for the assistant (ie. pdf-parser-assistant)
          assistant_metadata (AssistantMetadata): the metadata to use for the assistant
          stores (List): a list of the document stores to monitor (Default value = None)
          options (dict): The options to provide  (Default value = None)

        Returns:
          The assistant test harness

        """
        if stores is None:
            stores = []
        assistant = self.get_assistant(assistant_slug, options)

        return AssistantTestHarness(assistant, stores, self.file_path, assistant_metadata)

    def get_assistant(self, assistant_slug, options=None):
        """Create an instance of an assistant from the kodexa metadata

        Args:
          assistant_slug: param options:
          options:  (Default value = None)

        Returns:

        """
        if options is None:
            options = {}

        for service in self.kodexa_metadata.services:
            if service.type == 'assistant' and service.slug == assistant_slug:
                # TODO We need to validate all the options

                # We need to create and return our action

                logger.info(f"Creating new assistant {service.assistant}")
                module = importlib.import_module(service.assistant.package)
                klass = getattr(module, service.assistant['class'])
                return klass(**options)

        raise Exception("Unable to find the assistant " + assistant_slug)
