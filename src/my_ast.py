class ASTNode:
    """Clase base para todos los nodos del AST"""
    def __init__(self, lineno=None, lexpos=None):
        self.lineno = lineno
        self.lexpos = lexpos
    
    def accept(self, visitor):
        """Método para implementar el patrón Visitor"""
        method_name = 'visit_' + self.__class__.__name__.lower()
        visitor_method = getattr(visitor, method_name, visitor.generic_visit)
        return visitor_method(self)

# ------------------------- Declaraciones -------------------------
class Program(ASTNode):
    def __init__(self, statements):
        super().__init__()
        self.statements = statements

class Declaration(ASTNode):
    def __init__(self, type_specifier, identifier, value=None):
        super().__init__()
        self.type = type_specifier
        self.identifier = identifier
        self.value = value

class Assignment(ASTNode):
    def __init__(self, identifier, expression):
        super().__init__()
        self.identifier = identifier
        self.expression = expression
class ArrayAssignment(ASTNode):
    def __init__(self, array_name, index, values):
        self.array_name = array_name
        self.index = index
        self.values = values
            
class FunctionDeclaration(ASTNode):
    def __init__(self, name, params, body):
        super().__init__()
        self.name = name
        self.params = params
        self.body = body

class Parameter(ASTNode):
    def __init__(self, type_specifier, identifier):
        super().__init__()
        self.type = type_specifier
        self.identifier = identifier

# ------------------------- Estructuras de Control -------------------------
class IfStatement(ASTNode):
    def __init__(self, condition, true_block, false_block=None, elif_blocks=None):
        super().__init__()
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block
        self.elif_blocks = elif_blocks or []

class ElifBlock(ASTNode):
    def __init__(self, condition, block):
        super().__init__()
        self.condition = condition
        self.block = block

class WhileStatement(ASTNode):
    def __init__(self, condition, body):
        super().__init__()
        self.condition = condition
        self.body = body

class ForStatement(ASTNode):
    def __init__(self, init, condition, update, body):
        super().__init__()
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

class ForRangeStatement(ASTNode):
    def __init__(self, var, start, end, body):
        super().__init__()
        self.var = var
        self.start = start
        self.end = end
        self.body = body

# ------------------------- Expresiones -------------------------
class BinaryOperation(ASTNode):
    def __init__(self, left, op, right):
        super().__init__()
        self.left = left
        self.op = op
        self.right = right

class UnaryOperation(ASTNode):
    def __init__(self, op, operand):
        super().__init__()
        self.op = op
        self.operand = operand

class FunctionCall(ASTNode):
    def __init__(self, name, args):
        super().__init__()
        self.name = name
        self.args = args

class Identifier(ASTNode):
    def __init__(self, name):
        super().__init__()
        self.name = name
        
class PropertyAccess(ASTNode):
    def __init__(self, object, property):
        super().__init__()
        self.object = object  
        self.property = property 

class ArrayAccess(ASTNode):
    def __init__(self, array, index):
        super().__init__()
        self.array = array  
        self.index = index 
class ArrayDeclaration(ASTNode):
    def __init__(self, type_specifier, identifier, size, value=None):
        self.type = type_specifier
        self.identifier = identifier
        self.size = size
        self.value = value

class SpecialDeclaration(ASTNode):
    def __init__(self, decl_type, identifier, dimensions):
        self.decl_type = decl_type  # 'modeloDosVias' o 'efectos'
        self.identifier = identifier
        self.dimensions = dimensions

class MemberAccess(ASTNode):
    def __init__(self, base, index=None, member=None):
        self.base = base
        self.index = index
        self.member = member

class MatrixDeclaration(ASTNode):
    def __init__(self, name, dimensions_or_data):
        self.name = name
        if isinstance(dimensions_or_data, dict):
            # Formato: [2,3,[3,2,4;1,3,2]]
            self.rows = dimensions_or_data['rows']
            self.cols = dimensions_or_data['cols']
            self.data = dimensions_or_data['data']
        else:
            # Formato: [3,2,4;1,3,2]
            self.data = dimensions_or_data
            self.rows = len(dimensions_or_data)
            self.cols = len(dimensions_or_data[0]) if self.rows > 0 else 0

# ------------------------- Literales -------------------------
class Literal(ASTNode):
    def __init__(self, value, type=None):
        super().__init__()
        self.value = value
        self.type = type

class IntegerLiteral(Literal):
    def __init__(self, value):
        super().__init__(value, 'int')

class FloatLiteral(Literal):
    def __init__(self, value):
        super().__init__(value, 'float')

class StringLiteral(Literal):
    def __init__(self, value):
        super().__init__(value, 'string')

class BooleanLiteral(Literal):
    def __init__(self, value):
        super().__init__(value, 'bool')
class MatrixLiteral(Literal):
    def __init__(self, value):
        super().__init__(value, 'matrix')
                
# ------------------------- Visitor Pattern -------------------------
class ASTVisitor:
    def visit(self, node):
        return node.accept(self)
    
    def generic_visit(self, node):
        raise NotImplementedError(f'No hay método visit_{node.__class__.__name__} definido')