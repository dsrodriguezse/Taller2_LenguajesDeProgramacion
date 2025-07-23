class PrintVisitor(ASTVisitor):
    def __init__(self, indent=0):
        self.indent = indent
    
    def _print(self, text):
        print('  ' * self.indent + text)
    
    def visit_program(self, node):
        self._print('Program:')
        self.indent += 1
        for stmt in node.statements:
            self.visit(stmt)
        self.indent -= 1
    
    def visit_declaration(self, node):
        self._print(f'Declaration: {node.identifier} : {node.type}')
        if node.value:
            self.indent += 1
            self.visit(node.value)
            self.indent -= 1
    
    def visit_binaryoperation(self, node):
        self._print(f'BinaryOp: {node.op}')
        self.indent += 1
        self.visit(node.left)
        self.visit(node.right)
        self.indent -= 1
    
    def visit_integerliteral(self, node):
        self._print(f'Integer: {node.value}')
    
    # ... implementar los demás métodos visit_*