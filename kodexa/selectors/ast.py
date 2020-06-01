"""Abstract Syntax Tree nodes for parsed XPath.

This module contains basic nodes for representing parsed XPath expressions.
The parser provided by this module creates its parsed XPath representation
from the classes defined in this module. Library callers will mostly not use
this module directly, unless they need to produce XPath ASTs from scratch or
perhaps introspect ASTs returned by the parser.

This code was derived from https://github.com/emory-libraries/eulxml
"""

from __future__ import unicode_literals
import sys

# python2/3 string type logic borrowed from six
# NOTE: not importing six here because setup.py needs to generate
# the parser at install time, when six installation is not yet available
from kodexa import ContentNode, ContentFeature

__all__ = [
    'serialize',
    'UnaryExpression',
    'BinaryExpression',
    'PredicatedExpression',
    'AbsolutePath',
    'Step',
    'NameTest',
    'NodeType',
    'AbbreviatedStep',
    'VariableReference',
    'FunctionCall',
]


def serialize(xp_ast):
    '''Serialize an XPath AST as a valid XPath expression.'''
    return ''.join(_serialize(xp_ast))


def _serialize(xp_ast):
    '''Generate token strings which, when joined together, form a valid
    XPath serialization of the AST.'''

    if hasattr(xp_ast, '_serialize'):
        for tok in xp_ast._serialize():
            yield tok
    elif isinstance(xp_ast, str):
        # strings in serialized xpath needed to be quoted
        # (e.g. for use in paths, comparisons, etc)
        # using repr to quote them; for unicode, the leading
        # u (u'') needs to be removed.
        yield repr(xp_ast).lstrip('u')
    else:
        yield str(xp_ast)


class UnaryExpression(object):
    '''A unary XPath expression. Practially, this means -foo.'''

    def __init__(self, op, right):
        self.op = op
        '''the operator used in the expression'''
        self.right = right
        '''the expression the operator is applied to'''

    def __repr__(self):
        return '<%s %s %s>' % (self.__class__.__name__,
                               self.op, serialize(self.right))

    def _serialize(self):
        yield self.op
        for tok in _serialize(self.right):
            yield tok


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

    def __repr__(self):
        return '<%s %s %s %s>' % (self.__class__.__name__,
                                  serialize(self.left), self.op, serialize(self.right))

    def resolve(self, content_node: ContentNode):
        if self.op == '|':
            return self.left.resolve(content_node) + self.right.resolve(content_node)

    def _serialize(self):
        for tok in _serialize(self.left):
            yield tok

        if self.op in KEYWORDS:
            yield ' '
            yield self.op
            yield ' '
        else:
            yield self.op

        for tok in _serialize(self.right):
            yield tok


class PredicatedExpression(object):
    '''A filtered XPath expression. $var[1]; (a or b)[foo][@bar].'''

    def __init__(self, base, predicates=None):
        self.base = base
        '''the base expression to be filtered'''
        self.predicates = predicates or []
        '''a list of filter predicates'''

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__,
                            serialize(self))

    def append_predicate(self, pred):
        self.predicates.append(pred)

    def _serialize(self):
        yield '('
        for tok in _serialize(self.base):
            yield tok
        yield ')'
        for pred in self.predicates:
            yield '['
            for tok in _serialize(pred):
                yield tok
            yield ']'


class AbsolutePath(object):
    '''An absolute XPath path. /a/b/c; //a/ancestor:b/@c.'''

    def __init__(self, op='/', relative=None):
        self.op = op
        '''the operator used to root the expression'''
        self.relative = relative
        '''the relative path after the absolute root operator'''

    def __repr__(self):
        if self.relative:
            return '<%s %s %s>' % (self.__class__.__name__,
                                   self.op, serialize(self.relative))
        else:
            return '<%s %s>' % (self.__class__.__name__, self.op)

    def _serialize(self):
        yield self.op
        for tok in _serialize(self.relative):
            yield tok

    def resolve(self, content_node):
        if self.op == '/':
            return self.relative.resolve(content_node)
        if self.op == '//':
            results = []
            results = results + self.relative.resolve(content_node)
            for child in content_node.children:
                results = results + self.resolve(child)
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

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__,
                            serialize(self))

    def _serialize(self):
        if self.axis == '@':
            yield '@'
        elif self.axis:
            yield self.axis
            yield '::'

        for tok in self.node_test._serialize():
            yield tok

        for predicate in self.predicates:
            yield '['
            for tok in _serialize(predicate):
                yield tok
            yield ']'

    def resolve(self, obj):
        match = True

        if isinstance(obj, ContentFeature):
            match = self.node_test.test(obj)

        if isinstance(obj, ContentNode):
            content_node = obj
            for feature in content_node.get_features():
                for predicate in self.predicates:
                    if len(predicate.resolve(feature)) == 0:
                        match = False

            match = match and self.node_test.test(content_node)

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

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__,
                            serialize(self))

    def test(self, obj):
        if isinstance(obj, ContentNode):
            return self.name == '*' or obj.type == self.name
        if isinstance(obj, ContentFeature):
            return self.name == '*' or (obj.feature_type == self.prefix and obj.name == self.name)
        return False

    def _serialize(self):
        if self.prefix:
            yield self.prefix
            yield ':'
        yield self.name

    def __str__(self):
        return ''.join(self._serialize())


class NodeType(object):
    '''A node type node test for a Step.'''

    def __init__(self, name, literal=None):
        self.name = name
        '''the node type name, such as node or text'''
        self.literal = literal
        '''the argument to the node specifier. XPath allows these only for
        processing-instruction() node tests.'''

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__,
                            serialize(self))

    def _serialize(self):
        yield self.name
        yield '('
        if self.literal is not None:
            for tok in _serialize(self.literal):
                yield self.literal
        yield ')'

    def __str__(self):
        return ''.join(self._serialize())


class AbbreviatedStep(object):
    '''An abbreviated XPath step. . or ..'''

    def __init__(self, abbr):
        self.abbr = abbr
        '''the abbreviated step'''

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__,
                            serialize(self))

    def _serialize(self):
        yield self.abbr

    def resolve(self, content_node):
        if self.abbr == '.':
            return [content_node]
        raise Exception("Not implemented")


class VariableReference(object):
    '''An XPath variable reference. $foo; $myns:foo.'''

    def __init__(self, name):
        self.name = name
        '''a tuple (prefix, localname) containing the variable name'''

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__,
                            serialize(self))

    def _serialize(self):
        yield '$'
        prefix, localname = self.name
        if prefix:
            yield prefix
            yield ':'
        yield localname


class FunctionCall(object):
    '''An XPath function call. foo(); my:foo(1); foo(1, 'a', $var).'''

    def __init__(self, prefix, name, args):
        self.prefix = prefix
        '''the namespace prefix, or None if unspecified'''
        self.name = name
        '''the local function name'''
        self.args = args
        '''a list of argument expressions'''

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__,
                            serialize(self))

    def _serialize(self):
        if self.prefix:
            yield self.prefix
            yield ':'
        yield self.name
        yield '('
        if self.args:
            for tok in _serialize(self.args[0]):
                yield tok

            for arg in self.args[1:]:
                yield ','
                for tok in _serialize(arg):
                    yield tok
        yield ')'
