from enum import Enum
from enum import auto
import re
from parser_interface import ParserInterface
from ast import AST, NodeType


class TokenType(Enum):
    NAME = auto()
    INTEGER = auto()


class Parser(ParserInterface):
    __text = ''
    __current_index = 0
    __ast = AST()
    __eof = False

    def parse(self, text):
        self.__text = text
        self.__line = 1
        procedure_lst = []
        while (self.__eof != True):
            procedure_lst.append(self.__procedure())
            self.__check_eof()
            if (self.__eof != True):
                self.__skip_whitespace()
                self.__check_eof()
        return procedure_lst

    def __skip_whitespace(self):
        while (self.__text[self.__current_index].isspace() and
               self.__current_index < len(self.__text) - 1):
            if self.__text[self.__current_index] == '\n':
                self.__line += 1
            self.__current_index = self.__current_index + 1

    def __get_next_token(self):
        self.__skip_whitespace()
        next_char = self.__text[self.__current_index]
        if next_char in ';{}=+-*':
            return next_char
        if next_char.isalnum():
            m = re.search("[A-Za-z0-9][A-Za-z0-9]*", self.__text[self.__current_index:])
            return m.group(0)
        else:
            raise Exception("Parser error")

    def __match_text(self, text_to_match):
        self.__skip_whitespace()
        text_ahead = self.__text[self.__current_index: self.__current_index + len(text_to_match)]
        if text_ahead == text_to_match:
            self.__current_index = self.__current_index + len(text_to_match)
            print("Matched: " + text_to_match)
        else:
            raise Exception("Parser error")

    def __match_token(self, token):
        self.__skip_whitespace()

        if token == TokenType.NAME:
            print("Matching TokenType.NAME, line:" + str(self.__line))
            m = re.search("[A-Za-z][A-Za-z0-9]*", self.__text[self.__current_index:])
        elif token == TokenType.INTEGER:
            print("Matching TokenType.INTEGER, line:" + str(self.__line))
            m = re.search("[0-9]+", self.__text[self.__current_index:])

        if m and m.start() == 0:
            self.__current_index = self.__current_index + m.end()
            print("Matched: " + m.group(0))
            return m.group(0)
        else:
            raise Exception("Parser error")

    def __procedure(self):
        procedure_node = self.__ast.create_node(NodeType.PROCEDURE)

        self.__match_text('procedure')
        name = self.__match_token(TokenType.NAME)
        self.__ast.set_node_value(procedure_node, name)
        self.__ast.set_node_line(procedure_node, self.__line)
        self.__match_text('{')
        stmt_lst_node = self.__stmt_lst()
        self.__match_text('}')
        self.__ast.add_child(procedure_node, stmt_lst_node, 0)
        return procedure_node

    def __stmt_lst(self):
        stmt_lst_node = self.__ast.create_node(NodeType.STMT_LST)
        self.__ast.set_node_line(stmt_lst_node, self.__line)
        stmt_node = self.__stmt()
        next_child = 0
        self.__ast.add_child(stmt_lst_node, stmt_node, next_child)
        next_token = self.__get_next_token()
        while next_token != '}':
            next_child = next_child + 1
            stmt_node = self.__stmt()
            self.__ast.add_child(stmt_lst_node, stmt_node, next_child)
            next_token = self.__get_next_token()
        return stmt_lst_node

    def __stmt(self):
        next_token = self.__get_next_token()
        if next_token == 'while':
            node = self.__while()
        elif next_token == 'if':
            node = self.__if()
        elif next_token == 'call':
            node = self.__call()
        else:
            node = self.__assign()

        return node

    def __assign(self):
        assign_node = self.__ast.create_node(NodeType.ASSIGN)
        self.__ast.set_node_line(assign_node, self.__line)
        var_name = self.__match_token(TokenType.NAME)
        var_node = self.__ast.create_node(NodeType.VARIABLE)
        self.__ast.set_node_line(assign_node, self.__line)
        self.__ast.set_node_value(var_node, var_name)
        self.__ast.add_child(assign_node, var_node, 0)
        self.__match_text('=')
        expr_node = self.__expr()
        self.__ast.add_child(assign_node, expr_node, 1)
        self.__match_text(';')
        return assign_node

    def __while(self):
        while_node = self.__ast.create_node(NodeType.WHILE)
        self.__ast.set_node_line(while_node, self.__line)
        self.__match_text('while')
        var_name = self.__match_token(TokenType.NAME)
        var_node = self.__ast.create_node(NodeType.VARIABLE)
        self.__ast.set_node_line(var_node, self.__line)
        self.__ast.set_node_value(var_node, var_name)
        self.__ast.add_child(while_node, var_node, 0)
        self.__match_text('{')
        stmt_lst_node = self.__stmt_lst()
        self.__match_text('}')
        self.__ast.add_child(while_node, stmt_lst_node, 1)
        return while_node

    def __if(self):
        if_node = self.__ast.create_node(NodeType.IF)
        self.__ast.set_node_line(if_node, self.__line)
        self.__match_text('if')
        var_name = self.__match_token(TokenType.NAME)
        var_node = self.__ast.create_node(NodeType.VARIABLE)
        self.__ast.set_node_line(var_node, self.__line)
        self.__ast.set_node_value(var_node, var_name)
        self.__ast.add_child(if_node, var_node, 0)
        self.__match_text('then')
        self.__match_text('{')
        stmt_lst_node_1 = self.__stmt_lst()
        self.__ast.add_child(if_node, stmt_lst_node_1, 1)
        self.__match_text('}')
        self.__match_text('else')
        self.__match_text('{')
        stmt_lst_node_2 = self.__stmt_lst()
        self.__ast.add_child(if_node, stmt_lst_node_2, 2)
        self.__match_text('}')
        return if_node

    def __call(self):
        call_node = self.__ast.create_node(NodeType.CALL)
        self.__ast.set_node_line(call_node, self.__line)
        self.__match_text('call')
        proc_name = self.__match_token(TokenType.NAME)
        self.__match_text(';')
        self.__ast.set_node_value(call_node, proc_name)
        return call_node

    def __expr(self):
        expr = self.__term()
        token = self.__get_next_token()
        while token == '+' or token == '-':
            op = token
            self.__match_text(token)
            expr1 = self.__term()
            if op == '-':
                op_node = self.__ast.create_node(NodeType.ARITHMETIC)
                self.__ast.set_node_line(op_node, self.__line)
                self.__ast.set_node_value(op_node, op)
                self.__ast.add_child(op_node, expr, 0)
                self.__ast.add_child(op_node, expr1, 1)
                expr = op_node
            elif op == '+':
                op_node = self.__ast.create_node(NodeType.ARITHMETIC)
                self.__ast.set_node_line(op_node, self.__line)
                self.__ast.set_node_value(op_node, op)
                self.__ast.add_child(op_node, expr, 0)
                self.__ast.add_child(op_node, expr1, 1)
                expr = op_node
            token = self.__get_next_token()
        return expr

    def __term(self):
        term = self.__factor()
        token = self.__get_next_token()
        while token == '*':
            op = token
            self.__match_text(op)
            term1 = self.__factor()
            if op == '*':
                op_node = self.__ast.create_node(NodeType.ARITHMETIC)
                self.__ast.set_node_line(op_node, self.__line)
                self.__ast.set_node_value(op_node, op)
                self.__ast.add_child(op_node, term, 0)
                self.__ast.add_child(op_node, term1, 1)
                term = op_node
            token = self.__get_next_token()
        return term

    def __factor(self):
        next_token = self.__get_next_token()
        if next_token.isnumeric():
            value = self.__match_token(TokenType.INTEGER)
            node = self.__ast.create_node(NodeType.INTEGER)
            self.__ast.set_node_line(node, self.__line)
            self.__ast.set_node_value(node, value)
        elif next_token.isalnum():
            name = self.__match_token(TokenType.NAME)
            node = self.__ast.create_node(NodeType.VARIABLE)
            self.__ast.set_node_line(node, self.__line)
            self.__ast.set_node_value(node, name)
        elif next_token == '(':
            self.__match_text('(')
            node = self.__expr()
            self.__match_text(')')
        elif next_token == '-':
            self.__match_text('-')
            term1 = self.__term()

            emptyNode = self.__ast.create_node(NodeType.INTEGER)
            self.__ast.set_node_line(emptyNode, self.__line)
            self.__ast.set_node_value(emptyNode, 0)

            node = self.__ast.create_node(NodeType.ARITHMETIC)
            self.__ast.set_node_line(node, self.__line)
            self.__ast.set_node_value(node, next_token)
            self.__ast.add_child(node, emptyNode, 0)
            self.__ast.add_child(node, term1, 1)
        return node

    def __check_eof(self):
        if len(self.__text) - self.__current_index < 2:
            self.__eof = True
