from enum import Enum

class TokenType(Enum):
    LBRACE = '{'
    RBRACE = '}'
    LBRACKET = '['
    RBRACKET = ']'
    COMMA = ','
    COLON = ':'
    STRING = 'STRING'
    NUMBER = 'NUMBER'
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    NULL = 'NULL'
    EOF = 'EOF'
    QUOTE = "\""

    def __eq__(self, other : str):
        return other == self.value


class Token:
    def __init__(self, type_ : TokenType, value : str=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value is not None:
            return f'Token({self.type}, {self.value})'
        return f'Token({self.type})'
    
    def __eq__(self, other : str):
        return other == self.type
    
    def get_token_value(self):
        return self.value