from antlr4 import *
from kodexa.selectors.resources.KodexaSelectorParser import KodexaSelectorParser
from kodexa.selectors.resources.KodexaSelectorVisitor import KodexaSelectorVisitor
import kodexa.selectors.ast as ast

class KodexaASTVisitor(KodexaSelectorVisitor):
    """
    Visitor implementation for building an AST from an ANTLR parse tree.
    This converts the ANTLR parse tree to the same AST structure used in the original code.
    """

    def visitOrExpr(self, ctx:KodexaSelectorParser.OrExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        return ast.BinaryExpression(left, 'or', right)

    def visitAndExpr(self, ctx:KodexaSelectorParser.AndExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        return ast.BinaryExpression(left, 'and', right)

    def visitEqualsExpr(self, ctx:KodexaSelectorParser.EqualsExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.EQUALS().getText()
        return ast.BinaryExpression(left, op, right)

    def visitRelationalExpr(self, ctx:KodexaSelectorParser.RelationalExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.REL_OP().getText()
        return ast.BinaryExpression(left, op, right)

    def visitAddExpr(self, ctx:KodexaSelectorParser.AddExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        return ast.BinaryExpression(left, '+', right)

    def visitSubtractExpr(self, ctx:KodexaSelectorParser.SubtractExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        return ast.BinaryExpression(left, '-', right)

    def visitUnionExpr(self, ctx:KodexaSelectorParser.UnionExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        return ast.BinaryExpression(left, '|', right)

    def visitIntersectExpr(self, ctx:KodexaSelectorParser.IntersectExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        return ast.BinaryExpression(left, 'intersect', right)

    def visitUnaryMinusExpr(self, ctx:KodexaSelectorParser.UnaryMinusExprContext):
        operand = self.visit(ctx.expr())
        return ast.UnaryExpression('-', operand)

    def visitPipelineExpr(self, ctx:KodexaSelectorParser.PipelineExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        return ast.PipelineExpression(left, 'stream', right)

    def visitFuncCallExpr(self, ctx:KodexaSelectorParser.FuncCallExprContext):
        return self.visit(ctx.functionCall())

    def visitBooleanLiteralExpr(self, ctx:KodexaSelectorParser.BooleanLiteralExprContext):
        return self.visit(ctx.booleanLiteral())

    def visitPathBinaryExpr(self, ctx:KodexaSelectorParser.PathBinaryExprContext):
        left = self.visit(ctx.filterExpr())
        op = self.visit(ctx.pathSep())
        right = self.visit(ctx.relativeLocationPath())
        return ast.BinaryExpression(left, op, right)

    def visitRootOnly(self, ctx:KodexaSelectorParser.RootOnlyContext):
        return ast.AbsolutePath('/')

    def visitRootPath(self, ctx:KodexaSelectorParser.RootPathContext):
        relative = self.visit(ctx.relativeLocationPath())
        return ast.AbsolutePath('/', relative)

    def visitAbbreviatedAbsoluteLocationPath(self, ctx:KodexaSelectorParser.AbbreviatedAbsoluteLocationPathContext):
        relative = self.visit(ctx.relativeLocationPath())
        return ast.AbsolutePath('//', relative)

    def visitSingleStep(self, ctx:KodexaSelectorParser.SingleStepContext):
        return self.visit(ctx.step())

    def visitPathStep(self, ctx:KodexaSelectorParser.PathStepContext):
        left = self.visit(ctx.relativeLocationPath())
        right = self.visit(ctx.step())
        return ast.BinaryExpression(left, '/', right)

    def visitAbbrevPathStep(self, ctx:KodexaSelectorParser.AbbrevPathStepContext):
        left = self.visit(ctx.relativeLocationPath())
        right = self.visit(ctx.step())
        return ast.BinaryExpression(left, '//', right)

    def visitNodeTestStep(self, ctx:KodexaSelectorParser.NodeTestStepContext):
        node_test = self.visit(ctx.nodeTest())
        return ast.Step(None, node_test, [])

    def visitNodeTestPredStep(self, ctx:KodexaSelectorParser.NodeTestPredStepContext):
        node_test = self.visit(ctx.nodeTest())
        predicates = self.visit(ctx.predicateList())
        return ast.Step(None, node_test, predicates)

    def visitAxisNodeTestStep(self, ctx:KodexaSelectorParser.AxisNodeTestStepContext):
        axis = self.visit(ctx.axisSpecifier())
        node_test = self.visit(ctx.nodeTest())
        return ast.Step(axis, node_test, [])

    def visitAxisNodeTestPredStep(self, ctx:KodexaSelectorParser.AxisNodeTestPredStepContext):
        axis = self.visit(ctx.axisSpecifier())
        node_test = self.visit(ctx.nodeTest())
        predicates = self.visit(ctx.predicateList())
        return ast.Step(axis, node_test, predicates)

    def visitSelfStep(self, ctx:KodexaSelectorParser.SelfStepContext):
        return ast.AbbreviatedStep('.')

    def visitParentStep(self, ctx:KodexaSelectorParser.ParentStepContext):
        return ast.AbbreviatedStep('..')

    def visitFullAxis(self, ctx:KodexaSelectorParser.FullAxisContext):
        return ctx.AXISNAME().getText()

    def visitAttrAxis(self, ctx:KodexaSelectorParser.AttrAxisContext):
        return '@'

    def visitNameTestNode(self, ctx:KodexaSelectorParser.NameTestNodeContext):
        return self.visit(ctx.nameTest())

    def visitAnyNameTest(self, ctx:KodexaSelectorParser.AnyNameTestContext):
        return ast.NameTest(None, '*')

    def visitPrefixedAnyNameTest(self, ctx:KodexaSelectorParser.PrefixedAnyNameTestContext):
        prefix = ctx.NCNAME().getText()
        return ast.NameTest(prefix, '*')

    def visitQNameTest(self, ctx:KodexaSelectorParser.QNameTestContext):
        qname = self.visit(ctx.qName())
        return ast.NameTest(qname[0], qname[1])

    def visitPrefixedName(self, ctx:KodexaSelectorParser.PrefixedNameContext):
        prefix = ctx.NCNAME(0).getText()
        name = ctx.NCNAME(1).getText()
        return (prefix, name)

    def visitSimpleName(self, ctx:KodexaSelectorParser.SimpleNameContext):
        return (None, ctx.NCNAME().getText())

    def visitPrefixedFuncName(self, ctx:KodexaSelectorParser.PrefixedFuncNameContext):
        prefix = ctx.NCNAME().getText()
        name = ctx.FUNCNAME().getText()
        return (prefix, name)

    def visitSimpleFuncName(self, ctx:KodexaSelectorParser.SimpleFuncNameContext):
        return (None, ctx.FUNCNAME().getText())

    def visitVarRefFilter(self, ctx:KodexaSelectorParser.VarRefFilterContext):
        return self.visit(ctx.variableReference())

    def visitLiteralFilter(self, ctx:KodexaSelectorParser.LiteralFilterContext):
        literal = ctx.LITERAL().getText()
        return literal[1:-1]  # Remove quotes

    def visitBooleanFilter(self, ctx:KodexaSelectorParser.BooleanFilterContext):
        return self.visit(ctx.booleanLiteral())

    def visitBooleanLiteral(self, ctx:KodexaSelectorParser.BooleanLiteralContext):
        if ctx.TRUE() is not None:
            return True
        else:
            return False

    def visitTrueFunction(self, ctx:KodexaSelectorParser.TrueFunctionContext):
        args = self.visit(ctx.formalArguments())
        return ast.FunctionCall(None, "true", args)

    def visitFalseFunction(self, ctx:KodexaSelectorParser.FalseFunctionContext):
        args = self.visit(ctx.formalArguments())
        return ast.FunctionCall(None, "false", args)

    def visitNumberFilter(self, ctx:KodexaSelectorParser.NumberFilterContext):
        return self.visit(ctx.number())

    def visitFuncCallFilter(self, ctx:KodexaSelectorParser.FuncCallFilterContext):
        return self.visit(ctx.functionCall())

    def visitGroupedFilter(self, ctx:KodexaSelectorParser.GroupedFilterContext):
        return self.visit(ctx.expr())

    def visitPredicatedFilter(self, ctx:KodexaSelectorParser.PredicatedFilterContext):
        base = self.visit(ctx.filterExpr())
        predicate = self.visit(ctx.predicate())
        
        if not hasattr(base, 'append_predicate'):
            base = ast.PredicatedExpression(base)
        
        base.append_predicate(predicate)
        return base

    def visitSinglePredicate(self, ctx:KodexaSelectorParser.SinglePredicateContext):
        return [self.visit(ctx.predicate())]

    def visitMultiplePredicate(self, ctx:KodexaSelectorParser.MultiplePredicateContext):
        predicates = self.visit(ctx.predicateList())
        predicates.append(self.visit(ctx.predicate()))
        return predicates

    def visitPredicate(self, ctx:KodexaSelectorParser.PredicateContext):
        return self.visit(ctx.expr())

    def visitVariableReference(self, ctx:KodexaSelectorParser.VariableReferenceContext):
        qname = self.visit(ctx.qName())
        return ast.VariableReference(qname)

    def visitNumber(self, ctx:KodexaSelectorParser.NumberContext):
        if ctx.FLOAT() is not None:
            return float(ctx.FLOAT().getText())
        else:
            return int(ctx.INTEGER().getText())

    def visitFunctionCall(self, ctx:KodexaSelectorParser.FunctionCallContext):
        if ctx.builtInFunctionCall() is not None:
            return self.visit(ctx.builtInFunctionCall())
        else:
            qname = self.visit(ctx.funcQName())
            args = self.visit(ctx.formalArguments())
            return ast.FunctionCall(qname[0], qname[1], args)

    def visitEmptyArgs(self, ctx:KodexaSelectorParser.EmptyArgsContext):
        return []

    def visitArgsList(self, ctx:KodexaSelectorParser.ArgsListContext):
        return self.visit(ctx.argumentList())

    def visitSingleArg(self, ctx:KodexaSelectorParser.SingleArgContext):
        return [self.visit(ctx.expr())]

    def visitMultipleArgs(self, ctx:KodexaSelectorParser.MultipleArgsContext):
        args = self.visit(ctx.argumentList())
        args.append(self.visit(ctx.expr()))
        return args

    def visitPathSep(self, ctx:KodexaSelectorParser.PathSepContext):
        if ctx.PATH_SEP() is not None:
            return '/'
        else:
            return '//'

    # Add default implementations for any missing visit methods
    def visitChildren(self, ctx):
        result = self.defaultResult()
        n = ctx.getChildCount()
        for i in range(n):
            if not ctx.getChild(i).getText() in ['{', '}', ';']:
                c = ctx.getChild(i)
                childResult = c.accept(self)
                result = self.aggregateResult(result, childResult)
        return result

    def defaultResult(self):
        return None

    def aggregateResult(self, aggregate, nextResult):
        return nextResult if nextResult is not None else aggregate