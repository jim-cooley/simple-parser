from tokens import TK, Token


class TokenReader:
    _tokens = []

    def __init__(self, tk_reader):
        self._reader = tk_reader
        self._pos = 0
        self.token = None
        self._tokens = self.read()

    def __iter__(self):
        return self

    def __next__(self):
        if not self.readable():
            raise StopIteration
        return self.advance(skip_end_of_line=False)

    def readable(self):
        return self.has_more()

    def has_more(self):
        return False if self._tokens is None else self._pos < len(self._tokens) - 1

    def seek(self, pos):
        if self._tokens is None or len(self.token) <= pos:
            raise IndexError
        self._pos = pos

    def skip(self, offset):
        pos = self._pos + offset
        if self._tokens is None or len(self.token) < pos:
            raise IndexError
        self._pos = pos

    def tell(self):
        return Token.Loc(-1,-1) if self.token is None else self.token.location

    def advance(self, skip_end_of_line=True):
        if not self.has_more():
            return TK.EOF
        while True:
            self._pos += 1
            if self._pos > len(self._tokens) - 1:
                break
            token = self._tokens[self._pos]
            if not skip_end_of_line or token.id != TK.EOL:
                break
        print(token.format())
        self.token = token
        return self.token

    def peek(self):
        if self.token is None:
            self.advance()
        return self.token

    def read(self):
        if self._reader.readable():
            tokens = []
            for token in self._reader:
                tokens.append(token)
            self._tokens = tokens
        self._pos = -1
        self.token = None
        return self._tokens
