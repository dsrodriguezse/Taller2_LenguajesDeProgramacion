import ply.lex as lex
from ply.lex import TOKEN

# Lista de tokens
tokens = [
    # Literales
    'LIT_INT', 'LIT_FLOAT', 'LIT_STRING', 'IDENTIFICADOR',
    
    # Palabras reservadas
    'IN', 'RANGE', 'IF', 'ELSE', 'ELIF', 'WHILE', 'FOR', 'RETURN', 
    'BREAK', 'CONTINUE', 'FN', 'BOOL', 'INT', 'FLOAT', 'STRING', 
    'TWOWAYMODEL', 'EFECTS', 'STREAK', 'TRUE', 'FALSE', 'NULL', 'PRINT',
    
    # Funciones estadísticas/matemáticas
    'MEAN', 'MAX', 'MIN', 'MEDIAN', 'MODE',
    'SIN', 'COS', 'TAN', 'SEC', 'CSC', 'COT',
    'SINH', 'COSH', 'TANH',
    
    # Operadores
    'OP_SUMA', 'OP_RESTA', 'OP_MULT', 'OP_DIV', 'OP_MOD', 'OP_POT', 'OP_MCTMZ',
    'OP_MENOR', 'OP_MENOR_IGUAL', 'OP_MAYOR', 'OP_MAYOR_IGUAL',
    'OP_IGUAL', 'OP_DIFERENTE', 'OP_AND', 'OP_OR', 'OP_NOT', 'OP_ASIGN',
    
    # Delimitadores
    'L_PARENTESIS', 'R_PARENTESIS', 'L_LLAVE', 'R_LLAVE',
    'L_CORCHETE', 'R_CORCHETE', 'COMA', 'PUNTO_COMA',
    'PUNTO', 'DOS_PUNTOS'
]

# Palabras reservadas
reserved = {
    'in': 'IN',
    'range': 'RANGE',
    'if': 'IF',
    'else': 'ELSE',
    'elif': 'ELIF',
    'while': 'WHILE',
    'for': 'FOR',
    'return': 'RETURN',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'fn': 'FN',
    'bool': 'BOOL',
    'int': 'INT',
    'float': 'FLOAT',
    'string': 'STRING',
    'twoWayModel': 'TWOWAYMODEL',
    'efects': 'EFECTS',
    'streak': 'STREAK',
    'true': 'TRUE',
    'false': 'FALSE',
    'null': 'NULL',
    'print': 'PRINT',
    'mean': 'MEAN',
    'max': 'MAX',
    'min': 'MIN',
    'median': 'MEDIAN',
    'mode': 'MODE',
    'sin': 'SIN',
    'cos': 'COS',
    'tan': 'TAN',
    'sec': 'SEC',
    'csc': 'CSC',
    'cot': 'COT',
    'sinh': 'SINH',
    'cosh': 'COSH',
    'tanh': 'TANH'
}

# Operadores COMPUESTOS primero (>=, <=, ==, etc.)
def t_OP_MENOR_IGUAL(t):
    r'<='
    return t

def t_OP_MAYOR_IGUAL(t):
    r'>='
    return t

def t_OP_IGUAL(t):
    r'=='
    return t

def t_OP_DIFERENTE(t):
    r'!='
    return t

# Expresiones regulares para tokens simples
# Operadores SIMPLES después
def t_OP_SUMA(t):
    r'\+'
    return t

def t_OP_RESTA(t):
    r'-'
    return t

def t_OP_MULT(t):
    r'\*'
    return t

def t_OP_DIV(t):
    r'/'
    return t

def t_OP_MOD(t):
    r'%'
    return t

def t_OP_POT(t):
    r'\^'
    return t

def t_OP_MCTMZ(t):
    r'~'
    return t

def t_OP_MENOR(t):
    r'<'
    return t

def t_OP_MAYOR(t):
    r'>'
    return t

def t_OP_AND(t):
    r'&'
    return t

def t_OP_OR(t):
    r'\|'
    return t

def t_OP_NOT(t):
    r'!'
    return t

