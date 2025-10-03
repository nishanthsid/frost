from ftoken import Token, TokenType
from typing import List

class TokenStream:
    def __init__(self):
        self.tokens = []
        self.position = 0
    
    def push_token(self, token : Token):
        self.tokens.append(token)
    
    def pop_token(self) -> Token:
        if self.position < len(self.tokens):
            token = self.tokens[self.position]
            self.position += 1
            return token
        return Token(TokenType.EOF)
    