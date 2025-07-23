import ply.yacc as yacc
from src.lexer import tokens, lexer
from src.my_ast import (
    Program, Declaration, MemberAccess, FunctionDeclaration, Parameter, Assignment,
    IfStatement, ElifBlock, WhileStatement, ForStatement, ForRangeStatement, ArrayAssignment,
    BinaryOperation, UnaryOperation, FunctionCall, Identifier, MatrixDeclaration, MatrixLiteral,
    IntegerLiteral, FloatLiteral, StringLiteral, BooleanLiteral,Literal,ArrayDeclaration,SpecialDeclaration
)
from math import sin, cos, tan, sinh, cosh, tanh  # Para funciones trigonométricas

# Precedencia de operadores
precedence = (
    ('left', 'OP_OR'),
    ('left', 'OP_AND'),
    ('right', 'OP_NOT'),
    ('nonassoc', 'OP_MENOR', 'OP_MENOR_IGUAL', 'OP_MAYOR', 'OP_MAYOR_IGUAL', 'OP_IGUAL', 'OP_DIFERENTE'),
    ('left', 'OP_SUMA', 'OP_RESTA'),
    ('left', 'OP_MULT', 'OP_DIV', 'OP_MOD'),
    ('right', 'OP_POT', 'OP_MCTMZ'),
    ('right', 'UMINUS'),
)

## ------------------------- Gramática Principal -------------------------

def p_program(p):
    '''program : statement_list'''
    p[0] = Program(p[1])

def p_expression(p):
    '''expression : primary_expression     
                 | expression OP_SUMA expression
                 | expression OP_RESTA expression
                 | expression OP_MULT expression
                 | expression OP_DIV expression
                 | expression OP_MOD expression
                 | expression OP_POT expression
                 | expression OP_MCTMZ expression
                 | OP_RESTA expression %prec UMINUS
                 | OP_NOT expression
                 | expression OP_MENOR expression
                 | expression OP_MENOR_IGUAL expression
                 | expression OP_MAYOR expression
                 | expression OP_MAYOR_IGUAL expression
                 | expression OP_IGUAL expression
                 | expression OP_DIFERENTE expression
                 | expression OP_AND expression
                 | expression OP_OR expression
                 | L_PARENTESIS expression R_PARENTESIS
                 | IDENTIFICADOR
                 | literal
                 | function_call
                 | trig_function
                 | stat_function
                 | special_operation'''
    
    # Operadores binarios
    if len(p) == 4 and p[2] in ['+', '-', '*', '/', '%', '^', '~', '<', '<=', '>', '>=', '==', '!=', '&', '|']:
        p[0] = BinaryOperation(p[1], p[2], p[3])
    
    # Operadores unarios
    elif len(p) == 3 and p[1] in ['-', '!']:
        p[0] = UnaryOperation(p[1], p[2])
    
    # Paréntesis
    elif len(p) == 4 and p[1] == '(':
        p[0] = p[2]
    
    # Identificadores y literales
    elif len(p) == 2:
        if isinstance(p[1], (IntegerLiteral, FloatLiteral, StringLiteral, BooleanLiteral)):
            p[0] = p[1]
        elif p.slice[1].type == 'IDENTIFICADOR':
            p[0] = Identifier(p[1])
    
    # Llamadas a funciones y operaciones especiales
    elif len(p) == 2 and isinstance(p[1], (FunctionCall, tuple)):
        p[0] = p[1]
        
def p_assignment_statement(p):
    '''assignment_statement : IDENTIFICADOR OP_ASIGN expression PUNTO_COMA'''
    p[0] = Assignment(Identifier(p[1]), p[3])

def p_array_assignment(p):
    '''array_assignment : IDENTIFICADOR L_CORCHETE expression R_CORCHETE OP_ASIGN array_literal PUNTO_COMA'''
    print(f"Asignando array: {p[1]}[{p[3]}] = {p[6]}")
    p[0] = ArrayAssignment(Identifier(p[1]), p[3], p[6])

def p_statement_list(p):
    '''statement_list : statement_list statement
                     | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_jump_statement(p):
    '''jump_statement : RETURN expression PUNTO_COMA
                     | RETURN PUNTO_COMA
                     | BREAK PUNTO_COMA
                     | CONTINUE PUNTO_COMA'''
    if p[1] == 'return':
        if len(p) == 4:  # return con expresión
            p[0] = ('return_stmt', p[2])
        else:  # return sin expresión
            p[0] = ('return_stmt', None)
    else:
        p[0] = (f'{p[1].lower()}_stmt',)  # break o continue

def p_expression_statement(p):
    '''expression_statement : expression PUNTO_COMA
                           | PUNTO_COMA'''  # Para sentencias vacías ";"
    if len(p) == 3:
        p[0] = p[1]  # Retorna la expresión
    else:
        p[0] = None  # Sentencia vacía

def p_print_statement(p):
    '''print_statement : PRINT L_PARENTESIS print_args R_PARENTESIS
                      | PRINT L_PARENTESIS R_PARENTESIS'''
    if len(p) == 5:
        p[0] = ('print', p[3])
    else:
        p[0] = ('print', [])


def p_print_args(p):
    '''print_args : print_args COMA expression
                 | expression'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_if_statement(p):
    '''if_statement : IF L_PARENTESIS expression R_PARENTESIS block'''
    p[0] = ('if', p[3], p[5])

