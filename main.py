
INTEGER, PLUS, MINUS,  EOF = "INTEGER", "PLUS", "MINUS", "EOF"

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value
    def __repr__(self):
        return str("Token: " + str(self.type) + " " + str(self.value))

class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None # means that we reached EOF
        else:
            self.current_char = self.text[self.pos]

    def error(self):
        raise Exception("Error while parsing input")

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            if self.current_char == "+":
                self.advance()
                return Token(PLUS, "+")
            if self.current_char == "-":
                self.advance()
                return Token(MINUS, "-")
            self.error()

    def eat(self, token_type):
        """
        - Compare current token type with passed token
        -- if match:
        --- eat current ; assign next tok to self.current_token
        -- else:
        --- otherwise raise exception
        """
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        # self.current_token = self.get_next_token()
        # left = self.current_token
        # self.eat(INTEGER)
        # op = self.current_token
        # self.eat(PLUS)
        # right = self.current_token
        # self.eat(INTEGER)
        # result = left.value + right.value
        # return result
        self.current_token = self.get_next_token()
        left = self.current_token
        self.eat(INTEGER)

        op = self.current_token
        if op.type == PLUS:
            self.eat(PLUS)
        else:
            self.eat(MINUS)

        right = self.current_token
        self.eat(INTEGER)

        if op.type == PLUS:
            return left.value + right.value
        else:
            return left.value - right.value

def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__ == "__main__":
    main()
