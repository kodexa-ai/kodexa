"""Abstract Syntax Tree nodes for parsed XPath.

This module contains basic nodes for representing parsed XPath expressions.
The parser provided by this module creates its parsed XPath representation
from the classes defined in this module. Library callers will mostly not use
this module directly, unless they need to produce XPath ASTs from scratch or
perhaps introspect ASTs returned by the parser.

This code was derived from https://github.com/emory-libraries/eulxml
"""

from __future__ import unicode_literals

import re
import sys

# python2/3 string type logic borrowed from six
# NOTE: not importing six here because setup.py needs to generate
# the parser at install time, when six installation is not yet available
from kodexa import ContentNode, ContentFeature

__all__ = [
    'UnaryExpression',
    'BinaryExpression',
    'PredicatedExpression',
    'PipelineExpression',
    'AbsolutePath',
    'Step',
    'NameTest',
    'NodeType',
    'AbbreviatedStep',
    'VariableReference',
    'FunctionCall',
]


class PipelineExpression(object):
    '''A pipeline XPath expression'''

    def __init__(self, left, op, right):
        self.left = left
        '''the left side of the pipeline expression'''
        self.op = op
        '''the operator of the pipeline expression'''
        self.right = right
        '''the right side of the pipeline expression'''

    def resolve(self, content_node: ContentNode, variables):
        left_nodes = self.left.resolve(content_node, variables)
        result_nodes = []
        for node in left_nodes:
            result_nodes = result_nodes + self.right.resolve(node, variables)
        return result_nodes


class UnaryExpression(object):
    '''A unary XPath expression. Practially, this means -foo.'''

    def __init__(self, op, right):
        self.op = op
        '''the operator used in the expression'''
        self.right = right
        '''the expression the operator is applied to'''


KEYWORDS = {'or', 'and', 'div', 'mod'}


class BinaryExpression(object):
    '''Any binary XPath expression. a/b; a and b; a | b.'''

    def __init__(self, left, op, right):
        self.left = left
        '''the left side of the binary expression'''
        self.op = op
        '''the operator of the binary expression'''
        self.right = right
        '''the right side of the binary expression'''

    def resolve(self, content_node: ContentNode, variables):
        if self.op == '|':
            return self.left.resolve(content_node, variables) + self.right.resolve(content_node, variables)
        if self.op == '=':
            return self.get_value(self.left, content_node, variables) == self.get_value(self.right, content_node,
                                                                                        variables)
        if self.op == '!=':
            return self.get_value(self.left, content_node, variables) != self.get_value(self.right, content_node,
                                                                                        variables)
        if self.op == 'intersect':
            left_value = self.get_value(self.left, content_node, variables)
            right_value = self.get_value(self.right, content_node, variables)
            if isinstance(left_value, list) and isinstance(right_value, list):
                intersection_list = [value for value in left_value if value in right_value]
                return intersection_list
            else:
                return []
        if self.op == 'and':
            return bool(self.get_value(self.left, content_node, variables)) and bool(
                self.get_value(self.right, content_node, variables))
        if self.op == 'or':
            return bool(self.get_value(self.left, content_node, variables)) or bool(
                self.get_value(self.right, content_node, variables))

    def get_value(self, side, content_node, variables):
        if isinstance(side, FunctionCall):
            return side.resolve(content_node, variables)
        if isinstance(side, AbsolutePath):
            return side.resolve(content_node, variables)
        else:
            return side


class PredicatedExpression(object):
    '''A filtered XPath expression. $var[1]; (a or b)[foo][@bar].'''

    def __init__(self, base, predicates=None):
        self.base = base
        '''the base expression to be filtered'''
        self.predicates = predicates or []
        '''a list of filter predicates'''

    def append_predicate(self, pred):
        self.predicates.append(pred)

    def resolve(self, content_node, variables):
        nodes = self.base.resolve(content_node, variables)
        results = []
        for idx, node in enumerate(nodes):
            for predicate in self.predicates:
                if isinstance(predicate, int) and predicate == idx:
                    results.append(node)
                    return results
                else:
                    if predicate.resolve(node):
                        results.append(node)

        return results


class AbsolutePath(object):
    '''An absolute XPath path. /a/b/c; //a/ancestor:b/@c.'''

    def __init__(self, op='/', relative=None):
        self.op = op
        '''the operator used to root the expression'''
        self.relative = relative
        '''the relative path after the absolute root operator'''

    def resolve(self, content_node, variables):
        if self.op == '/':
            return self.relative.resolve(content_node, variables)
        if self.op == '//':
            results = []
            results = results + self.relative.resolve(content_node, variables)
            for child in content_node.children:
                results = results + self.resolve(child, variables)
            return results
        raise Exception("Not implemented")


