#mylexer.py 
TT_EOF = "EOF"
TT_INTEGER = "INTEGER"
TT_FLOAT = "FLOAT"
TT_STRING = "STRING"
TT_SLASH = "SLASH"
TT_STARSTAR = "STARSTAR"

#---Tokens-------------------------------------------------------------------------------------------------
class Token:
    """
    Structures all the token instances, the template for all the tokens, this is where  we input raw data about the tokens, it comes out as structured form ready to be appended to tokens list.
    """
    def __init__(self,type_,value,line):
        self.type_ = type_
        self.value = value 
        self.line = line 

    #Represents a formatted structure when printed instead of memory address.
    def __repr__(self):
        if self.value: #if the token has a value
            return f"({self.type_}:{self.value}, line = {self.line})" #return with type and its value
        else: #if it doesn't have a value
            return f"({self.type_}, line = {self.line})" #return only the type

#---LexerError-------------------------------------------------------------------------------------------
class LexerError(Exception):
    def __init__(self,message,line):
        super().__init__(f"{message} was found while parsing, line {line}")

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
    def current_char(self):
        """
        Returns the current character the pointer is at
        """

        if self.pos < len(self.source): #if the pointer is not after the end of the input
            return self.source[self.pos] #then, return the character on which the pointer is
        else: #if the pointer is after the end,
            return None #give None

    def peek(self) :
        """
        It gives the next char which we will go if we move one step, but 
        """
        if self.pos + 1 < len(self.source): #if the next pointer will not point to end upon succession
            return self.source[self.pos+1] #return the next value but don't store it 
        else:
            return None

    def advance(self):
        """
        Tells us which character it currently is on, and returns it, then moves one step ahead
        """
        char = self.source[self.pos] #store the value in a variable char
        self.pos += 1 #then move one step ahead

        if char == "\n": #if there is a line break, we need to update the line number
            self.line += 1 #increase the line number
        return char

    def add(self,type_,value=None):
        """
        Adds the value to the "tokens" list [line 10]
        """
        self.tokens.append(Token(type_,value,self.line))

    #---Main Tokenizer Function---------------------------------------------------------------------------------------------------
    def tokenize(self):
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
            
            #Ignore comments.
            elif char == '/' and self.peek() == '/': # //help me please :(
                while self.current_char() is not None and self.current_char() != '\n':
                    self.advance()

            




            else:
                raise LexerError(f"- Unknown character {char}",line = self.line)
                
                
                
        self.add(TT_EOF) #Always add EOF at the end.
        return self.tokens #return the list of tokens

    #---Number Readers---------------------------------------------        
    def read_numbers(self): 
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
            else:
                raise LexerError("Unterminated float literal - no digit after \'.\'",line = self.line)
            
            #if the current char is valid and a digit
            while self.current_char() is not None and self.current_char().isdigit():
                result.append(self.advance()) #add to list

        text = ''.join(result)

        if is_float:
            self.add(TT_FLOAT,float(text))
        else:
            self.add(TT_INTEGER,int(text))

    #---String Reader-------------------------------------------------------------------------------------------------------
    def read_strings(self,char): # "hello world"
             
            self.advance()
            result = []
            while self.current_char() is not None and self.current_char() != char:
                if self.current_char() == "\n":
                    raise LexerError("Unterminated string literal - newline inside string",line = self.line)
                result.append(self.advance())
            
            if self.current_char() is None:
                raise LexerError("Unterminated String Literal - EOF inside string",line = self.line)
            
            self.advance()
            text = ''.join(result)
            self.add(TT_STRING,text)


#---Testing------------------------
if __name__ == "__main__":
    source = """1234.122 123** 
    """
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    for tok in tokens:
        print(tok)