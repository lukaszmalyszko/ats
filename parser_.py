import abc
from enum import Enum
from enum import auto
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Union
import re
from parser_interface import ParserInterface
from ast import AST


class TokenType(Enum):
    NAME = auto()
    INTEGER = auto()


class Procedure(NamedTuple):
    proc_name: str
    line: int
    stmt_lst: 'List[Statement]'


class StmtCall(NamedTuple):
    proc_name: str
    line: int


class StmtWhile(NamedTuple):
    var_name: str
    line: int
    stmt_lst: 'List[Statement]'


class StmtIf(NamedTuple):
    var_name: str
    line: int
    then: 'List[Statement]'
    else_: 'Optional[List[Statement]]'


class StmtAssign(NamedTuple):
    var_name: str
    line: int
    expr: 'Expr'


Statement = Union[StmtCall, StmtIf, StmtWhile, StmtAssign]


class Var(NamedTuple):
    var_name: str


class Const(NamedTuple):
    const_value: int


class Parentheised(NamedTuple):
    expr: 'Expr'


Factor = Union[Var, Const, Parentheised]


class Multiply(NamedTuple):
    expr: 'Expr'
    term: 'Term'


Term = Union[Multiply, Factor]


class Plus(NamedTuple):
    expr: 'Expr'
    term: 'Term'


class Minus(NamedTuple):
    expr: 'Expr'
    term: 'Term'


Expr = Union[Plus, Minus, Term]


class Parser(ParserInterface):
    __text = ''
    __current_index = 0
    __ast = AST()

    def parse(self, text):
        self.__text = text
        self.__line = 1
        self.__procedure()

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

    def __get_curr_token(self):
        self.__skip_whitespace()
        return self.__text[self.__current_index]

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
            raise ("Parser error")

    def __procedure(self) -> Procedure:
        self.__match_text('procedure')
        proc_name = self.__match_token(TokenType.NAME)
        self.__match_text('{')
        stmt_lst = self.__stmt_lst()
        self.__match_text('}')
        return Procedure(proc_name, self.__line, stmt_lst)

    def __stmt_lst(self) -> List[Statement]:
        stmt_lst: List[Statement] = []
        stmt_lst.append(self.__stmt())
        next_token = self.__get_next_token()
        while next_token != '}':
            stmt_lst.append(self.__stmt())
            next_token = self.__get_next_token()
        return stmt_lst

    def __stmt(self) -> Statement:
        next_token = self.__get_next_token()
        if next_token == 'while':
            return self.__while()
        elif next_token == 'if':
            return self.__if()
        elif next_token == 'call':
            return self.__call()
        else:
            return self.__assign()

    def __assign(self) -> StmtAssign:
        var_name = self.__match_token(TokenType.NAME)
        self.__match_text('=')
        expr = self.__expr()
        self.__match_text(';')
        return StmtAssign(var_name, self.__line, expr)

    def __while(self) -> StmtWhile:
        self.__match_text('while')
        var_name = self.__match_token(TokenType.NAME)
        self.__match_text('{')
        stmt_lst = self.__stmt_lst()
        self.__match_text('}')
        return StmtWhile(var_name, self.__line, stmt_lst)

    def __if(self) -> StmtIf:
        self.__match_text('if')
        var_name = self.__match_token(TokenType.NAME)
        self.__match_text('then {')
        then = self.__stmt_lst()
        self.__match_text('}')
        self.__match_text('else')
        self.__match_text('{')
        else_ = self.__stmt_lst()
        self.__match_text('}')
        return StmtIf(var_name, self.__line, then, else_)

    def __call(self) -> StmtCall:
        self.__match_text('call')
        proc_name = self.__match_token(TokenType.NAME)
        self.__match_text(';')
        return StmtCall(proc_name, 1)

    def __expr(self) -> Expr:
        expr = self.__term()
        token = self.__get_next_token()
        while token == '+' or token == '-':
            op = token
            self.__match_text(token)
            expr1 = self.__term()
            if op == '-':
                expr =  Minus(expr, expr1)
            elif op == '+':
                expr = Plus(expr, expr1)
            token = self.__get_next_token()
        return expr

    def __term(self) -> Term:
        term = self.__factor()
        token = self.__get_next_token()
        while token == '*':
            op = token
            self.__match_text(op)
            term1 = self.__term()
            if op == '*':
                term = Multiply(term, term1)
            token = self.__get_next_token()
        return term

    def __factor(self) -> Factor:
        next_token = self.__get_next_token()
        if next_token.isnumeric():
            val = self.__match_token(TokenType.INTEGER)
            return Const(val)
        elif next_token.isalnum():
            val = self.__match_token(TokenType.NAME)
            return Var(val)
        elif next_token == '(':
            self.__match_text('(')
            expr = self.__expr()
            self.__match_text(')')
            return Parentheised(expr)
        elif next_token == '-':
            self.__match_text('-')
            term1 = self.__term()
            return Minus(Const(0), term1)
