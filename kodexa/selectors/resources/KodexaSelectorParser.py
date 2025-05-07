# Generated from resources/KodexaSelector.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,33,229,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,3,1,63,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,5,1,92,8,1,10,1,12,1,95,9,1,1,2,1,2,1,2,3,2,100,8,2,
        1,3,1,3,1,3,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,5,4,114,8,4,10,4,
        12,4,117,9,4,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,
        3,5,132,8,5,1,6,1,6,1,6,3,6,137,8,6,1,7,1,7,1,8,1,8,1,8,1,8,1,8,
        3,8,146,8,8,1,9,1,9,1,9,1,9,3,9,152,8,9,1,10,1,10,1,10,1,10,1,10,
        1,10,1,10,1,10,1,10,1,10,3,10,164,8,10,1,10,1,10,5,10,168,8,10,10,
        10,12,10,171,9,10,1,11,1,11,1,11,1,11,1,11,5,11,178,8,11,10,11,12,
        11,181,9,11,1,12,1,12,1,12,1,12,1,13,1,13,1,13,1,14,1,14,1,15,1,
        15,1,16,1,16,1,16,1,16,3,16,198,8,16,1,17,1,17,1,17,1,17,3,17,204,
        8,17,1,18,1,18,1,19,1,19,1,19,1,19,1,19,1,19,3,19,214,8,19,1,20,
        1,20,1,20,1,20,1,20,1,20,5,20,222,8,20,10,20,12,20,225,9,20,1,21,
        1,21,1,21,0,5,2,8,20,22,40,22,0,2,4,6,8,10,12,14,16,18,20,22,24,
        26,28,30,32,34,36,38,40,42,0,3,1,0,28,29,1,0,24,25,1,0,5,6,247,0,
        44,1,0,0,0,2,62,1,0,0,0,4,99,1,0,0,0,6,101,1,0,0,0,8,104,1,0,0,0,
        10,131,1,0,0,0,12,136,1,0,0,0,14,138,1,0,0,0,16,145,1,0,0,0,18,151,
        1,0,0,0,20,163,1,0,0,0,22,172,1,0,0,0,24,182,1,0,0,0,26,186,1,0,
        0,0,28,189,1,0,0,0,30,191,1,0,0,0,32,197,1,0,0,0,34,203,1,0,0,0,
        36,205,1,0,0,0,38,213,1,0,0,0,40,215,1,0,0,0,42,226,1,0,0,0,44,45,
        3,2,1,0,45,1,1,0,0,0,46,47,6,1,-1,0,47,48,5,19,0,0,48,63,3,2,1,11,
        49,63,3,32,16,0,50,51,3,20,10,0,51,52,3,42,21,0,52,53,3,8,4,0,53,
        63,1,0,0,0,54,63,3,8,4,0,55,63,3,4,2,0,56,63,3,6,3,0,57,63,3,20,
        10,0,58,63,3,16,8,0,59,60,5,5,0,0,60,63,3,16,8,0,61,63,3,30,15,0,
        62,46,1,0,0,0,62,49,1,0,0,0,62,50,1,0,0,0,62,54,1,0,0,0,62,55,1,
        0,0,0,62,56,1,0,0,0,62,57,1,0,0,0,62,58,1,0,0,0,62,59,1,0,0,0,62,
        61,1,0,0,0,63,93,1,0,0,0,64,65,10,19,0,0,65,66,5,1,0,0,66,92,3,2,
        1,20,67,68,10,18,0,0,68,69,5,2,0,0,69,92,3,2,1,19,70,71,10,17,0,
        0,71,72,5,16,0,0,72,92,3,2,1,18,73,74,10,16,0,0,74,75,5,17,0,0,75,
        92,3,2,1,17,76,77,10,15,0,0,77,78,5,18,0,0,78,92,3,2,1,16,79,80,
        10,14,0,0,80,81,5,19,0,0,81,92,3,2,1,15,82,83,10,13,0,0,83,84,5,
        15,0,0,84,92,3,2,1,14,85,86,10,12,0,0,86,87,5,3,0,0,87,92,3,2,1,
        13,88,89,10,10,0,0,89,90,5,4,0,0,90,92,3,2,1,11,91,64,1,0,0,0,91,
        67,1,0,0,0,91,70,1,0,0,0,91,73,1,0,0,0,91,76,1,0,0,0,91,79,1,0,0,
        0,91,82,1,0,0,0,91,85,1,0,0,0,91,88,1,0,0,0,92,95,1,0,0,0,93,91,
        1,0,0,0,93,94,1,0,0,0,94,3,1,0,0,0,95,93,1,0,0,0,96,100,5,5,0,0,
        97,98,5,5,0,0,98,100,3,8,4,0,99,96,1,0,0,0,99,97,1,0,0,0,100,5,1,
        0,0,0,101,102,5,6,0,0,102,103,3,8,4,0,103,7,1,0,0,0,104,105,6,4,
        -1,0,105,106,3,10,5,0,106,115,1,0,0,0,107,108,10,2,0,0,108,109,5,
        5,0,0,109,114,3,10,5,0,110,111,10,1,0,0,111,112,5,6,0,0,112,114,
        3,10,5,0,113,107,1,0,0,0,113,110,1,0,0,0,114,117,1,0,0,0,115,113,
        1,0,0,0,115,116,1,0,0,0,116,9,1,0,0,0,117,115,1,0,0,0,118,132,3,
        14,7,0,119,120,3,14,7,0,120,121,3,22,11,0,121,132,1,0,0,0,122,123,
        3,12,6,0,123,124,3,14,7,0,124,132,1,0,0,0,125,126,3,12,6,0,126,127,
        3,14,7,0,127,128,3,22,11,0,128,132,1,0,0,0,129,132,5,7,0,0,130,132,
        5,8,0,0,131,118,1,0,0,0,131,119,1,0,0,0,131,122,1,0,0,0,131,125,
        1,0,0,0,131,129,1,0,0,0,131,130,1,0,0,0,132,11,1,0,0,0,133,134,5,
        32,0,0,134,137,5,9,0,0,135,137,5,10,0,0,136,133,1,0,0,0,136,135,
        1,0,0,0,137,13,1,0,0,0,138,139,3,16,8,0,139,15,1,0,0,0,140,146,5,
        20,0,0,141,142,5,30,0,0,142,143,5,22,0,0,143,146,5,20,0,0,144,146,
        3,18,9,0,145,140,1,0,0,0,145,141,1,0,0,0,145,144,1,0,0,0,146,17,
        1,0,0,0,147,148,5,30,0,0,148,149,5,22,0,0,149,152,5,30,0,0,150,152,
        5,30,0,0,151,147,1,0,0,0,151,150,1,0,0,0,152,19,1,0,0,0,153,154,
        6,10,-1,0,154,164,3,26,13,0,155,164,5,27,0,0,156,164,3,28,14,0,157,
        164,3,30,15,0,158,164,3,32,16,0,159,160,5,11,0,0,160,161,3,2,1,0,
        161,162,5,12,0,0,162,164,1,0,0,0,163,153,1,0,0,0,163,155,1,0,0,0,
        163,156,1,0,0,0,163,157,1,0,0,0,163,158,1,0,0,0,163,159,1,0,0,0,
        164,169,1,0,0,0,165,166,10,1,0,0,166,168,3,24,12,0,167,165,1,0,0,
        0,168,171,1,0,0,0,169,167,1,0,0,0,169,170,1,0,0,0,170,21,1,0,0,0,
        171,169,1,0,0,0,172,173,6,11,-1,0,173,174,3,24,12,0,174,179,1,0,
        0,0,175,176,10,1,0,0,176,178,3,24,12,0,177,175,1,0,0,0,178,181,1,
        0,0,0,179,177,1,0,0,0,179,180,1,0,0,0,180,23,1,0,0,0,181,179,1,0,
        0,0,182,183,5,13,0,0,183,184,3,2,1,0,184,185,5,14,0,0,185,25,1,0,
        0,0,186,187,5,23,0,0,187,188,3,18,9,0,188,27,1,0,0,0,189,190,7,0,
        0,0,190,29,1,0,0,0,191,192,7,1,0,0,192,31,1,0,0,0,193,194,3,36,18,
        0,194,195,3,38,19,0,195,198,1,0,0,0,196,198,3,34,17,0,197,193,1,
        0,0,0,197,196,1,0,0,0,198,33,1,0,0,0,199,200,5,24,0,0,200,204,3,
        38,19,0,201,202,5,25,0,0,202,204,3,38,19,0,203,199,1,0,0,0,203,201,
        1,0,0,0,204,35,1,0,0,0,205,206,5,26,0,0,206,37,1,0,0,0,207,208,5,
        11,0,0,208,214,5,12,0,0,209,210,5,11,0,0,210,211,3,40,20,0,211,212,
        5,12,0,0,212,214,1,0,0,0,213,207,1,0,0,0,213,209,1,0,0,0,214,39,
        1,0,0,0,215,216,6,20,-1,0,216,217,3,2,1,0,217,223,1,0,0,0,218,219,
        10,1,0,0,219,220,5,21,0,0,220,222,3,2,1,0,221,218,1,0,0,0,222,225,
        1,0,0,0,223,221,1,0,0,0,223,224,1,0,0,0,224,41,1,0,0,0,225,223,1,
        0,0,0,226,227,7,2,0,0,227,43,1,0,0,0,17,62,91,93,99,113,115,131,
        136,145,151,163,169,179,197,203,213,223
    ]

