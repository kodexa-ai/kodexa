// Generated from /Users/pdodds/src/kodexa/kodexa/resources/KodexaSelector.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link KodexaSelectorParser}.
 */
public interface KodexaSelectorListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link KodexaSelectorParser#xpath}.
	 * @param ctx the parse tree
	 */
	void enterXpath(KodexaSelectorParser.XpathContext ctx);
	/**
	 * Exit a parse tree produced by {@link KodexaSelectorParser#xpath}.
	 * @param ctx the parse tree
	 */
	void exitXpath(KodexaSelectorParser.XpathContext ctx);
	/**
	 * Enter a parse tree produced by the {@code equalsExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterEqualsExpr(KodexaSelectorParser.EqualsExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code equalsExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitEqualsExpr(KodexaSelectorParser.EqualsExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code subtractExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterSubtractExpr(KodexaSelectorParser.SubtractExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code subtractExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitSubtractExpr(KodexaSelectorParser.SubtractExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code divideExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterDivideExpr(KodexaSelectorParser.DivideExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code divideExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitDivideExpr(KodexaSelectorParser.DivideExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code intersectExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterIntersectExpr(KodexaSelectorParser.IntersectExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code intersectExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitIntersectExpr(KodexaSelectorParser.IntersectExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code moduloExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterModuloExpr(KodexaSelectorParser.ModuloExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code moduloExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitModuloExpr(KodexaSelectorParser.ModuloExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code directNameTest}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterDirectNameTest(KodexaSelectorParser.DirectNameTestContext ctx);
	/**
	 * Exit a parse tree produced by the {@code directNameTest}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitDirectNameTest(KodexaSelectorParser.DirectNameTestContext ctx);
	/**
	 * Enter a parse tree produced by the {@code orExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterOrExpr(KodexaSelectorParser.OrExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code orExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitOrExpr(KodexaSelectorParser.OrExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code absolutePathExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterAbsolutePathExpr(KodexaSelectorParser.AbsolutePathExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code absolutePathExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitAbsolutePathExpr(KodexaSelectorParser.AbsolutePathExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code multiplyExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterMultiplyExpr(KodexaSelectorParser.MultiplyExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code multiplyExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitMultiplyExpr(KodexaSelectorParser.MultiplyExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code unionExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterUnionExpr(KodexaSelectorParser.UnionExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code unionExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitUnionExpr(KodexaSelectorParser.UnionExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code relationalExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterRelationalExpr(KodexaSelectorParser.RelationalExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code relationalExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitRelationalExpr(KodexaSelectorParser.RelationalExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code pipelineExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterPipelineExpr(KodexaSelectorParser.PipelineExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code pipelineExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitPipelineExpr(KodexaSelectorParser.PipelineExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code relativePathExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterRelativePathExpr(KodexaSelectorParser.RelativePathExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code relativePathExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitRelativePathExpr(KodexaSelectorParser.RelativePathExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code rootNameTest}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterRootNameTest(KodexaSelectorParser.RootNameTestContext ctx);
	/**
	 * Exit a parse tree produced by the {@code rootNameTest}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitRootNameTest(KodexaSelectorParser.RootNameTestContext ctx);
	/**
	 * Enter a parse tree produced by the {@code unaryMinusExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterUnaryMinusExpr(KodexaSelectorParser.UnaryMinusExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code unaryMinusExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitUnaryMinusExpr(KodexaSelectorParser.UnaryMinusExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code abbrevAbsPathExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterAbbrevAbsPathExpr(KodexaSelectorParser.AbbrevAbsPathExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code abbrevAbsPathExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitAbbrevAbsPathExpr(KodexaSelectorParser.AbbrevAbsPathExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code addExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterAddExpr(KodexaSelectorParser.AddExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code addExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitAddExpr(KodexaSelectorParser.AddExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code filterExpression}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterFilterExpression(KodexaSelectorParser.FilterExpressionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code filterExpression}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitFilterExpression(KodexaSelectorParser.FilterExpressionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code pathBinaryExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterPathBinaryExpr(KodexaSelectorParser.PathBinaryExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code pathBinaryExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitPathBinaryExpr(KodexaSelectorParser.PathBinaryExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code andExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterAndExpr(KodexaSelectorParser.AndExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code andExpr}
	 * labeled alternative in {@link KodexaSelectorParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitAndExpr(KodexaSelectorParser.AndExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code rootOnly}
	 * labeled alternative in {@link KodexaSelectorParser#absoluteLocationPath}.
	 * @param ctx the parse tree
	 */
	void enterRootOnly(KodexaSelectorParser.RootOnlyContext ctx);
	/**
	 * Exit a parse tree produced by the {@code rootOnly}
	 * labeled alternative in {@link KodexaSelectorParser#absoluteLocationPath}.
	 * @param ctx the parse tree
	 */
	void exitRootOnly(KodexaSelectorParser.RootOnlyContext ctx);
	/**
	 * Enter a parse tree produced by the {@code rootPath}
	 * labeled alternative in {@link KodexaSelectorParser#absoluteLocationPath}.
	 * @param ctx the parse tree
	 */
	void enterRootPath(KodexaSelectorParser.RootPathContext ctx);
	/**
	 * Exit a parse tree produced by the {@code rootPath}
	 * labeled alternative in {@link KodexaSelectorParser#absoluteLocationPath}.
	 * @param ctx the parse tree
	 */
	void exitRootPath(KodexaSelectorParser.RootPathContext ctx);
	/**
	 * Enter a parse tree produced by {@link KodexaSelectorParser#abbreviatedAbsoluteLocationPath}.
	 * @param ctx the parse tree
	 */
	void enterAbbreviatedAbsoluteLocationPath(KodexaSelectorParser.AbbreviatedAbsoluteLocationPathContext ctx);
	/**
	 * Exit a parse tree produced by {@link KodexaSelectorParser#abbreviatedAbsoluteLocationPath}.
	 * @param ctx the parse tree
	 */
	void exitAbbreviatedAbsoluteLocationPath(KodexaSelectorParser.AbbreviatedAbsoluteLocationPathContext ctx);
	/**
	 * Enter a parse tree produced by the {@code singleStep}
	 * labeled alternative in {@link KodexaSelectorParser#relativeLocationPath}.
	 * @param ctx the parse tree
	 */
	void enterSingleStep(KodexaSelectorParser.SingleStepContext ctx);
	/**
	 * Exit a parse tree produced by the {@code singleStep}
	 * labeled alternative in {@link KodexaSelectorParser#relativeLocationPath}.
	 * @param ctx the parse tree
	 */
	void exitSingleStep(KodexaSelectorParser.SingleStepContext ctx);
	/**
	 * Enter a parse tree produced by the {@code pathStep}
	 * labeled alternative in {@link KodexaSelectorParser#relativeLocationPath}.
	 * @param ctx the parse tree
	 */
	void enterPathStep(KodexaSelectorParser.PathStepContext ctx);
	/**
	 * Exit a parse tree produced by the {@code pathStep}
	 * labeled alternative in {@link KodexaSelectorParser#relativeLocationPath}.
	 * @param ctx the parse tree
	 */
	void exitPathStep(KodexaSelectorParser.PathStepContext ctx);
	/**
	 * Enter a parse tree produced by the {@code abbrevPathStep}
	 * labeled alternative in {@link KodexaSelectorParser#relativeLocationPath}.
	 * @param ctx the parse tree
	 */
	void enterAbbrevPathStep(KodexaSelectorParser.AbbrevPathStepContext ctx);
	/**
	 * Exit a parse tree produced by the {@code abbrevPathStep}
	 * labeled alternative in {@link KodexaSelectorParser#relativeLocationPath}.
	 * @param ctx the parse tree
	 */
	void exitAbbrevPathStep(KodexaSelectorParser.AbbrevPathStepContext ctx);
	/**
	 * Enter a parse tree produced by the {@code nodeTestStep}
	 * labeled alternative in {@link KodexaSelectorParser#step}.
	 * @param ctx the parse tree
	 */
	void enterNodeTestStep(KodexaSelectorParser.NodeTestStepContext ctx);
	/**
	 * Exit a parse tree produced by the {@code nodeTestStep}
	 * labeled alternative in {@link KodexaSelectorParser#step}.
	 * @param ctx the parse tree
	 */
	void exitNodeTestStep(KodexaSelectorParser.NodeTestStepContext ctx);
	/**
	 * Enter a parse tree produced by the {@code nodeTestPredStep}
	 * labeled alternative in {@link KodexaSelectorParser#step}.
	 * @param ctx the parse tree
	 */
	void enterNodeTestPredStep(KodexaSelectorParser.NodeTestPredStepContext ctx);
	/**
	 * Exit a parse tree produced by the {@code nodeTestPredStep}
	 * labeled alternative in {@link KodexaSelectorParser#step}.
	 * @param ctx the parse tree
	 */
	void exitNodeTestPredStep(KodexaSelectorParser.NodeTestPredStepContext ctx);
	/**
	 * Enter a parse tree produced by the {@code axisNodeTestStep}
	 * labeled alternative in {@link KodexaSelectorParser#step}.
	 * @param ctx the parse tree
	 */
	void enterAxisNodeTestStep(KodexaSelectorParser.AxisNodeTestStepContext ctx);
	/**
	 * Exit a parse tree produced by the {@code axisNodeTestStep}
	 * labeled alternative in {@link KodexaSelectorParser#step}.
	 * @param ctx the parse tree
	 */
	void exitAxisNodeTestStep(KodexaSelectorParser.AxisNodeTestStepContext ctx);
	/**
	 * Enter a parse tree produced by the {@code axisNodeTestPredStep}
	 * labeled alternative in {@link KodexaSelectorParser#step}.
	 * @param ctx the parse tree
	 */
	void enterAxisNodeTestPredStep(KodexaSelectorParser.AxisNodeTestPredStepContext ctx);
	/**
	 * Exit a parse tree produced by the {@code axisNodeTestPredStep}
	 * labeled alternative in {@link KodexaSelectorParser#step}.
	 * @param ctx the parse tree
	 */
	void exitAxisNodeTestPredStep(KodexaSelectorParser.AxisNodeTestPredStepContext ctx);
	/**
	 * Enter a parse tree produced by the {@code selfStep}
	 * labeled alternative in {@link KodexaSelectorParser#step}.
	 * @param ctx the parse tree
	 */
	void enterSelfStep(KodexaSelectorParser.SelfStepContext ctx);
	/**
	 * Exit a parse tree produced by the {@code selfStep}
	 * labeled alternative in {@link KodexaSelectorParser#step}.
	 * @param ctx the parse tree
	 */
	void exitSelfStep(KodexaSelectorParser.SelfStepContext ctx);
	/**
	 * Enter a parse tree produced by the {@code parentStep}
	 * labeled alternative in {@link KodexaSelectorParser#step}.
	 * @param ctx the parse tree
	 */
	void enterParentStep(KodexaSelectorParser.ParentStepContext ctx);
	/**
	 * Exit a parse tree produced by the {@code parentStep}
	 * labeled alternative in {@link KodexaSelectorParser#step}.
	 * @param ctx the parse tree
	 */
	void exitParentStep(KodexaSelectorParser.ParentStepContext ctx);
	/**
	 * Enter a parse tree produced by the {@code fullAxis}
	 * labeled alternative in {@link KodexaSelectorParser#axisSpecifier}.
	 * @param ctx the parse tree
	 */
	void enterFullAxis(KodexaSelectorParser.FullAxisContext ctx);
	/**
	 * Exit a parse tree produced by the {@code fullAxis}
	 * labeled alternative in {@link KodexaSelectorParser#axisSpecifier}.
	 * @param ctx the parse tree
	 */
	void exitFullAxis(KodexaSelectorParser.FullAxisContext ctx);
	/**
	 * Enter a parse tree produced by the {@code attrAxis}
	 * labeled alternative in {@link KodexaSelectorParser#axisSpecifier}.
	 * @param ctx the parse tree
	 */
	void enterAttrAxis(KodexaSelectorParser.AttrAxisContext ctx);
	/**
	 * Exit a parse tree produced by the {@code attrAxis}
	 * labeled alternative in {@link KodexaSelectorParser#axisSpecifier}.
	 * @param ctx the parse tree
	 */
	void exitAttrAxis(KodexaSelectorParser.AttrAxisContext ctx);
	/**
	 * Enter a parse tree produced by the {@code nameTestNode}
	 * labeled alternative in {@link KodexaSelectorParser#nodeTest}.
	 * @param ctx the parse tree
	 */
	void enterNameTestNode(KodexaSelectorParser.NameTestNodeContext ctx);
	/**
	 * Exit a parse tree produced by the {@code nameTestNode}
	 * labeled alternative in {@link KodexaSelectorParser#nodeTest}.
	 * @param ctx the parse tree
	 */
	void exitNameTestNode(KodexaSelectorParser.NameTestNodeContext ctx);
	/**
	 * Enter a parse tree produced by the {@code nodeTypeTest}
	 * labeled alternative in {@link KodexaSelectorParser#nodeTest}.
	 * @param ctx the parse tree
	 */
	void enterNodeTypeTest(KodexaSelectorParser.NodeTypeTestContext ctx);
	/**
	 * Exit a parse tree produced by the {@code nodeTypeTest}
	 * labeled alternative in {@link KodexaSelectorParser#nodeTest}.
	 * @param ctx the parse tree
	 */
	void exitNodeTypeTest(KodexaSelectorParser.NodeTypeTestContext ctx);
	/**
	 * Enter a parse tree produced by the {@code nodeTypeLiteralTest}
	 * labeled alternative in {@link KodexaSelectorParser#nodeTest}.
	 * @param ctx the parse tree
	 */
	void enterNodeTypeLiteralTest(KodexaSelectorParser.NodeTypeLiteralTestContext ctx);
	/**
	 * Exit a parse tree produced by the {@code nodeTypeLiteralTest}
	 * labeled alternative in {@link KodexaSelectorParser#nodeTest}.
	 * @param ctx the parse tree
	 */
	void exitNodeTypeLiteralTest(KodexaSelectorParser.NodeTypeLiteralTestContext ctx);
	/**
	 * Enter a parse tree produced by the {@code anyNameTest}
	 * labeled alternative in {@link KodexaSelectorParser#nameTest}.
	 * @param ctx the parse tree
	 */
	void enterAnyNameTest(KodexaSelectorParser.AnyNameTestContext ctx);
	/**
	 * Exit a parse tree produced by the {@code anyNameTest}
	 * labeled alternative in {@link KodexaSelectorParser#nameTest}.
	 * @param ctx the parse tree
	 */
	void exitAnyNameTest(KodexaSelectorParser.AnyNameTestContext ctx);
	/**
	 * Enter a parse tree produced by the {@code prefixedAnyNameTest}
	 * labeled alternative in {@link KodexaSelectorParser#nameTest}.
	 * @param ctx the parse tree
	 */
	void enterPrefixedAnyNameTest(KodexaSelectorParser.PrefixedAnyNameTestContext ctx);
	/**
	 * Exit a parse tree produced by the {@code prefixedAnyNameTest}
	 * labeled alternative in {@link KodexaSelectorParser#nameTest}.
	 * @param ctx the parse tree
	 */
	void exitPrefixedAnyNameTest(KodexaSelectorParser.PrefixedAnyNameTestContext ctx);
	/**
	 * Enter a parse tree produced by the {@code qNameTest}
	 * labeled alternative in {@link KodexaSelectorParser#nameTest}.
	 * @param ctx the parse tree
	 */
	void enterQNameTest(KodexaSelectorParser.QNameTestContext ctx);
	/**
	 * Exit a parse tree produced by the {@code qNameTest}
	 * labeled alternative in {@link KodexaSelectorParser#nameTest}.
	 * @param ctx the parse tree
	 */
	void exitQNameTest(KodexaSelectorParser.QNameTestContext ctx);
	/**
	 * Enter a parse tree produced by the {@code prefixedName}
	 * labeled alternative in {@link KodexaSelectorParser#qName}.
	 * @param ctx the parse tree
	 */
	void enterPrefixedName(KodexaSelectorParser.PrefixedNameContext ctx);
	/**
	 * Exit a parse tree produced by the {@code prefixedName}
	 * labeled alternative in {@link KodexaSelectorParser#qName}.
	 * @param ctx the parse tree
	 */
	void exitPrefixedName(KodexaSelectorParser.PrefixedNameContext ctx);
	/**
	 * Enter a parse tree produced by the {@code simpleName}
	 * labeled alternative in {@link KodexaSelectorParser#qName}.
	 * @param ctx the parse tree
	 */
	void enterSimpleName(KodexaSelectorParser.SimpleNameContext ctx);
	/**
	 * Exit a parse tree produced by the {@code simpleName}
	 * labeled alternative in {@link KodexaSelectorParser#qName}.
	 * @param ctx the parse tree
	 */
	void exitSimpleName(KodexaSelectorParser.SimpleNameContext ctx);
	/**
	 * Enter a parse tree produced by the {@code prefixedFuncName}
	 * labeled alternative in {@link KodexaSelectorParser#funcQName}.
	 * @param ctx the parse tree
	 */
	void enterPrefixedFuncName(KodexaSelectorParser.PrefixedFuncNameContext ctx);
	/**
	 * Exit a parse tree produced by the {@code prefixedFuncName}
	 * labeled alternative in {@link KodexaSelectorParser#funcQName}.
	 * @param ctx the parse tree
	 */
	void exitPrefixedFuncName(KodexaSelectorParser.PrefixedFuncNameContext ctx);
	/**
	 * Enter a parse tree produced by the {@code simpleFuncName}
	 * labeled alternative in {@link KodexaSelectorParser#funcQName}.
	 * @param ctx the parse tree
	 */
	void enterSimpleFuncName(KodexaSelectorParser.SimpleFuncNameContext ctx);
	/**
	 * Exit a parse tree produced by the {@code simpleFuncName}
	 * labeled alternative in {@link KodexaSelectorParser#funcQName}.
	 * @param ctx the parse tree
	 */
	void exitSimpleFuncName(KodexaSelectorParser.SimpleFuncNameContext ctx);
	/**
	 * Enter a parse tree produced by the {@code funcCallFilter}
	 * labeled alternative in {@link KodexaSelectorParser#filterExpr}.
	 * @param ctx the parse tree
	 */
	void enterFuncCallFilter(KodexaSelectorParser.FuncCallFilterContext ctx);
	/**
	 * Exit a parse tree produced by the {@code funcCallFilter}
	 * labeled alternative in {@link KodexaSelectorParser#filterExpr}.
	 * @param ctx the parse tree
	 */
	void exitFuncCallFilter(KodexaSelectorParser.FuncCallFilterContext ctx);
	/**
	 * Enter a parse tree produced by the {@code groupedFilter}
	 * labeled alternative in {@link KodexaSelectorParser#filterExpr}.
	 * @param ctx the parse tree
	 */
	void enterGroupedFilter(KodexaSelectorParser.GroupedFilterContext ctx);
	/**
	 * Exit a parse tree produced by the {@code groupedFilter}
	 * labeled alternative in {@link KodexaSelectorParser#filterExpr}.
	 * @param ctx the parse tree
	 */
	void exitGroupedFilter(KodexaSelectorParser.GroupedFilterContext ctx);
	/**
	 * Enter a parse tree produced by the {@code predicatedFilter}
	 * labeled alternative in {@link KodexaSelectorParser#filterExpr}.
	 * @param ctx the parse tree
	 */
	void enterPredicatedFilter(KodexaSelectorParser.PredicatedFilterContext ctx);
	/**
	 * Exit a parse tree produced by the {@code predicatedFilter}
	 * labeled alternative in {@link KodexaSelectorParser#filterExpr}.
	 * @param ctx the parse tree
	 */
	void exitPredicatedFilter(KodexaSelectorParser.PredicatedFilterContext ctx);
	/**
	 * Enter a parse tree produced by the {@code numberFilter}
	 * labeled alternative in {@link KodexaSelectorParser#filterExpr}.
	 * @param ctx the parse tree
	 */
	void enterNumberFilter(KodexaSelectorParser.NumberFilterContext ctx);
	/**
	 * Exit a parse tree produced by the {@code numberFilter}
	 * labeled alternative in {@link KodexaSelectorParser#filterExpr}.
	 * @param ctx the parse tree
	 */
	void exitNumberFilter(KodexaSelectorParser.NumberFilterContext ctx);
	/**
	 * Enter a parse tree produced by the {@code varRefFilter}
	 * labeled alternative in {@link KodexaSelectorParser#filterExpr}.
	 * @param ctx the parse tree
	 */
	void enterVarRefFilter(KodexaSelectorParser.VarRefFilterContext ctx);
	/**
	 * Exit a parse tree produced by the {@code varRefFilter}
	 * labeled alternative in {@link KodexaSelectorParser#filterExpr}.
	 * @param ctx the parse tree
	 */
	void exitVarRefFilter(KodexaSelectorParser.VarRefFilterContext ctx);
	/**
	 * Enter a parse tree produced by the {@code literalFilter}
	 * labeled alternative in {@link KodexaSelectorParser#filterExpr}.
	 * @param ctx the parse tree
	 */
	void enterLiteralFilter(KodexaSelectorParser.LiteralFilterContext ctx);
	/**
	 * Exit a parse tree produced by the {@code literalFilter}
	 * labeled alternative in {@link KodexaSelectorParser#filterExpr}.
	 * @param ctx the parse tree
	 */
	void exitLiteralFilter(KodexaSelectorParser.LiteralFilterContext ctx);
	/**
	 * Enter a parse tree produced by the {@code singlePredicate}
	 * labeled alternative in {@link KodexaSelectorParser#predicateList}.
	 * @param ctx the parse tree
	 */
	void enterSinglePredicate(KodexaSelectorParser.SinglePredicateContext ctx);
	/**
	 * Exit a parse tree produced by the {@code singlePredicate}
	 * labeled alternative in {@link KodexaSelectorParser#predicateList}.
	 * @param ctx the parse tree
	 */
	void exitSinglePredicate(KodexaSelectorParser.SinglePredicateContext ctx);
	/**
	 * Enter a parse tree produced by the {@code multiplePredicate}
	 * labeled alternative in {@link KodexaSelectorParser#predicateList}.
	 * @param ctx the parse tree
	 */
	void enterMultiplePredicate(KodexaSelectorParser.MultiplePredicateContext ctx);
	/**
	 * Exit a parse tree produced by the {@code multiplePredicate}
	 * labeled alternative in {@link KodexaSelectorParser#predicateList}.
	 * @param ctx the parse tree
	 */
	void exitMultiplePredicate(KodexaSelectorParser.MultiplePredicateContext ctx);
	/**
	 * Enter a parse tree produced by {@link KodexaSelectorParser#predicate}.
	 * @param ctx the parse tree
	 */
	void enterPredicate(KodexaSelectorParser.PredicateContext ctx);
	/**
	 * Exit a parse tree produced by {@link KodexaSelectorParser#predicate}.
	 * @param ctx the parse tree
	 */
	void exitPredicate(KodexaSelectorParser.PredicateContext ctx);
	/**
	 * Enter a parse tree produced by {@link KodexaSelectorParser#variableReference}.
	 * @param ctx the parse tree
	 */
	void enterVariableReference(KodexaSelectorParser.VariableReferenceContext ctx);
	/**
	 * Exit a parse tree produced by {@link KodexaSelectorParser#variableReference}.
	 * @param ctx the parse tree
	 */
	void exitVariableReference(KodexaSelectorParser.VariableReferenceContext ctx);
	/**
	 * Enter a parse tree produced by {@link KodexaSelectorParser#number}.
	 * @param ctx the parse tree
	 */
	void enterNumber(KodexaSelectorParser.NumberContext ctx);
	/**
	 * Exit a parse tree produced by {@link KodexaSelectorParser#number}.
	 * @param ctx the parse tree
	 */
	void exitNumber(KodexaSelectorParser.NumberContext ctx);
	/**
	 * Enter a parse tree produced by {@link KodexaSelectorParser#functionCall}.
	 * @param ctx the parse tree
	 */
	void enterFunctionCall(KodexaSelectorParser.FunctionCallContext ctx);
	/**
	 * Exit a parse tree produced by {@link KodexaSelectorParser#functionCall}.
	 * @param ctx the parse tree
	 */
	void exitFunctionCall(KodexaSelectorParser.FunctionCallContext ctx);
	/**
	 * Enter a parse tree produced by the {@code emptyArgs}
	 * labeled alternative in {@link KodexaSelectorParser#formalArguments}.
	 * @param ctx the parse tree
	 */
	void enterEmptyArgs(KodexaSelectorParser.EmptyArgsContext ctx);
	/**
	 * Exit a parse tree produced by the {@code emptyArgs}
	 * labeled alternative in {@link KodexaSelectorParser#formalArguments}.
	 * @param ctx the parse tree
	 */
	void exitEmptyArgs(KodexaSelectorParser.EmptyArgsContext ctx);
	/**
	 * Enter a parse tree produced by the {@code argsList}
	 * labeled alternative in {@link KodexaSelectorParser#formalArguments}.
	 * @param ctx the parse tree
	 */
	void enterArgsList(KodexaSelectorParser.ArgsListContext ctx);
	/**
	 * Exit a parse tree produced by the {@code argsList}
	 * labeled alternative in {@link KodexaSelectorParser#formalArguments}.
	 * @param ctx the parse tree
	 */
	void exitArgsList(KodexaSelectorParser.ArgsListContext ctx);
	/**
	 * Enter a parse tree produced by the {@code singleArg}
	 * labeled alternative in {@link KodexaSelectorParser#argumentList}.
	 * @param ctx the parse tree
	 */
	void enterSingleArg(KodexaSelectorParser.SingleArgContext ctx);
	/**
	 * Exit a parse tree produced by the {@code singleArg}
	 * labeled alternative in {@link KodexaSelectorParser#argumentList}.
	 * @param ctx the parse tree
	 */
	void exitSingleArg(KodexaSelectorParser.SingleArgContext ctx);
	/**
	 * Enter a parse tree produced by the {@code multipleArgs}
	 * labeled alternative in {@link KodexaSelectorParser#argumentList}.
	 * @param ctx the parse tree
	 */
	void enterMultipleArgs(KodexaSelectorParser.MultipleArgsContext ctx);
	/**
	 * Exit a parse tree produced by the {@code multipleArgs}
	 * labeled alternative in {@link KodexaSelectorParser#argumentList}.
	 * @param ctx the parse tree
	 */
	void exitMultipleArgs(KodexaSelectorParser.MultipleArgsContext ctx);
	/**
	 * Enter a parse tree produced by {@link KodexaSelectorParser#pathSep}.
	 * @param ctx the parse tree
	 */
	void enterPathSep(KodexaSelectorParser.PathSepContext ctx);
	/**
	 * Exit a parse tree produced by {@link KodexaSelectorParser#pathSep}.
	 * @param ctx the parse tree
	 */
	void exitPathSep(KodexaSelectorParser.PathSepContext ctx);
}