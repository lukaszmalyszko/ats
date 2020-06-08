import re


from query.utils import KEY_WORDS, IDENT
from query.declarations_parser.exceptions import InvalidDeclarationException
from query.declarations_parser.declarations_elements import (
    Stmt,
    While,
    Assign,
    ProgLine,
    Constant,
    Variable, Procedure,
)


class DeclarationsValidator:
    CONTSTRUCTION_TO_BUILD = {
        "stmt": Stmt,
        "while": While,
        "assign": Assign,
        "prog_line": ProgLine,
        "constant": Constant,
        "variable": Variable,
        "procedure": Procedure,
    }

    def __init__(self):
        self.declarations_validated = {}
        self.entity = ""

    def validate_declarations(self, declarations_input):
        declarations = declarations_input.split(";")
        if declarations[-1].strip() == "":
            declarations.pop()
            for declaration in declarations:
                self.__prepare_and_validate_single_declaration(declaration)
        else:
            raise InvalidDeclarationException("#Brak średnika na końcu deklaracji")

        return self.declarations_validated

    def __prepare_and_validate_single_declaration(self, declaration):
        values = declaration.strip().split(" ", 1)
        self.entity = values.pop(0)
        self.__prepare_entity()
        self.__validate_entity_name(values)

        self.__prepare_values(values[0])

    def __prepare_entity(self):
        self.__validate_entity()
        self.__add_entity()

    def __validate_entity(self):
        if self.entity not in self.CONTSTRUCTION_TO_BUILD.keys():
            raise InvalidDeclarationException("#Niepoprawne polecenie w deklaracji")

    def __add_entity(self,):
        try:
            self.declarations_validated[self.entity]
        except KeyError:
            self.declarations_validated[self.entity] = []

    def __prepare_values(self, values):
        values_list = values.split(",")
        for value in values_list:
            value = value.strip()
            value = self.__validate_value(value)
            self.__add_symbol_to_entity(value)

    def __validate_value(self, value):
        if "" == value:
            raise InvalidDeclarationException("#Niedozwolona znak")
        if not self.__validate_value_name(value):
            raise InvalidDeclarationException("#Niedozwolona nazwa zmiennej")
        return value

    def __validate_entity_name(self, values):
        if len(values) == 0:
            raise InvalidDeclarationException(f"#Brak nazwy w entity")

    def __add_symbol_to_entity(self, value):
        values_list = self.declarations_validated[self.entity]
        if values_list:
            for var in values_list:
                if value == var.name:
                    raise InvalidDeclarationException(
                        "#Zmienna o takiej nazwie już istnieje"
                    )

        value_obj = self.CONTSTRUCTION_TO_BUILD[self.entity](value)
        self.declarations_validated[self.entity].append(value_obj)

    def __validate_value_name(self, value):
        return value not in KEY_WORDS and re.match(IDENT, value)
