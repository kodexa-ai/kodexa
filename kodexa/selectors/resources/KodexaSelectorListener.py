# Generated from resources/KodexaSelector.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .KodexaSelectorParser import KodexaSelectorParser
else:
    from KodexaSelectorParser import KodexaSelectorParser

# This class defines a complete listener for a parse tree produced by KodexaSelectorParser.
class KodexaSelectorListener(ParseTreeListener):

    # Enter a parse tree produced by KodexaSelectorParser#xpath.
    def enterXpath(self, ctx:KodexaSelectorParser.XpathContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#xpath.
    def exitXpath(self, ctx:KodexaSelectorParser.XpathContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#equalsExpr.
    def enterEqualsExpr(self, ctx:KodexaSelectorParser.EqualsExprContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#equalsExpr.
    def exitEqualsExpr(self, ctx:KodexaSelectorParser.EqualsExprContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#subtractExpr.
    def enterSubtractExpr(self, ctx:KodexaSelectorParser.SubtractExprContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#subtractExpr.
    def exitSubtractExpr(self, ctx:KodexaSelectorParser.SubtractExprContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#intersectExpr.
    def enterIntersectExpr(self, ctx:KodexaSelectorParser.IntersectExprContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#intersectExpr.
    def exitIntersectExpr(self, ctx:KodexaSelectorParser.IntersectExprContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#directNameTest.
    def enterDirectNameTest(self, ctx:KodexaSelectorParser.DirectNameTestContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#directNameTest.
    def exitDirectNameTest(self, ctx:KodexaSelectorParser.DirectNameTestContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#orExpr.
    def enterOrExpr(self, ctx:KodexaSelectorParser.OrExprContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#orExpr.
    def exitOrExpr(self, ctx:KodexaSelectorParser.OrExprContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#absolutePathExpr.
    def enterAbsolutePathExpr(self, ctx:KodexaSelectorParser.AbsolutePathExprContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#absolutePathExpr.
    def exitAbsolutePathExpr(self, ctx:KodexaSelectorParser.AbsolutePathExprContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#funcCallExpr.
    def enterFuncCallExpr(self, ctx:KodexaSelectorParser.FuncCallExprContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#funcCallExpr.
    def exitFuncCallExpr(self, ctx:KodexaSelectorParser.FuncCallExprContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#unionExpr.
    def enterUnionExpr(self, ctx:KodexaSelectorParser.UnionExprContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#unionExpr.
    def exitUnionExpr(self, ctx:KodexaSelectorParser.UnionExprContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#relationalExpr.
    def enterRelationalExpr(self, ctx:KodexaSelectorParser.RelationalExprContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#relationalExpr.
    def exitRelationalExpr(self, ctx:KodexaSelectorParser.RelationalExprContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#pipelineExpr.
    def enterPipelineExpr(self, ctx:KodexaSelectorParser.PipelineExprContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#pipelineExpr.
    def exitPipelineExpr(self, ctx:KodexaSelectorParser.PipelineExprContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#relativePathExpr.
    def enterRelativePathExpr(self, ctx:KodexaSelectorParser.RelativePathExprContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#relativePathExpr.
    def exitRelativePathExpr(self, ctx:KodexaSelectorParser.RelativePathExprContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#rootNameTest.
    def enterRootNameTest(self, ctx:KodexaSelectorParser.RootNameTestContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#rootNameTest.
    def exitRootNameTest(self, ctx:KodexaSelectorParser.RootNameTestContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#unaryMinusExpr.
    def enterUnaryMinusExpr(self, ctx:KodexaSelectorParser.UnaryMinusExprContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#unaryMinusExpr.
    def exitUnaryMinusExpr(self, ctx:KodexaSelectorParser.UnaryMinusExprContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#abbrevAbsPathExpr.
    def enterAbbrevAbsPathExpr(self, ctx:KodexaSelectorParser.AbbrevAbsPathExprContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#abbrevAbsPathExpr.
    def exitAbbrevAbsPathExpr(self, ctx:KodexaSelectorParser.AbbrevAbsPathExprContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#addExpr.
    def enterAddExpr(self, ctx:KodexaSelectorParser.AddExprContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#addExpr.
    def exitAddExpr(self, ctx:KodexaSelectorParser.AddExprContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#filterExpression.
    def enterFilterExpression(self, ctx:KodexaSelectorParser.FilterExpressionContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#filterExpression.
    def exitFilterExpression(self, ctx:KodexaSelectorParser.FilterExpressionContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#booleanLiteralExpr.
    def enterBooleanLiteralExpr(self, ctx:KodexaSelectorParser.BooleanLiteralExprContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#booleanLiteralExpr.
    def exitBooleanLiteralExpr(self, ctx:KodexaSelectorParser.BooleanLiteralExprContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#pathBinaryExpr.
    def enterPathBinaryExpr(self, ctx:KodexaSelectorParser.PathBinaryExprContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#pathBinaryExpr.
    def exitPathBinaryExpr(self, ctx:KodexaSelectorParser.PathBinaryExprContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#andExpr.
    def enterAndExpr(self, ctx:KodexaSelectorParser.AndExprContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#andExpr.
    def exitAndExpr(self, ctx:KodexaSelectorParser.AndExprContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#rootOnly.
    def enterRootOnly(self, ctx:KodexaSelectorParser.RootOnlyContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#rootOnly.
    def exitRootOnly(self, ctx:KodexaSelectorParser.RootOnlyContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#rootPath.
    def enterRootPath(self, ctx:KodexaSelectorParser.RootPathContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#rootPath.
    def exitRootPath(self, ctx:KodexaSelectorParser.RootPathContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#abbreviatedAbsoluteLocationPath.
    def enterAbbreviatedAbsoluteLocationPath(self, ctx:KodexaSelectorParser.AbbreviatedAbsoluteLocationPathContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#abbreviatedAbsoluteLocationPath.
    def exitAbbreviatedAbsoluteLocationPath(self, ctx:KodexaSelectorParser.AbbreviatedAbsoluteLocationPathContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#singleStep.
    def enterSingleStep(self, ctx:KodexaSelectorParser.SingleStepContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#singleStep.
    def exitSingleStep(self, ctx:KodexaSelectorParser.SingleStepContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#pathStep.
    def enterPathStep(self, ctx:KodexaSelectorParser.PathStepContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#pathStep.
    def exitPathStep(self, ctx:KodexaSelectorParser.PathStepContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#abbrevPathStep.
    def enterAbbrevPathStep(self, ctx:KodexaSelectorParser.AbbrevPathStepContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#abbrevPathStep.
    def exitAbbrevPathStep(self, ctx:KodexaSelectorParser.AbbrevPathStepContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#nodeTestStep.
    def enterNodeTestStep(self, ctx:KodexaSelectorParser.NodeTestStepContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#nodeTestStep.
    def exitNodeTestStep(self, ctx:KodexaSelectorParser.NodeTestStepContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#nodeTestPredStep.
    def enterNodeTestPredStep(self, ctx:KodexaSelectorParser.NodeTestPredStepContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#nodeTestPredStep.
    def exitNodeTestPredStep(self, ctx:KodexaSelectorParser.NodeTestPredStepContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#axisNodeTestStep.
    def enterAxisNodeTestStep(self, ctx:KodexaSelectorParser.AxisNodeTestStepContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#axisNodeTestStep.
    def exitAxisNodeTestStep(self, ctx:KodexaSelectorParser.AxisNodeTestStepContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#axisNodeTestPredStep.
    def enterAxisNodeTestPredStep(self, ctx:KodexaSelectorParser.AxisNodeTestPredStepContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#axisNodeTestPredStep.
    def exitAxisNodeTestPredStep(self, ctx:KodexaSelectorParser.AxisNodeTestPredStepContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#selfStep.
    def enterSelfStep(self, ctx:KodexaSelectorParser.SelfStepContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#selfStep.
    def exitSelfStep(self, ctx:KodexaSelectorParser.SelfStepContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#parentStep.
    def enterParentStep(self, ctx:KodexaSelectorParser.ParentStepContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#parentStep.
    def exitParentStep(self, ctx:KodexaSelectorParser.ParentStepContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#fullAxis.
    def enterFullAxis(self, ctx:KodexaSelectorParser.FullAxisContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#fullAxis.
    def exitFullAxis(self, ctx:KodexaSelectorParser.FullAxisContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#attrAxis.
    def enterAttrAxis(self, ctx:KodexaSelectorParser.AttrAxisContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#attrAxis.
    def exitAttrAxis(self, ctx:KodexaSelectorParser.AttrAxisContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#nameTestNode.
    def enterNameTestNode(self, ctx:KodexaSelectorParser.NameTestNodeContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#nameTestNode.
    def exitNameTestNode(self, ctx:KodexaSelectorParser.NameTestNodeContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#anyNameTest.
    def enterAnyNameTest(self, ctx:KodexaSelectorParser.AnyNameTestContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#anyNameTest.
    def exitAnyNameTest(self, ctx:KodexaSelectorParser.AnyNameTestContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#prefixedAnyNameTest.
    def enterPrefixedAnyNameTest(self, ctx:KodexaSelectorParser.PrefixedAnyNameTestContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#prefixedAnyNameTest.
    def exitPrefixedAnyNameTest(self, ctx:KodexaSelectorParser.PrefixedAnyNameTestContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#qNameTest.
    def enterQNameTest(self, ctx:KodexaSelectorParser.QNameTestContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#qNameTest.
    def exitQNameTest(self, ctx:KodexaSelectorParser.QNameTestContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#prefixedName.
    def enterPrefixedName(self, ctx:KodexaSelectorParser.PrefixedNameContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#prefixedName.
    def exitPrefixedName(self, ctx:KodexaSelectorParser.PrefixedNameContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#simpleName.
    def enterSimpleName(self, ctx:KodexaSelectorParser.SimpleNameContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#simpleName.
    def exitSimpleName(self, ctx:KodexaSelectorParser.SimpleNameContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#funcCallFilter.
    def enterFuncCallFilter(self, ctx:KodexaSelectorParser.FuncCallFilterContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#funcCallFilter.
    def exitFuncCallFilter(self, ctx:KodexaSelectorParser.FuncCallFilterContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#booleanFilter.
    def enterBooleanFilter(self, ctx:KodexaSelectorParser.BooleanFilterContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#booleanFilter.
    def exitBooleanFilter(self, ctx:KodexaSelectorParser.BooleanFilterContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#groupedFilter.
    def enterGroupedFilter(self, ctx:KodexaSelectorParser.GroupedFilterContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#groupedFilter.
    def exitGroupedFilter(self, ctx:KodexaSelectorParser.GroupedFilterContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#predicatedFilter.
    def enterPredicatedFilter(self, ctx:KodexaSelectorParser.PredicatedFilterContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#predicatedFilter.
    def exitPredicatedFilter(self, ctx:KodexaSelectorParser.PredicatedFilterContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#numberFilter.
    def enterNumberFilter(self, ctx:KodexaSelectorParser.NumberFilterContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#numberFilter.
    def exitNumberFilter(self, ctx:KodexaSelectorParser.NumberFilterContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#varRefFilter.
    def enterVarRefFilter(self, ctx:KodexaSelectorParser.VarRefFilterContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#varRefFilter.
    def exitVarRefFilter(self, ctx:KodexaSelectorParser.VarRefFilterContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#literalFilter.
    def enterLiteralFilter(self, ctx:KodexaSelectorParser.LiteralFilterContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#literalFilter.
    def exitLiteralFilter(self, ctx:KodexaSelectorParser.LiteralFilterContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#singlePredicate.
    def enterSinglePredicate(self, ctx:KodexaSelectorParser.SinglePredicateContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#singlePredicate.
    def exitSinglePredicate(self, ctx:KodexaSelectorParser.SinglePredicateContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#multiplePredicate.
    def enterMultiplePredicate(self, ctx:KodexaSelectorParser.MultiplePredicateContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#multiplePredicate.
    def exitMultiplePredicate(self, ctx:KodexaSelectorParser.MultiplePredicateContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#exprPredicate.
    def enterExprPredicate(self, ctx:KodexaSelectorParser.ExprPredicateContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#exprPredicate.
    def exitExprPredicate(self, ctx:KodexaSelectorParser.ExprPredicateContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#variableReference.
    def enterVariableReference(self, ctx:KodexaSelectorParser.VariableReferenceContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#variableReference.
    def exitVariableReference(self, ctx:KodexaSelectorParser.VariableReferenceContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#number.
    def enterNumber(self, ctx:KodexaSelectorParser.NumberContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#number.
    def exitNumber(self, ctx:KodexaSelectorParser.NumberContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#booleanLiteral.
    def enterBooleanLiteral(self, ctx:KodexaSelectorParser.BooleanLiteralContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#booleanLiteral.
    def exitBooleanLiteral(self, ctx:KodexaSelectorParser.BooleanLiteralContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#functionCall.
    def enterFunctionCall(self, ctx:KodexaSelectorParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#functionCall.
    def exitFunctionCall(self, ctx:KodexaSelectorParser.FunctionCallContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#trueFunction.
    def enterTrueFunction(self, ctx:KodexaSelectorParser.TrueFunctionContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#trueFunction.
    def exitTrueFunction(self, ctx:KodexaSelectorParser.TrueFunctionContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#falseFunction.
    def enterFalseFunction(self, ctx:KodexaSelectorParser.FalseFunctionContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#falseFunction.
    def exitFalseFunction(self, ctx:KodexaSelectorParser.FalseFunctionContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#funcQName.
    def enterFuncQName(self, ctx:KodexaSelectorParser.FuncQNameContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#funcQName.
    def exitFuncQName(self, ctx:KodexaSelectorParser.FuncQNameContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#emptyArgs.
    def enterEmptyArgs(self, ctx:KodexaSelectorParser.EmptyArgsContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#emptyArgs.
    def exitEmptyArgs(self, ctx:KodexaSelectorParser.EmptyArgsContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#argsList.
    def enterArgsList(self, ctx:KodexaSelectorParser.ArgsListContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#argsList.
    def exitArgsList(self, ctx:KodexaSelectorParser.ArgsListContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#singleArg.
    def enterSingleArg(self, ctx:KodexaSelectorParser.SingleArgContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#singleArg.
    def exitSingleArg(self, ctx:KodexaSelectorParser.SingleArgContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#multipleArgs.
    def enterMultipleArgs(self, ctx:KodexaSelectorParser.MultipleArgsContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#multipleArgs.
    def exitMultipleArgs(self, ctx:KodexaSelectorParser.MultipleArgsContext):
        pass


    # Enter a parse tree produced by KodexaSelectorParser#pathSep.
    def enterPathSep(self, ctx:KodexaSelectorParser.PathSepContext):
        pass

    # Exit a parse tree produced by KodexaSelectorParser#pathSep.
    def exitPathSep(self, ctx:KodexaSelectorParser.PathSepContext):
        pass



del KodexaSelectorParser