def p_block(p):
    '''block : L_LLAVE statement_list R_LLAVE
                | statement'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = [p[1]]

def p_special_statement(p):
    '''special_statement : TWOWAYMODEL L_PARENTESIS expression R_PARENTESIS PUNTO_COMA
                        | EFECTS IDENTIFICADOR L_PARENTESIS argument_list R_PARENTESIS PUNTO_COMA
                        | STREAK L_PARENTESIS argument_list R_PARENTESIS PUNTO_COMA
                        | STREAK IDENTIFICADOR PUNTO_COMA'''  # 👈 nueva regla
    if p[1] == 'twoWayModel':
        p[0] = ('two_way_model', p[3])
    elif p[1] == 'efects':
        from src.my_ast import SpecialDeclaration
        p[0] = SpecialDeclaration(decl_type='efects', identifier=p[2], dimensions=p[4])
    elif p[1] == 'streak' and len(p) == 6:
        p[0] = ('streak', p[3])
    elif p[1] == 'streak' and len(p) == 4:
        from src.my_ast import SpecialDeclaration
        p[0] = SpecialDeclaration(decl_type='streak', identifier=p[2], dimensions=None)


def p_statement(p):
    '''statement : expression_statement
                | compound_statement
                | selection_statement
                | iteration_statement
                | jump_statement
                | function_declaration    
                | declaration_statement
                | assignment_statement
                | array_assignment
                | print_statement
                | if_statement
                | block
                | special_statement'''  # Para MODELODOSVIAS, EFECTOS, etc.
    p[0] = p[1]

## ------------------------- Declaraciones y Estructuras -------------------------

def p_declaration_statement(p):
    '''declaration_statement : variable_declaration
                            | array_declaration
                            | special_matrix_declaration'''
    p[0] = p[1]

def p_variable_declaration(p):
    '''variable_declaration : type_specifier IDENTIFICADOR OP_ASIGN expression PUNTO_COMA
                             | type_specifier IDENTIFICADOR PUNTO_COMA
                             | type_specifier IDENTIFICADOR L_PARENTESIS expression R_PARENTESIS PUNTO_COMA
                             | TWOWAYMODEL IDENTIFICADOR OP_ASIGN expression PUNTO_COMA'''
    if len(p) == 6 and p[3] == '=' and p[1] != 'twoWayModel':
        p[0] = Declaration(p[1], p[2], p[4])
    elif len(p) == 4:
        p[0] = Declaration(p[1], p[2])
    elif len(p) == 7:
        p[0] = ArrayDeclaration(p[1], p[2], p[4])
    elif p[1] == 'twoWayModel':
        print(f"Declaración especial: {p[2]} = {p[4]}")
        p[0] = Declaration('twoWayModel', p[2], p[4])



def p_type_specifier(p):
    '''type_specifier : INT
                     | FLOAT
                     | BOOL
                     | STRING'''
    p[0] = p[1]

def p_compound_statement(p):
    '''compound_statement : L_LLAVE statement_list R_LLAVE
                          | L_LLAVE R_LLAVE'''
    p[0] = p[2] if len(p) == 4 else []

# Reglas de producción
def p_parameter(p):
    '''parameter : type_specifier IDENTIFICADOR'''
    p[0] = Parameter(type=p[1], name=p[2])

def p_parameters(p):
    '''parameters : parameter
                 | parameters COMA parameter'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_function_declaration(p):
    '''function_declaration : FN IDENTIFICADOR L_PARENTESIS parameters R_PARENTESIS compound_statement
                           | FN IDENTIFICADOR L_PARENTESIS R_PARENTESIS compound_statement'''
    if len(p) == 7:
        p[0] = FunctionDeclaration(name=p[2], params=p[4], body=p[6])
    else:
        p[0] = FunctionDeclaration(name=p[2], params=[], body=p[5])

## ------------------------- Estructuras de Control -------------------------

def p_selection_statement(p):
    '''selection_statement : IF L_PARENTESIS expression R_PARENTESIS statement
                          | IF L_PARENTESIS expression R_PARENTESIS statement ELSE statement
                          | IF L_PARENTESIS expression R_PARENTESIS statement ELIF L_PARENTESIS expression R_PARENTESIS statement'''
    if len(p) == 6:
        p[0] = IfStatement(condition=p[3], true_block=p[5])
    elif len(p) == 8:
        p[0] = IfStatement(condition=p[3], true_block=p[5], false_block=p[7])
    else:
        p[0] = IfStatement(condition=p[3], true_block=p[5], 
                          elif_blocks=[ElifBlock(condition=p[7], block=p[9])])

