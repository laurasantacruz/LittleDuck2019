# Laura Santacruz Mayorga
# A01196377
# Diseño de compiladores

import ply.lex as lex
import ply.yacc as yacc
import sys

reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'print' : 'PRINT',
    'program' : 'PROGRAM',
    'var' : 'VAR',
    'int': 'INT',
    'float' : 'FLOAT'
}

'#lista de tokens'
tokens = [
   'CTEI', 'CTEF', 'ID',
   'PLUS', 'MINUS',
   'DIVIDE', 'MULTIPLY',
   'EQUALS',
   'OPENPAREN', 'CLOSEPAREN', 'DOT',
   'SEMICOLON', 'OPENCURL', 'CLOSECURL',
   'GREATER', 'LESS', 'DIFFERENT', 'CTESTRING', 'TWODOTS'
] + list(reserved.values())

'#tokens'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_EQUALS = r'\='
t_OPENPAREN = r'\('
t_CLOSEPAREN = r'\)'
t_DOT = r'\.'
t_SEMICOLON = r'\;'
t_TWODOTS = r'\:'
t_OPENCURL = r'\{'
t_CLOSECURL = r'\}'
t_GREATER = r'\>'
t_LESS = r'\<'
t_DIFFERENT = r'\<>'

t_ignore = r' '


def t_CTEF(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_CTEI(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_CTESTRING(t):
    r'[a-zA-Z]+'
    t.value = str(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("error: character not valid")
    t.lexer.skip(1)

lex.lex()


'#parsing rules'


'#programa'
def p_programa(p):
    '''
    programa : PROGRAM ID SEMICOLON vars bloque
            | PROGRAM ID SEMICOLON bloque
    '''
    p[0] = "PROGRAM COMPILED"


'#vars'
def p_vars(p):
    '''
    vars : VAR varsP
    '''

def p_varsP(p):
    '''
    varsP : ID TWODOTS tipo SEMICOLON
        | ID TWODOTS tipo TWODOTS varsP
        | ID DOT varsP
    '''

#tipo
def p_tipo(p):
    '''
    tipo : INT
         | FLOAT
    '''
    p[0] = p[1]

#bloque
def p_bloque(p):
    '''
    bloque : OPENCURL bloqueP CLOSECURL
    '''

def p_bloqueP(p):
    '''
    bloqueP : estatuto
            | estatuto bloqueP
            | empty
    '''

#estatuto
def p_estatuto(p):
    '''
    estatuto : asignacion
            | condicion
            | escritura
    '''

#asignacion
def p_asignacion(p):
    '''
    asignacion : ID EQUALS expresion SEMICOLON
    '''

#expresion
def p_expresion(p):
    '''
    expresion : exp expresionP
    '''

def p_expresionPrime(p):
    '''
    expresionP : LESS exp
            | GREATER exp
            | DIFFERENT exp
            | empty
    '''

#escritura
def p_escritura(p):
    '''
    escritura : PRINT OPENPAREN escrituraP CLOSEPAREN SEMICOLON
    '''

def p_escrituraPrime(p):
    '''
    escrituraP : expresion
            | expresion DOT escrituraP
            | CTESTRING
            | CTESTRING DOT
    '''

#condicion
def p_condicion(p):
    '''
    condicion : condicionP bloque SEMICOLON
            | condicionP bloque ELSE bloque SEMICOLON
    '''

def p_condicionP(p):
    '''
    condicionP : IF OPENPAREN expresion CLOSEPAREN
    '''

#exp
def p_exp(p):
    '''
    exp : termino expPrime
    '''

def p_expPrime(p):
    '''
    expPrime : PLUS exp
            | MINUS exp
            | empty
    '''

#termino
def p_termino(p):
    '''
    termino : factor terminoP
    '''

def p_terminoP(p):
    '''
    terminoP : MULTIPLY terminoP
            | DIVIDE terminoP
            | empty
    '''

#factor
def p_factor(p):
    '''
    factor : OPENPAREN expresion CLOSEPAREN
            | factorP
    '''

def p_factorP(p):
    '''
    factorP : PLUS varcte
            | MINUS varcte
            | varcte
    '''

#VARCTE
def p_varcte(p):
    '''
    varcte : ID
            | CTEI
            | CTEF
    '''

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

# Error rule for syntax errors
def p_error(p):
   print("Syntax error in input!")


# Build the parser
yacc.yacc()

# while True:
#   try:
#       s = input('> ')
#   except EOFError:
#       break
#   if not s: continue
#   result = yacc.parse(s)
#   print(result)


if __name__ == '__main__':
    try:
        arch_name = 'prueba2.txt'
        arch = open(arch_name,'r')
        print("Nombre de archivo a leer: " + arch_name)
        info = arch.read()
        # print(info)
        arch.close()
        if(yacc.parse(info, tracking=True) == 'PROGRAM COMPILED'):
            print("correct syntax")
        else:
            print("syntax error")
    except EOFError:
        print(EOFError)
