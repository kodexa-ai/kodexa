import logging
import os
import uuid
from typing import Optional, List

import jinja2
from kodexa import ContentNode
from kodexa.model.model import Tag, Document
from kodexa.model.objects import ContentException, Taxon, Taxonomy, Assistant
from pydantic import BaseModel

from kodexa.utils import snake_to_camel, to_snake, taxon_to_property_name, taxon_to_class_name, taxon_to_group_path

logger = logging.getLogger()


class KodexaDocumentLLMWrapper:

    doc = None
    entities = None

    def __init__(self, doc: Document):
        self.doc = doc


    def get_doc(self):
        return self.doc


class LLMDataAttribute(BaseModel):
    """
    This is the data structure that is used take the results from the LLM so
    we can use it.  We use this as a base class for building classes that align
    with a taxonomy
    """

    value: Optional[str] = None
    line_ids: Optional[list[str]] = None
    taxon_path: Optional[str] = None
    data_type: Optional[str] = None
    value_path: Optional[str] = None
    normalized_text: Optional[str] = None
    node_uuid_list: Optional[List[int]] = None
    tag_uuid: Optional[str] = None
    page_number: Optional[int] = None
    exceptions: Optional[list[ContentException]] = None

    def copy_from(self, source: "LLMDataAttribute"):
        self.tag_uuid = source.tag_uuid
        self.value = source.value
        self.normalized_text = source.normalized_text
        self.line_ids = source.line_ids
        self.exceptions = source.exceptions
        self.node_uuid_list = source.node_uuid_list
        self.page_number = source.page_number

    def create_exception(
            self,
            exception_type_id: str,
            exception_type: str,
            normalized_text: str,
            message: str,
            exception_detail: str,
    ):
        content_exception = ContentException(
            exception_type=exception_type,
            exception_detail=exception_detail,
            message=message,
            tag_uuid=self.tag_uuid,
        )
        self.exceptions.append(content_exception)


