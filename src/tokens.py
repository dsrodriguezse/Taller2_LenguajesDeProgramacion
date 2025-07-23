# Versión mejorada de tokens.py con validaciones
class Token:
    def __init__(self, type, value, lineno=None, lexpos=None):
        if not isinstance(type, str):
            raise ValueError("Token type must be a string")
            
        self.type = type
        self.value = value
        self.lineno = lineno if lineno is not None else 0
        self.lexpos = lexpos if lexpos is not None else 0
    
    def __str__(self):
        return f'Token(type={self.type}, value={repr(self.value)}, line={self.lineno}, position={self.lexpos})'
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return (self.type == other.type and 
                self.value == other.value)