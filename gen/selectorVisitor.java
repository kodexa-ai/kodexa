// Generated from /Users/pdodds/src/kodexa/kodexa/resources/selector.g4 by ANTLR 4.9.1
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link selectorParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface selectorVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link selectorParser#main}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMain(selectorParser.MainContext ctx);
	/**
	 * Visit a parse tree produced by {@link selectorParser#locationPath}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLocationPath(selectorParser.LocationPathContext ctx);
	/**
	 * Visit a parse tree produced by {@link selectorParser#absoluteLocationPathNoroot}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAbsoluteLocationPathNoroot(selectorParser.AbsoluteLocationPathNorootContext ctx);
	/**
	 * Visit a parse tree produced by {@link selectorParser#relativeLocationPath}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRelativeLocationPath(selectorParser.RelativeLocationPathContext ctx);
	/**
	 * Visit a parse tree produced by {@link selectorParser#step}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitStep(selectorParser.StepContext ctx);
	/**
	 * Visit a parse tree produced by {@link selectorParser#axisSpecifier}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAxisSpecifier(selectorParser.AxisSpecifierContext ctx);
	/**
	 * Visit a parse tree produced by {@link selectorParser#nodeTest}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNodeTest(selectorParser.NodeTestContext ctx);
	/**
	 * Visit a parse tree produced by {@link selectorParser#predicate}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPredicate(selectorParser.PredicateContext ctx);
	/**
	 * Visit a parse tree produced by {@link selectorParser#abbreviatedStep}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAbbreviatedStep(selectorParser.AbbreviatedStepContext ctx);
	/**
	 * Visit a parse tree produced by {@link selectorParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitExpr(selectorParser.ExprContext ctx);
	/**
	 * Visit a parse tree produced by {@link selectorParser#primaryExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPrimaryExpr(selectorParser.PrimaryExprContext ctx);
	/**
	 * Visit a parse tree produced by {@link selectorParser#functionCall}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFunctionCall(selectorParser.FunctionCallContext ctx);
	/**
	 * Visit a parse tree produced by {@link selectorParser#unionExprNoRoot}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnionExprNoRoot(selectorParser.UnionExprNoRootContext ctx);
	/**
	 * Visit a parse tree produced by {@link selectorParser#pathExprNoRoot}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPathExprNoRoot(selectorParser.PathExprNoRootContext ctx);
	/**
	 * Visit a parse tree produced by {@link selectorParser#filterExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFilterExpr(selectorParser.FilterExprContext ctx);
	/**
	 * Visit a parse tree produced by {@link selectorParser#orExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitOrExpr(selectorParser.OrExprContext ctx);
	/**
	 * Visit a parse tree produced by {@link selectorParser#andExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAndExpr(selectorParser.AndExprContext ctx);
	/**
	 * Visit a parse tree produced by {@link selectorParser#equalityExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEqualityExpr(selectorParser.EqualityExprContext ctx);
	/**
	 * Visit a parse tree produced by {@link selectorParser#relationalExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRelationalExpr(selectorParser.RelationalExprContext ctx);
	/**
	 * Visit a parse tree produced by {@link selectorParser#additiveExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAdditiveExpr(selectorParser.AdditiveExprContext ctx);
	/**
	 * Visit a parse tree produced by {@link selectorParser#multiplicativeExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMultiplicativeExpr(selectorParser.MultiplicativeExprContext ctx);
	/**
	 * Visit a parse tree produced by {@link selectorParser#unaryExprNoRoot}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnaryExprNoRoot(selectorParser.UnaryExprNoRootContext ctx);
	/**
	 * Visit a parse tree produced by {@link selectorParser#qName}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitQName(selectorParser.QNameContext ctx);
	/**
	 * Visit a parse tree produced by {@link selectorParser#functionName}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFunctionName(selectorParser.FunctionNameContext ctx);
	/**
	 * Visit a parse tree produced by {@link selectorParser#variableReference}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitVariableReference(selectorParser.VariableReferenceContext ctx);
	/**
	 * Visit a parse tree produced by {@link selectorParser#nameTest}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNameTest(selectorParser.NameTestContext ctx);
	/**
	 * Visit a parse tree produced by {@link selectorParser#nCName}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNCName(selectorParser.NCNameContext ctx);
}