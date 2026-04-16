#lexer.py 
#---Token Types----------------------------------------------------------------------------------------------
TT_INTEGER    = 'INTEGER'
TT_FLOAT      = 'FLOAT'
TT_STRING     = 'STRING'
TT_BOOL       = 'BOOL'
TT_NULL       = 'NULL'
TT_IDENT      = 'IDENT'
TT_KEYWORD    = 'KEYWORD'

TT_PLUS       = 'PLUS'        # +
TT_MINUS      = 'MINUS'       # -
TT_STAR       = 'STAR'        # *
TT_SLASH      = 'SLASH'       # /
TT_PERCENT    = 'PERCENT'     # %
TT_STARSTAR   = 'STARSTAR'    # **
TT_EQ         = 'EQ'          # =
TT_EQEQ       = 'EQEQ'        # ==
TT_NEQ        = 'NEQ'         # !=
TT_LT         = 'LT'          # 
TT_GT         = 'GT'          # >
TT_LTE        = 'LTE'         # <=
TT_GTE        = 'GTE'         # >=
TT_AND        = 'AND'         # &&
TT_OR         = 'OR'          # ||
TT_BANG       = 'BANG'        # !
TT_LPAREN     = 'LPAREN'      # (
TT_RPAREN     = 'RPAREN'      # )
TT_LBRACE     = 'LBRACE'      # {
TT_RBRACE     = 'RBRACE'      # }
TT_LBRACKET   = 'LBRACKET'    # [
TT_RBRACKET   = 'RBRACKET'    # ]
TT_COMMA      = 'COMMA'       # ,
TT_DOT        = 'DOT'         # .
TT_COLON      = 'COLON'       # :
TT_SEMICOLON  = 'SEMICOLON'   # ;
TT_EOF        = 'EOF'

#---Keywords----------------------------------------------------------------------------------------------
KEYWORDS = {
    'dec', 'const', 'func', 'return',
    'if', 'else', 'elif',
    'loop', 'for', 'in', 'break', 'skip',
    'out', 'prompt',
    'true', 'false', 'null',
    'use', 'type', 'init', 'ext',
    'try', 'catch', 'drop'
}

#---Tokens-------------------------------------------------------------------------------------------------
class Token:
    """
    Structures all the token instances, the template for all the tokens, this is where  we input raw data about the tokens, it comes out as structured form ready to be appended to tokens list.
    """
    def __init__(self,type_,value,line):
        self.type_ = type_
        self.value = value 
        self.line = line 

    # Represents a formatted structure when printed instead of memory address.
    def __repr__(self):
        if self.value is not None: #if the token has a value
            return f"({self.type_}:{self.value}, line = {self.line})" #return with type and its value
        else: #if it doesn't have a value
            return f"({self.type_}, line = {self.line})" #return only the type

#---LexerError-------------------------------------------------------------------------------------------
class LexerError(Exception):
    def __init__(self,message,line):
        super().__init__(f"{message}, line {line}")

