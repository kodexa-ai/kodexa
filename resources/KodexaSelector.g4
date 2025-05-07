grammar KodexaSelector;

// Parser Rules
xpath
    : expr
    ;

expr
    : expr OR expr                            # orExpr
    | expr AND expr                           # andExpr
    | expr EQUALS expr                        # equalsExpr
    | expr REL_OP expr                        # relationalExpr
    | expr PLUS expr                          # addExpr
    | expr MINUS expr                         # subtractExpr
    | expr UNION expr                         # unionExpr
    | expr INTERSECT expr                     # intersectExpr
    | MINUS expr                              # unaryMinusExpr
    | expr PIPELINE expr                      # pipelineExpr
    | functionCall                            # funcCallExpr
    | filterExpr pathSep relativeLocationPath # pathBinaryExpr
    | relativeLocationPath                    # relativePathExpr
    | absoluteLocationPath                    # absolutePathExpr
    | abbreviatedAbsoluteLocationPath         # abbrevAbsPathExpr
    | filterExpr                              # filterExpression
    | nameTest                                # directNameTest
    | PATH_SEP nameTest                       # rootNameTest
    | booleanLiteral                          # booleanLiteralExpr
    ;

absoluteLocationPath
    : PATH_SEP                         # rootOnly
    | PATH_SEP relativeLocationPath    # rootPath
    ;

abbreviatedAbsoluteLocationPath
    : ABBREV_PATH_SEP relativeLocationPath
    ;

relativeLocationPath
    : step                                      # singleStep
    | relativeLocationPath PATH_SEP step        # pathStep
    | relativeLocationPath ABBREV_PATH_SEP step # abbrevPathStep
    ;

step
    : nodeTest                            # nodeTestStep
    | nodeTest predicateList              # nodeTestPredStep
    | axisSpecifier nodeTest              # axisNodeTestStep
    | axisSpecifier nodeTest predicateList # axisNodeTestPredStep
    | ABBREV_STEP_SELF                    # selfStep
    | ABBREV_STEP_PARENT                  # parentStep
    ;

axisSpecifier
    : AXISNAME AXIS_SEP  # fullAxis
    | ABBREV_AXIS_AT     # attrAxis
    ;

nodeTest
    : nameTest                                   # nameTestNode
    | NODETYPE LPAREN RPAREN                     # nodeTypeTest
    | NODETYPE LPAREN LITERAL RPAREN             # nodeTypeLiteralTest
    ;

nameTest
    : STAR                      # anyNameTest
    | NCNAME COLON STAR         # prefixedAnyNameTest
    | qName                     # qNameTest
    ;

qName
    : NCNAME COLON NCNAME  # prefixedName
    | NCNAME               # simpleName
    ;

filterExpr
    : variableReference                   # varRefFilter
    | LITERAL                             # literalFilter
    | number                              # numberFilter
    | booleanLiteral                      # booleanFilter
    | functionCall                        # funcCallFilter
    | LPAREN expr RPAREN                  # groupedFilter
    | filterExpr predicate                # predicatedFilter
    ;

predicateList
    : predicate                     # singlePredicate
    | predicateList predicate       # multiplePredicate
    ;

predicate
    : LBRACKET expr RBRACKET                                # exprPredicate
    ;

variableReference
    : DOLLAR qName
    ;

number
    : FLOAT
    | INTEGER
    ;

booleanLiteral
    : TRUE 
    | FALSE
    ;

functionCall
    : funcQName formalArguments
    | builtInFunctionCall
    ;

builtInFunctionCall
    : TRUE formalArguments # trueFunction
    | FALSE formalArguments # falseFunction
    ;
    
funcQName: FUNCTION_NAME;

formalArguments
    : LPAREN RPAREN                 # emptyArgs
    | LPAREN argumentList RPAREN    # argsList
    ;

argumentList
    : expr                       # singleArg
    | argumentList COMMA expr    # multipleArgs
    ;

pathSep
    : PATH_SEP
    | ABBREV_PATH_SEP
    ;

// Lexer Rules
OR: 'or';
AND: 'and';
INTERSECT: 'intersect';
PIPELINE: 'stream';

PATH_SEP: '/';
ABBREV_PATH_SEP: '//';
ABBREV_STEP_SELF: '.';
ABBREV_STEP_PARENT: '..';
AXIS_SEP: '::';
ABBREV_AXIS_AT: '@';
LPAREN: '(';
RPAREN: ')';
LBRACKET: '[';
RBRACKET: ']';
UNION: '|';
EQUALS: '!=' | '=';
REL_OP: '<=' | '>=' | '<' | '>';
PLUS: '+';
MINUS: '-';
STAR: '*';
COMMA: ',';
COLON: ':';
DOLLAR: '$';
TRUE: 'true';
FALSE: 'false';

FUNCTION_NAME: 'contentRegex' | 'typeRegex' | 'tagRegex' | 'hasTag' | 'hasFeature' | 'hasFeatureValue' | 'content' | 'id' | 'node_type' | 'index';

LITERAL: '"' ~["]* '"' | '\'' ~[']* '\'';
FLOAT: DIGIT+ '.' DIGIT* | '.' DIGIT+;
INTEGER: DIGIT+;

// Node types
NODETYPE: 'comment' | 'text' | 'processing-instruction' | 'node';

// Names
NCNAME: NameStartChar NameChar*;
FUNCNAME: NCNAME;
AXISNAME: NCNAME;

fragment NameStartChar
    : [a-zA-Z]
    | '_'
    | [\u00C0-\u00D6]
    | [\u00D8-\u00F6]
    | [\u00F8-\u02FF]
    | [\u0370-\u037D]
    | [\u037F-\u1FFF]
    | [\u200C-\u200D]
    | [\u2070-\u218F]
    | [\u2C00-\u2FEF]
    | [\u3001-\uD7FF]
    | [\uF900-\uFDCF]
    | [\uFDF0-\uFFFD]
    // | [\u10000-\uEFFFF] // Uncomment this if your ANTLR supports these ranges
    ;

fragment NameChar
    : NameStartChar
    | '-'
    | '.'
    | [0-9]
    | '\u00B7'
    | [\u0300-\u036F]
    | [\u203F-\u2040]
    ;

fragment DIGIT: [0-9];

// Skip whitespace
WS: [ \t\r\n]+ -> skip;