# Generated from resources/KodexaSelector.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .KodexaSelectorParser import KodexaSelectorParser
else:
    from KodexaSelectorParser import KodexaSelectorParser

# This class defines a complete generic visitor for a parse tree produced by KodexaSelectorParser.

class KodexaSelectorVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by KodexaSelectorParser#xpath.
    def visitXpath(self, ctx:KodexaSelectorParser.XpathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#equalsExpr.
    def visitEqualsExpr(self, ctx:KodexaSelectorParser.EqualsExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#subtractExpr.
    def visitSubtractExpr(self, ctx:KodexaSelectorParser.SubtractExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#divideExpr.
    def visitDivideExpr(self, ctx:KodexaSelectorParser.DivideExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#intersectExpr.
    def visitIntersectExpr(self, ctx:KodexaSelectorParser.IntersectExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#moduloExpr.
    def visitModuloExpr(self, ctx:KodexaSelectorParser.ModuloExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#orExpr.
    def visitOrExpr(self, ctx:KodexaSelectorParser.OrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#absolutePathExpr.
    def visitAbsolutePathExpr(self, ctx:KodexaSelectorParser.AbsolutePathExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#multiplyExpr.
    def visitMultiplyExpr(self, ctx:KodexaSelectorParser.MultiplyExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#unionExpr.
    def visitUnionExpr(self, ctx:KodexaSelectorParser.UnionExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#relationalExpr.
    def visitRelationalExpr(self, ctx:KodexaSelectorParser.RelationalExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#pipelineExpr.
    def visitPipelineExpr(self, ctx:KodexaSelectorParser.PipelineExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#relativePathExpr.
    def visitRelativePathExpr(self, ctx:KodexaSelectorParser.RelativePathExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#unaryMinusExpr.
    def visitUnaryMinusExpr(self, ctx:KodexaSelectorParser.UnaryMinusExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#abbrevAbsPathExpr.
    def visitAbbrevAbsPathExpr(self, ctx:KodexaSelectorParser.AbbrevAbsPathExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#addExpr.
    def visitAddExpr(self, ctx:KodexaSelectorParser.AddExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#filterExpression.
    def visitFilterExpression(self, ctx:KodexaSelectorParser.FilterExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#pathBinaryExpr.
    def visitPathBinaryExpr(self, ctx:KodexaSelectorParser.PathBinaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#andExpr.
    def visitAndExpr(self, ctx:KodexaSelectorParser.AndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#rootOnly.
    def visitRootOnly(self, ctx:KodexaSelectorParser.RootOnlyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#rootPath.
    def visitRootPath(self, ctx:KodexaSelectorParser.RootPathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#abbreviatedAbsoluteLocationPath.
    def visitAbbreviatedAbsoluteLocationPath(self, ctx:KodexaSelectorParser.AbbreviatedAbsoluteLocationPathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#singleStep.
    def visitSingleStep(self, ctx:KodexaSelectorParser.SingleStepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#pathStep.
    def visitPathStep(self, ctx:KodexaSelectorParser.PathStepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#abbrevPathStep.
    def visitAbbrevPathStep(self, ctx:KodexaSelectorParser.AbbrevPathStepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#nodeTestStep.
    def visitNodeTestStep(self, ctx:KodexaSelectorParser.NodeTestStepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#nodeTestPredStep.
    def visitNodeTestPredStep(self, ctx:KodexaSelectorParser.NodeTestPredStepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#axisNodeTestStep.
    def visitAxisNodeTestStep(self, ctx:KodexaSelectorParser.AxisNodeTestStepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#axisNodeTestPredStep.
    def visitAxisNodeTestPredStep(self, ctx:KodexaSelectorParser.AxisNodeTestPredStepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#selfStep.
    def visitSelfStep(self, ctx:KodexaSelectorParser.SelfStepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#parentStep.
    def visitParentStep(self, ctx:KodexaSelectorParser.ParentStepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#fullAxis.
    def visitFullAxis(self, ctx:KodexaSelectorParser.FullAxisContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#attrAxis.
    def visitAttrAxis(self, ctx:KodexaSelectorParser.AttrAxisContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#nameTestNode.
    def visitNameTestNode(self, ctx:KodexaSelectorParser.NameTestNodeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#nodeTypeTest.
    def visitNodeTypeTest(self, ctx:KodexaSelectorParser.NodeTypeTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#nodeTypeLiteralTest.
    def visitNodeTypeLiteralTest(self, ctx:KodexaSelectorParser.NodeTypeLiteralTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#anyNameTest.
    def visitAnyNameTest(self, ctx:KodexaSelectorParser.AnyNameTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#prefixedAnyNameTest.
    def visitPrefixedAnyNameTest(self, ctx:KodexaSelectorParser.PrefixedAnyNameTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#qNameTest.
    def visitQNameTest(self, ctx:KodexaSelectorParser.QNameTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#prefixedName.
    def visitPrefixedName(self, ctx:KodexaSelectorParser.PrefixedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#simpleName.
    def visitSimpleName(self, ctx:KodexaSelectorParser.SimpleNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#prefixedFuncName.
    def visitPrefixedFuncName(self, ctx:KodexaSelectorParser.PrefixedFuncNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#simpleFuncName.
    def visitSimpleFuncName(self, ctx:KodexaSelectorParser.SimpleFuncNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#funcCallFilter.
    def visitFuncCallFilter(self, ctx:KodexaSelectorParser.FuncCallFilterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#groupedFilter.
    def visitGroupedFilter(self, ctx:KodexaSelectorParser.GroupedFilterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#predicatedFilter.
    def visitPredicatedFilter(self, ctx:KodexaSelectorParser.PredicatedFilterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#numberFilter.
    def visitNumberFilter(self, ctx:KodexaSelectorParser.NumberFilterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#varRefFilter.
    def visitVarRefFilter(self, ctx:KodexaSelectorParser.VarRefFilterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#literalFilter.
    def visitLiteralFilter(self, ctx:KodexaSelectorParser.LiteralFilterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#singlePredicate.
    def visitSinglePredicate(self, ctx:KodexaSelectorParser.SinglePredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#multiplePredicate.
    def visitMultiplePredicate(self, ctx:KodexaSelectorParser.MultiplePredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#predicate.
    def visitPredicate(self, ctx:KodexaSelectorParser.PredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#variableReference.
    def visitVariableReference(self, ctx:KodexaSelectorParser.VariableReferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#number.
    def visitNumber(self, ctx:KodexaSelectorParser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#functionCall.
    def visitFunctionCall(self, ctx:KodexaSelectorParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#emptyArgs.
    def visitEmptyArgs(self, ctx:KodexaSelectorParser.EmptyArgsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#argsList.
    def visitArgsList(self, ctx:KodexaSelectorParser.ArgsListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#singleArg.
    def visitSingleArg(self, ctx:KodexaSelectorParser.SingleArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#multipleArgs.
    def visitMultipleArgs(self, ctx:KodexaSelectorParser.MultipleArgsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by KodexaSelectorParser#pathSep.
    def visitPathSep(self, ctx:KodexaSelectorParser.PathSepContext):
        return self.visitChildren(ctx)



del KodexaSelectorParser