#---Lexer-------------------------------------------------------------------------------------------------
class Lexer:
    """
    It categorises raw input into tokens, it goes through each character, checks each individually and gives the proper type of output. Takes only the source input as arguement
    """

    def __init__(self,source):
        self.source = source
        self.pos = 0 #the current index at the input
        self.line = 1 #line number of the input
        self.tokens = [] #will store the tokens 

    #---Lexer Methods---------------------------------------
    def current_char(self) -> str:
        """
        Returns the current character the pointer is at
        """

        if self.pos < len(self.source): #if the pointer is not after the end of the input
            return self.source[self.pos] #then, return the character on which the pointer is
        else: #if the pointer is after the end,
            return None #give None

    def peek(self) -> str :
        """
        It gives the next char which we will go if we move one step, but 
        """
        if self.pos + 1 < len(self.source): #if the next pointer will not point to end upon succession
            return self.source[self.pos+1] #return the next value but don't store it 
        else:
            return None

    def advance(self) -> str:
        """
        Tells us which character it currently is on, and returns it, then moves one step ahead
        """
        char = self.source[self.pos] #store the value in a variable char
        self.pos += 1 #then move one step ahead

        if char == "\n": #if there is a line break, we need to update the line number
            self.line += 1 #increase the line number
        return char # and return the character

    def add(self,type_,value=None) -> Token:
        """
        Adds the value to the "tokens" list [line 10]
        """
        self.tokens.append(Token(type_,value,self.line)) #add the token

    #---Main Tokenizer Function---------------------------------------------------------------------------------------------------
    def tokenize(self) -> list:
        """
        The main method which checks and categorises the tokens.
        """
        while self.current_char() is not None: 
            char = self.current_char()

            # Skip whitespaces
            if char.isspace():
                self.advance()
            
            # Check for numbers
            elif char.isdigit():
                self.read_numbers()
            
            # String mode when " is found
            elif char == '"' or char == "'":
                self.read_strings(char)

            # Identifier or Keyword
            elif char.isalnum() or char == '_':
                self.read_ident()
            
            #Ignore comments.
            elif char == '/' and self.peek() == '/': # //help me please :(
                while self.current_char() is not None and self.current_char() != '\n':
                    self.advance()

            #---Multicharacter Tokens-------------------------------------------------------------
            #---Stars-------------
            elif char == '*':#**
                if self.peek() == '*':
                    self.add(TT_STARSTAR,'**')
                    self.advance()
                    self.advance()
                else:
                    self.add(TT_STAR,'*')
                    self.advance()
            
            #---Equals-------------
            elif char == '=':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    self.add(TT_EQEQ,'==')
                else:
                    self.advance()
                    self.add(TT_EQ,'=')
            
            #---Greater Thans-----------------
            elif char == '>':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    self.add(TT_GTE,'>=')
                else:
                    self.advance()
                    self.add(TT_GT,'>')
            
            #---Less Thans-------------------
            elif char == '<':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    self.add(TT_LTE,'<=')
                else:
                    self.advance()
                    self.add(TT_LT,'<')

            #---Bangs----------------------
            elif char == '!':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    self.add(TT_NEQ,'!=')
                else:
                    self.advance()
                    self.add(TT_BANG,'!')
           
            #---And-----------------------
            elif char == '&':
                if self.peek() == '&':
                    self.advance()
                    self.advance()
                    self.add(TT_AND,'&&')
                else:
                    raise LexerError("unexpected '&' - did you mean '&&'?",self.line)
            #---OR-----------------------
            elif char == '|':
                if self.peek() == '|':
                    self.advance()
                    self.advance()
                    self.add(TT_OR,'||')
                else:
                    raise LexerError("unexpected '|' - did you mean '||'?",self.line)

            #---Single Character Operators-----------------------------------------------------
            elif char == '+':self.advance();self.add(TT_PLUS,'+')
            elif char == '-':self.advance();self.add(TT_MINUS,'-')
            elif char == '%':self.advance();self.add(TT_PERCENT,'%')
            elif char == '(':self.advance();self.add(TT_LPAREN,'(')
            elif char == ')':self.advance();self.add(TT_RPAREN,')')
            elif char == '{':self.advance();self.add(TT_LBRACE,'{')
            elif char == '}':self.advance();self.add(TT_RBRACE,'}')
            elif char == '[':self.advance();self.add(TT_LBRACKET,'[')
            elif char == ']':self.advance();self.add(TT_RBRACKET,']')
            elif char == '.':self.advance();self.add(TT_DOT,'.')
            elif char == ',':self.advance();self.add(TT_COMMA,',')
            elif char == ':':self.advance();self.add(TT_COLON,':')
            elif char == ';':self.advance();self.add(TT_SEMICOLON,';')
            #---------------------------------------------------------------------------------

            #---Unknown Character Error--------------------------------------------------------------------
            else:
                raise LexerError(f"- Unknown character {char}",line = self.line)

        #---Always Add EOF-----------------------------------------------------------------------      
        self.add(TT_EOF) #Always add EOF at the end.
        return self.tokens #return the list of tokens

#---------------------------------------------------------------------------------------------------------------------
    #---Number Readers---------------------------------------------        
    def read_numbers(self)-> Token: 
        """
        Reads the numbers and classifies as integer or float.
        """
        result = [] #create an empty list
        is_float = False #init a var to store float state
        while self.current_char() is not None and self.current_char().isdigit(): #if the current char is valid and a digit
            result.append(self.advance()) #append it to list result
        
        if self.current_char() == '.':  #if you get a '.'
            if self.peek() is not None and self.peek().isdigit():
                is_float = True #set float state to true
                result.append(self.advance()) #append '.' and move
            
            #if the current char is valid and a digit
            while self.current_char() is not None and self.current_char().isdigit():
                result.append(self.advance()) #add to list

        text = ''.join(result) #join the list into a string 
        if is_float:
            self.add(TT_FLOAT,float(text)) # is it is a float, term as float
        else:
            self.add(TT_INTEGER,int(text)) # else integers
#-------------------------------------------------------------------------------------------------------------------------
    #---String Reader-------------------------------------------------------------------------------------------------------
    def read_strings(self,char) -> Token: # "hello world"
            """
            Called when a ' or " is spotted and continues consuming until another " found.
            """
             
            self.advance() # move over the first " and reach the first char
            result = [] # to store the chars into 
            while self.current_char() is not None and self.current_char() != char: # loop until the current char is not none and the current char is not ' or "
                if self.current_char() == "\n":
                    raise LexerError("Unterminated string literal - newline inside string",line = self.line) # error if there is a newline before closing ' or "
                result.append(self.advance()) #append the chars into result
            
            if self.current_char() is None: # if the current char is None
                raise LexerError("Unterminated String Literal - EOF inside string",line = self.line) #another error
            
            self.advance() #move over the ' or ""
            text = ''.join(result) #join the list into string
            self.add(TT_STRING,text) #add into tokens class

#------------------------------------------------------------------------------------------
    #---Identifier/Keyword Reader----------------------------------------------
    def read_ident(self) -> Token:
        """
        Given a word, it declares if it is a keyword or an identifier
        """
        result = []
        while self.current_char() is not None and self.current_char().isalnum(): #loop until the curr char is an alphanum
            result.append(self.advance()) #consume the char and append and move ahead
        
        text = ''.join(result) # join the list into string

        if text in KEYWORDS: # if the text is a keyword
            self.add(TT_KEYWORD,text)
        else:
            self.add(TT_IDENT,text) #if an identifier

#----------------------------------------------------------------------------------------
if __name__ == '__main__':
    source  = "dec x = 293923542865978265928376592783659278364592783659178;"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    for tok in tokens:
        print(tok)