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


def p_start_strategy(t):
    'Start : STRATEGY NAME COLON statement_group'
    t[0] = ('Strategy', t[2], t[4])


def p_strategy_statement_group(t):
    'statement_group : statement'
    t[0] = t[1]


def p_strategy_multi_statement_group(t):
    'statement_group : statement_group SEMI statement'
    t[0] = ('statement_group', t[3])


def p_statement_assign(t):
    'statement : NAME ASSIGN expression'
    names[t[1]] = t[3]
    t[0] = ('assign', t[1], t[3])


def p_statement_return(t):
    'statement : RETURN expression'
    t[0] = ('return', t[2])


def p_statement_if(t):
    'statement : IF LPAREN expression RPAREN LBRACE statement_group RBRACE'
    t[0] = ('if', t[3], 'then', t[6])


def p_statement_elseif(t):
    'statement : IF LPAREN expression RPAREN LBRACE statement_group RBRACE ELSE LBRACE statement_group RBRACE'
    t[0] = ('if', t[3], 'then', t[6], 'else', t[10])


def p_expression_and(t):
    'expression : expression AND compexpr'
    t[0] = ('and', t[1], t[3])


def p_expression_compexpr(t):
    'expression : compexpr'
    t[0] = t[1]


def p_compexpr_lt(t):
    'compexpr : compexpr LT expr'
    t[0] = ('lt', t[1], t[3])


def p_compexpr_eq(t):
    'compexpr : compexpr EQ expr'
    t[0] = ('eq', t[1], t[3])


def p_compexpr_expr(t):
    'compexpr : expr'
    t[0] = t[1]


def p_expr_plus(t):
    'expr : expr PLUS term'
    t[0] = ('+', t[1], t[3])


def p_expr_minus(t):
    'expr : expr MINUS term'
    t[0] = ('-', t[1], t[3])


def p_expr_term(t):
    'expr : term'
    t[0] = t[1]


def p_term_times(t):
    'term : term TIMES factor'
    t[0] = ('*', t[1], t[3])


def p_term_divide(t):
    'term : term DIVIDE factor'
    t[0] = ('/', t[1], t[3])


def p_term_factor(t):
    'term : factor'
    t[0] = t[1]


def p_factor_random(t):
    'factor : RANDOM LPAREN NUMBER RPAREN'
    t[0] = ('RANDOM', 0, t[3])


def p_factor_group(t):
    'factor : LPAREN expression RPAREN'
    t[0] = ('expression', t[2])


def p_factor_number(t):
    'factor : NUMBER'
    t[0] = ('NUM', t[1])


def p_factor_count(t):
    'factor : COUNT'
    t[0] = ('COUNT', 'count')


def p_factor_cur(t):
    'factor : CUR'
    t[0] = ('CUR', 'cur')


def p_factor_flag(t):
    'factor : FLAG'
    t[0] = ('FLAG', 'flag')


def p_factor_name(t):
    'factor : NAME'
    # global exceptions
    try:
        t[0] = names[t[1]]
        t[0] = ('ID', names[t[1]])
    except LookupError:
        e = str("Undefined name '%s'" % t[1])
        exceptions.append(e)
        t[0] = 0


def p_error(t):
    # global exceptions
    e = str("Syntax error at '%s'" % t)
    exceptions.append(e)


# Build the parser
parser = yacc.yacc()


class ParseTree(object):
    ''' 解析语法树
    '''

    def __init__(self, file_like_oject):
        exceptions = []
        self.exceptions = ''
        self.target = file_like_oject
        self.data = ''

    def parse(self):
        self.data = parser.parse(self.target)
        self.exceptions = exceptions.pop() if len(exceptions) > 0 else ''
        # print(self.data, '---', self.exceptions)
        if self.exceptions == '':
            return self.data
        return None
