# lexer.py

# ── Token Types ──────────────────────────────────────────────
TT_INT        = 'INT'
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
TT_EOF        = 'EOF'

KEYWORDS = {
    'dec', 'const', 'func', 'return',
    'if', 'else', 'elif',
    'loop', 'for', 'in', 'break', 'skip',
    'out', 'prompt',
    'true', 'false', 'null',
    'use', 'type', 'init', 'ext',
    'try', 'catch', 'drop'
}


# ── Token ─────────────────────────────────────────────────────
class Token:
    def __init__(self, type_, value, line):
        self.type  = type_
        self.value = value
        self.line  = line

    def __repr__(self):
        return f'Token({self.type}, {self.value!r}, line={self.line})'


# ── Lexer Error ───────────────────────────────────────────────
class LexerError(Exception):
    def __init__(self, message, line):
        super().__init__(f'[Line {line}] LexerError: {message}')


# ── Lexer ─────────────────────────────────────────────────────
class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos    = 0          # current character index
        self.line   = 1          # current line number (for error messages)
        self.tokens = []

    # ── Helpers ──
    def current(self):
        """Return current char, or None if past end."""
        if self.pos < len(self.source):
            return self.source[self.pos]
        return None

    def peek(self):
        """Look one character ahead without consuming."""
        if self.pos + 1 < len(self.source):
            return self.source[self.pos + 1]
        return None

    def advance(self):
        """Consume current char and move forward."""
        ch = self.source[self.pos]
        self.pos += 1
        if ch == '\n':
            self.line += 1
        return ch

    def add(self, type_, value=None):
        self.tokens.append(Token(type_, value, self.line))

    # ── Main tokenize loop ──
    def tokenize(self):
        while self.current() is not None:
            ch = self.current()

            # Whitespace — skip silently
            if ch in ' \t\r\n':
                self.advance()

            # Single-line comment //
            elif ch == '/' and self.peek() == '/':
                while self.current() is not None and self.current() != '\n':
                    self.advance()

            # String literal
            elif ch == '"':
                self.read_string()

            # Number (int or float)
            elif ch.isdigit():
                self.read_number()

            # Identifier or keyword
            elif ch.isalpha() or ch == '_':
                self.read_ident()

            # Multi-char and single-char operators
            elif ch == '*':
                if self.peek() == '*':
                    self.advance(); self.advance()
                    self.add(TT_STARSTAR, '**')
                else:
                    self.advance()
                    self.add(TT_STAR, '*')

            elif ch == '=':
                if self.peek() == '=':
                    self.advance(); self.advance()
                    self.add(TT_EQEQ, '==')
                else:
                    self.advance()
                    self.add(TT_EQ, '=')

            elif ch == '!':
                if self.peek() == '=':
                    self.advance(); self.advance()
                    self.add(TT_NEQ, '!=')
                else:
                    self.advance()
                    self.add(TT_BANG, '!')

            elif ch == '<':
                if self.peek() == '=':
                    self.advance(); self.advance()
                    self.add(TT_LTE, '<=')
                else:
                    self.advance()
                    self.add(TT_LT, '<')

            elif ch == '>':
                if self.peek() == '=':
                    self.advance(); self.advance()
                    self.add(TT_GTE, '>=')
                else:
                    self.advance()
                    self.add(TT_GT, '>')

            elif ch == '&':
                if self.peek() == '&':
                    self.advance(); self.advance()
                    self.add(TT_AND, '&&')
                else:
                    raise LexerError("unexpected '&' — did you mean '&&'?", self.line)

            elif ch == '|':
                if self.peek() == '|':
                    self.advance(); self.advance()
                    self.add(TT_OR, '||')
                else:
                    raise LexerError("unexpected '|' — did you mean '||'?", self.line)

            # Simple single-char tokens
            elif ch == '+': self.advance(); self.add(TT_PLUS,     '+')
            elif ch == '-': self.advance(); self.add(TT_MINUS,    '-')
            elif ch == '/': self.advance(); self.add(TT_SLASH,    '/')
            elif ch == '%': self.advance(); self.add(TT_PERCENT,  '%')
            elif ch == '(': self.advance(); self.add(TT_LPAREN,   '(')
            elif ch == ')': self.advance(); self.add(TT_RPAREN,   ')')
            elif ch == '{': self.advance(); self.add(TT_LBRACE,   '{')
            elif ch == '}': self.advance(); self.add(TT_RBRACE,   '}')
            elif ch == '[': self.advance(); self.add(TT_LBRACKET, '[')
            elif ch == ']': self.advance(); self.add(TT_RBRACKET, ']')
            elif ch == ',': self.advance(); self.add(TT_COMMA,    ',')
            elif ch == '.': self.advance(); self.add(TT_DOT,      '.')
            elif ch == ':': self.advance(); self.add(TT_COLON,    ':')

            else:
                raise LexerError(f"unexpected character '{ch}'", self.line)

        self.add(TT_EOF)
        return self.tokens

    # ── Sub-readers ──
    def read_string(self):
        self.advance()  # consume opening "
        result = []
        while self.current() is not None and self.current() != '"':
            if self.current() == '\n':
                raise LexerError("unterminated string — newline inside string literal", self.line)
            result.append(self.advance())
        if self.current() is None:
            raise LexerError("unterminated string — reached end of file", self.line)
        self.advance()  # consume closing "
        self.add(TT_STRING, ''.join(result))

    def read_number(self):
        result = []
        is_float = False
        while self.current() is not None and self.current().isdigit():
            result.append(self.advance())
        if self.current() == '.' and self.peek() is not None and self.peek().isdigit():
            is_float = True
            result.append(self.advance())  # consume '.'
            while self.current() is not None and self.current().isdigit():
                result.append(self.advance())
        text = ''.join(result)
        if is_float:
            self.add(TT_FLOAT, float(text))
        else:
            self.add(TT_INT, int(text))

    def read_ident(self):
        result = []
        while self.current() is not None and (self.current().isalnum() or self.current() == '_'):
            result.append(self.advance())
        text = ''.join(result)
        if text in KEYWORDS:
            self.add(TT_KEYWORD, text)
        else:
            self.add(TT_IDENT, text)


# ── Quick test ────────────────────────────────────────────────
if __name__ == '__main__':
    source = '''
dec x = 10
const PI = 3.14
dec name = "Arc"
if x > 5 && x < 20 {
    out("yes")
}
// this is a comment
func add(a, b) {
    return a + b
}
'''
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    for tok in tokens:
        print(tok)