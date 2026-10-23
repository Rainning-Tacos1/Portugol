from io import StringIO

class Stream:
    def __init__(self, _str: str, is_file=False):
        self.s = StringIO(_str) if not is_file else open(_str, "r", encoding="utf-8")
        self.p = 0

    def curr(self):
        if (c := (self.s.tell() - 1)) < 0:
            return None
        self.s.seek(c)

        return None if (c := self.s.read(1)) == "" else c

    def read(self):
        self.p = 0
        return None if (c := self.s.read(1)) == "" else c

    def peek(self):
        c = self.s.tell()  # Save

        self.s.seek(c + self.p, 0)
        r = self.s.read(1)
        self.p += 1

        self.s.seek(c)  # Restore current stream position

        return None if r == "" else r

    def reset_peek(self):
        self.p = 0
