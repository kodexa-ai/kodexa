from types import MethodType


def add_method_to_node(func, node):
    """

    Args:
      func: 
      node: 

    Returns:

    """
    setattr(node, func.__name__, MethodType(func, node))
