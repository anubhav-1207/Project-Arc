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

        if self.pos < len(source): #if the pointer is not after the end of the input
            return self.source[self.pos] #then, return the character on which the pointer is
        else: #if the pointer is after the end,
            return None #give None

    def peek(self) :
        """
        It gives the next char which we will go if we move one step, but 
        """
        if self.current_char is not None and self.pos + 1 < len(source): #if the next pointer will not point to end upon succession
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

    def add(self):
        """
        Adds the value to the "tokens" list [line 10]
        """
        self.tokens.append(Token(type_,value,self.line))





    





    

    