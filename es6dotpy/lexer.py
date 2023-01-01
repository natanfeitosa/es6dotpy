import re

__all__ = ('Lexer',)

class Lexer:
    # List of token names
    tokens = [
        'BREAK',
        'CASE',
        'CATCH',
        'CLASS',
        'CONST',
        'CONTINUE',
        'DEBUGGER',
        'DEFAULT',
        'DELETE',
        'DO',
        'ELSE',
        'EXPORT',
        'EXTENDS',
        'FINALLY',
        'FOR',
        'FUNCTION',
        'IF',
        'IMPORT',
        'IN',
        'INSTANCEOF',
        'NEW',
        'RETURN',
        'SUPER',
        'SWITCH',
        'THIS',
        'THROW',
        'TRY',
        'TYPEOF',
        'VAR',
        'VOID',
        'WHILE',
        'WITH',
        'YIELD',
        'NULL',
        'TRUE',
        'FALSE',
        'STRING',
        'NUMBER',
        'IDENTIFIER',
        'REGEX',
        'EQUAL',
        'PLUSEQUAL',
        'MINUSEQUAL',
        'TIMESEQUAL',
        'DIVEQUAL',
        'MODEQUAL',
        'PLUSPLUS',
        'MINUSMINUS',
        'LSHIFT',
        'RSHIFT',
        'URSHIFT',
        'ANDAND',
        'OROR',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'MOD',
        'NOT',
        'AND',
        'OR',
        'XOR',
        'LSHIFTASSIGN',
        'RSHIFTASSIGN',
        'URSHIFTASSIGN',
        'ANDASSIGN',
        'ORASSIGN',
        'XORASSIGN',
        'EQ',
        'NE',
        'GT',
        'GE',
        'LT',
        'LE',
        'LBRACKET',
        'RBRACKET',
        'LCURLY',
        'RCURLY',
        'LPAREN',
        'RPAREN',
        'SEMICOLON',
        'COMMA',
        'DOT',
        'ARROW',
        'ELLIPSIS',
        'AT',
        'BACKQUOTE',
    ]

    # Regular expression patterns for the different tokens
    token_patterns = {
        'BREAK': r'break',
        'CASE': r'case',
        'CATCH': r'catch',
        'CLASS': r'class',
        'CONST': r'const',
        'CONTINUE': r'continue',
        'DEBUGGER': r'debugger',
        'DEFAULT': r'default',
        'DELETE': r'delete',
        'DO': r'do',
        'ELSE': r'else',
        'EXPORT': r'export',
        'EXTENDS': r'extends',
        'FINALLY': r'finally',
        'FOR': r'for',
        'FUNCTION': r'function',
        'IF': r'if',
        'IMPORT': r'import',
        'IN': r'in',
        'INSTANCEOF': r'instanceof',
        'NEW': r'new',
        'RETURN': r'return',
        'SUPER': r'super',
        'SWITCH': r'switch',
        'THIS': r'this',
        'THROW': r'throw',
        'TRY': r'try',
        'TYPEOF': r'typeof',
        'VAR': r'var',
        'VOID': r'void',
        'WHILE': r'while',
        'WITH': r'with',
        'YIELD': r'yield',
        'NULL': r'null',
        'TRUE': r'true',
        'FALSE': r'false',
        'STRING': r'"(?:\\.|[^\\"])*"|\'(?:\\.|[^\\\'])*\'',
        'NUMBER': r'\d*\.\d+|\d+',
        'IDENTIFIER': r'[a-zA-Z_$][a-zA-Z0-9_$]*',
        'REGEX': r'/(?:\\.|[^/])*/[gimy]*',
        'EQUAL': r'=',
        'PLUSEQUAL': r'\+=',
        'MINUSEQUAL': r'-=',
        'TIMESEQUAL': r'\*=',
        'DIVEQUAL': r'/=',
        'MODEQUAL': r'%=',
        'PLUSPLUS': r'\+\+',
        'MINUSMINUS': r'--',
        'LSHIFT': r'<<',
        'RSHIFT': r'>>',
        'URSHIFT': r'>>>',
        'ANDAND': r'&&',
        'OROR': r'\|\|',
        'PLUS': r'\+',
        'MINUS': r'-',
        'TIMES': r'\*',
        'DIVIDE': r'/',
        'MOD': r'%',
        'NOT': r'!',
        'AND': r'&',
        'ANDAND': r'&&',
        'ANDEQUAL': r'&=',
        'OR': r'\|',
        'OROR': r'\|\|',
        'OREQUAL': r'\|=',
        'XOR': r'\^',
        'XOREQUAL': r'\^=',
        'NOT': r'!',
        'NOTEQUAL': r'!=',
        'EQUALEQUAL': r'==',
        'EQUAL': r'=',
        'PLUSEQUAL': r'\+=',
        'MINUSEQUAL': r'-=',
        'TIMESEQUAL': r'\*=',
        'DIVEQUAL': r'/=',
        'MODEQUAL': r'%=',
        'PLUSPLUS': r'\+\+',
        'MINUSMINUS': r'--',
        'LSHIFT': r'<<',
        'RSHIFT': r'>>',
        'URSHIFT': r'>>>',
        'LT': r'<',
        'LTEQUAL': r'<=',
        'GT': r'>',
        'GTEQUAL': r'>=',
        'LPAREN': r'\(',
        'RPAREN': r'\)',
        'LBRACK': r'\[',
        'RBRACK': r'\]',
        'LBRACE': r'\{',
        'RBRACE': r'\}',
        'COMMA': r',',
        'PERIOD': r'\.',
        'ELLIPSIS': r'\.\.\.',
        'ARROW': r'=>',
        'PLUS': r'\+',
        'MINUS': r'-',
        'TIMES': r'\*',
        'DIV': r'/',
        'MOD': r'%',
        'COLON': r':',
        'SEMICOLON': r';',
        'QUESTION': r'\?',
        'ignore': r'[\s\f\t\v\n]+|',
    }
    
    def __init__(self):
        # Regular expression for tracking line numbers
        self.newline_regex = re.compile(r'\n+')

        # Tokenization regular expressions
        self.token_regex = None
        self.ignore_regex = re.compile(r'\s+')
    
    def tokenize(self, code):
        # Create the regular expression for tokenization from the token patterns
        self.token_regex = re.compile('|'.join('(?P<%s>%s)' % pair for pair in self.token_patterns.items()))
        
        # Keep track of line numbers
        self.line = 1
        self.pos = 0

        # Tokenize the code
        tokens = []
        while self.pos < len(code):
            # Find the next token
            match = self.token_regex.match(code, self.pos)
            if not match:
                print({'c': code[self.pos]})
                self.error('Unexpected character')
            token_type = match.lastgroup
            token_text = match.group(token_type)
            self.pos = match.end()

            # Update line numbers
            newlines = self.newline_regex.findall(token_text)
            if newlines:
                self.line += len(newlines)

            # Ignore whitespace
            if token_type == 'ignore':
                continue

            # Process token
            tokens.append(self.process_token(token_type, token_text, self.line))
        
        return tokens
    
    def process_token(self, token_type, token_text, line):
        if token_type == 'STRING':
            token_text = token_text[1:-1]
            return (token_type, token_text, line)
        elif token_type == 'NUMBER':
            return (token_type, float(token_text), line)
        elif token_type == 'REGEX':
            return (token_type, re.compile(token_text), line)
        else:
            return (token_type, token_text, line)

    def error(self, message):
        raise ValueError('Line %d: %s' % (self.line, message))
