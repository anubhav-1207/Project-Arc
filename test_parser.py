from lexer import Lexer
from parser import Parser

# Test 1: Simple number
code1 = "5"
lexer1 = Lexer(code1)
tokens1 = lexer1.tokenize()
print("Tokens:", tokens1)

parser1 = Parser(tokens1)
ast1 = parser1.parse_factor()
print("AST:", ast1)
print()

# Test 2: Unary operator
code2 = "-5"
lexer2 = Lexer(code2)
tokens2 = lexer2.tokenize()
print("Tokens:", tokens2)

parser2 = Parser(tokens2)
ast2 = parser2.parse_unary()
print("AST:", ast2)
print()

# Test 3: Expression with operators
code3 = "(5 + 3) * 2"
lexer3 = Lexer(code3)
tokens3 = lexer3.tokenize()
print("Tokens:", tokens3)

parser3 = Parser(tokens3)
ast3 = parser3.parse_expression()
print("AST:", ast3)