class KodexaSelectorParser ( Parser ):

    grammarFileName = "KodexaSelector.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'or'", "'and'", "'intersect'", "'stream'", 
                     "'/'", "'//'", "'.'", "'..'", "'::'", "'@'", "'('", 
                     "')'", "'['", "']'", "'|'", "<INVALID>", "<INVALID>", 
                     "'+'", "'-'", "'*'", "','", "':'", "'$'", "'true'", 
                     "'false'" ]

    symbolicNames = [ "<INVALID>", "OR", "AND", "INTERSECT", "PIPELINE", 
                      "PATH_SEP", "ABBREV_PATH_SEP", "ABBREV_STEP_SELF", 
                      "ABBREV_STEP_PARENT", "AXIS_SEP", "ABBREV_AXIS_AT", 
                      "LPAREN", "RPAREN", "LBRACKET", "RBRACKET", "UNION", 
                      "EQUALS", "REL_OP", "PLUS", "MINUS", "STAR", "COMMA", 
                      "COLON", "DOLLAR", "TRUE", "FALSE", "FUNCTION_NAME", 
                      "LITERAL", "FLOAT", "INTEGER", "NCNAME", "FUNCNAME", 
                      "AXISNAME", "WS" ]

    RULE_xpath = 0
    RULE_expr = 1
    RULE_absoluteLocationPath = 2
    RULE_abbreviatedAbsoluteLocationPath = 3
    RULE_relativeLocationPath = 4
    RULE_step = 5
    RULE_axisSpecifier = 6
    RULE_nodeTest = 7
    RULE_nameTest = 8
    RULE_qName = 9
    RULE_filterExpr = 10
    RULE_predicateList = 11
    RULE_predicate = 12
    RULE_variableReference = 13
    RULE_number = 14
    RULE_booleanLiteral = 15
    RULE_functionCall = 16
    RULE_builtInFunctionCall = 17
    RULE_funcQName = 18
    RULE_formalArguments = 19
    RULE_argumentList = 20
    RULE_pathSep = 21

    ruleNames =  [ "xpath", "expr", "absoluteLocationPath", "abbreviatedAbsoluteLocationPath", 
                   "relativeLocationPath", "step", "axisSpecifier", "nodeTest", 
                   "nameTest", "qName", "filterExpr", "predicateList", "predicate", 
                   "variableReference", "number", "booleanLiteral", "functionCall", 
                   "builtInFunctionCall", "funcQName", "formalArguments", 
                   "argumentList", "pathSep" ]

    EOF = Token.EOF
    OR=1
    AND=2
    INTERSECT=3
    PIPELINE=4
    PATH_SEP=5
    ABBREV_PATH_SEP=6
    ABBREV_STEP_SELF=7
    ABBREV_STEP_PARENT=8
    AXIS_SEP=9
    ABBREV_AXIS_AT=10
    LPAREN=11
    RPAREN=12
    LBRACKET=13
    RBRACKET=14
    UNION=15
    EQUALS=16
    REL_OP=17
    PLUS=18
    MINUS=19
    STAR=20
    COMMA=21
    COLON=22
    DOLLAR=23
    TRUE=24
    FALSE=25
    FUNCTION_NAME=26
    LITERAL=27
    FLOAT=28
    INTEGER=29
    NCNAME=30
    FUNCNAME=31
    AXISNAME=32
    WS=33

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class XpathContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(KodexaSelectorParser.ExprContext,0)


        def getRuleIndex(self):
            return KodexaSelectorParser.RULE_xpath

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterXpath" ):
                listener.enterXpath(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitXpath" ):
                listener.exitXpath(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitXpath" ):
                return visitor.visitXpath(self)
            else:
                return visitor.visitChildren(self)




    def xpath(self):

        localctx = KodexaSelectorParser.XpathContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_xpath)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 44
            self.expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return KodexaSelectorParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class EqualsExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(KodexaSelectorParser.ExprContext)
            else:
                return self.getTypedRuleContext(KodexaSelectorParser.ExprContext,i)

        def EQUALS(self):
            return self.getToken(KodexaSelectorParser.EQUALS, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEqualsExpr" ):
                listener.enterEqualsExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEqualsExpr" ):
                listener.exitEqualsExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEqualsExpr" ):
                return visitor.visitEqualsExpr(self)
            else:
                return visitor.visitChildren(self)


    class SubtractExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(KodexaSelectorParser.ExprContext)
            else:
                return self.getTypedRuleContext(KodexaSelectorParser.ExprContext,i)

        def MINUS(self):
            return self.getToken(KodexaSelectorParser.MINUS, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSubtractExpr" ):
                listener.enterSubtractExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSubtractExpr" ):
                listener.exitSubtractExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSubtractExpr" ):
                return visitor.visitSubtractExpr(self)
            else:
                return visitor.visitChildren(self)


    class IntersectExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(KodexaSelectorParser.ExprContext)
            else:
                return self.getTypedRuleContext(KodexaSelectorParser.ExprContext,i)

        def INTERSECT(self):
            return self.getToken(KodexaSelectorParser.INTERSECT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIntersectExpr" ):
                listener.enterIntersectExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIntersectExpr" ):
                listener.exitIntersectExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIntersectExpr" ):
                return visitor.visitIntersectExpr(self)
            else:
                return visitor.visitChildren(self)


    class DirectNameTestContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def nameTest(self):
            return self.getTypedRuleContext(KodexaSelectorParser.NameTestContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDirectNameTest" ):
                listener.enterDirectNameTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDirectNameTest" ):
                listener.exitDirectNameTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDirectNameTest" ):
                return visitor.visitDirectNameTest(self)
            else:
                return visitor.visitChildren(self)


    class OrExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(KodexaSelectorParser.ExprContext)
            else:
                return self.getTypedRuleContext(KodexaSelectorParser.ExprContext,i)

        def OR(self):
            return self.getToken(KodexaSelectorParser.OR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrExpr" ):
                listener.enterOrExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrExpr" ):
                listener.exitOrExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrExpr" ):
                return visitor.visitOrExpr(self)
            else:
                return visitor.visitChildren(self)


    class AbsolutePathExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def absoluteLocationPath(self):
            return self.getTypedRuleContext(KodexaSelectorParser.AbsoluteLocationPathContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAbsolutePathExpr" ):
                listener.enterAbsolutePathExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAbsolutePathExpr" ):
                listener.exitAbsolutePathExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAbsolutePathExpr" ):
                return visitor.visitAbsolutePathExpr(self)
            else:
                return visitor.visitChildren(self)


    class FuncCallExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def functionCall(self):
            return self.getTypedRuleContext(KodexaSelectorParser.FunctionCallContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFuncCallExpr" ):
                listener.enterFuncCallExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFuncCallExpr" ):
                listener.exitFuncCallExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFuncCallExpr" ):
                return visitor.visitFuncCallExpr(self)
            else:
                return visitor.visitChildren(self)


    class UnionExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(KodexaSelectorParser.ExprContext)
            else:
                return self.getTypedRuleContext(KodexaSelectorParser.ExprContext,i)

        def UNION(self):
            return self.getToken(KodexaSelectorParser.UNION, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnionExpr" ):
                listener.enterUnionExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnionExpr" ):
                listener.exitUnionExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnionExpr" ):
                return visitor.visitUnionExpr(self)
            else:
                return visitor.visitChildren(self)


    class RelationalExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(KodexaSelectorParser.ExprContext)
            else:
                return self.getTypedRuleContext(KodexaSelectorParser.ExprContext,i)

        def REL_OP(self):
            return self.getToken(KodexaSelectorParser.REL_OP, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelationalExpr" ):
                listener.enterRelationalExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelationalExpr" ):
                listener.exitRelationalExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelationalExpr" ):
                return visitor.visitRelationalExpr(self)
            else:
                return visitor.visitChildren(self)


    class PipelineExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(KodexaSelectorParser.ExprContext)
            else:
                return self.getTypedRuleContext(KodexaSelectorParser.ExprContext,i)

        def PIPELINE(self):
            return self.getToken(KodexaSelectorParser.PIPELINE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPipelineExpr" ):
                listener.enterPipelineExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPipelineExpr" ):
                listener.exitPipelineExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPipelineExpr" ):
                return visitor.visitPipelineExpr(self)
            else:
                return visitor.visitChildren(self)


    class RelativePathExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def relativeLocationPath(self):
            return self.getTypedRuleContext(KodexaSelectorParser.RelativeLocationPathContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelativePathExpr" ):
                listener.enterRelativePathExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelativePathExpr" ):
                listener.exitRelativePathExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelativePathExpr" ):
                return visitor.visitRelativePathExpr(self)
            else:
                return visitor.visitChildren(self)


    class RootNameTestContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def PATH_SEP(self):
            return self.getToken(KodexaSelectorParser.PATH_SEP, 0)
        def nameTest(self):
            return self.getTypedRuleContext(KodexaSelectorParser.NameTestContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRootNameTest" ):
                listener.enterRootNameTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRootNameTest" ):
                listener.exitRootNameTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRootNameTest" ):
                return visitor.visitRootNameTest(self)
            else:
                return visitor.visitChildren(self)


    class UnaryMinusExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def MINUS(self):
            return self.getToken(KodexaSelectorParser.MINUS, 0)
        def expr(self):
            return self.getTypedRuleContext(KodexaSelectorParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnaryMinusExpr" ):
                listener.enterUnaryMinusExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnaryMinusExpr" ):
                listener.exitUnaryMinusExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnaryMinusExpr" ):
                return visitor.visitUnaryMinusExpr(self)
            else:
                return visitor.visitChildren(self)


    class AbbrevAbsPathExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def abbreviatedAbsoluteLocationPath(self):
            return self.getTypedRuleContext(KodexaSelectorParser.AbbreviatedAbsoluteLocationPathContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAbbrevAbsPathExpr" ):
                listener.enterAbbrevAbsPathExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAbbrevAbsPathExpr" ):
                listener.exitAbbrevAbsPathExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAbbrevAbsPathExpr" ):
                return visitor.visitAbbrevAbsPathExpr(self)
            else:
                return visitor.visitChildren(self)


    class AddExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(KodexaSelectorParser.ExprContext)
            else:
                return self.getTypedRuleContext(KodexaSelectorParser.ExprContext,i)

        def PLUS(self):
            return self.getToken(KodexaSelectorParser.PLUS, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAddExpr" ):
                listener.enterAddExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAddExpr" ):
                listener.exitAddExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddExpr" ):
                return visitor.visitAddExpr(self)
            else:
                return visitor.visitChildren(self)


    class FilterExpressionContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def filterExpr(self):
            return self.getTypedRuleContext(KodexaSelectorParser.FilterExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFilterExpression" ):
                listener.enterFilterExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFilterExpression" ):
                listener.exitFilterExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFilterExpression" ):
                return visitor.visitFilterExpression(self)
            else:
                return visitor.visitChildren(self)


    class BooleanLiteralExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def booleanLiteral(self):
            return self.getTypedRuleContext(KodexaSelectorParser.BooleanLiteralContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBooleanLiteralExpr" ):
                listener.enterBooleanLiteralExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBooleanLiteralExpr" ):
                listener.exitBooleanLiteralExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBooleanLiteralExpr" ):
                return visitor.visitBooleanLiteralExpr(self)
            else:
                return visitor.visitChildren(self)


    class PathBinaryExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def filterExpr(self):
            return self.getTypedRuleContext(KodexaSelectorParser.FilterExprContext,0)

        def pathSep(self):
            return self.getTypedRuleContext(KodexaSelectorParser.PathSepContext,0)

        def relativeLocationPath(self):
            return self.getTypedRuleContext(KodexaSelectorParser.RelativeLocationPathContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPathBinaryExpr" ):
                listener.enterPathBinaryExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPathBinaryExpr" ):
                listener.exitPathBinaryExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPathBinaryExpr" ):
                return visitor.visitPathBinaryExpr(self)
            else:
                return visitor.visitChildren(self)


    class AndExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(KodexaSelectorParser.ExprContext)
            else:
                return self.getTypedRuleContext(KodexaSelectorParser.ExprContext,i)

        def AND(self):
            return self.getToken(KodexaSelectorParser.AND, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAndExpr" ):
                listener.enterAndExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAndExpr" ):
                listener.exitAndExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAndExpr" ):
                return visitor.visitAndExpr(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = KodexaSelectorParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_expr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 62
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
            if la_ == 1:
                localctx = KodexaSelectorParser.UnaryMinusExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 47
                self.match(KodexaSelectorParser.MINUS)
                self.state = 48
                self.expr(11)
                pass

            elif la_ == 2:
                localctx = KodexaSelectorParser.FuncCallExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 49
                self.functionCall()
                pass

            elif la_ == 3:
                localctx = KodexaSelectorParser.PathBinaryExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 50
                self.filterExpr(0)
                self.state = 51
                self.pathSep()
                self.state = 52
                self.relativeLocationPath(0)
                pass

            elif la_ == 4:
                localctx = KodexaSelectorParser.RelativePathExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 54
                self.relativeLocationPath(0)
                pass

            elif la_ == 5:
                localctx = KodexaSelectorParser.AbsolutePathExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 55
                self.absoluteLocationPath()
                pass

            elif la_ == 6:
                localctx = KodexaSelectorParser.AbbrevAbsPathExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 56
                self.abbreviatedAbsoluteLocationPath()
                pass

            elif la_ == 7:
                localctx = KodexaSelectorParser.FilterExpressionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 57
                self.filterExpr(0)
                pass

            elif la_ == 8:
                localctx = KodexaSelectorParser.DirectNameTestContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 58
                self.nameTest()
                pass

            elif la_ == 9:
                localctx = KodexaSelectorParser.RootNameTestContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 59
                self.match(KodexaSelectorParser.PATH_SEP)
                self.state = 60
                self.nameTest()
                pass

            elif la_ == 10:
                localctx = KodexaSelectorParser.BooleanLiteralExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 61
                self.booleanLiteral()
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 93
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 91
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                    if la_ == 1:
                        localctx = KodexaSelectorParser.OrExprContext(self, KodexaSelectorParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 64
                        if not self.precpred(self._ctx, 19):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 19)")
                        self.state = 65
                        self.match(KodexaSelectorParser.OR)
                        self.state = 66
                        self.expr(20)
                        pass

                    elif la_ == 2:
                        localctx = KodexaSelectorParser.AndExprContext(self, KodexaSelectorParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 67
                        if not self.precpred(self._ctx, 18):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 18)")
                        self.state = 68
                        self.match(KodexaSelectorParser.AND)
                        self.state = 69
                        self.expr(19)
                        pass

                    elif la_ == 3:
                        localctx = KodexaSelectorParser.EqualsExprContext(self, KodexaSelectorParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 70
                        if not self.precpred(self._ctx, 17):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 17)")
                        self.state = 71
                        self.match(KodexaSelectorParser.EQUALS)
                        self.state = 72
                        self.expr(18)
                        pass

                    elif la_ == 4:
                        localctx = KodexaSelectorParser.RelationalExprContext(self, KodexaSelectorParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 73
                        if not self.precpred(self._ctx, 16):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 16)")
                        self.state = 74
                        self.match(KodexaSelectorParser.REL_OP)
                        self.state = 75
                        self.expr(17)
                        pass

                    elif la_ == 5:
                        localctx = KodexaSelectorParser.AddExprContext(self, KodexaSelectorParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 76
                        if not self.precpred(self._ctx, 15):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 15)")
                        self.state = 77
                        self.match(KodexaSelectorParser.PLUS)
                        self.state = 78
                        self.expr(16)
                        pass

                    elif la_ == 6:
                        localctx = KodexaSelectorParser.SubtractExprContext(self, KodexaSelectorParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 79
                        if not self.precpred(self._ctx, 14):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 14)")
                        self.state = 80
                        self.match(KodexaSelectorParser.MINUS)
                        self.state = 81
                        self.expr(15)
                        pass

                    elif la_ == 7:
                        localctx = KodexaSelectorParser.UnionExprContext(self, KodexaSelectorParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 82
                        if not self.precpred(self._ctx, 13):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 13)")
                        self.state = 83
                        self.match(KodexaSelectorParser.UNION)
                        self.state = 84
                        self.expr(14)
                        pass

                    elif la_ == 8:
                        localctx = KodexaSelectorParser.IntersectExprContext(self, KodexaSelectorParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 85
                        if not self.precpred(self._ctx, 12):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 12)")
                        self.state = 86
                        self.match(KodexaSelectorParser.INTERSECT)
                        self.state = 87
                        self.expr(13)
                        pass

                    elif la_ == 9:
                        localctx = KodexaSelectorParser.PipelineExprContext(self, KodexaSelectorParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 88
                        if not self.precpred(self._ctx, 10):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 10)")
                        self.state = 89
                        self.match(KodexaSelectorParser.PIPELINE)
                        self.state = 90
                        self.expr(11)
                        pass

             
                self.state = 95
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class AbsoluteLocationPathContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return KodexaSelectorParser.RULE_absoluteLocationPath

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class RootOnlyContext(AbsoluteLocationPathContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.AbsoluteLocationPathContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def PATH_SEP(self):
            return self.getToken(KodexaSelectorParser.PATH_SEP, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRootOnly" ):
                listener.enterRootOnly(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRootOnly" ):
                listener.exitRootOnly(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRootOnly" ):
                return visitor.visitRootOnly(self)
            else:
                return visitor.visitChildren(self)


    class RootPathContext(AbsoluteLocationPathContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.AbsoluteLocationPathContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def PATH_SEP(self):
            return self.getToken(KodexaSelectorParser.PATH_SEP, 0)
        def relativeLocationPath(self):
            return self.getTypedRuleContext(KodexaSelectorParser.RelativeLocationPathContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRootPath" ):
                listener.enterRootPath(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRootPath" ):
                listener.exitRootPath(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRootPath" ):
                return visitor.visitRootPath(self)
            else:
                return visitor.visitChildren(self)



    def absoluteLocationPath(self):

        localctx = KodexaSelectorParser.AbsoluteLocationPathContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_absoluteLocationPath)
        try:
            self.state = 99
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                localctx = KodexaSelectorParser.RootOnlyContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 96
                self.match(KodexaSelectorParser.PATH_SEP)
                pass

            elif la_ == 2:
                localctx = KodexaSelectorParser.RootPathContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 97
                self.match(KodexaSelectorParser.PATH_SEP)
                self.state = 98
                self.relativeLocationPath(0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AbbreviatedAbsoluteLocationPathContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ABBREV_PATH_SEP(self):
            return self.getToken(KodexaSelectorParser.ABBREV_PATH_SEP, 0)

        def relativeLocationPath(self):
            return self.getTypedRuleContext(KodexaSelectorParser.RelativeLocationPathContext,0)


        def getRuleIndex(self):
            return KodexaSelectorParser.RULE_abbreviatedAbsoluteLocationPath

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAbbreviatedAbsoluteLocationPath" ):
                listener.enterAbbreviatedAbsoluteLocationPath(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAbbreviatedAbsoluteLocationPath" ):
                listener.exitAbbreviatedAbsoluteLocationPath(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAbbreviatedAbsoluteLocationPath" ):
                return visitor.visitAbbreviatedAbsoluteLocationPath(self)
            else:
                return visitor.visitChildren(self)




    def abbreviatedAbsoluteLocationPath(self):

        localctx = KodexaSelectorParser.AbbreviatedAbsoluteLocationPathContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_abbreviatedAbsoluteLocationPath)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 101
            self.match(KodexaSelectorParser.ABBREV_PATH_SEP)
            self.state = 102
            self.relativeLocationPath(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RelativeLocationPathContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return KodexaSelectorParser.RULE_relativeLocationPath

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class SingleStepContext(RelativeLocationPathContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.RelativeLocationPathContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def step(self):
            return self.getTypedRuleContext(KodexaSelectorParser.StepContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSingleStep" ):
                listener.enterSingleStep(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSingleStep" ):
                listener.exitSingleStep(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSingleStep" ):
                return visitor.visitSingleStep(self)
            else:
                return visitor.visitChildren(self)


    class PathStepContext(RelativeLocationPathContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.RelativeLocationPathContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def relativeLocationPath(self):
            return self.getTypedRuleContext(KodexaSelectorParser.RelativeLocationPathContext,0)

        def PATH_SEP(self):
            return self.getToken(KodexaSelectorParser.PATH_SEP, 0)
        def step(self):
            return self.getTypedRuleContext(KodexaSelectorParser.StepContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPathStep" ):
                listener.enterPathStep(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPathStep" ):
                listener.exitPathStep(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPathStep" ):
                return visitor.visitPathStep(self)
            else:
                return visitor.visitChildren(self)


    class AbbrevPathStepContext(RelativeLocationPathContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.RelativeLocationPathContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def relativeLocationPath(self):
            return self.getTypedRuleContext(KodexaSelectorParser.RelativeLocationPathContext,0)

        def ABBREV_PATH_SEP(self):
            return self.getToken(KodexaSelectorParser.ABBREV_PATH_SEP, 0)
        def step(self):
            return self.getTypedRuleContext(KodexaSelectorParser.StepContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAbbrevPathStep" ):
                listener.enterAbbrevPathStep(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAbbrevPathStep" ):
                listener.exitAbbrevPathStep(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAbbrevPathStep" ):
                return visitor.visitAbbrevPathStep(self)
            else:
                return visitor.visitChildren(self)



    def relativeLocationPath(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = KodexaSelectorParser.RelativeLocationPathContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 8
        self.enterRecursionRule(localctx, 8, self.RULE_relativeLocationPath, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            localctx = KodexaSelectorParser.SingleStepContext(self, localctx)
            self._ctx = localctx
            _prevctx = localctx

            self.state = 105
            self.step()
            self._ctx.stop = self._input.LT(-1)
            self.state = 115
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 113
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
                    if la_ == 1:
                        localctx = KodexaSelectorParser.PathStepContext(self, KodexaSelectorParser.RelativeLocationPathContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_relativeLocationPath)
                        self.state = 107
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 108
                        self.match(KodexaSelectorParser.PATH_SEP)
                        self.state = 109
                        self.step()
                        pass

                    elif la_ == 2:
                        localctx = KodexaSelectorParser.AbbrevPathStepContext(self, KodexaSelectorParser.RelativeLocationPathContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_relativeLocationPath)
                        self.state = 110
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 111
                        self.match(KodexaSelectorParser.ABBREV_PATH_SEP)
                        self.state = 112
                        self.step()
                        pass

             
                self.state = 117
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class StepContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return KodexaSelectorParser.RULE_step

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class NodeTestPredStepContext(StepContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.StepContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def nodeTest(self):
            return self.getTypedRuleContext(KodexaSelectorParser.NodeTestContext,0)

        def predicateList(self):
            return self.getTypedRuleContext(KodexaSelectorParser.PredicateListContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNodeTestPredStep" ):
                listener.enterNodeTestPredStep(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNodeTestPredStep" ):
                listener.exitNodeTestPredStep(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNodeTestPredStep" ):
                return visitor.visitNodeTestPredStep(self)
            else:
                return visitor.visitChildren(self)


    class SelfStepContext(StepContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.StepContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ABBREV_STEP_SELF(self):
            return self.getToken(KodexaSelectorParser.ABBREV_STEP_SELF, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSelfStep" ):
                listener.enterSelfStep(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSelfStep" ):
                listener.exitSelfStep(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSelfStep" ):
                return visitor.visitSelfStep(self)
            else:
                return visitor.visitChildren(self)


    class AxisNodeTestStepContext(StepContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.StepContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def axisSpecifier(self):
            return self.getTypedRuleContext(KodexaSelectorParser.AxisSpecifierContext,0)

        def nodeTest(self):
            return self.getTypedRuleContext(KodexaSelectorParser.NodeTestContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAxisNodeTestStep" ):
                listener.enterAxisNodeTestStep(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAxisNodeTestStep" ):
                listener.exitAxisNodeTestStep(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAxisNodeTestStep" ):
                return visitor.visitAxisNodeTestStep(self)
            else:
                return visitor.visitChildren(self)


    class AxisNodeTestPredStepContext(StepContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.StepContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def axisSpecifier(self):
            return self.getTypedRuleContext(KodexaSelectorParser.AxisSpecifierContext,0)

        def nodeTest(self):
            return self.getTypedRuleContext(KodexaSelectorParser.NodeTestContext,0)

        def predicateList(self):
            return self.getTypedRuleContext(KodexaSelectorParser.PredicateListContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAxisNodeTestPredStep" ):
                listener.enterAxisNodeTestPredStep(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAxisNodeTestPredStep" ):
                listener.exitAxisNodeTestPredStep(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAxisNodeTestPredStep" ):
                return visitor.visitAxisNodeTestPredStep(self)
            else:
                return visitor.visitChildren(self)


    class ParentStepContext(StepContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.StepContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ABBREV_STEP_PARENT(self):
            return self.getToken(KodexaSelectorParser.ABBREV_STEP_PARENT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParentStep" ):
                listener.enterParentStep(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParentStep" ):
                listener.exitParentStep(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParentStep" ):
                return visitor.visitParentStep(self)
            else:
                return visitor.visitChildren(self)


    class NodeTestStepContext(StepContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.StepContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def nodeTest(self):
            return self.getTypedRuleContext(KodexaSelectorParser.NodeTestContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNodeTestStep" ):
                listener.enterNodeTestStep(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNodeTestStep" ):
                listener.exitNodeTestStep(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNodeTestStep" ):
                return visitor.visitNodeTestStep(self)
            else:
                return visitor.visitChildren(self)



    def step(self):

        localctx = KodexaSelectorParser.StepContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_step)
        try:
            self.state = 131
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                localctx = KodexaSelectorParser.NodeTestStepContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 118
                self.nodeTest()
                pass

            elif la_ == 2:
                localctx = KodexaSelectorParser.NodeTestPredStepContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 119
                self.nodeTest()
                self.state = 120
                self.predicateList(0)
                pass

            elif la_ == 3:
                localctx = KodexaSelectorParser.AxisNodeTestStepContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 122
                self.axisSpecifier()
                self.state = 123
                self.nodeTest()
                pass

            elif la_ == 4:
                localctx = KodexaSelectorParser.AxisNodeTestPredStepContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 125
                self.axisSpecifier()
                self.state = 126
                self.nodeTest()
                self.state = 127
                self.predicateList(0)
                pass

            elif la_ == 5:
                localctx = KodexaSelectorParser.SelfStepContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 129
                self.match(KodexaSelectorParser.ABBREV_STEP_SELF)
                pass

            elif la_ == 6:
                localctx = KodexaSelectorParser.ParentStepContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 130
                self.match(KodexaSelectorParser.ABBREV_STEP_PARENT)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AxisSpecifierContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return KodexaSelectorParser.RULE_axisSpecifier

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class FullAxisContext(AxisSpecifierContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.AxisSpecifierContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def AXISNAME(self):
            return self.getToken(KodexaSelectorParser.AXISNAME, 0)
        def AXIS_SEP(self):
            return self.getToken(KodexaSelectorParser.AXIS_SEP, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFullAxis" ):
                listener.enterFullAxis(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFullAxis" ):
                listener.exitFullAxis(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFullAxis" ):
                return visitor.visitFullAxis(self)
            else:
                return visitor.visitChildren(self)


    class AttrAxisContext(AxisSpecifierContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.AxisSpecifierContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ABBREV_AXIS_AT(self):
            return self.getToken(KodexaSelectorParser.ABBREV_AXIS_AT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAttrAxis" ):
                listener.enterAttrAxis(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAttrAxis" ):
                listener.exitAttrAxis(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAttrAxis" ):
                return visitor.visitAttrAxis(self)
            else:
                return visitor.visitChildren(self)



    def axisSpecifier(self):

        localctx = KodexaSelectorParser.AxisSpecifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_axisSpecifier)
        try:
            self.state = 136
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [32]:
                localctx = KodexaSelectorParser.FullAxisContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 133
                self.match(KodexaSelectorParser.AXISNAME)
                self.state = 134
                self.match(KodexaSelectorParser.AXIS_SEP)
                pass
            elif token in [10]:
                localctx = KodexaSelectorParser.AttrAxisContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 135
                self.match(KodexaSelectorParser.ABBREV_AXIS_AT)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NodeTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return KodexaSelectorParser.RULE_nodeTest

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class NameTestNodeContext(NodeTestContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.NodeTestContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def nameTest(self):
            return self.getTypedRuleContext(KodexaSelectorParser.NameTestContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNameTestNode" ):
                listener.enterNameTestNode(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNameTestNode" ):
                listener.exitNameTestNode(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNameTestNode" ):
                return visitor.visitNameTestNode(self)
            else:
                return visitor.visitChildren(self)



    def nodeTest(self):

        localctx = KodexaSelectorParser.NodeTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_nodeTest)
        try:
            localctx = KodexaSelectorParser.NameTestNodeContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 138
            self.nameTest()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NameTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return KodexaSelectorParser.RULE_nameTest

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class AnyNameTestContext(NameTestContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.NameTestContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def STAR(self):
            return self.getToken(KodexaSelectorParser.STAR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAnyNameTest" ):
                listener.enterAnyNameTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAnyNameTest" ):
                listener.exitAnyNameTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAnyNameTest" ):
                return visitor.visitAnyNameTest(self)
            else:
                return visitor.visitChildren(self)


    class QNameTestContext(NameTestContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.NameTestContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def qName(self):
            return self.getTypedRuleContext(KodexaSelectorParser.QNameContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQNameTest" ):
                listener.enterQNameTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQNameTest" ):
                listener.exitQNameTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQNameTest" ):
                return visitor.visitQNameTest(self)
            else:
                return visitor.visitChildren(self)


    class PrefixedAnyNameTestContext(NameTestContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.NameTestContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NCNAME(self):
            return self.getToken(KodexaSelectorParser.NCNAME, 0)
        def COLON(self):
            return self.getToken(KodexaSelectorParser.COLON, 0)
        def STAR(self):
            return self.getToken(KodexaSelectorParser.STAR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrefixedAnyNameTest" ):
                listener.enterPrefixedAnyNameTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrefixedAnyNameTest" ):
                listener.exitPrefixedAnyNameTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrefixedAnyNameTest" ):
                return visitor.visitPrefixedAnyNameTest(self)
            else:
                return visitor.visitChildren(self)



    def nameTest(self):

        localctx = KodexaSelectorParser.NameTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_nameTest)
        try:
            self.state = 145
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
            if la_ == 1:
                localctx = KodexaSelectorParser.AnyNameTestContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 140
                self.match(KodexaSelectorParser.STAR)
                pass

            elif la_ == 2:
                localctx = KodexaSelectorParser.PrefixedAnyNameTestContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 141
                self.match(KodexaSelectorParser.NCNAME)
                self.state = 142
                self.match(KodexaSelectorParser.COLON)
                self.state = 143
                self.match(KodexaSelectorParser.STAR)
                pass

            elif la_ == 3:
                localctx = KodexaSelectorParser.QNameTestContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 144
                self.qName()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return KodexaSelectorParser.RULE_qName

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class SimpleNameContext(QNameContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.QNameContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NCNAME(self):
            return self.getToken(KodexaSelectorParser.NCNAME, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSimpleName" ):
                listener.enterSimpleName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSimpleName" ):
                listener.exitSimpleName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSimpleName" ):
                return visitor.visitSimpleName(self)
            else:
                return visitor.visitChildren(self)


    class PrefixedNameContext(QNameContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.QNameContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NCNAME(self, i:int=None):
            if i is None:
                return self.getTokens(KodexaSelectorParser.NCNAME)
            else:
                return self.getToken(KodexaSelectorParser.NCNAME, i)
        def COLON(self):
            return self.getToken(KodexaSelectorParser.COLON, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrefixedName" ):
                listener.enterPrefixedName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrefixedName" ):
                listener.exitPrefixedName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrefixedName" ):
                return visitor.visitPrefixedName(self)
            else:
                return visitor.visitChildren(self)



    def qName(self):

        localctx = KodexaSelectorParser.QNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_qName)
        try:
            self.state = 151
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                localctx = KodexaSelectorParser.PrefixedNameContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 147
                self.match(KodexaSelectorParser.NCNAME)
                self.state = 148
                self.match(KodexaSelectorParser.COLON)
                self.state = 149
                self.match(KodexaSelectorParser.NCNAME)
                pass

            elif la_ == 2:
                localctx = KodexaSelectorParser.SimpleNameContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 150
                self.match(KodexaSelectorParser.NCNAME)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FilterExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return KodexaSelectorParser.RULE_filterExpr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class FuncCallFilterContext(FilterExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.FilterExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def functionCall(self):
            return self.getTypedRuleContext(KodexaSelectorParser.FunctionCallContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFuncCallFilter" ):
                listener.enterFuncCallFilter(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFuncCallFilter" ):
                listener.exitFuncCallFilter(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFuncCallFilter" ):
                return visitor.visitFuncCallFilter(self)
            else:
                return visitor.visitChildren(self)


    class BooleanFilterContext(FilterExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.FilterExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def booleanLiteral(self):
            return self.getTypedRuleContext(KodexaSelectorParser.BooleanLiteralContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBooleanFilter" ):
                listener.enterBooleanFilter(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBooleanFilter" ):
                listener.exitBooleanFilter(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBooleanFilter" ):
                return visitor.visitBooleanFilter(self)
            else:
                return visitor.visitChildren(self)


    class GroupedFilterContext(FilterExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.FilterExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(KodexaSelectorParser.LPAREN, 0)
        def expr(self):
            return self.getTypedRuleContext(KodexaSelectorParser.ExprContext,0)

        def RPAREN(self):
            return self.getToken(KodexaSelectorParser.RPAREN, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGroupedFilter" ):
                listener.enterGroupedFilter(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGroupedFilter" ):
                listener.exitGroupedFilter(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGroupedFilter" ):
                return visitor.visitGroupedFilter(self)
            else:
                return visitor.visitChildren(self)


    class PredicatedFilterContext(FilterExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.FilterExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def filterExpr(self):
            return self.getTypedRuleContext(KodexaSelectorParser.FilterExprContext,0)

        def predicate(self):
            return self.getTypedRuleContext(KodexaSelectorParser.PredicateContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPredicatedFilter" ):
                listener.enterPredicatedFilter(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPredicatedFilter" ):
                listener.exitPredicatedFilter(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPredicatedFilter" ):
                return visitor.visitPredicatedFilter(self)
            else:
                return visitor.visitChildren(self)


    class NumberFilterContext(FilterExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.FilterExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def number(self):
            return self.getTypedRuleContext(KodexaSelectorParser.NumberContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumberFilter" ):
                listener.enterNumberFilter(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumberFilter" ):
                listener.exitNumberFilter(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumberFilter" ):
                return visitor.visitNumberFilter(self)
            else:
                return visitor.visitChildren(self)


    class VarRefFilterContext(FilterExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.FilterExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def variableReference(self):
            return self.getTypedRuleContext(KodexaSelectorParser.VariableReferenceContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVarRefFilter" ):
                listener.enterVarRefFilter(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVarRefFilter" ):
                listener.exitVarRefFilter(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarRefFilter" ):
                return visitor.visitVarRefFilter(self)
            else:
                return visitor.visitChildren(self)


    class LiteralFilterContext(FilterExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.FilterExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LITERAL(self):
            return self.getToken(KodexaSelectorParser.LITERAL, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteralFilter" ):
                listener.enterLiteralFilter(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteralFilter" ):
                listener.exitLiteralFilter(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiteralFilter" ):
                return visitor.visitLiteralFilter(self)
            else:
                return visitor.visitChildren(self)



    def filterExpr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = KodexaSelectorParser.FilterExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 20
        self.enterRecursionRule(localctx, 20, self.RULE_filterExpr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 163
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                localctx = KodexaSelectorParser.VarRefFilterContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 154
                self.variableReference()
                pass

            elif la_ == 2:
                localctx = KodexaSelectorParser.LiteralFilterContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 155
                self.match(KodexaSelectorParser.LITERAL)
                pass

            elif la_ == 3:
                localctx = KodexaSelectorParser.NumberFilterContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 156
                self.number()
                pass

            elif la_ == 4:
                localctx = KodexaSelectorParser.BooleanFilterContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 157
                self.booleanLiteral()
                pass

            elif la_ == 5:
                localctx = KodexaSelectorParser.FuncCallFilterContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 158
                self.functionCall()
                pass

            elif la_ == 6:
                localctx = KodexaSelectorParser.GroupedFilterContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 159
                self.match(KodexaSelectorParser.LPAREN)
                self.state = 160
                self.expr(0)
                self.state = 161
                self.match(KodexaSelectorParser.RPAREN)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 169
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,11,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = KodexaSelectorParser.PredicatedFilterContext(self, KodexaSelectorParser.FilterExprContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_filterExpr)
                    self.state = 165
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 166
                    self.predicate() 
                self.state = 171
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,11,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class PredicateListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return KodexaSelectorParser.RULE_predicateList

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class SinglePredicateContext(PredicateListContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.PredicateListContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def predicate(self):
            return self.getTypedRuleContext(KodexaSelectorParser.PredicateContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSinglePredicate" ):
                listener.enterSinglePredicate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSinglePredicate" ):
                listener.exitSinglePredicate(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSinglePredicate" ):
                return visitor.visitSinglePredicate(self)
            else:
                return visitor.visitChildren(self)


    class MultiplePredicateContext(PredicateListContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.PredicateListContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def predicateList(self):
            return self.getTypedRuleContext(KodexaSelectorParser.PredicateListContext,0)

        def predicate(self):
            return self.getTypedRuleContext(KodexaSelectorParser.PredicateContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultiplePredicate" ):
                listener.enterMultiplePredicate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultiplePredicate" ):
                listener.exitMultiplePredicate(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultiplePredicate" ):
                return visitor.visitMultiplePredicate(self)
            else:
                return visitor.visitChildren(self)



    def predicateList(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = KodexaSelectorParser.PredicateListContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 22
        self.enterRecursionRule(localctx, 22, self.RULE_predicateList, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            localctx = KodexaSelectorParser.SinglePredicateContext(self, localctx)
            self._ctx = localctx
            _prevctx = localctx

            self.state = 173
            self.predicate()
            self._ctx.stop = self._input.LT(-1)
            self.state = 179
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,12,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = KodexaSelectorParser.MultiplePredicateContext(self, KodexaSelectorParser.PredicateListContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_predicateList)
                    self.state = 175
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 176
                    self.predicate() 
                self.state = 181
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,12,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class PredicateContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return KodexaSelectorParser.RULE_predicate

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ExprPredicateContext(PredicateContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.PredicateContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LBRACKET(self):
            return self.getToken(KodexaSelectorParser.LBRACKET, 0)
        def expr(self):
            return self.getTypedRuleContext(KodexaSelectorParser.ExprContext,0)

        def RBRACKET(self):
            return self.getToken(KodexaSelectorParser.RBRACKET, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExprPredicate" ):
                listener.enterExprPredicate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExprPredicate" ):
                listener.exitExprPredicate(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExprPredicate" ):
                return visitor.visitExprPredicate(self)
            else:
                return visitor.visitChildren(self)



    def predicate(self):

        localctx = KodexaSelectorParser.PredicateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_predicate)
        try:
            localctx = KodexaSelectorParser.ExprPredicateContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 182
            self.match(KodexaSelectorParser.LBRACKET)
            self.state = 183
            self.expr(0)
            self.state = 184
            self.match(KodexaSelectorParser.RBRACKET)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VariableReferenceContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DOLLAR(self):
            return self.getToken(KodexaSelectorParser.DOLLAR, 0)

        def qName(self):
            return self.getTypedRuleContext(KodexaSelectorParser.QNameContext,0)


        def getRuleIndex(self):
            return KodexaSelectorParser.RULE_variableReference

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVariableReference" ):
                listener.enterVariableReference(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVariableReference" ):
                listener.exitVariableReference(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVariableReference" ):
                return visitor.visitVariableReference(self)
            else:
                return visitor.visitChildren(self)




    def variableReference(self):

        localctx = KodexaSelectorParser.VariableReferenceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_variableReference)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 186
            self.match(KodexaSelectorParser.DOLLAR)
            self.state = 187
            self.qName()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NumberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FLOAT(self):
            return self.getToken(KodexaSelectorParser.FLOAT, 0)

        def INTEGER(self):
            return self.getToken(KodexaSelectorParser.INTEGER, 0)

        def getRuleIndex(self):
            return KodexaSelectorParser.RULE_number

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumber" ):
                listener.enterNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumber" ):
                listener.exitNumber(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumber" ):
                return visitor.visitNumber(self)
            else:
                return visitor.visitChildren(self)




    def number(self):

        localctx = KodexaSelectorParser.NumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_number)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 189
            _la = self._input.LA(1)
            if not(_la==28 or _la==29):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BooleanLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TRUE(self):
            return self.getToken(KodexaSelectorParser.TRUE, 0)

        def FALSE(self):
            return self.getToken(KodexaSelectorParser.FALSE, 0)

        def getRuleIndex(self):
            return KodexaSelectorParser.RULE_booleanLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBooleanLiteral" ):
                listener.enterBooleanLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBooleanLiteral" ):
                listener.exitBooleanLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBooleanLiteral" ):
                return visitor.visitBooleanLiteral(self)
            else:
                return visitor.visitChildren(self)




    def booleanLiteral(self):

        localctx = KodexaSelectorParser.BooleanLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_booleanLiteral)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 191
            _la = self._input.LA(1)
            if not(_la==24 or _la==25):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionCallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def funcQName(self):
            return self.getTypedRuleContext(KodexaSelectorParser.FuncQNameContext,0)


        def formalArguments(self):
            return self.getTypedRuleContext(KodexaSelectorParser.FormalArgumentsContext,0)


        def builtInFunctionCall(self):
            return self.getTypedRuleContext(KodexaSelectorParser.BuiltInFunctionCallContext,0)


        def getRuleIndex(self):
            return KodexaSelectorParser.RULE_functionCall

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionCall" ):
                listener.enterFunctionCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionCall" ):
                listener.exitFunctionCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionCall" ):
                return visitor.visitFunctionCall(self)
            else:
                return visitor.visitChildren(self)




    def functionCall(self):

        localctx = KodexaSelectorParser.FunctionCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_functionCall)
        try:
            self.state = 197
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [26]:
                self.enterOuterAlt(localctx, 1)
                self.state = 193
                self.funcQName()
                self.state = 194
                self.formalArguments()
                pass
            elif token in [24, 25]:
                self.enterOuterAlt(localctx, 2)
                self.state = 196
                self.builtInFunctionCall()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BuiltInFunctionCallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return KodexaSelectorParser.RULE_builtInFunctionCall

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class TrueFunctionContext(BuiltInFunctionCallContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.BuiltInFunctionCallContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def TRUE(self):
            return self.getToken(KodexaSelectorParser.TRUE, 0)
        def formalArguments(self):
            return self.getTypedRuleContext(KodexaSelectorParser.FormalArgumentsContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTrueFunction" ):
                listener.enterTrueFunction(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTrueFunction" ):
                listener.exitTrueFunction(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTrueFunction" ):
                return visitor.visitTrueFunction(self)
            else:
                return visitor.visitChildren(self)


    class FalseFunctionContext(BuiltInFunctionCallContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.BuiltInFunctionCallContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def FALSE(self):
            return self.getToken(KodexaSelectorParser.FALSE, 0)
        def formalArguments(self):
            return self.getTypedRuleContext(KodexaSelectorParser.FormalArgumentsContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFalseFunction" ):
                listener.enterFalseFunction(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFalseFunction" ):
                listener.exitFalseFunction(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFalseFunction" ):
                return visitor.visitFalseFunction(self)
            else:
                return visitor.visitChildren(self)



    def builtInFunctionCall(self):

        localctx = KodexaSelectorParser.BuiltInFunctionCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_builtInFunctionCall)
        try:
            self.state = 203
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [24]:
                localctx = KodexaSelectorParser.TrueFunctionContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 199
                self.match(KodexaSelectorParser.TRUE)
                self.state = 200
                self.formalArguments()
                pass
            elif token in [25]:
                localctx = KodexaSelectorParser.FalseFunctionContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 201
                self.match(KodexaSelectorParser.FALSE)
                self.state = 202
                self.formalArguments()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FuncQNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FUNCTION_NAME(self):
            return self.getToken(KodexaSelectorParser.FUNCTION_NAME, 0)

        def getRuleIndex(self):
            return KodexaSelectorParser.RULE_funcQName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFuncQName" ):
                listener.enterFuncQName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFuncQName" ):
                listener.exitFuncQName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFuncQName" ):
                return visitor.visitFuncQName(self)
            else:
                return visitor.visitChildren(self)




    def funcQName(self):

        localctx = KodexaSelectorParser.FuncQNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_funcQName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 205
            self.match(KodexaSelectorParser.FUNCTION_NAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FormalArgumentsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return KodexaSelectorParser.RULE_formalArguments

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class EmptyArgsContext(FormalArgumentsContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.FormalArgumentsContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(KodexaSelectorParser.LPAREN, 0)
        def RPAREN(self):
            return self.getToken(KodexaSelectorParser.RPAREN, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEmptyArgs" ):
                listener.enterEmptyArgs(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEmptyArgs" ):
                listener.exitEmptyArgs(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEmptyArgs" ):
                return visitor.visitEmptyArgs(self)
            else:
                return visitor.visitChildren(self)


    class ArgsListContext(FormalArgumentsContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.FormalArgumentsContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(KodexaSelectorParser.LPAREN, 0)
        def argumentList(self):
            return self.getTypedRuleContext(KodexaSelectorParser.ArgumentListContext,0)

        def RPAREN(self):
            return self.getToken(KodexaSelectorParser.RPAREN, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArgsList" ):
                listener.enterArgsList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArgsList" ):
                listener.exitArgsList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArgsList" ):
                return visitor.visitArgsList(self)
            else:
                return visitor.visitChildren(self)



    def formalArguments(self):

        localctx = KodexaSelectorParser.FormalArgumentsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_formalArguments)
        try:
            self.state = 213
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,15,self._ctx)
            if la_ == 1:
                localctx = KodexaSelectorParser.EmptyArgsContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 207
                self.match(KodexaSelectorParser.LPAREN)
                self.state = 208
                self.match(KodexaSelectorParser.RPAREN)
                pass

            elif la_ == 2:
                localctx = KodexaSelectorParser.ArgsListContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 209
                self.match(KodexaSelectorParser.LPAREN)
                self.state = 210
                self.argumentList(0)
                self.state = 211
                self.match(KodexaSelectorParser.RPAREN)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgumentListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return KodexaSelectorParser.RULE_argumentList

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class SingleArgContext(ArgumentListContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.ArgumentListContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(KodexaSelectorParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSingleArg" ):
                listener.enterSingleArg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSingleArg" ):
                listener.exitSingleArg(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSingleArg" ):
                return visitor.visitSingleArg(self)
            else:
                return visitor.visitChildren(self)


    class MultipleArgsContext(ArgumentListContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a KodexaSelectorParser.ArgumentListContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def argumentList(self):
            return self.getTypedRuleContext(KodexaSelectorParser.ArgumentListContext,0)

        def COMMA(self):
            return self.getToken(KodexaSelectorParser.COMMA, 0)
        def expr(self):
            return self.getTypedRuleContext(KodexaSelectorParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultipleArgs" ):
                listener.enterMultipleArgs(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultipleArgs" ):
                listener.exitMultipleArgs(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultipleArgs" ):
                return visitor.visitMultipleArgs(self)
            else:
                return visitor.visitChildren(self)



    def argumentList(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = KodexaSelectorParser.ArgumentListContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 40
        self.enterRecursionRule(localctx, 40, self.RULE_argumentList, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            localctx = KodexaSelectorParser.SingleArgContext(self, localctx)
            self._ctx = localctx
            _prevctx = localctx

            self.state = 216
            self.expr(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 223
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,16,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = KodexaSelectorParser.MultipleArgsContext(self, KodexaSelectorParser.ArgumentListContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_argumentList)
                    self.state = 218
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 219
                    self.match(KodexaSelectorParser.COMMA)
                    self.state = 220
                    self.expr(0) 
                self.state = 225
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,16,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class PathSepContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PATH_SEP(self):
            return self.getToken(KodexaSelectorParser.PATH_SEP, 0)

        def ABBREV_PATH_SEP(self):
            return self.getToken(KodexaSelectorParser.ABBREV_PATH_SEP, 0)

        def getRuleIndex(self):
            return KodexaSelectorParser.RULE_pathSep

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPathSep" ):
                listener.enterPathSep(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPathSep" ):
                listener.exitPathSep(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPathSep" ):
                return visitor.visitPathSep(self)
            else:
                return visitor.visitChildren(self)




    def pathSep(self):

        localctx = KodexaSelectorParser.PathSepContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_pathSep)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 226
            _la = self._input.LA(1)
            if not(_la==5 or _la==6):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[1] = self.expr_sempred
        self._predicates[4] = self.relativeLocationPath_sempred
        self._predicates[10] = self.filterExpr_sempred
        self._predicates[11] = self.predicateList_sempred
        self._predicates[20] = self.argumentList_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 19)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 18)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 17)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 16)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 15)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 14)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 13)
         

            if predIndex == 7:
                return self.precpred(self._ctx, 12)
         

            if predIndex == 8:
                return self.precpred(self._ctx, 10)
         

    def relativeLocationPath_sempred(self, localctx:RelativeLocationPathContext, predIndex:int):
            if predIndex == 9:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 10:
                return self.precpred(self._ctx, 1)
         

    def filterExpr_sempred(self, localctx:FilterExprContext, predIndex:int):
            if predIndex == 11:
                return self.precpred(self._ctx, 1)
         

    def predicateList_sempred(self, localctx:PredicateListContext, predIndex:int):
            if predIndex == 12:
                return self.precpred(self._ctx, 1)
         

    def argumentList_sempred(self, localctx:ArgumentListContext, predIndex:int):
            if predIndex == 13:
                return self.precpred(self._ctx, 1)
         




