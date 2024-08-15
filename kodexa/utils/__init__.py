"""
This module provides a set of functions to manipulate and convert taxonomy objects for use within a data model.
It includes functions to convert taxonomy names to various naming conventions such as property names, class names,
and group paths. Additionally, it offers utility functions for string manipulation, like converting snake case strings
to camel case or title case, making string names safe for use as attribute names, converting strings to hexadecimal
color codes, estimating the token count of a text, and recursively finding all non-abstract subclasses of a given class.
"""

import keyword
import logging
import re
from inspect import isabstract

from kodexa.model.objects import Taxon

logger = logging.getLogger(__name__)


def taxon_to_property_name(taxon: Taxon):
    # We need to convert the taxon name to a property name
    # if the name of the taxon doesn't look like a UUID we will camel case
    # it otherwise we will camelcase the taxon label
    safe_property_name = to_snake(safe_name(taxon.label))
    taxon.external_name = safe_property_name
    return safe_property_name


def taxon_to_class_name(taxon: Taxon):
    # We need to convert the taxon name to a class name
    # if the name of the taxon doesn't look like a UUID we will camel case
    # it otherwise we will camelcase the taxon label
    safe_class_name = snake_to_camel(safe_name(taxon.label))
    taxon.external_name = safe_class_name
    return safe_class_name


def taxon_to_group_path(taxon: Taxon):
    # We need to get the "group_name" from one of the taxons
    # Which is the first part of the taxon path
    return taxon.path.split('/')[0]


def snake_to_camel(snake_str):
    components = snake_str.replace(" ", "_").split("_")
    # We convert first letter of second word to uppercase
    return components[0].strip().title() + "".join(
        x.strip().title() for x in components[1:]
    )


def to_snake(base_str):
    components = base_str.replace(" ", "_").replace("-", "_").split("_")

    # if the base string starts with a number than we add n_ to the start
    if components[0].isdigit():
        components[0] = "n_" + components[0]

    # We convert first letter of second word to uppercase
    return "_".join(x.strip().lower() for x in components)


def make_safe_attribute_name(name):
    # Replace invalid characters (anything not a letter, digit, or underscore) with an underscore
    safe_name = ''.join(char if char.isalnum() or char == '_' else '_' for char in name)

    # If the name starts with a digit, prepend an underscore
    if safe_name[0].isdigit():
        safe_name = '_' + safe_name

    # Append an underscore if the name is a Python keyword
    if keyword.iskeyword(safe_name):
        safe_name += '_'

    return safe_name


def safe_name(string):
    """
    Removes invalid characters from a string, replaces spaces with underscores, removes leading/trailing underscores and hyphens, and makes the string lowercase. If the resulting string
    * starts with a number, it prefixes it with "n_".

    :param string: The string to be transformed.
    :return: The transformed string.
    """
    # Remove invalid characters

    # trim the string
    string = string.strip()

    string = re.sub(r"[^\w\s-]", "", string)

    # Replace spaces with underscores
    string = re.sub(r"\s+", "_", string)

    # Remove leading/trailing underscores and hyphens
    string = string.strip("_-")

    # Make it lowercase
    string = string.lower()

    if string[0].isdigit():
        # can't have things starting with a number
        string = "n_" + string

    # make sure we don't collide with a python keyword
    return make_safe_attribute_name(string)


def snake_case_to_title_case(snake_case_string):
    words = snake_case_string.split("_")
    title_case_words = [word.capitalize() for word in words]
    return " ".join(title_case_words)


def string_to_hex_color(string):
    # Remove any leading or trailing whitespace from the string
    string = string.strip()

    # Calculate the hash value of the string
    hash_value = hash(string)

    # Convert the hash value to a 24-bit hexadecimal color code
    hex_color = "#{:06x}".format(hash_value & 0xFFFFFF)

    return hex_color


def get_is_square_bracket_first(string):
    first_square_bracket = string.find("[")
    first_bracket = string.find("{")
    # Check if both "{" and "[" exist in the string
    if first_bracket != -1 and first_square_bracket != -1:
        # Compare their indices to determine which appears first
        if first_bracket < first_square_bracket:
            return False
        else:
            return True
    # If only one of them exists, return the one that appears
    elif first_bracket != -1:
        return False
    elif first_square_bracket != -1:
        return True
    else:
        return None


def cosine_similarity(v1, v2):
    """Compute the cosine similarity between two vectors."""
    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm_a = sum(a * a for a in v1) ** 0.5
    norm_b = sum(b * b for b in v2) ** 0.5
    return dot_product / (norm_a * norm_b)


def estimate_token_count(text, avg_token_length=1):
    # Removing spaces to focus on characters that form tokens
    char_count = len(text.replace(" ", ""))
    # Estimating token count
    estimated_tokens = char_count / avg_token_length
    return round(estimated_tokens)


def get_all_concrete_subclasses(cls):
    """
    Recursively find all non-abstract subclasses of a given class.

    Parameters:
    cls (class): The parent class to find subclasses for.

    Returns:
    list: A list of all non-abstract subclasses of cls.
    """
    concrete_subclasses = []
    for subclass in cls.__subclasses__():
        if not isabstract(subclass):
            concrete_subclasses.append(subclass)
        concrete_subclasses.extend(get_all_concrete_subclasses(subclass))
    return concrete_subclasses
