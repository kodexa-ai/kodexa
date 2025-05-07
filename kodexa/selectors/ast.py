"""Abstract Syntax Tree nodes for parsed XPath expressions.

This module contains basic nodes for representing parsed XPath expressions
created by the ANTLR-based parser. These classes provide the same functionality
as the original PLY-based parser's AST classes but are designed to work with
the ANTLR-generated parse tree.
"""

from __future__ import annotations

import re
from typing import List, Optional, Any, Dict, Union, Tuple

# Import these types but make them optional to avoid circular imports
# In a real implementation, you'd use proper type annotations
try:
    from kodexa import ContentNode, ContentFeature, Document
except ImportError:
    ContentNode = Any  
    ContentFeature = Any
    Document = Any

__all__ = [
    "SelectorContext",
    "UnaryExpression",
    "BinaryExpression",
    "PredicatedExpression",
    "PipelineExpression",
    "AbsolutePath",
    "Step",
    "NameTest",
    "NodeType",
    "AbbreviatedStep",
    "VariableReference",
    "FunctionCall",
]


class SelectorContext:
    """Context for selector resolution, maintains state during traversal."""
    
    def __init__(self, document: Document, first_only=False):
        """Initialize a new SelectorContext.
        
        Args:
            document: The document being searched
            first_only: Whether to return only the first match
        """
        self.pattern_cache = {}
        self.last_op = None
        self.document: Document = document
        self.stream = 0
        self.first_only = first_only

    def cache_pattern(self, pattern: str) -> re.Pattern:
        """Get a compiled regex pattern, caching for reuse.
        
        Args:
            pattern: The regex pattern string
            
        Returns:
            The compiled regex pattern
        """
        if pattern not in self.pattern_cache:
            self.pattern_cache[pattern] = re.compile(pattern)
        return self.pattern_cache[pattern]


class PipelineExpression:
    """A pipeline XPath expression (e.g., a stream b)."""

    def __init__(self, left: Any, op: str, right: Any):
        """Initialize a new PipelineExpression.
        
        Args:
            left: Left side of the pipeline
            op: The pipeline operator
            right: Right side of the pipeline
        """
        self.left = left
        self.op = op
        self.right = right

    def resolve(self, content_node: ContentNode, variables: Dict, context: SelectorContext) -> List[ContentNode]:
        """Resolve this pipeline expression.
        
        Args:
            content_node: The current content node
            variables: Variable bindings
            context: The selector context
            
        Returns:
            List of matching content nodes
        """
        left_nodes = self.left.resolve(content_node, variables, context)
        result_nodes: List[ContentNode] = []
        context.stream = context.stream + 1

        # If first_only is True and we already have left nodes, only process the first one
        nodes_to_process = left_nodes[:1] if context.first_only and left_nodes else left_nodes

        for node in nodes_to_process:
            right_results = self.right.resolve(node, variables, context)
            result_nodes.extend(right_results)
            # If first_only is True and we found a match, return immediately
            if context.first_only and result_nodes:
                break

        context.stream = context.stream - 1
        return result_nodes[:1] if context.first_only else result_nodes


class UnaryExpression:
    """A unary XPath expression (e.g., -foo)."""

    def __init__(self, op: str, right: Any):
        """Initialize a new UnaryExpression.
        
        Args:
            op: The operator
            right: The expression the operator is applied to
        """
        self.op = op
        self.right = right

    def resolve(self, content_node: ContentNode, variables: Dict, context: SelectorContext) -> Any:
        """Resolve this unary expression.
        
        Args:
            content_node: The current content node
            variables: Variable bindings
            context: The selector context
            
        Returns:
            The result of applying the operator to the right expression
        """
        # Handle negation
        if self.op == "-":
            right_value = self.right.resolve(content_node, variables, context)
            if isinstance(right_value, (int, float)):
                return -right_value
        
        return None


