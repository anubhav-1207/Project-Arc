class ASTNodes: #parent class, all others inherit this 
    pass

class IntegerLiteral(ASTNodes): #only stores the value of the integer
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"{self.value}"

class Identifier(ASTNodes): #only stores the name of the identifier
    def __init__(self,name):
        self.name = name 

    def __repr__(self):
        return f"Identifier({self.name})"


class StringLiteral(ASTNodes): #only stores the value of the string literal
    def __init__(self,value):
        self.value = value 
    
    def __repr__(self):
        return f"String({self.value})"

class BooleanLiteral(ASTNodes): #only stores either true or false
    def __init__(self,value):
        self.value = value 

    def __repr__(self):
        return f"Bool({self.value})"

class NullLiteral(ASTNodes): #doesn't store anything 
    def __repr__(self):
        return f"Null()"

class ArrayLiteral(ASTNodes): #stores the elements 
    def __init__(self,elements):
        self.elements = elements 
    
    def __repr__(self):
        elements_str = ", ".join(str(elem) for elem in self.elements)
        return f"Array({elements_str})"

class BinaryOp(ASTNodes): #stores the left, right value and the operator 
    def __init__(self,left,op,right):
        self.left = left
        self.op = op
        self.right = right 

    def __repr__(self):
        return f"BinOp({self.left} {self.op} {self.right})"

class UnaryOp(ASTNodes): #stores the operator and the value 
    def __init__(self,op,value):
        self.op = op
        self.value = value 

    def __repr__(self):
        return f"UnaryOp({self.op}{self.value})"

class Assignment(ASTNodes): #stores the target to assign and the value to assign 
    def __init__(self,target,value):
        self.target = target 
        self.value = value 

    def __repr__(self):
        return f"Assignment({self.target} = {self.value})"

class Declaration(ASTNodes): #stores the name, value, and maintains a srare if its a constant 
    def __init__(self,name,value,is_const = False):
        self.name = name 
        self.value = value 
        self.is_const = is_const

    def __repr__(self):
        kind = "const" if self.is_const else "dec"
        return f"{kind} {name} = {value}"

class FunctionCall(ASTNodes): #stores the function name and arguements
    def __init__(self,name,arguements):
        self.name = name 
        self.arguements = arguements

    def __repr__(self):
        arg_str = ", ".join(str(arg) for arg in self.arguements)
        return f"{self.name} {arg_str}"

class IfStatement(ASTNodes): #stores the expression to check for, the then body, elif and else clauses if any
    def __init__(self,condition,then_part,elif_part = None ,else_part = None):
        self.condition = condition
        self.then_part = then_part
        self.elif_part = elif_part or [] #so later we don't get an error saying can't iterate over None so we initialise an empty list
        self.else_part = else_part or []

    def __repr__(self):
        return f"If({self.condition})"

class LoopStatement(ASTNodes): #only stores the loop body
    def __init__(self,body):
        self.body = body

    def __repr__(self):
        return f"Loop({self.body})"

class ForStatement(ASTNodes):
    def __init__(self,variable,iterable,body):
        self.variable = variable
        self.iterable = iterable
        self.body = body

    def __repr__(self):
        return f"For({self.variable} in {self.iterable}: {self.body})"

class FuncDef(ASTNodes):
    def __init__(self,name,arguements,body):
        self.name = name
        self.arguements = arguements
        self.body = body

    def __repr__(self):
        arg_str = ", ".join(str(arg) for arg in self.arguements)
        return f"FunctionCall({self.name}({arg_str}:{self.body}))"

class ReturnStatement(ASTNodes):
    def __init__(self,expression):
        self.expression = expression

    def __repr__(self):
        return f"Return({self.expression})"

class BreakStatement(ASTNodes):
    def __repr__(self):
        return f"Break()"

class SkipStatement(ASTNodes):
    def __repr__(self):
        return f"Skip()"

class OutStatement(ASTNodes):
    def __init__(self,expression):
        self.expression = expression

    def __repr__(self):
        return f"Out({self.expression})"

class PromptStatement(ASTNodes):
    def __init__(self,variable):
        self.variable = variable 

    def __repr__(self):
        return f"Prompt({self.variable})"

class TryStatement(ASTNodes):
    def __init__(self,try_body,catch_body):
        self.try_body = try_body 
        self.catch_body = catch_body
    
    def __repr__(self):
        return f"Try({self.try_body}\nCatch({self.catch_body}))"

class IndexAccess(ASTNodes):
    def __init__(self,array,index):
        self.array = array
        self.index = index 

    def __repr__(self):
        return f"IndexAccess({self.array}[{self.index}])"

