# coding: utf-8
import ply.yacc as yacc
import random
# Get the token map from the lexer.  This is required.
from .zako_lex import tokens
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)
# dictionary of names
names = {}
exceptions = []
# extra variable for syntax sugar
# flag = False


def p_start_strategy(t):
    'Start : STRATEGY NAME COLON statement_group'
    names[t[1]] = t[2]
    t[0] = t[4]


def p_strategy_statement_group(t):
    'statement_group : statement'
    t[0] = t[1]


def p_strategy_multi_statement_group(t):
    'statement_group : statement_group SEMI statement'
    t[0] = t[3]


def p_statement_assign(t):
    'statement : NAME ASSIGN expression'
    names[t[1]] = t[3]
    t[0] = t[3]


def p_statement_return(t):
    'statement : RETURN expression'
    t[0] = t[2]


def p_statement_if(t):
    'statement : IF expression LBRACE statement_group RBRACE'
    if(t[2] >= 1):
        t[0] = t[4]


def p_statement_elseif(t):
    'statement : IF expression LBRACE statement_group RBRACE ELSE LBRACE statement_group RBRACE'
    if(t[2] >= 1):
        t[0] = t[4]
    else:
        t[0] = t[8]


def p_expression_and(t):
    'expression : expression AND compexpr'
    if(t[1] == 1 and t[3] == 1):
        t[0] = 1
    else:
        t[0] = 0


def p_expression_compexpr(t):
    'expression : compexpr'
    t[0] = t[1]


def p_compexpr_lt(t):
    'compexpr : compexpr LT expr'
    if(t[1] < t[3]):
        t[0] = 1
    else:
        t[0] = 0


def p_compexpr_eq(t):
    'compexpr : compexpr EQ expr'
    if(t[1] == t[3]):
        t[0] = 1
    else:
        t[0] = 0


def p_compexpr_expr(t):
    'compexpr : expr'
    t[0] = t[1]


def p_expr_plus(t):
    'expr : expr PLUS term'
    t[0] = t[1] + t[3]


def p_expr_minus(t):
    'expr : expr MINUS term'
    t[0] = t[1] - t[3]


def p_expr_term(t):
    'expr : term'
    t[0] = t[1]


def p_term_times(t):
    'term : term TIMES factor'
    t[0] = t[1] * t[3]


def p_term_divide(t):
    'term : term DIVIDE factor'
    t[0] = t[1] / t[3]


def p_term_factor(t):
    'term : factor'
    t[0] = t[1]


def p_factor_random(t):
    'factor : RANDOM LPAREN NUMBER RPAREN'
    t[0] = random.randint(0, t[3])


def p_factor_group(t):
    'factor : LPAREN expression RPAREN'
    t[0] = t[2]


def p_factor_number(t):
    'factor : NUMBER'
    t[0] = t[1]


def p_factor_count(t):
    'factor : COUNT'
    t[0] = names['COUNT']


def p_factor_flag(t):
    'factor : FLAG'
    # 判断哨兵位置，哨兵为真则返回为真，哨兵为假则返回为假
    # if(flag):
    #     t[0] = 1 
    # else:
    #     t[0] = 0
    t[0] = names['FLAG']


def p_factor_cur(t):
    'factor : CUR'
    t[0] = names['LCUR']


def p_factor_name(t):
    'factor : NAME'
    global exceptions
    try:
        if(t[1] == 'LCUR'):
            print("Existed name can't use LCUR")
        elif(t[1] == 'COUNT'):
            print("Existed name can't use COUNT")
        else:
            t[0] = names[t[1]]
    except LookupError:
        exceptions.append(str("Undefined name '%s'" % t[1]))
        t[0] = 0


def p_error(t):
    global exceptions
    exceptions.append(str("Syntax error at '%s'" % t.value))


# Build the parser
parser = yacc.yacc()