class LLMDataObject(BaseModel):
    """
    A class to represent a LLM (Large Language Model) data object.

    ...

    Attributes
    ----------
    group_uuid : str, optional
        A unique identifier for the group, by default None
    cell_index : int, optional
        The index of the cell which is really the row, by default 0

    Methods
    -------
    __init__(self, document: "KodexaDocumentLLMWrapper" = None, **data: Any):
        Initializes the LLMDataObject with a given document and additional data.
    apply_labels(self, document: KodexaDocumentLLMWrapper, parent_group_uuid: str = None):
        Applies labels to the document if it exists.
    """

    group_uuid: Optional[str] = None
    cell_index: int = 0
    exceptions: Optional[list[ContentException]] = None

    class Config:
        arbitrary_types_allowed = True

    def get_all_review_pages(self):
        """
        Returns a list of unique page numbers that would be included in the review.

        :return: list of unique page numbers
        """
        pages = set()
        for field in self.__fields__:
            pages.update(self._get_field_pages(field))
        return sorted(list(pages))

    def _get_field_pages(self, field):
        if isinstance(getattr(self, field), list):
            pages = set()
            for item in getattr(self, field):

                if isinstance(item, LLMDataObject):
                    pages.update(item.get_all_review_pages())
            return pages
        elif isinstance(getattr(self, field), LLMDataAttribute):
            if getattr(self, field).value != getattr(self, field).normalized_text:
                return {getattr(self, field).page_number}
        elif isinstance(getattr(self, field), LLMDataObject):
            return getattr(self, field).get_all_review_pages()
        return set()

    def update_from_review(self, review_dict):
        """
        Update the node UUIDs and value based on the provided review dictionary.

        :param review_dict: A dictionary containing the updated review information
        """
        for field, field_data in review_dict.items():
            self._update_field_review(field, field_data)

    def _update_field_review(self, field, field_data):
        if isinstance(field_data, list):
            for i, item_data in enumerate(field_data):
                if i < len(getattr(self, field)):
                    getattr(self, field)[i].update_from_review(item_data)
        elif isinstance(field_data, dict):
            if isinstance(getattr(self, field), LLMDataAttribute):
                self._update_data_attribute(field, field_data)
            elif isinstance(getattr(self, field), LLMDataObject):
                getattr(self, field).update_from_review(field_data)

    def _update_data_attribute(self, field, field_data):
        attr = getattr(self, field)
        if 'value' in field_data:
            attr.value = field_data['value']
        if 'node_uuids' in field_data:
            attr.node_uuid_list = field_data['node_uuids']
        if 'normalized_text' in field_data:
            attr.normalized_text = field_data['normalized_text']

    def to_review(self, page_number=None):
        """
        Build a representation of the data object and its data attributes that is a dict that includes the
        value, normalized text and node UUIDs so we can use this to review mismatched value/normalized
        with the LLM for a specific page number.

        :param page_number: Optional page number to filter the review items
        :return: dict of this data object and children for the specified page
        """
        review = {}
        for field in self.__fields__:
            review_field = self._build_review(field, page_number)
            if review_field:
                review[field] = review_field
        return review

    def _build_review(self, field, page_number=None):
        if isinstance(getattr(self, field), list):
            review_field = []
            for item in getattr(self, field):
                if isinstance(item, LLMDataObject):
                    new_review = item.to_review(page_number)
                    if new_review:
                        review_field.append(new_review)
            return review_field if review_field else None
        elif isinstance(getattr(self, field), LLMDataAttribute):
            if getattr(self, field).value != getattr(self, field).normalized_text:
                if page_number is None or getattr(self, field).page_number == page_number:
                    return {
                        "value": getattr(self, field).value,
                        "normalized_text": getattr(self, field).normalized_text,
                        "node_uuids": getattr(self, field).node_uuid_list,
                        "page_number": getattr(self, field).page_number,
                    }
        elif isinstance(getattr(self, field), LLMDataObject):
            return getattr(self, field).to_review(page_number)

        return None

    def create_exception(
            self,
            exception_type_id: str,
            exception_type: str,
            message: str,
            exception_detail: str,
            severity: str = "ERROR",
    ):
        content_exception = ContentException(
            exception_type=exception_type,
            exception_details=exception_detail,
            message=message,
            group_uuid=self.group_uuid,
            severity=severity,
        )
        if self.exceptions is None:
            self.exceptions = []

        self.exceptions.append(content_exception)

    def apply_labels(
            self, document: "KodexaDocumentLLMWrapper", parent_group_uuid: str = None,
            assistant: Optional["Assistant"] = None
    ):
        """
        Applies labels to the document if it exists.

        If a document has been assigned to the LLMDataObject, it calls the
        apply_labels method of the document with the current LLMDataObject and
        the parent group uuid.

        Parameters
        ----------
        document : KodexaDocumentLLMWrapper
            The Kodexa document LLM wrapper
        parent_group_uuid : str, optional
            A unique identifier for the parent group, by default None
        assistant : Assistant, optional
        """

        # Lets make sure we add all the content exceptions
        if self.exceptions is not None:
            for exception in self.exceptions:
                # We have two types of exception, one in the API and one in the
                # document
                from kodexa.model import ContentException as KodexaContentException
                internal_exception = KodexaContentException(
                    exception_type=exception.exception_type,
                    message=exception.message,
                    exception_details=exception.exception_details,
                    severity=exception.severity,
                    group_uuid=exception.group_uuid,
                    tag_uuid=exception.tag_uuid,
                )
                document.doc.add_exception(internal_exception)

        # Let's go through this data object and find all the attributes that have a value
        # then we will apply the labels to the document
        for field in self.__fields__:
            logger.info(f"Processing field {field}")
            value = getattr(self, field)

            if isinstance(value, list):
                logger.info(f"Processing as a list {value}")
                for item in value:
                    self.process_child(item, document, parent_group_uuid, assistant)
            else:
                logger.info(f"Processing as a single value {value}")
                self.process_child(value, document, parent_group_uuid, assistant)

    def process_child(self, value, document, parent_group_uuid, assistant):

        logger.info(f"Processing child {value}")
        if isinstance(value, LLMDataAttribute):
            # We need to add the label to the document for this attribute

            tag = value.taxon_path

            # TODO need to work out why we are missing them?
            logger.info(f"Value: {value.normalized_text}, node_uuid_list: {value.node_uuid_list}")
            if value.node_uuid_list is None:
                value.node_uuid_list = value.line_ids
            logger.info(f"Applying label {tag} to node UUIDs {value.node_uuid_list}")

            if isinstance(value.node_uuid_list, int):
                value.node_uuid_list = [value.node_uuid_list]

            nodes_to_label: list[ContentNode] = (
                [
                    document.doc.get_persistence().get_node(node_uuid)
                    for node_uuid in value.node_uuid_list if (node_uuid != '0' and node_uuid != 0)
                ]
                if value.node_uuid_list
                else []
            )

            tag_uuid = str(uuid.uuid4())
            for node in nodes_to_label:
                if node:
                    if not node.has_tag(tag):
                        try:
                            confidence = -1 if value.value_path == 'DERIVED' else 1
                            node.tag(
                                tag_to_apply=tag,
                                value=value.normalized_text,
                                tag_uuid=tag_uuid,
                                cell_index=self.cell_index,
                                selector="//word",
                                confidence=confidence,
                                group_uuid=self.group_uuid,
                                parent_group_uuid=parent_group_uuid,
                                owner_uri=f"assistant://{assistant.id}" if assistant else f"model://taxonomy-llm",
                            )
                        except:
                            logger.error(f"Error tagging node {node.uuid} with tag {tag}")
                    else:
                        current_value = node.get_feature_values("tag", tag)
                        new_tag = Tag(cell_index=self.cell_index,
                                      uuid=tag_uuid,
                                      value=value.normalized_text,
                                      confidence=-1,
                                      group_uuid=self.group_uuid,
                                      parent_group_uuid=parent_group_uuid,
                                      owner_uri=f"assistant://{assistant.id}" if assistant else f"model://taxonomy-llm")
                        current_value.append(new_tag)
                        node.remove_feature("tag", tag)
                        node.add_feature("tag", tag, current_value, single=False)
                        # try:
                        #     if value.data_type == 'Derived':
                        #         logger.info(f"Node already has tag {tag} - Tagging something nearby {node.get_all_content()}")
                        #         nearby_node = find_nearby_word_to_tag(node, tag)
                        #         nearby_node.tag(
                        #             tag_to_apply=tag,
                        #             value=value.normalized_text,
                        #             tag_uuid=tag_uuid,
                        #             cell_index=self.cell_index,
                        #             selector="//word",
                        #             confidence=-1,
                        #             group_uuid=self.group_uuid,
                        #             parent_group_uuid=parent_group_uuid,
                        #             owner_uri=f"assistant://{assistant.id}" if assistant else f"model://taxonomy-llm",
                        #         )
                        #     else:
                        #         logger.info(f"Node already has tag {tag} - Skipping.")
                        # except:
                        #     logger.error(f"Error tagging nearby node with tag {tag}")

            logger.info(f"Applied label {tag} to {len(nodes_to_label)} nodes")
        if isinstance(value, LLMDataObject):
            # We need to apply the labels to the document for this object
            value.apply_labels(document, parent_group_uuid=self.group_uuid)
            # logger.info(f"Applied labels to data object {value.group_uuid}")


