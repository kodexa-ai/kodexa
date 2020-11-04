"""Core XPath parsing glue.

"""

from __future__ import unicode_literals

import os
import re
import tempfile

from ply import lex, yacc

from kodexa.selectors import lexrules
from kodexa.selectors import parserules

__all__ = ['lexer', 'parser', 'parse']

OPERATOR_FORCERS = {'PIPELINE_OP', 'ABBREV_AXIS_AT', 'AXIS_SEP', 'OPEN_PAREN', 'OPEN_BRACKET', 'AND_OP', 'OR_OP',
                    'MOD_OP', 'DIV_OP',
                    'MULT_OP', 'PATH_SEP', 'ABBREV_PATH_SEP', 'UNION_OP', 'PLUS_OP', 'MINUS_OP', 'EQUAL_OP', 'REL_OP',
                    'COLON'}

NODE_TYPES = {'comment', 'text', 'processing-instruction', 'node'}


class LexerWrapper(lex.Lexer):
    def token(self):
        tok = lex.Lexer.token(self)
        if tok is not None:
            if tok.type == 'STAR_OP':
                if self.last is not None and self.last.type not in OPERATOR_FORCERS:
                    # first half of point 1
                    tok.type = 'MULT_OP'

            if tok.type == 'NCNAME':
                if self.last is not None and self.last.type not in OPERATOR_FORCERS:
                    # second half of point 1
                    operator = lexrules.operator_names.get(tok.value, None)
                    if operator is not None:
                        tok.type = operator
                else:
                    next = self.peek()
                    if next is not None:
                        if next.type == 'OPEN_PAREN':
                            # point 2
                            if tok.value in NODE_TYPES:
                                tok.type = 'NODETYPE'
                            else:
                                tok.type = 'FUNCNAME'
                        elif next.type == 'AXIS_SEP':
                            # point 3
                            tok.type = 'AXISNAME'

        self.last = tok
        return tok

    def peek(self):
        clone = self.clone()
        return clone.token()


# try to build the lexer with cached lex table generation. this will fail if
# the user doesn't have write perms on the source directory. in that case,
# try again without lex table generation.
lexdir = os.path.dirname(lexrules.__file__)
lexer = None
try:
    lexer = lex.lex(module=lexrules, optimize=1, outputdir=lexdir,
                    reflags=re.UNICODE)
except IOError as e:
    import errno

    if e.errno != errno.EACCES:
        raise
if lexer is None:
    lexer = lex.lex(module=lexrules, reflags=re.UNICODE)
# then dynamically rewrite the lexer class to use the wonky override logic
# above
lexer.__class__ = LexerWrapper
lexer.last = None

# build the parser. This will generate a parsetab.py in the eulxml.xpath
# directory. Unlike lex, though, this just logs a complaint when it fails
# (contrast lex's explosion). Other than that, it's much less exciting
# than the lexer wackiness.
parsedir = os.path.dirname(parserules.__file__)
# By default, store generated parse files with the code
# If we don't have write permission, put them in the configured tempdir
if (not os.access(parsedir, os.W_OK)):
    parsedir = tempfile.gettempdir()
parser = yacc.yacc(module=parserules, outputdir=parsedir, debug=0)


def parse(xpath):
    '''Parse an xpath.'''
    # Expose the parse method of the constructed parser,
    # but explicitly specify the lexer created here,
    # since otherwise parse will use the most-recently created lexer.
    return parser.parse(xpath, lexer=lexer)


def ptokens(s):
    '''Lex a string as XPath tokens, and print each token as it is lexed.
    This is used primarily for debugging. You probably don't want this
    function.'''

    lexer.input(s)
    for tok in lexer:
        print(tok)
