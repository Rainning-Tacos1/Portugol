from enum import Enum
import stream
import string

class TokenType(Enum):
    EOF = 1,
    ERR_TOK = 2,

    COMMENT = 3,
    NEWLINE = 4,
    IDENTIFIER = 5,

class Token:
    def __init__(self, tok, meta=None):
        self.tok = tok
        self.meta = meta


class Lexer:
    def __init__(self, s: stream.Stream):
        self.s: stream.Stream = s

    def next_token(self):

        # Skip space
        while (c := self.s.read()) == " " or c == "\t":
            pass

        # Eof
        if c is None:
            return Token(TokenType.EOF)

        # Coments
        if c == "/" and self.s.peek() == "/":
            self.s.read() # Safe read
            m = ""

            while not ((_c := self.s.read()) is None) and (_c not in "\n\r"):
                m += _c

            return Token(TokenType.COMMENT, m)

        # New line
        if c == "\n":
            return Token(TokenType.NEWLINE)

        # Identifiers

        # Add 'a' to fake an identidier name
        ident = ""
        while (c == '_' or (c + 'a').isidentifier()):
            ident += c

            c = self.s.read()

        if ident:
            return Token(TokenType.IDENTIFIER, ident)


        return Token(TokenType.ERR_TOK)

s = stream.Stream(
"""
// Comentario
Variavel Inteiro x = 10

"""
)
l = Lexer(s)
while (t := l.next_token()).tok not in [TokenType.EOF, TokenType.ERR_TOK]:
    print("token:",t.tok.name, "meta:", t.meta)
print("Erro: ", s.curr())