def find_nearby_word_to_tag(node, tag):
    logger.info(f"find_nearby_word_to_tag: {tag}")
    # Create an ordered list of the lines on the page, sorted by distance from the target node
    target_line_index = node.index if node.node_type == 'line' else node.select('parent::line')[0].index
    all_lines_on_page = node.select('parent::page')[0].select('//line')

    print(target_line_index, len(all_lines_on_page), all_lines_on_page)
    sorted_lines = sorted(all_lines_on_page, key=lambda line: abs(target_line_index - line.index))
    # Find the first word that isn't yet tagged by this tag
    for line in sorted_lines:
        for word in line.select('//word'):
            if not word.has_tag(tag):
                return word
    return None


def get_template_env():
    """Get the Jinja2 template environmnet

    :return:

    Args:

    Returns:

    """
    cli_path = os.path.dirname(os.path.abspath(__file__))
    package_location = os.path.join(cli_path, "templates")
    template_loader = jinja2.FileSystemLoader([os.getcwd(), package_location])
    env = jinja2.Environment(loader=template_loader, autoescape=True)
    env.globals["snake_to_camel"] = snake_to_camel
    env.globals["to_snake"] = to_snake
    env.globals['taxon_to_property_name'] = taxon_to_property_name
    env.globals['taxon_to_class_name'] = taxon_to_class_name
    env.globals['taxon_to_group_path'] = taxon_to_group_path
    return env


def write_template(template, output_location, output_filename, context):
    """
    Write the given template out to a file

    Args:
      template: the name of the template
      output_location: the location to write the output
      output_filename: the name of the output file
      context: the context
    """
    template = get_template_env().get_template(template)
    processed_template = template.render(context)

    from pathlib import Path

    Path(output_location).mkdir(parents=True, exist_ok=True)
    with open(output_location + "/" + output_filename, "w") as text_file:
        text_file.write(processed_template)


def build_llm_data_classes_for_taxonomy(
        taxonomy: Taxonomy, output_dir: str, output_file: str, use_labels: bool = False
):
    """
    This function will use jinja templates to build a set of classes that represent a taxonomy,
    these classes will extend the LLMData class and therefore have the ability to take an LLM
    response and map it to the Kodexa Document identifying and labeling the nodes as needed

    :param taxonomy:
    :param output_dir:
    :param output_file:
    :param use_labels:
    :return:
    """

    # We will use a jinja template to build all the classes we need, to do this
    # will iterate over all the taxons the taxonomy
    def set_path(taxon: Taxon, parent_path: Optional[str] = None):
        if parent_path is not None:
            taxon.path = parent_path + "/" + taxon.name
        else:
            taxon.path = taxon.name
        if taxon.children:
            for child_taxon in taxon.children:
                set_path(child_taxon, taxon.path)

    for taxon in taxonomy.taxons:
        set_path(taxon, None)

    def collect_group_taxons(taxons: list[Taxon]) -> list[Taxon]:
        """
        Recursively collects all group taxons from a list of taxons.

        Args:
            taxons (list[Taxon]): The list of taxons to collect group taxons from.

        Returns:
            list[Taxon]: A list of group taxons.

        """
        group_taxons = []
        for taxon in taxons:
            if taxon.group:
                group_taxons.append(taxon)
            if taxon.children:
                group_taxons = group_taxons + collect_group_taxons(taxon.children)
        return group_taxons

    all_group_taxons = collect_group_taxons(taxonomy.taxons)
    all_group_taxons.reverse()
    context = {"taxons": all_group_taxons, "use_labels": use_labels}
    write_template("llm_data_class.j2", output_dir, output_file, context)

    # Lets log what we created
    logger.info(f"Created the following classes in {output_dir}/{output_file}")
    with open(f"{output_dir}/{output_file}", "r") as file:
        logger.info(file.read())
