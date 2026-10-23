from enum import Enum
import stream
import string

class TokenType(Enum):
    EOF = 1,
    ERR_TOK = 2,
    SYNTAX_ERROR = 3,

    COMMENT = 4,
    NEWLINE = 5,
    IDENTIFIER = 6,
    NUMBER = 7,

class Token:
    def __init__(self, tok, meta=None):
        self.tok = tok
        self.meta = meta


class Lexer:
    def __init__(self, s: stream.Stream):
        self.s: stream.Stream = s

    def __verify_end_of_number(self, c: str):
        return not (c + 'a').isidentifier()


    def next_token(self):
        self.s.reset_peek()

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

        # CR
        if c == "\r":
            c = self.s.read()

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

        # Numbers
        num = c
        if c in string.digits:
            # Hex, Oct or Bin
            # Will ony loop once but must use while to allow break to read decimal numbers
            while c == "0":
                num += (c := self.s.read())

                # Hex number
                if c in ("Xx"):
                    num += (c := self.s.read())

                    while True:
                        # Ignore underscores
                        if c == "_":
                            num += (c := self.s.read())

                        if c not in string.hexdigits:
                            return Token(TokenType.SYNTAX_ERROR, "Invalid hexadecimal literal")

                        while (c := self.s.read()) and (num := num + c) and c in string.hexdigits:
                            pass

                        if c != "_":
                            break

                    if not self.__verify_end_of_number(c):
                        return Token(TokenType.SYNTAX_ERROR, "Invalid hexadecimal literal")

                # Oct number
                elif c in ("Oo"):
                    num += (c := self.s.read())

                    while True:
                        # Ignore underscores
                        if c == "_":
                            num += (c := self.s.read())

                        if c not in string.octdigits:
                            if c in string.digits:
                                return Token(TokenType.SYNTAX_ERROR, f"Invalid digit {c} in octal literal")
                            return Token(TokenType.SYNTAX_ERROR, "Invalid octal literal")

                        while (c := self.s.read()) and (num := num + c) and c in string.hexdigits:
                            pass

                        if c != "_":
                            break

                    if not self.__verify_end_of_number(c):
                        return Token(TokenType.SYNTAX_ERROR, "Invalid octal literal")

                else:
                    break # goto decimal
        
                return Token(TokenType.NUMBER, num)

            # Decimal / Float

            return Token(TokenType.NUMBER, "not implemented yet")

        return Token(TokenType.ERR_TOK)

s = stream.Stream(
"""
// Comentario
Variavel Inteiro x 0o9

"""
)
l = Lexer(s)
while (t := l.next_token()).tok not in [TokenType.EOF, TokenType.ERR_TOK]:
    print("token:",t.tok.name, "meta:", t.meta)
print("Erro: ", s.curr())
