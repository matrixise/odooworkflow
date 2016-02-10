import ply.lex as lex
import textwrap

tokens = (
    'BOOLEAN_TRUE',
    'BOOLEAN_FALSE',
    'IDENTIFIER',
    'LBRACKET',
    'RBRACKET',
    'LPAREN',
    'RPAREN',
    'COMMA',
    'COLON',
    'DBLQUOTE3',
    'STRING',
    'ARROW',
)

t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON =  r':'
t_COMMA = r','
t_ARROW = r'->'
t_ignore = ' \t'




25502667



RESERVED = {
    'True': 'BOOLEAN_TRUE',
    'False': 'BOOLEAN_FALSE',
}

def t_STRING(t):
    r"\'.*\'"
    t.value = t.value[1:-1]
    return t

def t_DBLQUOTE3(t):
    r'\"\"\"(.|\n)*?\"\"\"'
    t.value = textwrap.dedent(t.value[3:-3]).strip()
    return t

def t_IDENTIFIER(t):
    r'[A-Za-z_][\.\w_\-]*'
    t.type = RESERVED.get(t.value, 'IDENTIFIER')
    if t.type == 'BOOLEAN_TRUE':
        t.value = True
    elif t.type == 'BOOLEAN_FALSE':
        t.value = False
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

def t_comments(t):
    r'\#.*'
    t.lineno += t.value.count('\n')

def t_error(t):
    raise SyntaxError("Unknown symbol %r" % (t.value[0], ))

lex.lex(debug=False)