class BinaryExpression:
    """Any binary XPath expression (e.g., a/b, a and b, a | b)."""

    def __init__(self, left: Any, op: str, right: Any):
        """Initialize a new BinaryExpression.
        
        Args:
            left: Left side of the expression
            op: The operator
            right: Right side of the expression
        """
        self.left = left
        self.op = op
        self.right = right

    def resolve(self, content_node: ContentNode, variables: Dict, context: SelectorContext) -> Any:
        """Resolve this binary expression.
        
        Args:
            content_node: The current content node
            variables: Variable bindings
            context: The selector context
            
        Returns:
            The result of applying the operator to the left and right expressions
        """
        if self.op == "|":
            return self.left.resolve(
                content_node, variables, context
            ) + self.right.resolve(content_node, variables, context)
        if self.op == "=":
            return self.get_value(
                self.left, content_node, variables, context
            ) == self.get_value(self.right, content_node, variables, context)
        if self.op == "!=":
            return self.get_value(
                self.left, content_node, variables, context
            ) != self.get_value(self.right, content_node, variables, context)
        if self.op == "intersect":
            left_value = self.get_value(self.left, content_node, variables, context)
            right_value = self.get_value(self.right, content_node, variables, context)
            if isinstance(left_value, list) and isinstance(right_value, list):
                intersection_list = [
                    value for value in left_value if value in right_value
                ]
                return intersection_list

            return []
        if self.op == "and":
            return bool(
                self.get_value(self.left, content_node, variables, context)
            ) and bool(self.get_value(self.right, content_node, variables, context))
        if self.op == "or":
            return bool(
                self.get_value(self.left, content_node, variables, context)
            ) or bool(self.get_value(self.right, content_node, variables, context))
        
        # Handle path operations
        if self.op == "/" or self.op == "//":
            # For path expressions, resolve left first then apply right to each result
            left_results = self.left.resolve(content_node, variables, context)
            context.last_op = self.op
            
            all_results = []
            for node in left_results:
                right_results = self.right.resolve(node, variables, context)
                all_results.extend(right_results)
                
                # If first_only is True and we found a match, return immediately
                if context.first_only and all_results:
                    break
                    
            return all_results[:1] if context.first_only else all_results
        
        return None

    def get_value(self, side: Any, content_node: ContentNode, variables: Dict, context: SelectorContext) -> Any:
        """Get the value of an expression.
        
        Args:
            side: The expression to evaluate
            content_node: The current content node
            variables: Variable bindings
            context: The selector context
            
        Returns:
            The evaluated value
        """
        if isinstance(side, FunctionCall):
            return side.resolve(content_node, variables, context)
        if isinstance(side, (AbsolutePath, BinaryExpression, UnaryExpression)):
            return side.resolve(content_node, variables, context)

        return side


class PredicatedExpression:
    """A filtered XPath expression (e.g., $var[1], (a or b)[foo][@bar])."""

    def __init__(self, base: Any, predicates: List = None):
        """Initialize a new PredicatedExpression.
        
        Args:
            base: The base expression to be filtered
            predicates: List of filter predicates
        """
        self.base = base
        self.predicates = predicates or []

    def append_predicate(self, pred: Any) -> None:
        """Add a predicate to this expression.
        
        Args:
            pred: The predicate to add
        """
        self.predicates.append(pred)

    def resolve(self, content_node: ContentNode, variables: Dict, context: SelectorContext) -> List[ContentNode]:
        """Resolve this predicated expression.
        
        Args:
            content_node: The current content node
            variables: Variable bindings
            context: The selector context
            
        Returns:
            List of content nodes that match the predicates
        """
        nodes = self.base.resolve(content_node, variables, context)
        results = []
        for idx, node in enumerate(nodes):
            for predicate in self.predicates:
                if isinstance(predicate, int) and predicate == idx:
                    results.append(node)
                    return results

                if not isinstance(predicate, int) and predicate.resolve(node, variables, context):
                    results.append(node)

        return results


class AbsolutePath:
    """An absolute XPath path (e.g., /a/b/c, //a/ancestor:b/@c)."""

    def __init__(self, op: str = "/", relative: Any = None):
        """Initialize a new AbsolutePath.
        
        Args:
            op: The operator used to root the expression
            relative: The relative path after the absolute root operator
        """
        self.op = op
        self.relative = relative

    def resolve(self, content_node: ContentNode, variables: Dict, context: SelectorContext) -> List[ContentNode]:
        """Resolve this absolute path.
        
        Args:
            content_node: The current content node
            variables: Variable bindings
            context: The selector context
            
        Returns:
            List of matching content nodes
        """
        if self.op == "/":
            context.last_op = "/"
            # Start from the root node for absolute paths
            root_node = content_node
            while root_node.get_parent() is not None:
                root_node = root_node.get_parent()
            
            if self.relative is None:
                return [root_node]
                
            return self.relative.resolve(root_node, variables, context)
            
        if self.op == "//":
            context.last_op = "//"
            # Start from the root but search all descendants
            root_node = content_node
            while root_node.get_parent() is not None:
                root_node = root_node.get_parent()
                
            return self.relative.resolve(root_node, variables, context)
            
        raise Exception(f"Unsupported absolute path operator: {self.op}")


