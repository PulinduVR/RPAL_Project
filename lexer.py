import re
from enum import Enum, auto

# Define token types using Enum
class TokenType(Enum):
    KEYWORD = auto()
    IDENTIFIER = auto()
    INTEGER = auto()
    STRING = auto()
    PUNCTUATION = auto()
    OPERATOR = auto()
    END_OF_TOKENS = auto()

# Token class to hold type and value
class MyToken:
    def __init__(self, token_type, value):
        if not isinstance(token_type, TokenType):
            raise ValueError("token_type must be an instance of TokenType enum")
        self.type = token_type
        self.value = value

    def get_type(self):
        return self.type

    def get_value(self):
        return self.value

    def __str__(self):
        return f'{self.type.name}: {self.value}'

# Tokenize function
def tokenize(input_str):
    tokens = []

    # Keywords in RPAL
    keywords = {
        'let', 'in', 'fn', 'where', 'aug', 'or', 'not', 'gr', 'ge',
        'ls', 'le', 'eq', 'ne', 'true', 'false', 'nil', 'dummy',
        'within', 'and', 'rec'
    }

    # Regular expression patterns for tokens
    token_patterns = [
        ('COMMENT', r'//[^\n]*'),
        ('STRING', r"\'(\\[tn'\\]|[^'])*\'"),  # String literal
        ('INTEGER', r'\d+'),
        ('IDENTIFIER', r'[a-zA-Z][a-zA-Z0-9_]*'),
        ('OPERATOR', r'(\*\*|->|>=|<=|==|!=|[+\-*/<>&@|=~|:$!#%^_\[\]{}"\'?])'),
        ('PUNCTUATION', r'[();,]'),
        ('SKIP', r'[ \t\n]+'),
    ]

    master_pattern = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_patterns))

    # Tokenize input string
    pos = 0
    while pos < len(input_str):
        match = master_pattern.match(input_str, pos)
        if not match:
            print(f"Error: Unexpected character at position {pos}: {input_str[pos]}")
            pos += 1
            continue

        kind = match.lastgroup
        value = match.group()

        if kind == 'COMMENT' or kind == 'SKIP':
            # Ignore comments and spaces
            pos = match.end()
            continue
        elif kind == 'IDENTIFIER':
            if value in keywords:
                tokens.append(MyToken(TokenType.KEYWORD, value))
            else:
                tokens.append(MyToken(TokenType.IDENTIFIER, value))
        elif kind == 'INTEGER':
            tokens.append(MyToken(TokenType.INTEGER, value))
        elif kind == 'STRING':
            # Remove surrounding quotes
            tokens.append(MyToken(TokenType.STRING, value[1:-1]))
        elif kind == 'OPERATOR':
            tokens.append(MyToken(TokenType.OPERATOR, value))
        elif kind == 'PUNCTUATION':
            tokens.append(MyToken(TokenType.PUNCTUATION, value))

        pos = match.end()

    # Add end-of-tokens marker if needed
    tokens.append(MyToken(TokenType.END_OF_TOKENS, 'EOF'))

    return tokens

# For testing
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python lexer.py <input_file>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        code = f.read()

    tokens = tokenize(code)
    for token in tokens:
        print(f"{token.get_type().name}: {token.get_value()}")
