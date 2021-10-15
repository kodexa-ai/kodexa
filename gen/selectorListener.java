// Generated from /Users/pdodds/src/kodexa/kodexa/resources/selector.g4 by ANTLR 4.9.1
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link selectorParser}.
 */
public interface selectorListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link selectorParser#main}.
	 * @param ctx the parse tree
	 */
	void enterMain(selectorParser.MainContext ctx);
	/**
	 * Exit a parse tree produced by {@link selectorParser#main}.
	 * @param ctx the parse tree
	 */
	void exitMain(selectorParser.MainContext ctx);
	/**
	 * Enter a parse tree produced by {@link selectorParser#locationPath}.
	 * @param ctx the parse tree
	 */
	void enterLocationPath(selectorParser.LocationPathContext ctx);
	/**
	 * Exit a parse tree produced by {@link selectorParser#locationPath}.
	 * @param ctx the parse tree
	 */
	void exitLocationPath(selectorParser.LocationPathContext ctx);
	/**
	 * Enter a parse tree produced by {@link selectorParser#absoluteLocationPathNoroot}.
	 * @param ctx the parse tree
	 */
	void enterAbsoluteLocationPathNoroot(selectorParser.AbsoluteLocationPathNorootContext ctx);
	/**
	 * Exit a parse tree produced by {@link selectorParser#absoluteLocationPathNoroot}.
	 * @param ctx the parse tree
	 */
	void exitAbsoluteLocationPathNoroot(selectorParser.AbsoluteLocationPathNorootContext ctx);
	/**
	 * Enter a parse tree produced by {@link selectorParser#relativeLocationPath}.
	 * @param ctx the parse tree
	 */
	void enterRelativeLocationPath(selectorParser.RelativeLocationPathContext ctx);
	/**
	 * Exit a parse tree produced by {@link selectorParser#relativeLocationPath}.
	 * @param ctx the parse tree
	 */
	void exitRelativeLocationPath(selectorParser.RelativeLocationPathContext ctx);
	/**
	 * Enter a parse tree produced by {@link selectorParser#step}.
	 * @param ctx the parse tree
	 */
	void enterStep(selectorParser.StepContext ctx);
	/**
	 * Exit a parse tree produced by {@link selectorParser#step}.
	 * @param ctx the parse tree
	 */
	void exitStep(selectorParser.StepContext ctx);
	/**
	 * Enter a parse tree produced by {@link selectorParser#axisSpecifier}.
	 * @param ctx the parse tree
	 */
	void enterAxisSpecifier(selectorParser.AxisSpecifierContext ctx);
	/**
	 * Exit a parse tree produced by {@link selectorParser#axisSpecifier}.
	 * @param ctx the parse tree
	 */
	void exitAxisSpecifier(selectorParser.AxisSpecifierContext ctx);
	/**
	 * Enter a parse tree produced by {@link selectorParser#nodeTest}.
	 * @param ctx the parse tree
	 */
	void enterNodeTest(selectorParser.NodeTestContext ctx);
	/**
	 * Exit a parse tree produced by {@link selectorParser#nodeTest}.
	 * @param ctx the parse tree
	 */
	void exitNodeTest(selectorParser.NodeTestContext ctx);
	/**
	 * Enter a parse tree produced by {@link selectorParser#predicate}.
	 * @param ctx the parse tree
	 */
	void enterPredicate(selectorParser.PredicateContext ctx);
	/**
	 * Exit a parse tree produced by {@link selectorParser#predicate}.
	 * @param ctx the parse tree
	 */
	void exitPredicate(selectorParser.PredicateContext ctx);
	/**
	 * Enter a parse tree produced by {@link selectorParser#abbreviatedStep}.
	 * @param ctx the parse tree
	 */
	void enterAbbreviatedStep(selectorParser.AbbreviatedStepContext ctx);
	/**
	 * Exit a parse tree produced by {@link selectorParser#abbreviatedStep}.
	 * @param ctx the parse tree
	 */
	void exitAbbreviatedStep(selectorParser.AbbreviatedStepContext ctx);
	/**
	 * Enter a parse tree produced by {@link selectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterExpr(selectorParser.ExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link selectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitExpr(selectorParser.ExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link selectorParser#primaryExpr}.
	 * @param ctx the parse tree
	 */
	void enterPrimaryExpr(selectorParser.PrimaryExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link selectorParser#primaryExpr}.
	 * @param ctx the parse tree
	 */
	void exitPrimaryExpr(selectorParser.PrimaryExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link selectorParser#functionCall}.
	 * @param ctx the parse tree
	 */
	void enterFunctionCall(selectorParser.FunctionCallContext ctx);
	/**
	 * Exit a parse tree produced by {@link selectorParser#functionCall}.
	 * @param ctx the parse tree
	 */
	void exitFunctionCall(selectorParser.FunctionCallContext ctx);
	/**
	 * Enter a parse tree produced by {@link selectorParser#unionExprNoRoot}.
	 * @param ctx the parse tree
	 */
	void enterUnionExprNoRoot(selectorParser.UnionExprNoRootContext ctx);
	/**
	 * Exit a parse tree produced by {@link selectorParser#unionExprNoRoot}.
	 * @param ctx the parse tree
	 */
	void exitUnionExprNoRoot(selectorParser.UnionExprNoRootContext ctx);
	/**
	 * Enter a parse tree produced by {@link selectorParser#pathExprNoRoot}.
	 * @param ctx the parse tree
	 */
	void enterPathExprNoRoot(selectorParser.PathExprNoRootContext ctx);
	/**
	 * Exit a parse tree produced by {@link selectorParser#pathExprNoRoot}.
	 * @param ctx the parse tree
	 */
	void exitPathExprNoRoot(selectorParser.PathExprNoRootContext ctx);
	/**
	 * Enter a parse tree produced by {@link selectorParser#filterExpr}.
	 * @param ctx the parse tree
	 */
	void enterFilterExpr(selectorParser.FilterExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link selectorParser#filterExpr}.
	 * @param ctx the parse tree
	 */
	void exitFilterExpr(selectorParser.FilterExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link selectorParser#orExpr}.
	 * @param ctx the parse tree
	 */
	void enterOrExpr(selectorParser.OrExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link selectorParser#orExpr}.
	 * @param ctx the parse tree
	 */
	void exitOrExpr(selectorParser.OrExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link selectorParser#andExpr}.
	 * @param ctx the parse tree
	 */
	void enterAndExpr(selectorParser.AndExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link selectorParser#andExpr}.
	 * @param ctx the parse tree
	 */
	void exitAndExpr(selectorParser.AndExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link selectorParser#equalityExpr}.
	 * @param ctx the parse tree
	 */
	void enterEqualityExpr(selectorParser.EqualityExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link selectorParser#equalityExpr}.
	 * @param ctx the parse tree
	 */
	void exitEqualityExpr(selectorParser.EqualityExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link selectorParser#relationalExpr}.
	 * @param ctx the parse tree
	 */
	void enterRelationalExpr(selectorParser.RelationalExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link selectorParser#relationalExpr}.
	 * @param ctx the parse tree
	 */
	void exitRelationalExpr(selectorParser.RelationalExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link selectorParser#additiveExpr}.
	 * @param ctx the parse tree
	 */
	void enterAdditiveExpr(selectorParser.AdditiveExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link selectorParser#additiveExpr}.
	 * @param ctx the parse tree
	 */
	void exitAdditiveExpr(selectorParser.AdditiveExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link selectorParser#multiplicativeExpr}.
	 * @param ctx the parse tree
	 */
	void enterMultiplicativeExpr(selectorParser.MultiplicativeExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link selectorParser#multiplicativeExpr}.
	 * @param ctx the parse tree
	 */
	void exitMultiplicativeExpr(selectorParser.MultiplicativeExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link selectorParser#unaryExprNoRoot}.
	 * @param ctx the parse tree
	 */
	void enterUnaryExprNoRoot(selectorParser.UnaryExprNoRootContext ctx);
	/**
	 * Exit a parse tree produced by {@link selectorParser#unaryExprNoRoot}.
	 * @param ctx the parse tree
	 */
	void exitUnaryExprNoRoot(selectorParser.UnaryExprNoRootContext ctx);
	/**
	 * Enter a parse tree produced by {@link selectorParser#qName}.
	 * @param ctx the parse tree
	 */
	void enterQName(selectorParser.QNameContext ctx);
	/**
	 * Exit a parse tree produced by {@link selectorParser#qName}.
	 * @param ctx the parse tree
	 */
	void exitQName(selectorParser.QNameContext ctx);
	/**
	 * Enter a parse tree produced by {@link selectorParser#functionName}.
	 * @param ctx the parse tree
	 */
	void enterFunctionName(selectorParser.FunctionNameContext ctx);
	/**
	 * Exit a parse tree produced by {@link selectorParser#functionName}.
	 * @param ctx the parse tree
	 */
	void exitFunctionName(selectorParser.FunctionNameContext ctx);
	/**
	 * Enter a parse tree produced by {@link selectorParser#variableReference}.
	 * @param ctx the parse tree
	 */
	void enterVariableReference(selectorParser.VariableReferenceContext ctx);
	/**
	 * Exit a parse tree produced by {@link selectorParser#variableReference}.
	 * @param ctx the parse tree
	 */
	void exitVariableReference(selectorParser.VariableReferenceContext ctx);
	/**
	 * Enter a parse tree produced by {@link selectorParser#nameTest}.
	 * @param ctx the parse tree
	 */
	void enterNameTest(selectorParser.NameTestContext ctx);
	/**
	 * Exit a parse tree produced by {@link selectorParser#nameTest}.
	 * @param ctx the parse tree
	 */
	void exitNameTest(selectorParser.NameTestContext ctx);
	/**
	 * Enter a parse tree produced by {@link selectorParser#nCName}.
	 * @param ctx the parse tree
	 */
	void enterNCName(selectorParser.NCNameContext ctx);
	/**
	 * Exit a parse tree produced by {@link selectorParser#nCName}.
	 * @param ctx the parse tree
	 */
	void exitNCName(selectorParser.NCNameContext ctx);
}