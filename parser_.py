import abc
from enum import Enum
import re
from parser_interface import ParserInterface
from ast import AST

class TokenType(Enum):
    NAME = 1
    INTEGER = 2


class Parser(ParserInterface):  
    __text = ''
    __current_index = 0
    __ast = AST()


    def parse(self, text):
        self.__text = text
        self.__procedure()


    def __skip_whitespace(self):
        while (self.__text[self.__current_index].isspace() and 
                self.__current_index < len(self.__text) - 1):
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
        text_ahead = self.__text[self.__current_index : self.__current_index + len(text_to_match)]
        if text_ahead == text_to_match:
            self.__current_index = self.__current_index + len(text_to_match)
            print("Matched: " + text_to_match)
        else:
            raise Exception("Parser error")


    def __match_token(self, token):
        self.__skip_whitespace()
        
        if token == TokenType.NAME:
            print("Matching TokenType.NAME")
            m = re.search("[A-Za-z][A-Za-z0-9]*", self.__text[self.__current_index:])
        elif token == TokenType.INTEGER:
            print("Matching TokenType.INTEGER")
            m = re.search("[0-9]+", self.__text[self.__current_index:])
        
        if m and m.start() == 0:
            self.__current_index = self.__current_index + m.end()
            print("Matched: " + m.group(0))
            return m.group(0)
        else:
            raise ("Parser error")


    def __procedure(self):
        self.__match_text('procedure')
        self.__match_token(TokenType.NAME)
        self.__match_text('{')
        self.__stmt_lst()
        self.__match_text('}') 


    def __stmt_lst(self):
        self.__stmt()
        next_token = self.__get_next_token()
        if next_token != '}':
            self.__stmt_lst()


    def __stmt(self):
        next_token = self.__get_next_token()
        if next_token == 'while':
            self.__while()
        elif next_token == 'if':
            self.__if()
        else:
            self.__assign()


    def __assign(self):
        self.__match_token(TokenType.NAME)
        self.__match_text('=')
        self.__expr()
        self.__match_text(';')


    def __while(self):
        self.__match_text('while')
        self.__match_token(TokenType.NAME)
        self.__match_text('{')
        self.__stmt_lst()
        self.__match_text('}')


    def __if(self):
        self.__match_text('if')
        self.__match_token(TokenType.NAME)
        self.__match_text('{')
        self.__stmt_lst()
        self.__match_text('}')
        self.__match_text('else')
        self.__match_text('{')
        self.__stmt_lst()
        self.__match_text('}')


    def __expr(self):
        next_token = self.__get_next_token()
        if next_token.isnumeric():
            self.__match_token(TokenType.INTEGER)
        elif next_token.isalnum():
            self.__match_token(TokenType.NAME)

        next_token = self.__get_next_token()
        if next_token == '+':
            self.__match_text('+')
        elif next_token == '-':
            self.__match_text('-')
        elif next_token == '*':
            self.__match_text('*')
        elif next_token == ';':
            return
        
        self.__expr()
