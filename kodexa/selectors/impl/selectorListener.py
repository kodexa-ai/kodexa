# Generated from /Users/pdodds/src/kodexa/kodexa/resources/selector.g4 by ANTLR 4.9.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .selectorParser import selectorParser
else:
    from selectorParser import selectorParser

# This class defines a complete listener for a parse tree produced by selectorParser.
class selectorListener(ParseTreeListener):

    # Enter a parse tree produced by selectorParser#main.
    def enterMain(self, ctx:selectorParser.MainContext):
        pass

    # Exit a parse tree produced by selectorParser#main.
    def exitMain(self, ctx:selectorParser.MainContext):
        pass


    # Enter a parse tree produced by selectorParser#locationPath.
    def enterLocationPath(self, ctx:selectorParser.LocationPathContext):
        pass

    # Exit a parse tree produced by selectorParser#locationPath.
    def exitLocationPath(self, ctx:selectorParser.LocationPathContext):
        pass


    # Enter a parse tree produced by selectorParser#absoluteLocationPathNoroot.
    def enterAbsoluteLocationPathNoroot(self, ctx:selectorParser.AbsoluteLocationPathNorootContext):
        pass

    # Exit a parse tree produced by selectorParser#absoluteLocationPathNoroot.
    def exitAbsoluteLocationPathNoroot(self, ctx:selectorParser.AbsoluteLocationPathNorootContext):
        pass


    # Enter a parse tree produced by selectorParser#relativeLocationPath.
    def enterRelativeLocationPath(self, ctx:selectorParser.RelativeLocationPathContext):
        pass

    # Exit a parse tree produced by selectorParser#relativeLocationPath.
    def exitRelativeLocationPath(self, ctx:selectorParser.RelativeLocationPathContext):
        pass


    # Enter a parse tree produced by selectorParser#step.
    def enterStep(self, ctx:selectorParser.StepContext):
        pass

    # Exit a parse tree produced by selectorParser#step.
    def exitStep(self, ctx:selectorParser.StepContext):
        pass


    # Enter a parse tree produced by selectorParser#axisSpecifier.
    def enterAxisSpecifier(self, ctx:selectorParser.AxisSpecifierContext):
        pass

    # Exit a parse tree produced by selectorParser#axisSpecifier.
    def exitAxisSpecifier(self, ctx:selectorParser.AxisSpecifierContext):
        pass


    # Enter a parse tree produced by selectorParser#nodeTest.
    def enterNodeTest(self, ctx:selectorParser.NodeTestContext):
        pass

    # Exit a parse tree produced by selectorParser#nodeTest.
    def exitNodeTest(self, ctx:selectorParser.NodeTestContext):
        pass


    # Enter a parse tree produced by selectorParser#predicate.
    def enterPredicate(self, ctx:selectorParser.PredicateContext):
        pass

    # Exit a parse tree produced by selectorParser#predicate.
    def exitPredicate(self, ctx:selectorParser.PredicateContext):
        pass


    # Enter a parse tree produced by selectorParser#abbreviatedStep.
    def enterAbbreviatedStep(self, ctx:selectorParser.AbbreviatedStepContext):
        pass

    # Exit a parse tree produced by selectorParser#abbreviatedStep.
    def exitAbbreviatedStep(self, ctx:selectorParser.AbbreviatedStepContext):
        pass


    # Enter a parse tree produced by selectorParser#expr.
    def enterExpr(self, ctx:selectorParser.ExprContext):
        pass

    # Exit a parse tree produced by selectorParser#expr.
    def exitExpr(self, ctx:selectorParser.ExprContext):
        pass


    # Enter a parse tree produced by selectorParser#primaryExpr.
    def enterPrimaryExpr(self, ctx:selectorParser.PrimaryExprContext):
        pass

    # Exit a parse tree produced by selectorParser#primaryExpr.
    def exitPrimaryExpr(self, ctx:selectorParser.PrimaryExprContext):
        pass


    # Enter a parse tree produced by selectorParser#functionCall.
    def enterFunctionCall(self, ctx:selectorParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by selectorParser#functionCall.
    def exitFunctionCall(self, ctx:selectorParser.FunctionCallContext):
        pass


    # Enter a parse tree produced by selectorParser#unionExprNoRoot.
    def enterUnionExprNoRoot(self, ctx:selectorParser.UnionExprNoRootContext):
        pass

    # Exit a parse tree produced by selectorParser#unionExprNoRoot.
    def exitUnionExprNoRoot(self, ctx:selectorParser.UnionExprNoRootContext):
        pass


    # Enter a parse tree produced by selectorParser#pathExprNoRoot.
    def enterPathExprNoRoot(self, ctx:selectorParser.PathExprNoRootContext):
        pass

    # Exit a parse tree produced by selectorParser#pathExprNoRoot.
    def exitPathExprNoRoot(self, ctx:selectorParser.PathExprNoRootContext):
        pass


    # Enter a parse tree produced by selectorParser#filterExpr.
    def enterFilterExpr(self, ctx:selectorParser.FilterExprContext):
        pass

    # Exit a parse tree produced by selectorParser#filterExpr.
    def exitFilterExpr(self, ctx:selectorParser.FilterExprContext):
        pass


    # Enter a parse tree produced by selectorParser#orExpr.
    def enterOrExpr(self, ctx:selectorParser.OrExprContext):
        pass

    # Exit a parse tree produced by selectorParser#orExpr.
    def exitOrExpr(self, ctx:selectorParser.OrExprContext):
        pass


    # Enter a parse tree produced by selectorParser#andExpr.
    def enterAndExpr(self, ctx:selectorParser.AndExprContext):
        pass

    # Exit a parse tree produced by selectorParser#andExpr.
    def exitAndExpr(self, ctx:selectorParser.AndExprContext):
        pass


    # Enter a parse tree produced by selectorParser#equalityExpr.
    def enterEqualityExpr(self, ctx:selectorParser.EqualityExprContext):
        pass

    # Exit a parse tree produced by selectorParser#equalityExpr.
    def exitEqualityExpr(self, ctx:selectorParser.EqualityExprContext):
        pass


    # Enter a parse tree produced by selectorParser#relationalExpr.
    def enterRelationalExpr(self, ctx:selectorParser.RelationalExprContext):
        pass

    # Exit a parse tree produced by selectorParser#relationalExpr.
    def exitRelationalExpr(self, ctx:selectorParser.RelationalExprContext):
        pass


    # Enter a parse tree produced by selectorParser#additiveExpr.
    def enterAdditiveExpr(self, ctx:selectorParser.AdditiveExprContext):
        pass

    # Exit a parse tree produced by selectorParser#additiveExpr.
    def exitAdditiveExpr(self, ctx:selectorParser.AdditiveExprContext):
        pass


    # Enter a parse tree produced by selectorParser#multiplicativeExpr.
    def enterMultiplicativeExpr(self, ctx:selectorParser.MultiplicativeExprContext):
        pass

    # Exit a parse tree produced by selectorParser#multiplicativeExpr.
    def exitMultiplicativeExpr(self, ctx:selectorParser.MultiplicativeExprContext):
        pass


    # Enter a parse tree produced by selectorParser#unaryExprNoRoot.
    def enterUnaryExprNoRoot(self, ctx:selectorParser.UnaryExprNoRootContext):
        pass

    # Exit a parse tree produced by selectorParser#unaryExprNoRoot.
    def exitUnaryExprNoRoot(self, ctx:selectorParser.UnaryExprNoRootContext):
        pass


    # Enter a parse tree produced by selectorParser#qName.
    def enterQName(self, ctx:selectorParser.QNameContext):
        pass

    # Exit a parse tree produced by selectorParser#qName.
    def exitQName(self, ctx:selectorParser.QNameContext):
        pass


    # Enter a parse tree produced by selectorParser#functionName.
    def enterFunctionName(self, ctx:selectorParser.FunctionNameContext):
        pass

    # Exit a parse tree produced by selectorParser#functionName.
    def exitFunctionName(self, ctx:selectorParser.FunctionNameContext):
        pass


    # Enter a parse tree produced by selectorParser#variableReference.
    def enterVariableReference(self, ctx:selectorParser.VariableReferenceContext):
        pass

    # Exit a parse tree produced by selectorParser#variableReference.
    def exitVariableReference(self, ctx:selectorParser.VariableReferenceContext):
        pass


    # Enter a parse tree produced by selectorParser#nameTest.
    def enterNameTest(self, ctx:selectorParser.NameTestContext):
        pass

    # Exit a parse tree produced by selectorParser#nameTest.
    def exitNameTest(self, ctx:selectorParser.NameTestContext):
        pass


    # Enter a parse tree produced by selectorParser#nCName.
    def enterNCName(self, ctx:selectorParser.NCNameContext):
        pass

    # Exit a parse tree produced by selectorParser#nCName.
    def exitNCName(self, ctx:selectorParser.NCNameContext):
        pass



del selectorParser