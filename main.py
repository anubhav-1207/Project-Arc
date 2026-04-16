from lexer import Lexer

# invalid file type error class
class InvalidFileType(Exception):
    def __init__(self,message):
        super().__init__(f"{message}")

# invalid command error class
class InvalidCommand(Exception):
    def __init__(self,message):
        super().__init__(f"{message}")

#infinite loop for infinite number of inputs
while True:
    userInput = input("~$ : ")
    userInput = userInput.strip().split() #strip and split to parse 
    name = userInput[0] #store the first word in variable

    if name == 'arc' and userInput[1] == 'exec': # if the command starts with 'arc exec'
        filepath = userInput[2] #get the file path or name
        if filepath.endswith('.arc'): # check for correct file extension
            with open(filepath,'r') as file: #open the file
                source = file.read()  #store the source code in source
                lexer = Lexer(source) #call the lexer class from lexer.py
                tokens = lexer.tokenize() # tokenise the lexer
                for tok in tokens: 
                    print(tok) #print the tokens
        else:
            raise InvalidFileType(f"unsupported  file type - couldn't parse '{filepath}'")#

    else:
        raise InvalidCommand(f"command not recognised - please recheck")
