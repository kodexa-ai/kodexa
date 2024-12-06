import logging

from kodexa import ContentNode

logger = logging.getLogger(__name__)

def get_pretty_text_from_lines(lines: list[ContentNode], scale, include_line_uuid=False) -> str:
    pretty_text = ""
    for line_index, line in enumerate(lines):
        line_content = f"('{line.uuid}')" if include_line_uuid else ""
        current_x = 0
        for word in line.select('//word'):
            x = int(word.get_bbox()[0] * scale)
            spaces_needed = max(1, x - current_x)  # Ensure at least one space
            line_content += " " * spaces_needed
            line_content += f"{word.get_all_content()}"
            current_x = x + len(word.get_all_content())

        pretty_text += line_content + "\n"

    return pretty_text


def get_max_width(lines: list[ContentNode], max_width=None) -> int:
    if max_width is None:
        # Find the line with the most words
        max_words_line = max(lines, key=lambda line: sum(len(word.get_all_content()) for word in line.select('//word')))

        # Calculate max_width based on the length of all words plus spaces
        max_width = sum(len(word.get_all_content()) for word in max_words_line.select('//word')) + (len(max_words_line.select('//word'))*4) - 1

    if max_width < 250:
        max_width = 250

    return max_width


def get_scale_from_words(words: list[ContentNode], max_width) -> float:
    # Get the bboxes
    bboxes = [word.get_bbox() for word in words]

    # Find the overall bounding box
    min_x = min(bbox[0] for bbox in bboxes)
    max_x = max(bbox[2] for bbox in bboxes)
    min_y = min(bbox[1] for bbox in bboxes)
    max_y = max(bbox[3] for bbox in bboxes)

    # Invert y-axis
    max_y, min_y = min_y, max_y

    # Calculate scale factor to fit within max_width
    scale = max_width / (max_x - min_x)

    return scale


def get_pretty_page(page: ContentNode, max_width=None, include_line_uuid=False) -> str:
    """
    Get a pretty representation of the page

    :param page: The page to get the pretty representation for
    :param max_width: The maximum width of the page
    :param include_line_uuid: Include the line UUID in the pretty representation

    :return: A pretty representation of the page
    """

    logger.info(f"Getting pretty page {page.index}")

    pretty_text = ""
    content_areas = page.select('//content-area')

    lines = page.select('//line')

    max_width = get_max_width(lines, max_width)
    logger.info(f"Max width: {max_width}")

    words = page.select('//word')
    if len(words) == 0:
        return page.get_all_content()

    scale = get_scale_from_words(words, max_width)
    for area_index, area in enumerate(content_areas):

        if area_index > 0:
            pretty_text += "\n\n"  # Add extra newline between content areas

        pretty_text += get_pretty_text_from_lines(area.select('//line'), scale, include_line_uuid)

    logger.debug(f"Pretty Page: {page.index}: \n{pretty_text}")

    return pretty_text