def p_iteration_statement(p):
    '''iteration_statement : WHILE L_PARENTESIS expression R_PARENTESIS statement
                          | FOR L_PARENTESIS expression PUNTO_COMA expression PUNTO_COMA expression R_PARENTESIS statement
                          | FOR IDENTIFICADOR IN RANGE L_PARENTESIS expression COMA expression R_PARENTESIS statement'''
    if p[1] == 'while':
        p[0] = WhileStatement(condition=p[3], body=p[5])
    elif len(p) == 10 and p[3] == ';':
        p[0] = ForStatement(init=p[3], condition=p[5], update=p[7], body=p[9])
    else:
        p[0] = ForRangeStatement(var=p[2], start=p[6], end=p[8], body=p[10])

def p_key_value_pair(p):
    '''key_value_pair : expression DOS_PUNTOS expression'''
    p[0] = (p[1], p[3])

def p_array_access(p):
    '''array_access : IDENTIFICADOR L_CORCHETE expression R_CORCHETE
                   | array_access L_CORCHETE expression R_CORCHETE'''
    p[0] = ('array_access', p[1], p[3])

def p_property_access(p):
    '''property_access : IDENTIFICADOR PUNTO IDENTIFICADOR
                      | property_access PUNTO IDENTIFICADOR'''
    p[0] = ('property_access', p[1], p[3])



def p_trig_function(p):
    '''trig_function : SIN L_PARENTESIS expression R_PARENTESIS
                    | COS L_PARENTESIS expression R_PARENTESIS
                    | TAN L_PARENTESIS expression R_PARENTESIS
                    | SINH L_PARENTESIS expression R_PARENTESIS
                    | COSH L_PARENTESIS expression R_PARENTESIS
                    | TANH L_PARENTESIS expression R_PARENTESIS
                    | SEC L_PARENTESIS expression R_PARENTESIS
                    | CSC L_PARENTESIS expression R_PARENTESIS
                    | COT L_PARENTESIS expression R_PARENTESIS'''
    p[0] = ('trig_function', p[1], p[3])

## ------------------------- Funciones Estadísticas y Especiales -------------------------

def p_stat_function(p):
    '''stat_function : MEAN L_PARENTESIS argument_list R_PARENTESIS
                    | MEDIAN L_PARENTESIS argument_list R_PARENTESIS
                    | MODE L_PARENTESIS argument_list R_PARENTESIS
                    | STREAK L_PARENTESIS argument_list R_PARENTESIS
                    | EFECTS L_PARENTESIS argument_list R_PARENTESIS'''
    p[0] = ('stat_function', p[1], p[3])

def p_special_operation(p):
    '''special_operation : TWOWAYMODEL L_PARENTESIS expression R_PARENTESIS'''
    p[0] = ('two_way_model', p[3])

def p_special_matrix_declaration(p):
    '''special_matrix_declaration : TWOWAYMODEL IDENTIFICADOR L_CORCHETE dimensions R_CORCHETE PUNTO_COMA'''
    try:
        # Verificar que las dimensiones sean correctas
        if not isinstance(p[4]['rows'], int) or not isinstance(p[4]['cols'], int):
            raise ValueError("Las dimensiones deben ser enteros")
            
        # Verificar que los datos coincidan con las dimensiones
        data_node = p[4]['data']
        data = data_node.value if isinstance(data_node, Literal) else data_node

        if len(data) != p[4]['rows']:
            raise ValueError(f"Número de filas incorrecto. Esperado: {p[4]['rows']}, Obtenido: {len(data)}")

        for row in data:
            if len(row) != p[4]['cols']:
                raise ValueError(f"Número de columnas incorrecto. Esperado: {p[4]['cols']}, Obtenido: {len(row)}")

        
        print(f"twoWayModel creado: {p[2]} con dimensiones {p[4]['rows']}x{p[4]['cols']}")
        p[0] = MatrixDeclaration(p[2], p[4])
        
    except ValueError as e:
        print(f"Error en twoWayModel: {str(e)}")
        p_error(p)

def p_dimensions(p):
    '''dimensions : expression COMA expression COMA matrix_literal'''
    # Asegurarse de que las dimensiones sean valores numéricos
    rows = int(p[1].value) if hasattr(p[1], 'value') else int(p[1])
    cols = int(p[3].value) if hasattr(p[3], 'value') else int(p[3])
    
    matrix = p[5]
    if isinstance(matrix, MatrixLiteral):
        matrix_data = matrix.value
    else:
        matrix_data = matrix  # fallback por si algo no fue procesado como MatrixLiteral

    p[0] = {
        'rows': rows,
        'cols': cols,
        'data': matrix_data
    }

    print(f"Dimensiones procesadas: {rows} filas, {cols} columnas, datos: {p[5]}")