def t_OP_ASIGN(t):
    r'='
    return t


# Con funciones:
def t_L_PARENTESIS(t):
    r'\('
    t.type = 'L_PARENTESIS'
    return t

# Delimitadores como funciones
def t_R_PARENTESIS(t):
    r'\)'
    t.type = 'R_PARENTESIS'
    return t

def t_L_LLAVE(t):
    r'\{'
    t.type = 'L_LLAVE'
    return t

def t_R_LLAVE(t):
    r'\}'
    t.type = 'R_LLAVE'
    return t

def t_L_CORCHETE(t):
    r'\['
    t.type = 'L_CORCHETE'
    return t

def t_R_CORCHETE(t):
    r'\]'
    t.type = 'R_CORCHETE'
    return t

def t_COMA(t):
    r','
    t.type = 'COMA'
    return t

def t_PUNTO_COMA(t):
    r';'
    t.type = 'PUNTO_COMA'
    return t

def t_PUNTO(t):
    r'\.'
    t.type = 'PUNTO'
    return t

def t_DOS_PUNTOS(t):
    r':'
    t.type = 'DOS_PUNTOS'
    return t
# Definiciones para manejar números, identificadores, strings, etc.
def t_LIT_FLOAT(t):
    r'(?<!\d)-?(0|[1-9][0-9]*)\.[0-9]+'  # Lookbehind para evitar conflicto
    t.value = float(t.value)
    return t

def t_LIT_INT(t):
    r'(?<!\d)-?(0|[1-9][0-9]*)'  # Lookbehind para evitar conflicto
    t.value = int(t.value)
    return t

def t_IDENTIFICADOR(t):
    r'[A-Za-zÑñ_ÁÉÍÓÚáéíóúÜü][A-Za-zÑñ_ÁÉÍÓÚáéíóúÜü0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFICADOR')  # Check for reserved words
    return t

def t_LIT_STRING(t):
    r'\"([^"\\]|\\.)*\"|\'([^\'\\]|\\.)*\''
    t.value = t.value[1:-1]  # Elimina las comillas exteriores
    return t

def t_TWOWAYMODEL(t):
    r'twoWayModel'
    return t

def t_EFECTS(t):
    r'efects'
    return t

def STREAK(t):
    r'streak'
    return t
# Comentarios (ignorados)
def t_ComentarioTradicional(t):
    r'\#[^\n]*'
    pass  # No return value. Token discarded

def t_ComentarioDocumentacion(t):
    r'\"\"\"(\\.|[^\\])*\"\"\"|\'\'\'(\\.|[^\\])*\'\'\''
    pass  # No return value. Token discarded

# Errores
def t_E_NUM_START_ZERO(t):
    r'0[0-9]+'
    print(f"Error léxico en línea {t.lineno}: Número inválido '{t.value}'")

def t_E_ID_START_DIGIT(t):
    r'[0-9]+[A-Za-zÑñ_ÁÉÍÓÚáéíóúÜü][A-Za-zÑñ_ÁÉÍÓÚáéíóúÜü0-9]*'
    print(f"ERROR LÉXICO (Línea {t.lineno}): Identificador no puede comenzar con dígitos: '{t.value}'")
    t.lexer.skip(len(t.value))  # Saltar todos los caracteres del identificador inválido
    return None  # No retornar token

# Caracteres ignorados (espacios, tabs, etc.)
t_ignore = ' \t'

# Manejo de saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en línea {t.lineno}")
    t.lexer.skip(1)

def t_E_SIMB_NOT_FOUND(t):
    r'[^\w\s]'  # Más restrictivo que antes
    # Verificar si ya fue capturado por otras reglas
    if t.value in {'+', '-', '*', '/', '%', '^', '~', '<', '>', '=', '!', '&', '|'}:
        print(f"ERROR INTERNO: Operador '{t.value}' no debió llegar aquí")
        t.lexer.skip(1)
        return None
    print(f"ERROR: Símbolo no permitido '{t.value}' en línea {t.lineno}")
    t.lexer.skip(1)
# Construir el lexer
lexer = lex.lex()