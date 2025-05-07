// Generated from /Users/pdodds/src/kodexa/kodexa/resources/KodexaSelector.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue"})
public class KodexaSelectorParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.13.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		OR=1, AND=2, DIV=3, MOD=4, INTERSECT=5, PIPELINE=6, PATH_SEP=7, ABBREV_PATH_SEP=8, 
		ABBREV_STEP_SELF=9, ABBREV_STEP_PARENT=10, AXIS_SEP=11, ABBREV_AXIS_AT=12, 
		LPAREN=13, RPAREN=14, LBRACKET=15, RBRACKET=16, UNION=17, EQUALS=18, REL_OP=19, 
		PLUS=20, MINUS=21, STAR=22, COMMA=23, COLON=24, DOLLAR=25, TRUE=26, FALSE=27, 
		FUNCTION_NAME=28, LITERAL=29, FLOAT=30, INTEGER=31, NODETYPE=32, NCNAME=33, 
		FUNCNAME=34, AXISNAME=35, WS=36;
	public static final int
		RULE_xpath = 0, RULE_expr = 1, RULE_absoluteLocationPath = 2, RULE_abbreviatedAbsoluteLocationPath = 3, 
		RULE_relativeLocationPath = 4, RULE_step = 5, RULE_axisSpecifier = 6, 
		RULE_nodeTest = 7, RULE_nameTest = 8, RULE_qName = 9, RULE_filterExpr = 10, 
		RULE_predicateList = 11, RULE_predicate = 12, RULE_variableReference = 13, 
		RULE_number = 14, RULE_booleanLiteral = 15, RULE_functionCall = 16, RULE_builtInFunctionCall = 17, 
		RULE_funcQName = 18, RULE_formalArguments = 19, RULE_argumentList = 20, 
		RULE_pathSep = 21;
	private static String[] makeRuleNames() {
		return new String[] {
			"xpath", "expr", "absoluteLocationPath", "abbreviatedAbsoluteLocationPath", 
			"relativeLocationPath", "step", "axisSpecifier", "nodeTest", "nameTest", 
			"qName", "filterExpr", "predicateList", "predicate", "variableReference", 
			"number", "booleanLiteral", "functionCall", "builtInFunctionCall", "funcQName", 
			"formalArguments", "argumentList", "pathSep"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'or'", "'and'", "'div'", "'mod'", "'intersect'", "'stream'", "'/'", 
			"'//'", "'.'", "'..'", "'::'", "'@'", "'('", "')'", "'['", "']'", "'|'", 
			null, null, "'+'", "'-'", "'*'", "','", "':'", "'$'", "'true'", "'false'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "OR", "AND", "DIV", "MOD", "INTERSECT", "PIPELINE", "PATH_SEP", 
			"ABBREV_PATH_SEP", "ABBREV_STEP_SELF", "ABBREV_STEP_PARENT", "AXIS_SEP", 
			"ABBREV_AXIS_AT", "LPAREN", "RPAREN", "LBRACKET", "RBRACKET", "UNION", 
			"EQUALS", "REL_OP", "PLUS", "MINUS", "STAR", "COMMA", "COLON", "DOLLAR", 
			"TRUE", "FALSE", "FUNCTION_NAME", "LITERAL", "FLOAT", "INTEGER", "NODETYPE", 
			"NCNAME", "FUNCNAME", "AXISNAME", "WS"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "KodexaSelector.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public KodexaSelectorParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@SuppressWarnings("CheckReturnValue")
	public static class XpathContext extends ParserRuleContext {
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public XpathContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_xpath; }
	}

	public final XpathContext xpath() throws RecognitionException {
		XpathContext _localctx = new XpathContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_xpath);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(44);
			expr(0);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ExprContext extends ParserRuleContext {
		public ExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_expr; }
	 
		public ExprContext() { }
		public void copyFrom(ExprContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class EqualsExprContext extends ExprContext {
		public List<ExprContext> expr() {
			return getRuleContexts(ExprContext.class);
		}
		public ExprContext expr(int i) {
			return getRuleContext(ExprContext.class,i);
		}
		public TerminalNode EQUALS() { return getToken(KodexaSelectorParser.EQUALS, 0); }
		public EqualsExprContext(ExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SubtractExprContext extends ExprContext {
		public List<ExprContext> expr() {
			return getRuleContexts(ExprContext.class);
		}
		public ExprContext expr(int i) {
			return getRuleContext(ExprContext.class,i);
		}
		public TerminalNode MINUS() { return getToken(KodexaSelectorParser.MINUS, 0); }
		public SubtractExprContext(ExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DivideExprContext extends ExprContext {
		public List<ExprContext> expr() {
			return getRuleContexts(ExprContext.class);
		}
		public ExprContext expr(int i) {
			return getRuleContext(ExprContext.class,i);
		}
		public TerminalNode DIV() { return getToken(KodexaSelectorParser.DIV, 0); }
		public DivideExprContext(ExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class IntersectExprContext extends ExprContext {
		public List<ExprContext> expr() {
			return getRuleContexts(ExprContext.class);
		}
		public ExprContext expr(int i) {
			return getRuleContext(ExprContext.class,i);
		}
		public TerminalNode INTERSECT() { return getToken(KodexaSelectorParser.INTERSECT, 0); }
		public IntersectExprContext(ExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ModuloExprContext extends ExprContext {
		public List<ExprContext> expr() {
			return getRuleContexts(ExprContext.class);
		}
		public ExprContext expr(int i) {
			return getRuleContext(ExprContext.class,i);
		}
		public TerminalNode MOD() { return getToken(KodexaSelectorParser.MOD, 0); }
		public ModuloExprContext(ExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DirectNameTestContext extends ExprContext {
		public NameTestContext nameTest() {
			return getRuleContext(NameTestContext.class,0);
		}
		public DirectNameTestContext(ExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class OrExprContext extends ExprContext {
		public List<ExprContext> expr() {
			return getRuleContexts(ExprContext.class);
		}
		public ExprContext expr(int i) {
			return getRuleContext(ExprContext.class,i);
		}
		public TerminalNode OR() { return getToken(KodexaSelectorParser.OR, 0); }
		public OrExprContext(ExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class AbsolutePathExprContext extends ExprContext {
		public AbsoluteLocationPathContext absoluteLocationPath() {
			return getRuleContext(AbsoluteLocationPathContext.class,0);
		}
		public AbsolutePathExprContext(ExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class FuncCallExprContext extends ExprContext {
		public FunctionCallContext functionCall() {
			return getRuleContext(FunctionCallContext.class,0);
		}
		public FuncCallExprContext(ExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class UnionExprContext extends ExprContext {
		public List<ExprContext> expr() {
			return getRuleContexts(ExprContext.class);
		}
		public ExprContext expr(int i) {
			return getRuleContext(ExprContext.class,i);
		}
		public TerminalNode UNION() { return getToken(KodexaSelectorParser.UNION, 0); }
		public UnionExprContext(ExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class RelationalExprContext extends ExprContext {
		public List<ExprContext> expr() {
			return getRuleContexts(ExprContext.class);
		}
		public ExprContext expr(int i) {
			return getRuleContext(ExprContext.class,i);
		}
		public TerminalNode REL_OP() { return getToken(KodexaSelectorParser.REL_OP, 0); }
		public RelationalExprContext(ExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class PipelineExprContext extends ExprContext {
		public List<ExprContext> expr() {
			return getRuleContexts(ExprContext.class);
		}
		public ExprContext expr(int i) {
			return getRuleContext(ExprContext.class,i);
		}
		public TerminalNode PIPELINE() { return getToken(KodexaSelectorParser.PIPELINE, 0); }
		public PipelineExprContext(ExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class RelativePathExprContext extends ExprContext {
		public RelativeLocationPathContext relativeLocationPath() {
			return getRuleContext(RelativeLocationPathContext.class,0);
		}
		public RelativePathExprContext(ExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class RootNameTestContext extends ExprContext {
		public TerminalNode PATH_SEP() { return getToken(KodexaSelectorParser.PATH_SEP, 0); }
		public NameTestContext nameTest() {
			return getRuleContext(NameTestContext.class,0);
		}
		public RootNameTestContext(ExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class UnaryMinusExprContext extends ExprContext {
		public TerminalNode MINUS() { return getToken(KodexaSelectorParser.MINUS, 0); }
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public UnaryMinusExprContext(ExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class AbbrevAbsPathExprContext extends ExprContext {
		public AbbreviatedAbsoluteLocationPathContext abbreviatedAbsoluteLocationPath() {
			return getRuleContext(AbbreviatedAbsoluteLocationPathContext.class,0);
		}
		public AbbrevAbsPathExprContext(ExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class AddExprContext extends ExprContext {
		public List<ExprContext> expr() {
			return getRuleContexts(ExprContext.class);
		}
		public ExprContext expr(int i) {
			return getRuleContext(ExprContext.class,i);
		}
		public TerminalNode PLUS() { return getToken(KodexaSelectorParser.PLUS, 0); }
		public AddExprContext(ExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class FilterExpressionContext extends ExprContext {
		public FilterExprContext filterExpr() {
			return getRuleContext(FilterExprContext.class,0);
		}
		public FilterExpressionContext(ExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class BooleanLiteralExprContext extends ExprContext {
		public BooleanLiteralContext booleanLiteral() {
			return getRuleContext(BooleanLiteralContext.class,0);
		}
		public BooleanLiteralExprContext(ExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class PathBinaryExprContext extends ExprContext {
		public FilterExprContext filterExpr() {
			return getRuleContext(FilterExprContext.class,0);
		}
		public PathSepContext pathSep() {
			return getRuleContext(PathSepContext.class,0);
		}
		public RelativeLocationPathContext relativeLocationPath() {
			return getRuleContext(RelativeLocationPathContext.class,0);
		}
		public PathBinaryExprContext(ExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class AndExprContext extends ExprContext {
		public List<ExprContext> expr() {
			return getRuleContexts(ExprContext.class);
		}
		public ExprContext expr(int i) {
			return getRuleContext(ExprContext.class,i);
		}
		public TerminalNode AND() { return getToken(KodexaSelectorParser.AND, 0); }
		public AndExprContext(ExprContext ctx) { copyFrom(ctx); }
	}

	public final ExprContext expr() throws RecognitionException {
		return expr(0);
	}

	private ExprContext expr(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		ExprContext _localctx = new ExprContext(_ctx, _parentState);
		ExprContext _prevctx = _localctx;
		int _startState = 2;
		enterRecursionRule(_localctx, 2, RULE_expr, _p);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(62);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,0,_ctx) ) {
			case 1:
				{
				_localctx = new UnaryMinusExprContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;

				setState(47);
				match(MINUS);
				setState(48);
				expr(11);
				}
				break;
			case 2:
				{
				_localctx = new FuncCallExprContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(49);
				functionCall();
				}
				break;
			case 3:
				{
				_localctx = new PathBinaryExprContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(50);
				filterExpr(0);
				setState(51);
				pathSep();
				setState(52);
				relativeLocationPath(0);
				}
				break;
			case 4:
				{
				_localctx = new RelativePathExprContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(54);
				relativeLocationPath(0);
				}
				break;
			case 5:
				{
				_localctx = new AbsolutePathExprContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(55);
				absoluteLocationPath();
				}
				break;
			case 6:
				{
				_localctx = new AbbrevAbsPathExprContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(56);
				abbreviatedAbsoluteLocationPath();
				}
				break;
			case 7:
				{
				_localctx = new FilterExpressionContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(57);
				filterExpr(0);
				}
				break;
			case 8:
				{
				_localctx = new DirectNameTestContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(58);
				nameTest();
				}
				break;
			case 9:
				{
				_localctx = new RootNameTestContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(59);
				match(PATH_SEP);
				setState(60);
				nameTest();
				}
				break;
			case 10:
				{
				_localctx = new BooleanLiteralExprContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(61);
				booleanLiteral();
				}
				break;
			}
			_ctx.stop = _input.LT(-1);
			setState(99);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,2,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					setState(97);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,1,_ctx) ) {
					case 1:
						{
						_localctx = new OrExprContext(new ExprContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_expr);
						setState(64);
						if (!(precpred(_ctx, 21))) throw new FailedPredicateException(this, "precpred(_ctx, 21)");
						setState(65);
						match(OR);
						setState(66);
						expr(22);
						}
						break;
					case 2:
						{
						_localctx = new AndExprContext(new ExprContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_expr);
						setState(67);
						if (!(precpred(_ctx, 20))) throw new FailedPredicateException(this, "precpred(_ctx, 20)");
						setState(68);
						match(AND);
						setState(69);
						expr(21);
						}
						break;
					case 3:
						{
						_localctx = new EqualsExprContext(new ExprContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_expr);
						setState(70);
						if (!(precpred(_ctx, 19))) throw new FailedPredicateException(this, "precpred(_ctx, 19)");
						setState(71);
						match(EQUALS);
						setState(72);
						expr(20);
						}
						break;
					case 4:
						{
						_localctx = new RelationalExprContext(new ExprContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_expr);
						setState(73);
						if (!(precpred(_ctx, 18))) throw new FailedPredicateException(this, "precpred(_ctx, 18)");
						setState(74);
						match(REL_OP);
						setState(75);
						expr(19);
						}
						break;
					case 5:
						{
						_localctx = new AddExprContext(new ExprContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_expr);
						setState(76);
						if (!(precpred(_ctx, 17))) throw new FailedPredicateException(this, "precpred(_ctx, 17)");
						setState(77);
						match(PLUS);
						setState(78);
						expr(18);
						}
						break;
					case 6:
						{
						_localctx = new SubtractExprContext(new ExprContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_expr);
						setState(79);
						if (!(precpred(_ctx, 16))) throw new FailedPredicateException(this, "precpred(_ctx, 16)");
						setState(80);
						match(MINUS);
						setState(81);
						expr(17);
						}
						break;
					case 7:
						{
						_localctx = new DivideExprContext(new ExprContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_expr);
						setState(82);
						if (!(precpred(_ctx, 15))) throw new FailedPredicateException(this, "precpred(_ctx, 15)");
						setState(83);
						match(DIV);
						setState(84);
						expr(16);
						}
						break;
					case 8:
						{
						_localctx = new ModuloExprContext(new ExprContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_expr);
						setState(85);
						if (!(precpred(_ctx, 14))) throw new FailedPredicateException(this, "precpred(_ctx, 14)");
						setState(86);
						match(MOD);
						setState(87);
						expr(15);
						}
						break;
					case 9:
						{
						_localctx = new UnionExprContext(new ExprContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_expr);
						setState(88);
						if (!(precpred(_ctx, 13))) throw new FailedPredicateException(this, "precpred(_ctx, 13)");
						setState(89);
						match(UNION);
						setState(90);
						expr(14);
						}
						break;
					case 10:
						{
						_localctx = new IntersectExprContext(new ExprContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_expr);
						setState(91);
						if (!(precpred(_ctx, 12))) throw new FailedPredicateException(this, "precpred(_ctx, 12)");
						setState(92);
						match(INTERSECT);
						setState(93);
						expr(13);
						}
						break;
					case 11:
						{
						_localctx = new PipelineExprContext(new ExprContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_expr);
						setState(94);
						if (!(precpred(_ctx, 10))) throw new FailedPredicateException(this, "precpred(_ctx, 10)");
						setState(95);
						match(PIPELINE);
						setState(96);
						expr(11);
						}
						break;
					}
					} 
				}
				setState(101);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,2,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class AbsoluteLocationPathContext extends ParserRuleContext {
		public AbsoluteLocationPathContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_absoluteLocationPath; }
	 
		public AbsoluteLocationPathContext() { }
		public void copyFrom(AbsoluteLocationPathContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class RootOnlyContext extends AbsoluteLocationPathContext {
		public TerminalNode PATH_SEP() { return getToken(KodexaSelectorParser.PATH_SEP, 0); }
		public RootOnlyContext(AbsoluteLocationPathContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class RootPathContext extends AbsoluteLocationPathContext {
		public TerminalNode PATH_SEP() { return getToken(KodexaSelectorParser.PATH_SEP, 0); }
		public RelativeLocationPathContext relativeLocationPath() {
			return getRuleContext(RelativeLocationPathContext.class,0);
		}
		public RootPathContext(AbsoluteLocationPathContext ctx) { copyFrom(ctx); }
	}

	public final AbsoluteLocationPathContext absoluteLocationPath() throws RecognitionException {
		AbsoluteLocationPathContext _localctx = new AbsoluteLocationPathContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_absoluteLocationPath);
		try {
			setState(105);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,3,_ctx) ) {
			case 1:
				_localctx = new RootOnlyContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(102);
				match(PATH_SEP);
				}
				break;
			case 2:
				_localctx = new RootPathContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(103);
				match(PATH_SEP);
				setState(104);
				relativeLocationPath(0);
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class AbbreviatedAbsoluteLocationPathContext extends ParserRuleContext {
		public TerminalNode ABBREV_PATH_SEP() { return getToken(KodexaSelectorParser.ABBREV_PATH_SEP, 0); }
		public RelativeLocationPathContext relativeLocationPath() {
			return getRuleContext(RelativeLocationPathContext.class,0);
		}
		public AbbreviatedAbsoluteLocationPathContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_abbreviatedAbsoluteLocationPath; }
	}

	public final AbbreviatedAbsoluteLocationPathContext abbreviatedAbsoluteLocationPath() throws RecognitionException {
		AbbreviatedAbsoluteLocationPathContext _localctx = new AbbreviatedAbsoluteLocationPathContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_abbreviatedAbsoluteLocationPath);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(107);
			match(ABBREV_PATH_SEP);
			setState(108);
			relativeLocationPath(0);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class RelativeLocationPathContext extends ParserRuleContext {
		public RelativeLocationPathContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_relativeLocationPath; }
	 
		public RelativeLocationPathContext() { }
		public void copyFrom(RelativeLocationPathContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SingleStepContext extends RelativeLocationPathContext {
		public StepContext step() {
			return getRuleContext(StepContext.class,0);
		}
		public SingleStepContext(RelativeLocationPathContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class PathStepContext extends RelativeLocationPathContext {
		public RelativeLocationPathContext relativeLocationPath() {
			return getRuleContext(RelativeLocationPathContext.class,0);
		}
		public TerminalNode PATH_SEP() { return getToken(KodexaSelectorParser.PATH_SEP, 0); }
		public StepContext step() {
			return getRuleContext(StepContext.class,0);
		}
		public PathStepContext(RelativeLocationPathContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class AbbrevPathStepContext extends RelativeLocationPathContext {
		public RelativeLocationPathContext relativeLocationPath() {
			return getRuleContext(RelativeLocationPathContext.class,0);
		}
		public TerminalNode ABBREV_PATH_SEP() { return getToken(KodexaSelectorParser.ABBREV_PATH_SEP, 0); }
		public StepContext step() {
			return getRuleContext(StepContext.class,0);
		}
		public AbbrevPathStepContext(RelativeLocationPathContext ctx) { copyFrom(ctx); }
	}

	public final RelativeLocationPathContext relativeLocationPath() throws RecognitionException {
		return relativeLocationPath(0);
	}

	private RelativeLocationPathContext relativeLocationPath(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		RelativeLocationPathContext _localctx = new RelativeLocationPathContext(_ctx, _parentState);
		RelativeLocationPathContext _prevctx = _localctx;
		int _startState = 8;
		enterRecursionRule(_localctx, 8, RULE_relativeLocationPath, _p);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			{
			_localctx = new SingleStepContext(_localctx);
			_ctx = _localctx;
			_prevctx = _localctx;

			setState(111);
			step();
			}
			_ctx.stop = _input.LT(-1);
			setState(121);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,5,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					setState(119);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,4,_ctx) ) {
					case 1:
						{
						_localctx = new PathStepContext(new RelativeLocationPathContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_relativeLocationPath);
						setState(113);
						if (!(precpred(_ctx, 2))) throw new FailedPredicateException(this, "precpred(_ctx, 2)");
						setState(114);
						match(PATH_SEP);
						setState(115);
						step();
						}
						break;
					case 2:
						{
						_localctx = new AbbrevPathStepContext(new RelativeLocationPathContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_relativeLocationPath);
						setState(116);
						if (!(precpred(_ctx, 1))) throw new FailedPredicateException(this, "precpred(_ctx, 1)");
						setState(117);
						match(ABBREV_PATH_SEP);
						setState(118);
						step();
						}
						break;
					}
					} 
				}
				setState(123);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,5,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class StepContext extends ParserRuleContext {
		public StepContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_step; }
	 
		public StepContext() { }
		public void copyFrom(StepContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class NodeTestPredStepContext extends StepContext {
		public NodeTestContext nodeTest() {
			return getRuleContext(NodeTestContext.class,0);
		}
		public PredicateListContext predicateList() {
			return getRuleContext(PredicateListContext.class,0);
		}
		public NodeTestPredStepContext(StepContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SelfStepContext extends StepContext {
		public TerminalNode ABBREV_STEP_SELF() { return getToken(KodexaSelectorParser.ABBREV_STEP_SELF, 0); }
		public SelfStepContext(StepContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class AxisNodeTestStepContext extends StepContext {
		public AxisSpecifierContext axisSpecifier() {
			return getRuleContext(AxisSpecifierContext.class,0);
		}
		public NodeTestContext nodeTest() {
			return getRuleContext(NodeTestContext.class,0);
		}
		public AxisNodeTestStepContext(StepContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class AxisNodeTestPredStepContext extends StepContext {
		public AxisSpecifierContext axisSpecifier() {
			return getRuleContext(AxisSpecifierContext.class,0);
		}
		public NodeTestContext nodeTest() {
			return getRuleContext(NodeTestContext.class,0);
		}
		public PredicateListContext predicateList() {
			return getRuleContext(PredicateListContext.class,0);
		}
		public AxisNodeTestPredStepContext(StepContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ParentStepContext extends StepContext {
		public TerminalNode ABBREV_STEP_PARENT() { return getToken(KodexaSelectorParser.ABBREV_STEP_PARENT, 0); }
		public ParentStepContext(StepContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class NodeTestStepContext extends StepContext {
		public NodeTestContext nodeTest() {
			return getRuleContext(NodeTestContext.class,0);
		}
		public NodeTestStepContext(StepContext ctx) { copyFrom(ctx); }
	}

	public final StepContext step() throws RecognitionException {
		StepContext _localctx = new StepContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_step);
		try {
			setState(137);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,6,_ctx) ) {
			case 1:
				_localctx = new NodeTestStepContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(124);
				nodeTest();
				}
				break;
			case 2:
				_localctx = new NodeTestPredStepContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(125);
				nodeTest();
				setState(126);
				predicateList(0);
				}
				break;
			case 3:
				_localctx = new AxisNodeTestStepContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(128);
				axisSpecifier();
				setState(129);
				nodeTest();
				}
				break;
			case 4:
				_localctx = new AxisNodeTestPredStepContext(_localctx);
				enterOuterAlt(_localctx, 4);
				{
				setState(131);
				axisSpecifier();
				setState(132);
				nodeTest();
				setState(133);
				predicateList(0);
				}
				break;
			case 5:
				_localctx = new SelfStepContext(_localctx);
				enterOuterAlt(_localctx, 5);
				{
				setState(135);
				match(ABBREV_STEP_SELF);
				}
				break;
			case 6:
				_localctx = new ParentStepContext(_localctx);
				enterOuterAlt(_localctx, 6);
				{
				setState(136);
				match(ABBREV_STEP_PARENT);
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class AxisSpecifierContext extends ParserRuleContext {
		public AxisSpecifierContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_axisSpecifier; }
	 
		public AxisSpecifierContext() { }
		public void copyFrom(AxisSpecifierContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class FullAxisContext extends AxisSpecifierContext {
		public TerminalNode AXISNAME() { return getToken(KodexaSelectorParser.AXISNAME, 0); }
		public TerminalNode AXIS_SEP() { return getToken(KodexaSelectorParser.AXIS_SEP, 0); }
		public FullAxisContext(AxisSpecifierContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class AttrAxisContext extends AxisSpecifierContext {
		public TerminalNode ABBREV_AXIS_AT() { return getToken(KodexaSelectorParser.ABBREV_AXIS_AT, 0); }
		public AttrAxisContext(AxisSpecifierContext ctx) { copyFrom(ctx); }
	}

	public final AxisSpecifierContext axisSpecifier() throws RecognitionException {
		AxisSpecifierContext _localctx = new AxisSpecifierContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_axisSpecifier);
		try {
			setState(142);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case AXISNAME:
				_localctx = new FullAxisContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(139);
				match(AXISNAME);
				setState(140);
				match(AXIS_SEP);
				}
				break;
			case ABBREV_AXIS_AT:
				_localctx = new AttrAxisContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(141);
				match(ABBREV_AXIS_AT);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class NodeTestContext extends ParserRuleContext {
		public NodeTestContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_nodeTest; }
	 
		public NodeTestContext() { }
		public void copyFrom(NodeTestContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class NameTestNodeContext extends NodeTestContext {
		public NameTestContext nameTest() {
			return getRuleContext(NameTestContext.class,0);
		}
		public NameTestNodeContext(NodeTestContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class NodeTypeTestContext extends NodeTestContext {
		public TerminalNode NODETYPE() { return getToken(KodexaSelectorParser.NODETYPE, 0); }
		public TerminalNode LPAREN() { return getToken(KodexaSelectorParser.LPAREN, 0); }
		public TerminalNode RPAREN() { return getToken(KodexaSelectorParser.RPAREN, 0); }
		public NodeTypeTestContext(NodeTestContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class NodeTypeLiteralTestContext extends NodeTestContext {
		public TerminalNode NODETYPE() { return getToken(KodexaSelectorParser.NODETYPE, 0); }
		public TerminalNode LPAREN() { return getToken(KodexaSelectorParser.LPAREN, 0); }
		public TerminalNode LITERAL() { return getToken(KodexaSelectorParser.LITERAL, 0); }
		public TerminalNode RPAREN() { return getToken(KodexaSelectorParser.RPAREN, 0); }
		public NodeTypeLiteralTestContext(NodeTestContext ctx) { copyFrom(ctx); }
	}

	public final NodeTestContext nodeTest() throws RecognitionException {
		NodeTestContext _localctx = new NodeTestContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_nodeTest);
		try {
			setState(152);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,8,_ctx) ) {
			case 1:
				_localctx = new NameTestNodeContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(144);
				nameTest();
				}
				break;
			case 2:
				_localctx = new NodeTypeTestContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(145);
				match(NODETYPE);
				setState(146);
				match(LPAREN);
				setState(147);
				match(RPAREN);
				}
				break;
			case 3:
				_localctx = new NodeTypeLiteralTestContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(148);
				match(NODETYPE);
				setState(149);
				match(LPAREN);
				setState(150);
				match(LITERAL);
				setState(151);
				match(RPAREN);
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class NameTestContext extends ParserRuleContext {
		public NameTestContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_nameTest; }
	 
		public NameTestContext() { }
		public void copyFrom(NameTestContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class AnyNameTestContext extends NameTestContext {
		public TerminalNode STAR() { return getToken(KodexaSelectorParser.STAR, 0); }
		public AnyNameTestContext(NameTestContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class QNameTestContext extends NameTestContext {
		public QNameContext qName() {
			return getRuleContext(QNameContext.class,0);
		}
		public QNameTestContext(NameTestContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class PrefixedAnyNameTestContext extends NameTestContext {
		public TerminalNode NCNAME() { return getToken(KodexaSelectorParser.NCNAME, 0); }
		public TerminalNode COLON() { return getToken(KodexaSelectorParser.COLON, 0); }
		public TerminalNode STAR() { return getToken(KodexaSelectorParser.STAR, 0); }
		public PrefixedAnyNameTestContext(NameTestContext ctx) { copyFrom(ctx); }
	}

	public final NameTestContext nameTest() throws RecognitionException {
		NameTestContext _localctx = new NameTestContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_nameTest);
		try {
			setState(159);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,9,_ctx) ) {
			case 1:
				_localctx = new AnyNameTestContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(154);
				match(STAR);
				}
				break;
			case 2:
				_localctx = new PrefixedAnyNameTestContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(155);
				match(NCNAME);
				setState(156);
				match(COLON);
				setState(157);
				match(STAR);
				}
				break;
			case 3:
				_localctx = new QNameTestContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(158);
				qName();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class QNameContext extends ParserRuleContext {
		public QNameContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_qName; }
	 
		public QNameContext() { }
		public void copyFrom(QNameContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SimpleNameContext extends QNameContext {
		public TerminalNode NCNAME() { return getToken(KodexaSelectorParser.NCNAME, 0); }
		public SimpleNameContext(QNameContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class PrefixedNameContext extends QNameContext {
		public List<TerminalNode> NCNAME() { return getTokens(KodexaSelectorParser.NCNAME); }
		public TerminalNode NCNAME(int i) {
			return getToken(KodexaSelectorParser.NCNAME, i);
		}
		public TerminalNode COLON() { return getToken(KodexaSelectorParser.COLON, 0); }
		public PrefixedNameContext(QNameContext ctx) { copyFrom(ctx); }
	}

	public final QNameContext qName() throws RecognitionException {
		QNameContext _localctx = new QNameContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_qName);
		try {
			setState(165);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,10,_ctx) ) {
			case 1:
				_localctx = new PrefixedNameContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(161);
				match(NCNAME);
				setState(162);
				match(COLON);
				setState(163);
				match(NCNAME);
				}
				break;
			case 2:
				_localctx = new SimpleNameContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(164);
				match(NCNAME);
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class FilterExprContext extends ParserRuleContext {
		public FilterExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_filterExpr; }
	 
		public FilterExprContext() { }
		public void copyFrom(FilterExprContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class FuncCallFilterContext extends FilterExprContext {
		public FunctionCallContext functionCall() {
			return getRuleContext(FunctionCallContext.class,0);
		}
		public FuncCallFilterContext(FilterExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class BooleanFilterContext extends FilterExprContext {
		public BooleanLiteralContext booleanLiteral() {
			return getRuleContext(BooleanLiteralContext.class,0);
		}
		public BooleanFilterContext(FilterExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class GroupedFilterContext extends FilterExprContext {
		public TerminalNode LPAREN() { return getToken(KodexaSelectorParser.LPAREN, 0); }
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public TerminalNode RPAREN() { return getToken(KodexaSelectorParser.RPAREN, 0); }
		public GroupedFilterContext(FilterExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class PredicatedFilterContext extends FilterExprContext {
		public FilterExprContext filterExpr() {
			return getRuleContext(FilterExprContext.class,0);
		}
		public PredicateContext predicate() {
			return getRuleContext(PredicateContext.class,0);
		}
		public PredicatedFilterContext(FilterExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class NumberFilterContext extends FilterExprContext {
		public NumberContext number() {
			return getRuleContext(NumberContext.class,0);
		}
		public NumberFilterContext(FilterExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class VarRefFilterContext extends FilterExprContext {
		public VariableReferenceContext variableReference() {
			return getRuleContext(VariableReferenceContext.class,0);
		}
		public VarRefFilterContext(FilterExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class LiteralFilterContext extends FilterExprContext {
		public TerminalNode LITERAL() { return getToken(KodexaSelectorParser.LITERAL, 0); }
		public LiteralFilterContext(FilterExprContext ctx) { copyFrom(ctx); }
	}

	public final FilterExprContext filterExpr() throws RecognitionException {
		return filterExpr(0);
	}

	private FilterExprContext filterExpr(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		FilterExprContext _localctx = new FilterExprContext(_ctx, _parentState);
		FilterExprContext _prevctx = _localctx;
		int _startState = 20;
		enterRecursionRule(_localctx, 20, RULE_filterExpr, _p);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(177);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,11,_ctx) ) {
			case 1:
				{
				_localctx = new VarRefFilterContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;

				setState(168);
				variableReference();
				}
				break;
			case 2:
				{
				_localctx = new LiteralFilterContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(169);
				match(LITERAL);
				}
				break;
			case 3:
				{
				_localctx = new NumberFilterContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(170);
				number();
				}
				break;
			case 4:
				{
				_localctx = new BooleanFilterContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(171);
				booleanLiteral();
				}
				break;
			case 5:
				{
				_localctx = new FuncCallFilterContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(172);
				functionCall();
				}
				break;
			case 6:
				{
				_localctx = new GroupedFilterContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(173);
				match(LPAREN);
				setState(174);
				expr(0);
				setState(175);
				match(RPAREN);
				}
				break;
			}
			_ctx.stop = _input.LT(-1);
			setState(183);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,12,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					{
					_localctx = new PredicatedFilterContext(new FilterExprContext(_parentctx, _parentState));
					pushNewRecursionContext(_localctx, _startState, RULE_filterExpr);
					setState(179);
					if (!(precpred(_ctx, 1))) throw new FailedPredicateException(this, "precpred(_ctx, 1)");
					setState(180);
					predicate();
					}
					} 
				}
				setState(185);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,12,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class PredicateListContext extends ParserRuleContext {
		public PredicateListContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_predicateList; }
	 
		public PredicateListContext() { }
		public void copyFrom(PredicateListContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SinglePredicateContext extends PredicateListContext {
		public PredicateContext predicate() {
			return getRuleContext(PredicateContext.class,0);
		}
		public SinglePredicateContext(PredicateListContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class MultiplePredicateContext extends PredicateListContext {
		public PredicateListContext predicateList() {
			return getRuleContext(PredicateListContext.class,0);
		}
		public PredicateContext predicate() {
			return getRuleContext(PredicateContext.class,0);
		}
		public MultiplePredicateContext(PredicateListContext ctx) { copyFrom(ctx); }
	}

	public final PredicateListContext predicateList() throws RecognitionException {
		return predicateList(0);
	}

	private PredicateListContext predicateList(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		PredicateListContext _localctx = new PredicateListContext(_ctx, _parentState);
		PredicateListContext _prevctx = _localctx;
		int _startState = 22;
		enterRecursionRule(_localctx, 22, RULE_predicateList, _p);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			{
			_localctx = new SinglePredicateContext(_localctx);
			_ctx = _localctx;
			_prevctx = _localctx;

			setState(187);
			predicate();
			}
			_ctx.stop = _input.LT(-1);
			setState(193);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,13,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					{
					_localctx = new MultiplePredicateContext(new PredicateListContext(_parentctx, _parentState));
					pushNewRecursionContext(_localctx, _startState, RULE_predicateList);
					setState(189);
					if (!(precpred(_ctx, 1))) throw new FailedPredicateException(this, "precpred(_ctx, 1)");
					setState(190);
					predicate();
					}
					} 
				}
				setState(195);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,13,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class PredicateContext extends ParserRuleContext {
		public PredicateContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_predicate; }
	 
		public PredicateContext() { }
		public void copyFrom(PredicateContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ExprPredicateContext extends PredicateContext {
		public TerminalNode LBRACKET() { return getToken(KodexaSelectorParser.LBRACKET, 0); }
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public TerminalNode RBRACKET() { return getToken(KodexaSelectorParser.RBRACKET, 0); }
		public ExprPredicateContext(PredicateContext ctx) { copyFrom(ctx); }
	}

	public final PredicateContext predicate() throws RecognitionException {
		PredicateContext _localctx = new PredicateContext(_ctx, getState());
		enterRule(_localctx, 24, RULE_predicate);
		try {
			_localctx = new ExprPredicateContext(_localctx);
			enterOuterAlt(_localctx, 1);
			{
			setState(196);
			match(LBRACKET);
			setState(197);
			expr(0);
			setState(198);
			match(RBRACKET);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class VariableReferenceContext extends ParserRuleContext {
		public TerminalNode DOLLAR() { return getToken(KodexaSelectorParser.DOLLAR, 0); }
		public QNameContext qName() {
			return getRuleContext(QNameContext.class,0);
		}
		public VariableReferenceContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_variableReference; }
	}

	public final VariableReferenceContext variableReference() throws RecognitionException {
		VariableReferenceContext _localctx = new VariableReferenceContext(_ctx, getState());
		enterRule(_localctx, 26, RULE_variableReference);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(200);
			match(DOLLAR);
			setState(201);
			qName();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class NumberContext extends ParserRuleContext {
		public TerminalNode FLOAT() { return getToken(KodexaSelectorParser.FLOAT, 0); }
		public TerminalNode INTEGER() { return getToken(KodexaSelectorParser.INTEGER, 0); }
		public NumberContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_number; }
	}

	public final NumberContext number() throws RecognitionException {
		NumberContext _localctx = new NumberContext(_ctx, getState());
		enterRule(_localctx, 28, RULE_number);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(203);
			_la = _input.LA(1);
			if ( !(_la==FLOAT || _la==INTEGER) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class BooleanLiteralContext extends ParserRuleContext {
		public TerminalNode TRUE() { return getToken(KodexaSelectorParser.TRUE, 0); }
		public TerminalNode FALSE() { return getToken(KodexaSelectorParser.FALSE, 0); }
		public BooleanLiteralContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_booleanLiteral; }
	}

	public final BooleanLiteralContext booleanLiteral() throws RecognitionException {
		BooleanLiteralContext _localctx = new BooleanLiteralContext(_ctx, getState());
		enterRule(_localctx, 30, RULE_booleanLiteral);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(205);
			_la = _input.LA(1);
			if ( !(_la==TRUE || _la==FALSE) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class FunctionCallContext extends ParserRuleContext {
		public FuncQNameContext funcQName() {
			return getRuleContext(FuncQNameContext.class,0);
		}
		public FormalArgumentsContext formalArguments() {
			return getRuleContext(FormalArgumentsContext.class,0);
		}
		public BuiltInFunctionCallContext builtInFunctionCall() {
			return getRuleContext(BuiltInFunctionCallContext.class,0);
		}
		public FunctionCallContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_functionCall; }
	}

	public final FunctionCallContext functionCall() throws RecognitionException {
		FunctionCallContext _localctx = new FunctionCallContext(_ctx, getState());
		enterRule(_localctx, 32, RULE_functionCall);
		try {
			setState(211);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case FUNCTION_NAME:
				enterOuterAlt(_localctx, 1);
				{
				setState(207);
				funcQName();
				setState(208);
				formalArguments();
				}
				break;
			case TRUE:
			case FALSE:
				enterOuterAlt(_localctx, 2);
				{
				setState(210);
				builtInFunctionCall();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class BuiltInFunctionCallContext extends ParserRuleContext {
		public BuiltInFunctionCallContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_builtInFunctionCall; }
	 
		public BuiltInFunctionCallContext() { }
		public void copyFrom(BuiltInFunctionCallContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class TrueFunctionContext extends BuiltInFunctionCallContext {
		public TerminalNode TRUE() { return getToken(KodexaSelectorParser.TRUE, 0); }
		public FormalArgumentsContext formalArguments() {
			return getRuleContext(FormalArgumentsContext.class,0);
		}
		public TrueFunctionContext(BuiltInFunctionCallContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class FalseFunctionContext extends BuiltInFunctionCallContext {
		public TerminalNode FALSE() { return getToken(KodexaSelectorParser.FALSE, 0); }
		public FormalArgumentsContext formalArguments() {
			return getRuleContext(FormalArgumentsContext.class,0);
		}
		public FalseFunctionContext(BuiltInFunctionCallContext ctx) { copyFrom(ctx); }
	}

	public final BuiltInFunctionCallContext builtInFunctionCall() throws RecognitionException {
		BuiltInFunctionCallContext _localctx = new BuiltInFunctionCallContext(_ctx, getState());
		enterRule(_localctx, 34, RULE_builtInFunctionCall);
		try {
			setState(217);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case TRUE:
				_localctx = new TrueFunctionContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(213);
				match(TRUE);
				setState(214);
				formalArguments();
				}
				break;
			case FALSE:
				_localctx = new FalseFunctionContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(215);
				match(FALSE);
				setState(216);
				formalArguments();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class FuncQNameContext extends ParserRuleContext {
		public TerminalNode FUNCTION_NAME() { return getToken(KodexaSelectorParser.FUNCTION_NAME, 0); }
		public FuncQNameContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_funcQName; }
	}

	public final FuncQNameContext funcQName() throws RecognitionException {
		FuncQNameContext _localctx = new FuncQNameContext(_ctx, getState());
		enterRule(_localctx, 36, RULE_funcQName);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(219);
			match(FUNCTION_NAME);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class FormalArgumentsContext extends ParserRuleContext {
		public FormalArgumentsContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_formalArguments; }
	 
		public FormalArgumentsContext() { }
		public void copyFrom(FormalArgumentsContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class EmptyArgsContext extends FormalArgumentsContext {
		public TerminalNode LPAREN() { return getToken(KodexaSelectorParser.LPAREN, 0); }
		public TerminalNode RPAREN() { return getToken(KodexaSelectorParser.RPAREN, 0); }
		public EmptyArgsContext(FormalArgumentsContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ArgsListContext extends FormalArgumentsContext {
		public TerminalNode LPAREN() { return getToken(KodexaSelectorParser.LPAREN, 0); }
		public ArgumentListContext argumentList() {
			return getRuleContext(ArgumentListContext.class,0);
		}
		public TerminalNode RPAREN() { return getToken(KodexaSelectorParser.RPAREN, 0); }
		public ArgsListContext(FormalArgumentsContext ctx) { copyFrom(ctx); }
	}

	public final FormalArgumentsContext formalArguments() throws RecognitionException {
		FormalArgumentsContext _localctx = new FormalArgumentsContext(_ctx, getState());
		enterRule(_localctx, 38, RULE_formalArguments);
		try {
			setState(227);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,16,_ctx) ) {
			case 1:
				_localctx = new EmptyArgsContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(221);
				match(LPAREN);
				setState(222);
				match(RPAREN);
				}
				break;
			case 2:
				_localctx = new ArgsListContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(223);
				match(LPAREN);
				setState(224);
				argumentList(0);
				setState(225);
				match(RPAREN);
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ArgumentListContext extends ParserRuleContext {
		public ArgumentListContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_argumentList; }
	 
		public ArgumentListContext() { }
		public void copyFrom(ArgumentListContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SingleArgContext extends ArgumentListContext {
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public SingleArgContext(ArgumentListContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class MultipleArgsContext extends ArgumentListContext {
		public ArgumentListContext argumentList() {
			return getRuleContext(ArgumentListContext.class,0);
		}
		public TerminalNode COMMA() { return getToken(KodexaSelectorParser.COMMA, 0); }
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public MultipleArgsContext(ArgumentListContext ctx) { copyFrom(ctx); }
	}

	public final ArgumentListContext argumentList() throws RecognitionException {
		return argumentList(0);
	}

	private ArgumentListContext argumentList(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		ArgumentListContext _localctx = new ArgumentListContext(_ctx, _parentState);
		ArgumentListContext _prevctx = _localctx;
		int _startState = 40;
		enterRecursionRule(_localctx, 40, RULE_argumentList, _p);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			{
			_localctx = new SingleArgContext(_localctx);
			_ctx = _localctx;
			_prevctx = _localctx;

			setState(230);
			expr(0);
			}
			_ctx.stop = _input.LT(-1);
			setState(237);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,17,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					{
					_localctx = new MultipleArgsContext(new ArgumentListContext(_parentctx, _parentState));
					pushNewRecursionContext(_localctx, _startState, RULE_argumentList);
					setState(232);
					if (!(precpred(_ctx, 1))) throw new FailedPredicateException(this, "precpred(_ctx, 1)");
					setState(233);
					match(COMMA);
					setState(234);
					expr(0);
					}
					} 
				}
				setState(239);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,17,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class PathSepContext extends ParserRuleContext {
		public TerminalNode PATH_SEP() { return getToken(KodexaSelectorParser.PATH_SEP, 0); }
		public TerminalNode ABBREV_PATH_SEP() { return getToken(KodexaSelectorParser.ABBREV_PATH_SEP, 0); }
		public PathSepContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_pathSep; }
	}

	public final PathSepContext pathSep() throws RecognitionException {
		PathSepContext _localctx = new PathSepContext(_ctx, getState());
		enterRule(_localctx, 42, RULE_pathSep);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(240);
			_la = _input.LA(1);
			if ( !(_la==PATH_SEP || _la==ABBREV_PATH_SEP) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public boolean sempred(RuleContext _localctx, int ruleIndex, int predIndex) {
		switch (ruleIndex) {
		case 1:
			return expr_sempred((ExprContext)_localctx, predIndex);
		case 4:
			return relativeLocationPath_sempred((RelativeLocationPathContext)_localctx, predIndex);
		case 10:
			return filterExpr_sempred((FilterExprContext)_localctx, predIndex);
		case 11:
			return predicateList_sempred((PredicateListContext)_localctx, predIndex);
		case 20:
			return argumentList_sempred((ArgumentListContext)_localctx, predIndex);
		}
		return true;
	}
	private boolean expr_sempred(ExprContext _localctx, int predIndex) {
		switch (predIndex) {
		case 0:
			return precpred(_ctx, 21);
		case 1:
			return precpred(_ctx, 20);
		case 2:
			return precpred(_ctx, 19);
		case 3:
			return precpred(_ctx, 18);
		case 4:
			return precpred(_ctx, 17);
		case 5:
			return precpred(_ctx, 16);
		case 6:
			return precpred(_ctx, 15);
		case 7:
			return precpred(_ctx, 14);
		case 8:
			return precpred(_ctx, 13);
		case 9:
			return precpred(_ctx, 12);
		case 10:
			return precpred(_ctx, 10);
		}
		return true;
	}
	private boolean relativeLocationPath_sempred(RelativeLocationPathContext _localctx, int predIndex) {
		switch (predIndex) {
		case 11:
			return precpred(_ctx, 2);
		case 12:
			return precpred(_ctx, 1);
		}
		return true;
	}
	private boolean filterExpr_sempred(FilterExprContext _localctx, int predIndex) {
		switch (predIndex) {
		case 13:
			return precpred(_ctx, 1);
		}
		return true;
	}
	private boolean predicateList_sempred(PredicateListContext _localctx, int predIndex) {
		switch (predIndex) {
		case 14:
			return precpred(_ctx, 1);
		}
		return true;
	}
	private boolean argumentList_sempred(ArgumentListContext _localctx, int predIndex) {
		switch (predIndex) {
		case 15:
			return precpred(_ctx, 1);
		}
		return true;
	}

	public static final String _serializedATN =
		"\u0004\u0001$\u00f3\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001\u0002"+
		"\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004\u0007\u0004\u0002"+
		"\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007\u0007\u0007\u0002"+
		"\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0002\u000b\u0007\u000b\u0002"+
		"\f\u0007\f\u0002\r\u0007\r\u0002\u000e\u0007\u000e\u0002\u000f\u0007\u000f"+
		"\u0002\u0010\u0007\u0010\u0002\u0011\u0007\u0011\u0002\u0012\u0007\u0012"+
		"\u0002\u0013\u0007\u0013\u0002\u0014\u0007\u0014\u0002\u0015\u0007\u0015"+
		"\u0001\u0000\u0001\u0000\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001"+
		"\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001"+
		"\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001"+
		"\u0003\u0001?\b\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001"+
		"\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001"+
		"\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001"+
		"\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001"+
		"\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001"+
		"\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0005\u0001"+
		"b\b\u0001\n\u0001\f\u0001e\t\u0001\u0001\u0002\u0001\u0002\u0001\u0002"+
		"\u0003\u0002j\b\u0002\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0004"+
		"\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004"+
		"\u0001\u0004\u0001\u0004\u0005\u0004x\b\u0004\n\u0004\f\u0004{\t\u0004"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0003\u0005\u008a\b\u0005\u0001\u0006\u0001\u0006\u0001\u0006"+
		"\u0003\u0006\u008f\b\u0006\u0001\u0007\u0001\u0007\u0001\u0007\u0001\u0007"+
		"\u0001\u0007\u0001\u0007\u0001\u0007\u0001\u0007\u0003\u0007\u0099\b\u0007"+
		"\u0001\b\u0001\b\u0001\b\u0001\b\u0001\b\u0003\b\u00a0\b\b\u0001\t\u0001"+
		"\t\u0001\t\u0001\t\u0003\t\u00a6\b\t\u0001\n\u0001\n\u0001\n\u0001\n\u0001"+
		"\n\u0001\n\u0001\n\u0001\n\u0001\n\u0001\n\u0003\n\u00b2\b\n\u0001\n\u0001"+
		"\n\u0005\n\u00b6\b\n\n\n\f\n\u00b9\t\n\u0001\u000b\u0001\u000b\u0001\u000b"+
		"\u0001\u000b\u0001\u000b\u0005\u000b\u00c0\b\u000b\n\u000b\f\u000b\u00c3"+
		"\t\u000b\u0001\f\u0001\f\u0001\f\u0001\f\u0001\r\u0001\r\u0001\r\u0001"+
		"\u000e\u0001\u000e\u0001\u000f\u0001\u000f\u0001\u0010\u0001\u0010\u0001"+
		"\u0010\u0001\u0010\u0003\u0010\u00d4\b\u0010\u0001\u0011\u0001\u0011\u0001"+
		"\u0011\u0001\u0011\u0003\u0011\u00da\b\u0011\u0001\u0012\u0001\u0012\u0001"+
		"\u0013\u0001\u0013\u0001\u0013\u0001\u0013\u0001\u0013\u0001\u0013\u0003"+
		"\u0013\u00e4\b\u0013\u0001\u0014\u0001\u0014\u0001\u0014\u0001\u0014\u0001"+
		"\u0014\u0001\u0014\u0005\u0014\u00ec\b\u0014\n\u0014\f\u0014\u00ef\t\u0014"+
		"\u0001\u0015\u0001\u0015\u0001\u0015\u0000\u0005\u0002\b\u0014\u0016("+
		"\u0016\u0000\u0002\u0004\u0006\b\n\f\u000e\u0010\u0012\u0014\u0016\u0018"+
		"\u001a\u001c\u001e \"$&(*\u0000\u0003\u0001\u0000\u001e\u001f\u0001\u0000"+
		"\u001a\u001b\u0001\u0000\u0007\b\u0109\u0000,\u0001\u0000\u0000\u0000"+
		"\u0002>\u0001\u0000\u0000\u0000\u0004i\u0001\u0000\u0000\u0000\u0006k"+
		"\u0001\u0000\u0000\u0000\bn\u0001\u0000\u0000\u0000\n\u0089\u0001\u0000"+
		"\u0000\u0000\f\u008e\u0001\u0000\u0000\u0000\u000e\u0098\u0001\u0000\u0000"+
		"\u0000\u0010\u009f\u0001\u0000\u0000\u0000\u0012\u00a5\u0001\u0000\u0000"+
		"\u0000\u0014\u00b1\u0001\u0000\u0000\u0000\u0016\u00ba\u0001\u0000\u0000"+
		"\u0000\u0018\u00c4\u0001\u0000\u0000\u0000\u001a\u00c8\u0001\u0000\u0000"+
		"\u0000\u001c\u00cb\u0001\u0000\u0000\u0000\u001e\u00cd\u0001\u0000\u0000"+
		"\u0000 \u00d3\u0001\u0000\u0000\u0000\"\u00d9\u0001\u0000\u0000\u0000"+
		"$\u00db\u0001\u0000\u0000\u0000&\u00e3\u0001\u0000\u0000\u0000(\u00e5"+
		"\u0001\u0000\u0000\u0000*\u00f0\u0001\u0000\u0000\u0000,-\u0003\u0002"+
		"\u0001\u0000-\u0001\u0001\u0000\u0000\u0000./\u0006\u0001\uffff\uffff"+
		"\u0000/0\u0005\u0015\u0000\u00000?\u0003\u0002\u0001\u000b1?\u0003 \u0010"+
		"\u000023\u0003\u0014\n\u000034\u0003*\u0015\u000045\u0003\b\u0004\u0000"+
		"5?\u0001\u0000\u0000\u00006?\u0003\b\u0004\u00007?\u0003\u0004\u0002\u0000"+
		"8?\u0003\u0006\u0003\u00009?\u0003\u0014\n\u0000:?\u0003\u0010\b\u0000"+
		";<\u0005\u0007\u0000\u0000<?\u0003\u0010\b\u0000=?\u0003\u001e\u000f\u0000"+
		">.\u0001\u0000\u0000\u0000>1\u0001\u0000\u0000\u0000>2\u0001\u0000\u0000"+
		"\u0000>6\u0001\u0000\u0000\u0000>7\u0001\u0000\u0000\u0000>8\u0001\u0000"+
		"\u0000\u0000>9\u0001\u0000\u0000\u0000>:\u0001\u0000\u0000\u0000>;\u0001"+
		"\u0000\u0000\u0000>=\u0001\u0000\u0000\u0000?c\u0001\u0000\u0000\u0000"+
		"@A\n\u0015\u0000\u0000AB\u0005\u0001\u0000\u0000Bb\u0003\u0002\u0001\u0016"+
		"CD\n\u0014\u0000\u0000DE\u0005\u0002\u0000\u0000Eb\u0003\u0002\u0001\u0015"+
		"FG\n\u0013\u0000\u0000GH\u0005\u0012\u0000\u0000Hb\u0003\u0002\u0001\u0014"+
		"IJ\n\u0012\u0000\u0000JK\u0005\u0013\u0000\u0000Kb\u0003\u0002\u0001\u0013"+
		"LM\n\u0011\u0000\u0000MN\u0005\u0014\u0000\u0000Nb\u0003\u0002\u0001\u0012"+
		"OP\n\u0010\u0000\u0000PQ\u0005\u0015\u0000\u0000Qb\u0003\u0002\u0001\u0011"+
		"RS\n\u000f\u0000\u0000ST\u0005\u0003\u0000\u0000Tb\u0003\u0002\u0001\u0010"+
		"UV\n\u000e\u0000\u0000VW\u0005\u0004\u0000\u0000Wb\u0003\u0002\u0001\u000f"+
		"XY\n\r\u0000\u0000YZ\u0005\u0011\u0000\u0000Zb\u0003\u0002\u0001\u000e"+
		"[\\\n\f\u0000\u0000\\]\u0005\u0005\u0000\u0000]b\u0003\u0002\u0001\r^"+
		"_\n\n\u0000\u0000_`\u0005\u0006\u0000\u0000`b\u0003\u0002\u0001\u000b"+
		"a@\u0001\u0000\u0000\u0000aC\u0001\u0000\u0000\u0000aF\u0001\u0000\u0000"+
		"\u0000aI\u0001\u0000\u0000\u0000aL\u0001\u0000\u0000\u0000aO\u0001\u0000"+
		"\u0000\u0000aR\u0001\u0000\u0000\u0000aU\u0001\u0000\u0000\u0000aX\u0001"+
		"\u0000\u0000\u0000a[\u0001\u0000\u0000\u0000a^\u0001\u0000\u0000\u0000"+
		"be\u0001\u0000\u0000\u0000ca\u0001\u0000\u0000\u0000cd\u0001\u0000\u0000"+
		"\u0000d\u0003\u0001\u0000\u0000\u0000ec\u0001\u0000\u0000\u0000fj\u0005"+
		"\u0007\u0000\u0000gh\u0005\u0007\u0000\u0000hj\u0003\b\u0004\u0000if\u0001"+
		"\u0000\u0000\u0000ig\u0001\u0000\u0000\u0000j\u0005\u0001\u0000\u0000"+
		"\u0000kl\u0005\b\u0000\u0000lm\u0003\b\u0004\u0000m\u0007\u0001\u0000"+
		"\u0000\u0000no\u0006\u0004\uffff\uffff\u0000op\u0003\n\u0005\u0000py\u0001"+
		"\u0000\u0000\u0000qr\n\u0002\u0000\u0000rs\u0005\u0007\u0000\u0000sx\u0003"+
		"\n\u0005\u0000tu\n\u0001\u0000\u0000uv\u0005\b\u0000\u0000vx\u0003\n\u0005"+
		"\u0000wq\u0001\u0000\u0000\u0000wt\u0001\u0000\u0000\u0000x{\u0001\u0000"+
		"\u0000\u0000yw\u0001\u0000\u0000\u0000yz\u0001\u0000\u0000\u0000z\t\u0001"+
		"\u0000\u0000\u0000{y\u0001\u0000\u0000\u0000|\u008a\u0003\u000e\u0007"+
		"\u0000}~\u0003\u000e\u0007\u0000~\u007f\u0003\u0016\u000b\u0000\u007f"+
		"\u008a\u0001\u0000\u0000\u0000\u0080\u0081\u0003\f\u0006\u0000\u0081\u0082"+
		"\u0003\u000e\u0007\u0000\u0082\u008a\u0001\u0000\u0000\u0000\u0083\u0084"+
		"\u0003\f\u0006\u0000\u0084\u0085\u0003\u000e\u0007\u0000\u0085\u0086\u0003"+
		"\u0016\u000b\u0000\u0086\u008a\u0001\u0000\u0000\u0000\u0087\u008a\u0005"+
		"\t\u0000\u0000\u0088\u008a\u0005\n\u0000\u0000\u0089|\u0001\u0000\u0000"+
		"\u0000\u0089}\u0001\u0000\u0000\u0000\u0089\u0080\u0001\u0000\u0000\u0000"+
		"\u0089\u0083\u0001\u0000\u0000\u0000\u0089\u0087\u0001\u0000\u0000\u0000"+
		"\u0089\u0088\u0001\u0000\u0000\u0000\u008a\u000b\u0001\u0000\u0000\u0000"+
		"\u008b\u008c\u0005#\u0000\u0000\u008c\u008f\u0005\u000b\u0000\u0000\u008d"+
		"\u008f\u0005\f\u0000\u0000\u008e\u008b\u0001\u0000\u0000\u0000\u008e\u008d"+
		"\u0001\u0000\u0000\u0000\u008f\r\u0001\u0000\u0000\u0000\u0090\u0099\u0003"+
		"\u0010\b\u0000\u0091\u0092\u0005 \u0000\u0000\u0092\u0093\u0005\r\u0000"+
		"\u0000\u0093\u0099\u0005\u000e\u0000\u0000\u0094\u0095\u0005 \u0000\u0000"+
		"\u0095\u0096\u0005\r\u0000\u0000\u0096\u0097\u0005\u001d\u0000\u0000\u0097"+
		"\u0099\u0005\u000e\u0000\u0000\u0098\u0090\u0001\u0000\u0000\u0000\u0098"+
		"\u0091\u0001\u0000\u0000\u0000\u0098\u0094\u0001\u0000\u0000\u0000\u0099"+
		"\u000f\u0001\u0000\u0000\u0000\u009a\u00a0\u0005\u0016\u0000\u0000\u009b"+
		"\u009c\u0005!\u0000\u0000\u009c\u009d\u0005\u0018\u0000\u0000\u009d\u00a0"+
		"\u0005\u0016\u0000\u0000\u009e\u00a0\u0003\u0012\t\u0000\u009f\u009a\u0001"+
		"\u0000\u0000\u0000\u009f\u009b\u0001\u0000\u0000\u0000\u009f\u009e\u0001"+
		"\u0000\u0000\u0000\u00a0\u0011\u0001\u0000\u0000\u0000\u00a1\u00a2\u0005"+
		"!\u0000\u0000\u00a2\u00a3\u0005\u0018\u0000\u0000\u00a3\u00a6\u0005!\u0000"+
		"\u0000\u00a4\u00a6\u0005!\u0000\u0000\u00a5\u00a1\u0001\u0000\u0000\u0000"+
		"\u00a5\u00a4\u0001\u0000\u0000\u0000\u00a6\u0013\u0001\u0000\u0000\u0000"+
		"\u00a7\u00a8\u0006\n\uffff\uffff\u0000\u00a8\u00b2\u0003\u001a\r\u0000"+
		"\u00a9\u00b2\u0005\u001d\u0000\u0000\u00aa\u00b2\u0003\u001c\u000e\u0000"+
		"\u00ab\u00b2\u0003\u001e\u000f\u0000\u00ac\u00b2\u0003 \u0010\u0000\u00ad"+
		"\u00ae\u0005\r\u0000\u0000\u00ae\u00af\u0003\u0002\u0001\u0000\u00af\u00b0"+
		"\u0005\u000e\u0000\u0000\u00b0\u00b2\u0001\u0000\u0000\u0000\u00b1\u00a7"+
		"\u0001\u0000\u0000\u0000\u00b1\u00a9\u0001\u0000\u0000\u0000\u00b1\u00aa"+
		"\u0001\u0000\u0000\u0000\u00b1\u00ab\u0001\u0000\u0000\u0000\u00b1\u00ac"+
		"\u0001\u0000\u0000\u0000\u00b1\u00ad\u0001\u0000\u0000\u0000\u00b2\u00b7"+
		"\u0001\u0000\u0000\u0000\u00b3\u00b4\n\u0001\u0000\u0000\u00b4\u00b6\u0003"+
		"\u0018\f\u0000\u00b5\u00b3\u0001\u0000\u0000\u0000\u00b6\u00b9\u0001\u0000"+
		"\u0000\u0000\u00b7\u00b5\u0001\u0000\u0000\u0000\u00b7\u00b8\u0001\u0000"+
		"\u0000\u0000\u00b8\u0015\u0001\u0000\u0000\u0000\u00b9\u00b7\u0001\u0000"+
		"\u0000\u0000\u00ba\u00bb\u0006\u000b\uffff\uffff\u0000\u00bb\u00bc\u0003"+
		"\u0018\f\u0000\u00bc\u00c1\u0001\u0000\u0000\u0000\u00bd\u00be\n\u0001"+
		"\u0000\u0000\u00be\u00c0\u0003\u0018\f\u0000\u00bf\u00bd\u0001\u0000\u0000"+
		"\u0000\u00c0\u00c3\u0001\u0000\u0000\u0000\u00c1\u00bf\u0001\u0000\u0000"+
		"\u0000\u00c1\u00c2\u0001\u0000\u0000\u0000\u00c2\u0017\u0001\u0000\u0000"+
		"\u0000\u00c3\u00c1\u0001\u0000\u0000\u0000\u00c4\u00c5\u0005\u000f\u0000"+
		"\u0000\u00c5\u00c6\u0003\u0002\u0001\u0000\u00c6\u00c7\u0005\u0010\u0000"+
		"\u0000\u00c7\u0019\u0001\u0000\u0000\u0000\u00c8\u00c9\u0005\u0019\u0000"+
		"\u0000\u00c9\u00ca\u0003\u0012\t\u0000\u00ca\u001b\u0001\u0000\u0000\u0000"+
		"\u00cb\u00cc\u0007\u0000\u0000\u0000\u00cc\u001d\u0001\u0000\u0000\u0000"+
		"\u00cd\u00ce\u0007\u0001\u0000\u0000\u00ce\u001f\u0001\u0000\u0000\u0000"+
		"\u00cf\u00d0\u0003$\u0012\u0000\u00d0\u00d1\u0003&\u0013\u0000\u00d1\u00d4"+
		"\u0001\u0000\u0000\u0000\u00d2\u00d4\u0003\"\u0011\u0000\u00d3\u00cf\u0001"+
		"\u0000\u0000\u0000\u00d3\u00d2\u0001\u0000\u0000\u0000\u00d4!\u0001\u0000"+
		"\u0000\u0000\u00d5\u00d6\u0005\u001a\u0000\u0000\u00d6\u00da\u0003&\u0013"+
		"\u0000\u00d7\u00d8\u0005\u001b\u0000\u0000\u00d8\u00da\u0003&\u0013\u0000"+
		"\u00d9\u00d5\u0001\u0000\u0000\u0000\u00d9\u00d7\u0001\u0000\u0000\u0000"+
		"\u00da#\u0001\u0000\u0000\u0000\u00db\u00dc\u0005\u001c\u0000\u0000\u00dc"+
		"%\u0001\u0000\u0000\u0000\u00dd\u00de\u0005\r\u0000\u0000\u00de\u00e4"+
		"\u0005\u000e\u0000\u0000\u00df\u00e0\u0005\r\u0000\u0000\u00e0\u00e1\u0003"+
		"(\u0014\u0000\u00e1\u00e2\u0005\u000e\u0000\u0000\u00e2\u00e4\u0001\u0000"+
		"\u0000\u0000\u00e3\u00dd\u0001\u0000\u0000\u0000\u00e3\u00df\u0001\u0000"+
		"\u0000\u0000\u00e4\'\u0001\u0000\u0000\u0000\u00e5\u00e6\u0006\u0014\uffff"+
		"\uffff\u0000\u00e6\u00e7\u0003\u0002\u0001\u0000\u00e7\u00ed\u0001\u0000"+
		"\u0000\u0000\u00e8\u00e9\n\u0001\u0000\u0000\u00e9\u00ea\u0005\u0017\u0000"+
		"\u0000\u00ea\u00ec\u0003\u0002\u0001\u0000\u00eb\u00e8\u0001\u0000\u0000"+
		"\u0000\u00ec\u00ef\u0001\u0000\u0000\u0000\u00ed\u00eb\u0001\u0000\u0000"+
		"\u0000\u00ed\u00ee\u0001\u0000\u0000\u0000\u00ee)\u0001\u0000\u0000\u0000"+
		"\u00ef\u00ed\u0001\u0000\u0000\u0000\u00f0\u00f1\u0007\u0002\u0000\u0000"+
		"\u00f1+\u0001\u0000\u0000\u0000\u0012>aciwy\u0089\u008e\u0098\u009f\u00a5"+
		"\u00b1\u00b7\u00c1\u00d3\u00d9\u00e3\u00ed";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}