def p_row_list(p):
    '''row_list : row
                | row_list PUNTO_COMA row'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_row(p):
    '''row : expression
           | row COMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]
## ------------------------- Funciones y Llamadas -------------------------

def p_function_call(p):
    '''function_call : IDENTIFICADOR L_PARENTESIS argument_list R_PARENTESIS
                    | IDENTIFICADOR L_PARENTESIS R_PARENTESIS
                    | stat_function
                    | math_function
                    | special_operation'''
    if len(p) == 5:
        p[0] = FunctionCall(p[1], p[3])
    elif len(p) == 3:
        p[0] = FunctionCall(p[1], [])
    else:
        p[0] = p[1]

def p_argument_list(p):
    '''argument_list : argument_list COMA expression
                    | expression'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

## ------------------------- Expresiones Primarias -------------------------

def p_primary_expression(p):
    '''primary_expression : IDENTIFICADOR
                         | literal
                         | L_PARENTESIS expression R_PARENTESIS
                         | function_call
                         | member_access
                         | array_access     
                         | property_access
                         | key_value_pair
                         | matrix_literal
                         | trig_function'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_literal(p):
    '''literal : LIT_INT
               | LIT_FLOAT
               | LIT_STRING
                | NULL
               | TRUE
               | FALSE'''
    if p.slice[1].type == 'LIT_INT':
        p[0] = IntegerLiteral(p[1])
    elif p.slice[1].type == 'LIT_FLOAT':
        p[0] = FloatLiteral(p[1])
    elif p.slice[1].type == 'LIT_STRING':
        p[0] = StringLiteral(p[1])
    elif p.slice[1].type == 'TRUE':
        p[0] = BooleanLiteral(True)
    elif p.slice[1].type == 'FALSE':
        p[0] = BooleanLiteral(False)
        
def p_math_function(p):
    '''math_function : MAX L_PARENTESIS argument_list R_PARENTESIS
                    | MIN L_PARENTESIS argument_list R_PARENTESIS'''
    p[0] = ('math_function', p[1], p[3])

def p_array_declaration(p):
    '''array_declaration : type_specifier IDENTIFICADOR L_PARENTESIS expression R_PARENTESIS
                        | type_specifier IDENTIFICADOR L_PARENTESIS expression R_PARENTESIS OP_ASIGN array_literal'''
    if len(p) == 6:
        p[0] = ArrayDeclaration(p[1], p[2], p[4])
    else:
        p[0] = ArrayDeclaration(p[1], p[2], p[4], p[7])

def p_array_literal(p):
    '''array_literal : L_CORCHETE expression_list R_CORCHETE
                     | L_CORCHETE matrix_literal R_CORCHETE'''
    p[0] = p[2]

# Conserva solo UNA de estas definiciones (la más completa)
def p_matrix_literal(p):
    '''matrix_literal : L_CORCHETE row_list R_CORCHETE'''
    # Convertir las expresiones a valores numéricos
    processed_data = []
    for row in p[2]:
        processed_row = []
        for item in row:
            if hasattr(item, 'value'):
                processed_row.append(item.value)
            else:
                processed_row.append(item)
        processed_data.append(processed_row)
    
    print(f"Matriz literal procesada: {processed_data}")
    p[0] = FloatLiteral(processed_data)  # o usa Literal(processed_data, 'matrix')


def p_expression_list(p):
    '''expression_list : expression
                      | expression_list COMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_member_access(p):
    '''member_access : IDENTIFICADOR
                    | member_access PUNTO IDENTIFICADOR
                    | member_access L_CORCHETE expression R_CORCHETE
                    | member_access L_CORCHETE expression R_CORCHETE PUNTO IDENTIFICADOR'''
    if len(p) == 2:
        p[0] = MemberAccess(p[1])
    elif p[2] == '.':
        p[0] = MemberAccess(p[1], p[3])
    elif len(p) == 5:
        p[0] = MemberAccess(p[1], index=p[3])
    else:
        p[0] = MemberAccess(p[1], index=p[3], member=p[6])        
## ------------------------- Manejo de Errores -------------------------

def p_error(p):
    if p:
        if p.type == 'TWOWAYMODEL':
            print(f"Error de sintaxis en twoWayModel en línea {p.lineno}. Verifique las dimensiones y los datos.")
        else:
            print(f"Error de sintaxis en '{p.value}' (línea {p.lineno})")
    else:
        print("Error de sintaxis: fin de archivo inesperado")
# Construir el parser
parser = yacc.yacc(debug=False, write_tables=False)