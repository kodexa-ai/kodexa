from antlr4.error.ErrorListener import ErrorListener

class KodexaSyntaxErrorListener(ErrorListener):
    """
    Custom error listener for ANTLR parser to provide better error messages.
    """
    
    def __init__(self):
        super(KodexaSyntaxErrorListener, self).__init__()
        self.errors = []
    
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        """
        Collect syntax errors during parsing.
        """
        error_msg = f"line {line}:{column} {msg}"
        self.errors.append(error_msg)
    
    def hasErrors(self):
        """
        Check if any errors were detected.
        """
        return len(self.errors) > 0
    
    def getErrors(self):
        """
        Get the list of error messages.
        """
        return self.errors