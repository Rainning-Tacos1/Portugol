
class PrattParser:
    def __init__(self, s: str):
        self.s: str = s.replace(" ", "")
        self.c: int = 0
        self.err = ""
        self.UNARY_BP = 120
        pass

        # Cursor routines
    def __read_char(self):
        if self.c == len(self.s):
            return None
        c = self.s[self.c]
        self.c += 1
        return c

    def __peek_char(self):
        if self.c == len(self.s):
            return None
        return self.s[self.c]

        # Numbers
    def __get_num(self):
        num = ""

        while True:
            c = self.__peek_char()

            if c is None or (not c.isdigit() and c != '.'):
                break


            num += c
            self.__read_char()

        return num



    def __get_prefix(self):
        if n := self.__get_num():
            return [float(n)]

        c = self.__read_char()

        if c == '(':
            left = self.build()

            if left is None:
                return None
            
            self.__read_char()
            return left

        elif (c == '+') or (c == '-'):


            if (c == '-') and (n := self.__get_num()):
                return ['-', [float(n)]]

            right = self.build(min_bp=self.UNARY_BP)
            if right is None:
                return None
            
            return [c, right]
        else:
            p = "Erro na expressão"
            self.err = f"{p}: {self.s}\n" + (" " * len(p)) + "  " + (" " * (self.c-1)) + "^"
            return None

    def __get_bp(self, c):
        if c == '+' or c == '-':
            return (100, 101)
        elif c == '/' or c == '*':
            return (110, 111)
        elif c == '^':
                return (120, 120)
        return None

    def build(self, min_bp=0):
        left = self.__get_prefix()

        if left is None: 
            return None

        while True:
            c = self.__peek_char()

            if c == ')' or c is None:
                break


            if (bp := self.__get_bp(c)) is None:
                p = "Operador Inválido"
                self.err = f"{p}: {self.s}\n" + (" " * len(p)) + "  " + (" " * (self.c)) + "^"
                return None

            if bp[0] < min_bp:
                break

            self.__read_char()

            right = self.build(min_bp=bp[1])
            if right is None:
                return None

            left = [left, c, right]
        return left

    def eval(self, ast):
        if len(ast) == 1:
            return ast[0]

        elif len(ast) == 2:
            res = self.eval(ast[1])
            if ast[0] == '-':
                res = -res
            return res

        elif len(ast) == 3:
            left = self.eval(ast[0])
            right = self.eval(ast[2])
            res = 0
            if ast[1] == '+':
                res = left + right
            elif ast[1] == '-':
                res = left - right
            elif ast[1] == '*':
                res = left * right
            elif ast[1] == '/':
                if right == 0.0:
                    self.err = "Divisão por 0"
                    return None
                res = left / right
            elif ast[1] == '^':
                res = left ** right
            else:
                self.err = "Operador inválido na avaliação"
                return None
            return res
        else:
            self.err = "Nó da AST com tamanho inválido"
            return None     


p = PrattParser("10")
print(ast := p.build())

if p.err:
    print(p.err)
    exit(1)

print(p.eval(ast))

printf("%g")

if p.err:
    print(p.err)
    exit(1)