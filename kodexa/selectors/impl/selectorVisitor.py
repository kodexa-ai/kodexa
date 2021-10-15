# Generated from /Users/pdodds/src/kodexa/kodexa/resources/selector.g4 by ANTLR 4.9.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .selectorParser import selectorParser
else:
    from selectorParser import selectorParser

# This class defines a complete generic visitor for a parse tree produced by selectorParser.

class selectorVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by selectorParser#main.
    def visitMain(self, ctx:selectorParser.MainContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by selectorParser#locationPath.
    def visitLocationPath(self, ctx:selectorParser.LocationPathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by selectorParser#absoluteLocationPathNoroot.
    def visitAbsoluteLocationPathNoroot(self, ctx:selectorParser.AbsoluteLocationPathNorootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by selectorParser#relativeLocationPath.
    def visitRelativeLocationPath(self, ctx:selectorParser.RelativeLocationPathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by selectorParser#step.
    def visitStep(self, ctx:selectorParser.StepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by selectorParser#axisSpecifier.
    def visitAxisSpecifier(self, ctx:selectorParser.AxisSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by selectorParser#nodeTest.
    def visitNodeTest(self, ctx:selectorParser.NodeTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by selectorParser#predicate.
    def visitPredicate(self, ctx:selectorParser.PredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by selectorParser#abbreviatedStep.
    def visitAbbreviatedStep(self, ctx:selectorParser.AbbreviatedStepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by selectorParser#expr.
    def visitExpr(self, ctx:selectorParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by selectorParser#primaryExpr.
    def visitPrimaryExpr(self, ctx:selectorParser.PrimaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by selectorParser#functionCall.
    def visitFunctionCall(self, ctx:selectorParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by selectorParser#unionExprNoRoot.
    def visitUnionExprNoRoot(self, ctx:selectorParser.UnionExprNoRootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by selectorParser#pathExprNoRoot.
    def visitPathExprNoRoot(self, ctx:selectorParser.PathExprNoRootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by selectorParser#filterExpr.
    def visitFilterExpr(self, ctx:selectorParser.FilterExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by selectorParser#orExpr.
    def visitOrExpr(self, ctx:selectorParser.OrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by selectorParser#andExpr.
    def visitAndExpr(self, ctx:selectorParser.AndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by selectorParser#equalityExpr.
    def visitEqualityExpr(self, ctx:selectorParser.EqualityExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by selectorParser#relationalExpr.
    def visitRelationalExpr(self, ctx:selectorParser.RelationalExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by selectorParser#additiveExpr.
    def visitAdditiveExpr(self, ctx:selectorParser.AdditiveExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by selectorParser#multiplicativeExpr.
    def visitMultiplicativeExpr(self, ctx:selectorParser.MultiplicativeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by selectorParser#unaryExprNoRoot.
    def visitUnaryExprNoRoot(self, ctx:selectorParser.UnaryExprNoRootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by selectorParser#qName.
    def visitQName(self, ctx:selectorParser.QNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by selectorParser#functionName.
    def visitFunctionName(self, ctx:selectorParser.FunctionNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by selectorParser#variableReference.
    def visitVariableReference(self, ctx:selectorParser.VariableReferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by selectorParser#nameTest.
    def visitNameTest(self, ctx:selectorParser.NameTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by selectorParser#nCName.
    def visitNCName(self, ctx:selectorParser.NCNameContext):
        return self.visitChildren(ctx)



del selectorParser