class Step:
    """A single step in a relative path."""

    def __init__(self, axis: Optional[str], node_test: Any, predicates: List):
        """Initialize a new Step.
        
        Args:
            axis: The axis for this step
            node_test: The node test to apply
            predicates: List of predicates to filter nodes
        """
        self.axis = axis
        self.node_test = node_test
        self.predicates = predicates

    def resolve(self, content_node: ContentNode, variables: Dict, context: SelectorContext) -> List[ContentNode]:
        """Resolve this step.
        
        Args:
            content_node: The current content node
            variables: Variable bindings
            context: The selector context
            
        Returns:
            List of matching content nodes
        """
        if content_node is None:
            return []

        match = True
        if isinstance(content_node, ContentFeature):
            match = self.node_test.test(content_node, variables, context)

        axis_node = None

        if isinstance(content_node, ContentNode):
            axis_node = content_node

            if self.axis == "parent":
                parent = axis_node.get_parent()
                # For parent axis, we need to check if any parent in the hierarchy matches
                while parent is not None:
                    # For wildcard, return any parent
                    if self.node_test is None or (hasattr(self.node_test, 'name') and self.node_test.name == '*'):
                        return [parent]
                    
                    # If the parent node type matches the requested node type, return it
                    if hasattr(self.node_test, 'name') and (parent.node_type == self.node_test.name):
                        return [parent]
                    
                    # Try the next parent
                    parent = parent.get_parent()
                
                # Look for parents elsewhere in the document to handle cross-references
                if hasattr(self.node_test, 'name') and self.node_test.name != '*':
                    possible_parents = context.document.get_persistence().get_content_nodes(
                        self.node_test.name, 
                        axis_node, 
                        True
                    )
                    for possible_parent in possible_parents:
                        # Check if this node is a parent of our node
                        current = axis_node
                        while current is not None:
                            if current.get_parent() is not None and current.get_parent().id == possible_parent.id:
                                return [possible_parent]
                            current = current.get_parent()
                
                return []

            nodes = self.node_test.test(axis_node, variables, context)
            final_nodes = []

            # Special case for the direct node type with index selector pattern (like '//p[0]')
            # This pattern should return all nodes of the given type, regardless of their index
            direct_node_index_pattern = len(self.predicates) == 1 and isinstance(self.predicates[0], int)

            # If first_only is True, only process until we find the first match
            for node in nodes:
                match = True
                for predicate in self.predicates:
                    if isinstance(predicate, int):
                        # For direct node type with index patterns (//p[0]), ignore the index check
                        if direct_node_index_pattern:
                            # Keep match as True
                            pass
                        elif predicate == node.index:
                            match = True
                        else:
                            match = False
                    elif not predicate.resolve(node, variables, context):
                        match = False

                if match:
                    final_nodes.append(node)
                    if context.first_only:
                        break

            return final_nodes

        if match:
            return [axis_node]

        if self.axis is not None:
            return self.resolve(axis_node, variables, context)

        return []


class NameTest:
    """An element name node test for a Step."""

    def __init__(self, prefix: Optional[str], name: str):
        """Initialize a new NameTest.
        
        Args:
            prefix: The namespace prefix, or None if unspecified
            name: The local element name
        """
        self.prefix = prefix
        self.name = name

    def test(self, obj: Union[ContentNode, ContentFeature], variables: Dict, context: SelectorContext) -> Union[bool, List[ContentNode]]:
        """Test if a node matches this name test.
        
        Args:
            obj: The node or feature to test
            variables: Variable bindings
            context: The selector context
            
        Returns:
            Either a boolean result or a list of matching nodes
        """
        if isinstance(obj, ContentNode):
            if context.stream > 0:
                # For streaming contexts, ensure exact node type match
                if self.name == "*" or self.name == obj.node_type:
                    return [obj]
                return []
            else:
                # For "//p" style selectors, we need to be more careful
                # Get all possible matching nodes first
                nodes = context.document.get_persistence().get_content_nodes(
                    self.name, obj, context.last_op != "/"
                )

                # Only add the current node if it exactly matches the node type
                if self.name == "*" or self.name == obj.node_type:
                    nodes = [obj] + nodes
                
                # Filter the nodes to ensure exact node type matches
                if self.name != "*":
                    nodes = [node for node in nodes if node.node_type == self.name]

                # If first_only is True, return only the first matching node
                return nodes[:1] if context.first_only else nodes

        if isinstance(obj, ContentFeature):
            return self.name == "*" or (
                    obj.feature_type == self.prefix and obj.name == self.name
            )
        return False


