from lexer import *
from ast_nodes import *

class Parser:
    def __init__(self,tokens):
        self.tokens = tokens 
        self.pos = pos 
        self.current_token = self.tokens[0] if tokens else None

    def advance(self):
        self.pos += 1 
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None 

    def peek(self):
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos+1]
        else:
            return None

    def match(self, *token_types):
        return self.current_token.type_ in token_types
        
    def expect(self,token_type):
        if self.match(token_type):
            tok = self.current_token
            self.advance()
            return tok
        else:
            print("error")
        
    def parse_factor(self):
        if self.current_token.type_ in (TT_INTEGER,TT_FLOAT):
            val = self.current_token.value
            self.advance()
            return IntegerLiteral(val)
        
        elif self.current_token.type_ in (TT_STRING):
            val = self.current_token.value
            self.advance()
            return StringLiteral(val)
        
        elif self.current_token.type_ in (TT_BOOL):
            val = self.current_token.value
            self.advance()
            return BooleanLiteral(val)

        elif self.current_token.type_ in (TT_NULL):
            self.advance()
            return NullLiteral()

        elif self.current_token.type_ in (TT_IDENT):
            val = self.current_token.value
            self.advance()
            return Identifier(val)
        
        elif self.current_token.type_ in (TT_LPAREN):
            self.advance()
            expression = self.parse_expression()
            self.expect(TT_RPAREN)
            return expression 

        else:
            raise Exception("Invalid factor")
