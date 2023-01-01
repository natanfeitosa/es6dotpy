
__all__ = ('Parser',)

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.pos = 0
        
        self.current_token = None
    
    def _move_cursor(self):
        try:
            self.next_token = self.tokens[self.pos + 1]
        except IndexError:
            self.next_token = ('EOF', 'EOF')
        self.previous_token = self.current_token
        try:
            self.current_token = self.tokens[self.pos]
        except IndexError:
            self.current_token = ('EOF', 'EOF')
        self.pos += 1

    def parse(self, code):
        self.tokens = self.lexer.tokenize(code)
        self._move_cursor()

        # Parse the program
        return self.parse_program()

    def parse_program(self):
        # Parse all statements in the program
        statements = []
        while self.current_token[0] != 'EOF':
            statements.append(self.parse_statement())
            self._move_cursor()
        return statements

    def parse_statement(self):
        # Parse the appropriate type of statement based on the current token
        if self.current_token[0] == 'VAR':
            return self.parse_var_declaration()
        elif self.current_token[0] == 'IDENTIFIER':
            return self.parse_assignment()
        elif self.current_token[0] == 'FUNCTION':
            return self.parse_function_declaration()
        elif self.current_token[0] == 'RETURN':
            return self.parse_return()
        elif self.current_token[0] == 'PLUS':
            # Parse a binary operator expression
            left = self.previous_token
            self._move_cursor()
            right = self.parse_expression()
            return ('BINOP', 'PLUS', left, right)
        # elif self.current_token[0] == 'EOF':
        #     return
        else:
            raise ValueError('Unexpected token: %s' % self.current_token[1])
    
    def parse_return(self):
        # Parse a return statement
    
        # Advance to the next token
        self._move_cursor()
    
        # Parse the return expression
        expr = self.parse_expression()
        
        return ('RETURN', expr)
    
    def parse_function_declaration(self):
        # Parse a function declaration
    
        # Advance to the next token
        self._move_cursor()
    
        # Get the function name
        func_name = self.current_token[1]
        
        self._move_cursor()
    
        # Parse the function parameters
        params = self.parse_parameters()
        
        self._move_cursor()
    
        # Parse the function body
        body = self.parse_function_body()
    
        return ('FUNCTION_DECLARATION', func_name, params, body)
    
    def parse_parameters(self):
        # Parse the function parameters
    
        # Expect an opening parenthesis
        if self.current_token[0] != 'LPAREN':
            raise ValueError('Expected "(": %s' % self.current_token[1])
    
        # Advance to the next token
        self._move_cursor()
    
        params = []
        while self.current_token[0] != 'RPAREN':
            # Get the parameter name
            param_name = self.current_token[1]
            params.append(param_name)
    
            # Advance to the next token
            self._move_cursor()
    
            # Check for a comma
            if self.current_token[0] == 'COMMA':
                self._move_cursor()
    
        return params
    
    def parse_function_body(self):
        # Parse the function body
    
        # Expect an opening brace
        if self.current_token[0] != 'LBRACE':
            raise ValueError('Expected "{": %s' % self.current_token[1])
    
        # Advance to the next token
        self._move_cursor()
    
        # Parse all statements in the function body
        statements = []
        while self.current_token[0] != 'RBRACE':
            statements.append(self.parse_statement())
            self._move_cursor()
    
        return statements

    def parse_var_declaration(self):
        # Parse a variable declaration
        self._move_cursor()

        # Get the variable name
        var_name = self.current_token[1]

        # Check for an assignment
        if self.next_token[0] == 'EQUAL':
            self._move_cursor()

            # Parse the assignment value
            value = self.parse_expression()

            return ('VAR_DECLARATION', var_name, value)
        else:
            return ('VAR_DECLARATION', var_name, None)

    def parse_assignment(self):
        # Parse an assignment
        var_name = self.current_token[1]

        self._move_cursor()

        # Check for an assignment
        if self.current_token[0] != 'EQUAL':
            raise ValueError('Expected "=": %s' % self.current_token[1])

        # Parse the assignment value
        self._move_cursor()

        value = self.parse_expression()

        return ('ASSIGNMENT', var_name, value)
    
    def parse_expression(self):
        # }, end='\n\n')
        
        # Parse a simple expression
        if self.current_token[0] == 'IDENTIFIER':
            if self.next_token[0] == 'PLUS':
                self._move_cursor()
                return self.parse_expression()
            return ('IDENTIFIER', self.current_token[1])
        elif self.current_token[0] == 'NUMBER':
            return ('NUMBER', self.current_token[1])
        elif self.current_token[0] == 'PLUS':
            # Parse a binary operator expression
            if self.next_token[0] in ('IDENTIFIER', 'NUMBER'):
                left = ('IDENTIFIER', self.previous_token[1])
                # debugger
                self._move_cursor()
                right = self.parse_expression()
                return ('BINOP', 'PLUS', left, right)
            else:
                raise ValueError('Unexpected token: %s' % self.current_token[1])
        else:
            raise ValueError('Unexpected token: %s' % self.current_token[1])
            
