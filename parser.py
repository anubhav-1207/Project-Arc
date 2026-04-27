# parser.py
#====================================================================================================
# Goes through the flat list of tokens and creates an AST to create hierarchy of operators like '*' before '+'
#====================================================================================================

#---Importing Dependencies----------------------------------------------------------------------------------------
from lexer import *
from ast_nodes import *
#--------------------------------------------------------------------------------------------------

# parser class contains all the methods required to parse the tokens 
class Parser:
    def __init__(self,tokens): # Parser needs only "tokens" as input 
        self.tokens = tokens 
        self.pos = 0 #create a pointer to for easier manipulation
        self.current_token = self.tokens[0] if tokens else None #store the current token
    
    #---Advance------------------------------------------------------------------------------
    def advance(self): #moves one charac ahead and returns the character it just moved over
        self.pos += 1 
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None 

    #---Peek---------------------------------------------------------------------------------
    def peek(self):
        if self.pos + 1 < len(self.tokens): 
            return self.tokens[self.pos+1]
        else:
            return None

    #---Match-----------------------------------------------------------------------------------
    def match(self, *token_types): 
        """
        Checks if the current token type is in the given parameters of token types.
        """
        return self.current_token.type_ in token_types
        
    #---Expect---------------------------------------------------------------------------------
    def expect(self,token_type): 
        """
        Checks if the token type matches the expected token type.
        """
        if self.match(token_type):
            tok = self.current_token
            self.advance()
            return tok
        else:
            print("error")

    #---Parse Factor--------------------------------------------------------------------------    
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

    #---Parse Unary-----------------------------------------------------------------------
    def parse_unary(self): # -5, !7
        if self.current_token.type_ in (TT_MINUS,TT_BANG): #if the token is - or !
            op = self.current_token #store the operator in a variable 
            self.advance() 
            value = self.parse_unary() #get the value by recursion because the it can be -5 or -(x+y)
            return UnaryOp(op, value)
        
        else:
            return self.parse_factor() #if the token is not - or !, it is not unary, fall back to parse it as a factor

    #---Parse Term (* / %)-------------------------------------------------------------------------
    def parse_term(self): # 5 + 7 * 8
        left = self.parse_unary()

        while self.current_token.type_ in (TT_STAR,TT_BANG,TT_PERCENT):
            op = self.current_token
            self.advance()
            right = self.parse_unary()
            left = BinaryOp(left,op,right)
        return left

    #---Parse Expression------------------------------------------------------------------
    def parse_expression(self):
        left = self.parse_term()
    
        while self.current_token.type_ in (TT_PLUS, TT_MINUS):
            op = self.current_token
            self.advance()
            right = self.parse_term()
            left = BinaryOp(left, op, right)
        return left

    #---Parse Statement--------------------------------------------------------------------
    def parse_statement(self):
        token_type = self.current_token.type_

        if token_type == TT_KEYWORD:
            keyword = self.current_token.value
            if keyword == "dec" or keyword == "const":
                return self.parse_declaration()
            elif keyword == "if":
                return self.parse_if()
            elif keyword == "loop":
                return self.parse_loop()
            elif keyword == "for":
                return self.parse_for()
            elif keyword == "return":
                return self.parse_return()
            elif keyword == "break":
                return self.parse_break()
            elif keyword == "skip":
                return self.parse_skip()
            elif keyword == "out":
                return self.parse_out()
            elif keyword == "prompt":
                return self.parse_prompt()
            elif keyword == "try":
                return self.parse_try()
            
            else:
                return self.parse_expression()
