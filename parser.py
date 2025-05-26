# parser.py

from lexer import tokenize, TokenType, MyToken
from ast2 import ASTNode

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def current_token(self):
        return self.tokens[self.index]

    def match(self, expected_type, expected_value=None):
        token = self.current_token()
        if token.get_type() == expected_type and (expected_value is None or token.get_value() == expected_value):
            self.index += 1
            return token
        else:
            raise SyntaxError(f"Expected {expected_type} '{expected_value}' but got {token.get_type()} '{token.get_value()}'")

    def parse(self):
        return self.E()

    # === PARSE FUNCTIONS (GRAMMAR) ===
    def E(self):
        # Example rule: E -> 'let' D 'in' E => 'let'
        if self.current_token().get_type() == TokenType.KEYWORD and self.current_token().get_value() == 'let':
            self.match(TokenType.KEYWORD, 'let')
            let_node = ASTNode('let')
            let_node.add_child(self.D())
            self.match(TokenType.KEYWORD, 'in')
            let_node.add_child(self.E())
            return let_node

        # TODO: Add other E rules (fn, Ew, etc.)
        # Refer to RPAL_Grammar.pdf

    def D(self):
        # Example placeholder (write full logic later)
        # For now, create a dummy node
        return ASTNode('D (Definition)')

# === Main driver ===
if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python parser.py <input_file>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        code = f.read()

    tokens = tokenize(code)
    parser = Parser(tokens)
    try:
        ast = parser.parse()
        ast.print_tree()
    except SyntaxError as e:
        print("Syntax Error:", e)
