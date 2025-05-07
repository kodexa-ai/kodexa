"""Core XPath parsing using ANTLR.

This module provides the interface for parsing XPath expressions using ANTLR.
"""

import re
from antlr4 import InputStream, CommonTokenStream
from kodexa.model.model import Document
from kodexa.selectors.resources.KodexaSelectorLexer import KodexaSelectorLexer
from kodexa.selectors.resources.KodexaSelectorParser import KodexaSelectorParser
from kodexa.selectors.visitor import KodexaASTVisitor
from kodexa.selectors.error import KodexaSyntaxErrorListener

__all__ = ["parse"]

class SelectorContext:
    def __init__(self, document: Document, first_only=False):
        self.pattern_cache = {}
        self.last_op = None
        self.document: Document = document
        self.stream = 0
        self.first_only = first_only

    def cache_pattern(self, pattern):
        if pattern not in self.pattern_cache:
            self.pattern_cache[pattern] = re.compile(pattern)
        return self.pattern_cache[pattern]

def parse(xpath):
    """Parse an xpath expression.
    
    Args:
        xpath (str): The XPath expression to parse.
        
    Returns:
        The AST representing the parsed XPath expression.
        
    Raises:
        RuntimeError: If there are syntax errors in the XPath expression.
    """
    # Create an input stream from the xpath string
    input_stream = InputStream(xpath)
    
    # Create a lexer that feeds off of the input stream
    lexer = KodexaSelectorLexer(input_stream)
    
    # Remove the default console error listener
    lexer.removeErrorListeners()
    
    # Add our custom error listener
    error_listener = KodexaSyntaxErrorListener()
    lexer.addErrorListener(error_listener)
    
    # Create a buffer of tokens pulled from the lexer
    token_stream = CommonTokenStream(lexer)
    
    # Create a parser that feeds off the tokens buffer
    parser = KodexaSelectorParser(token_stream)
    
    # Remove the default console error listener
    parser.removeErrorListeners()
    
    # Add our custom error listener
    parser.addErrorListener(error_listener)
    
    # Begin parsing at the "xpath" rule
    tree = parser.xpath()
    
    # Check if there were any syntax errors
    if error_listener.hasErrors():
        error_msg = "\n".join(error_listener.getErrors())
        raise RuntimeError(f"Syntax error in Kodexa selector expression: {error_msg}")
    
    # Create a visitor to build the AST
    visitor = KodexaASTVisitor()
    
    # Visit the parse tree and get the resulting AST
    ast = visitor.visit(tree)
    
    return ast

def debug_tokens(s):
    """Lex a string as XPath tokens, and print each token as it is lexed.
    This is used primarily for debugging."""
    input_stream = InputStream(s)
    lexer = KodexaSelectorLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    token_stream.fill()
    
    for token in token_stream.tokens:
        print(token)