class Step(object):
    '''A single step in a relative path. a; @b; text(); parent::foo:bar[5].'''

    def __init__(self, axis, node_test, predicates):
        self.axis = axis
        '''the step's axis, or @ or None if abbreviated or undefined'''
        self.node_test = node_test
        '''a NameTest or NodeType object describing the test represented'''
        self.predicates = predicates
        '''a list of predicates filtering the step'''

    def resolve(self, obj, variables):
        match = True

        if isinstance(obj, ContentFeature):
            match = self.node_test.test(obj)

        if isinstance(obj, ContentNode):
            content_node = obj
            for predicate in self.predicates:
                if isinstance(predicate, int):
                    if predicate == content_node.index:
                        match = True
                elif not predicate.resolve(content_node, variables):
                    match = False

            match = match and self.node_test.test(content_node, variables)

        if match:
            return [obj]
        else:
            return []


class NameTest(object):
    '''An element name node test for a Step.'''

    def __init__(self, prefix, name):
        self.prefix = prefix
        '''the namespace prefix used for the test, or None if unset'''
        self.name = name
        '''the node name used for the test, or *'''

    def test(self, obj, variables):
        if isinstance(obj, ContentNode):
            return self.name == '*' or obj.type == self.name
        if isinstance(obj, ContentFeature):
            return self.name == '*' or (obj.feature_type == self.prefix and obj.name == self.name)
        return False


class NodeType(object):
    '''A node type node test for a Step.'''

    def __init__(self, name, literal=None):
        self.name = name
        '''the node type name, such as node or text'''
        self.literal = literal
        '''the argument to the node specifier. XPath allows these only for
        processing-instruction() node tests.'''


class AbbreviatedStep(object):
    '''An abbreviated XPath step. . or ..'''

    def __init__(self, abbr):
        self.abbr = abbr
        '''the abbreviated step'''

    def resolve(self, content_node, variables):
        if self.abbr == '.':
            return [content_node]
        if self.abbr == '..':
            return [content_node.parent] if content_node.parent else []
        raise Exception("Not implemented")


class VariableReference(object):
    '''An XPath variable reference. $foo; $myns:foo.'''

    def __init__(self, name):
        self.name = name
        '''a tuple (prefix, localname) containing the variable name'''

    def resolve(self, variables):
        if self.name[1] in variables:
            return variables[self.name[1]]
        else:
            return None


class FunctionCall(object):
    '''An XPath function call. foo(); my:foo(1); foo(1, 'a', $var).'''

    def __init__(self, prefix, name, args):
        self.prefix = prefix
        '''the namespace prefix, or None if unspecified'''
        self.name = name
        '''the local function name'''
        self.args = args
        '''a list of argument expressions'''

    def resolve(self, content_node, variables):

        args = []
        for arg in self.args:
            if isinstance(arg, VariableReference):
                args.append(arg.resolve(variables))
            else:
                args.append(arg)

        if self.name == 'true':
            return True

        if self.name == 'false':
            return False

        if self.name == 'contentRegex':
            compiled_pattern = re.compile(args[0])

            content_to_test = content_node.content

            if len(args) > 1:
                if bool(args[2]):
                    content_to_test = content_node.get_all_content()

            if content_to_test is not None and compiled_pattern.match(content_to_test):
                return content_to_test
            else:
                return None

        if self.name == 'typeRegex':
            compiled_pattern = re.compile(args[0])
            if content_node.type is not None and compiled_pattern.match(content_node.type):
                return content_node.type
            else:
                return None

        if self.name == 'tagRegex':
            compiled_pattern = re.compile(args[0])
            for feature in content_node.get_features_of_type('tag'):
                if feature.name is not None and compiled_pattern.match(feature.name):
                    return True
            else:
                return False

        if self.name == 'hasTag':
            if len(self.args) == 0:
                return len(content_node.get_tags()) > 0
            else:
                return content_node.has_feature('tag', args[0])

        if self.name == 'hasFeature':
            if len(args) == 0:
                return len(content_node.get_features()) > 0
            else:
                return content_node.has_feature(args[0], args[1])

        if self.name == 'content':
            return content_node.content

        if self.name == 'uuid':
            return content_node.uuid

        if self.name == 'type':
            return content_node.type

        if self.name == 'index':
            return content_node.index

        return []
