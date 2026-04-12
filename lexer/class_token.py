#class_token.py 

#Initialise the class
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
            return f"{self.type_}:{self.value}" #return with type and its value
        else: #if it doesn't have a value
            return f"{self.type_}" #return only the type