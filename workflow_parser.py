import workflow_lexer
import ply.yacc as yacc

tokens = workflow_lexer.tokens


def p_program(p):
    """program : workflow"""
    p[0] = p[1]


def p_program_error(p):
    """program : error"""
    p[0] = None
    p.parser.error = 1


def p_workflow(p):
    """workflow : workflow_declaration LBRACKET statements RBRACKET"""
    parameters = []
    if len(p[1]) == 2:
        name, parameters = p[1]
    else:
        name = p[1][0]

    entities = p[3]

    p[0] = ('workflow', name, parameters, entities)
    #p[0] = Workflow(name, parameters=parameters, entities=entities)

def p_workflow_declaration(p):
    """workflow_declaration : identifier LPAREN parameters RPAREN"""
    # print('workflow_declaration', p[1], p[3])
    p[0] = (p[1], p[3])


def p_workflow_declaration_without_parameters(p):
    """workflow_declaration : identifier"""
    # print('p_workflow_declaration_without_parameters')
    p[0] = (p[1],)


def p_identifier(p):
    """identifier : IDENTIFIER"""
    p[0] = p[1]

def p_parameters(p):
    """parameters : parameters COMMA parameter"""
    p[0] = p[1] + [p[3]]

def p_parameters_2(p):
    """parameters : parameter"""
    p[0] = [p[1]]

def p_parameter(p):
    """parameter : identifier COLON value"""
    p[0] = (p[1], p[3])

def p_value(p):
    """value : IDENTIFIER
             | STRING
             | DBLQUOTE3
             | BOOLEAN_TRUE
             | BOOLEAN_FALSE"""
    p[0] = p[1]

def p_statements(p):
    """statements : statements statement"""
    p[0] = p[1] + [p[2]]

def p_statements_new_statement(p):
    """statements : statement"""
    if p[1] is None:
        p[0] = []
    else:
        p[0] = [p[1]]

def p_statement(p):
    """statement : activity
                 | transition
                 | empty"""
    p[0] = p[1]

def p_activity(p):
    """activity : activity_description LBRACKET parameters RBRACKET"""
    description, parameters = p[1], p[3]
    identifier, meta = description
    #p[0] = Activity(p[1], p[3])

    p[0] = ('activity', identifier, meta, parameters)

def p_activity_empty(p):
    """activity : activity_description LBRACKET RBRACKET"""
    identifier, meta = p[1]
    p[0] = ('activity', identifier, meta, [])

def p_activity_description(p):
    """activity_description : identifier LPAREN parameters RPAREN
                            | identifier"""
    if len(p) == 5:
        p[0] = (p[1], p[3])
    else:
        p[0] = (p[1], [])


def p_transition(p):
    """transition : transition_description LPAREN parameters RPAREN
                  | transition_description LBRACKET parameters RBRACKET
                  | transition_description LPAREN parameters RPAREN LBRACKET parameters RBRACKET
                  | transition_description"""
    parameters = []
    others = []
    src, dst = p[1]
    len_production = len(p)

    if len_production == 5:
        if p[2] == '(':
            others = p[3]
        elif p[2] == '{':
            parameters = p[3]
    elif len_production == 8:
        others = p[3]
        parameters = p[6]

    p[0] = ('transition', src, dst, others, parameters)

def p_transition_descrition(p):
    """transition_description : identifier ARROW identifier"""
    p[0] = p[1], p[3]

def p_empty(p):
    "empty : "

def p_error(p):
    if p:
        print("Syntax error at '{}'".format(p.value))
    else:
        print("Syntax error at EOF")

def parse(code):
    parser = yacc.yacc(debug=False)
    return parser.parse(code)