class NodeType:
    """A node type node test for a Step."""

    def __init__(self, name: str, literal: Optional[str] = None):
        """Initialize a new NodeType.
        
        Args:
            name: The node type name, such as node or text
            literal: The literal argument (for processing-instruction type)
        """
        self.name = name
        self.literal = literal


class AbbreviatedStep:
    """An abbreviated XPath step (. or ..)."""

    def __init__(self, abbr: str):
        """Initialize a new AbbreviatedStep.
        
        Args:
            abbr: The abbreviated step (. or ..)
        """
        self.abbr = abbr

    def resolve(self, content_node: ContentNode, variables: Dict, context: SelectorContext) -> List[ContentNode]:
        """Resolve this abbreviated step.
        
        Args:
            content_node: The current content node
            variables: Variable bindings
            context: The selector context
            
        Returns:
            List of matching content nodes
        """
        if self.abbr == ".":
            return [content_node]
        if self.abbr == "..":
            return [content_node.get_parent()] if content_node.get_parent() else []
        raise Exception(f"Unsupported abbreviated step: {self.abbr}")


class VariableReference:
    """An XPath variable reference (e.g., $foo, $myns:foo)."""

    def __init__(self, name: Tuple[Optional[str], str]):
        """Initialize a new VariableReference.
        
        Args:
            name: A tuple (prefix, localname) containing the variable name
        """
        self.name = name

    def resolve(self, variables: Dict, context: SelectorContext) -> Any:
        """Resolve this variable reference.
        
        Args:
            variables: Variable bindings
            context: The selector context
            
        Returns:
            The value of the variable, or None if not found
        """
        if self.name[1] in variables:
            return variables[self.name[1]]

        return None


class FunctionCall:
    """An XPath function call (e.g., foo(), my:foo(1), foo(1, 'a', $var))."""

    def __init__(self, prefix: Optional[str], name: str, args: List):
        """Initialize a new FunctionCall.
        
        Args:
            prefix: The namespace prefix, or None if unspecified
            name: The local function name
            args: A list of argument expressions
        """
        self.prefix = prefix
        self.name = name
        self.args = args

    def resolve(self, content_node: "ContentNode", variables: Dict, context: "SelectorContext") -> Any:
        """Resolve this function call.
        
        Args:
            content_node: The current content node
            variables: Variable bindings
            context: The selector context
            
        Returns:
            The result of the function call
        """
        args = []
        for arg in self.args:
            if isinstance(arg, VariableReference):
                args.append(arg.resolve(variables, context))
            elif hasattr(arg, 'resolve'):
                args.append(arg.resolve(content_node, variables, context))
            else:
                args.append(arg)

        if self.name == "true":
            return True

        if self.name == "false":
            return False

        if self.name == "contentRegex":
            compiled_pattern = context.cache_pattern(args[0])

            content_to_test = content_node.content

            if len(args) > 1:
                if bool(args[1]):
                    content_to_test = content_node.get_all_content()

            if content_to_test is not None and compiled_pattern.match(content_to_test):
                return content_to_test

            return None

        if self.name == "typeRegex":
            compiled_pattern = context.cache_pattern(args[0])
            if content_node.node_type is not None and compiled_pattern.match(
                content_node.node_type
            ):
                return content_node.node_type

            return None

        if self.name == "tagRegex":
            compiled_pattern = context.cache_pattern(args[0])
            for feature in content_node.get_features_of_type("tag"):
                if feature.name is not None and compiled_pattern.match(feature.name):
                    return True

            return False

        if self.name == "hasTag":

            if len(args) > 0:
                # Check for a specific tag
                return content_node.has_feature("tag", args[0])
            else:
                print(content_node.get_tags())
                return len(content_node.get_tags()) > 0

        if self.name == "hasFeature":
            if len(args) == 0:
                return len(content_node.get_features()) > 0

            return content_node.has_feature(args[0], args[1])

        if self.name == "hasFeatureValue":
            values = content_node.get_feature_values(args[0], args[1])
            if values:
                for value in values:
                    if value == args[2]:
                        return True
            return False

        if self.name == "content":
            return content_node.content

        if self.name == "id":
            return content_node.id

        if self.name == "node_type":
            return content_node.node_type

        if self.name == "index":
            return content_node.index

        return []