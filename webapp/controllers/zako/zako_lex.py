import ply.lex as lex

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'return': 'RETURN',
    'Strategy': 'STRATEGY',
    'RANDOM': 'RANDOM',
    'CUR': 'CUR',
    'COUNT': 'COUNT',
    'FLAG': 'FLAG',
}

# List of token names.   This is always required
tokens = [
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'COLON',
    'SEMI',
    'ASSIGN',
    'EQ',
    'LT',
    'AND',
    'NAME'
] + list(reserved.values())

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_ASSIGN = r'='
t_EQ = r'=='
t_COLON = r'\:'
t_SEMI = r';'
t_LT = r'\<'
t_AND = r'\&\&'

# A regular expression rule with some action code


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'NAME')    # Check for reserved words
    return t

# Define a rule so we can track line numbers


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = " \t\n"

# Error handling rule


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()
