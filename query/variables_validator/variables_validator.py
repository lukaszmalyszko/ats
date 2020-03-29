import re


from query.utils import KEY_WORDS, IDENT
from query.variables_validator.exceptions import InvalidVariablesException
from query.variables_validator.variables_elements import Stmt, While, Assign, ProgLine, Constant, Variable


class VariablesValidator:
    CONTSTRUCTION_TO_BUILD = {
        "stmt": Stmt,
        "while": While,
        "assign": Assign,
        "prog_line": ProgLine,
        "constant": Constant,
        "variable": Variable,
    }

    def __init__(self):
        self.variables_validated = {}
        self.entity = ""

    def validate_variables(self, variables_input):
        variables = variables_input.split(";")
        if variables[-1].strip() == "":
            variables.pop()
            for variable in variables:
                self.__prepare_and_validate_single_variable(variable)
        else:
            raise InvalidVariablesException("#Brak średnika na końcu deklaracji")

        return self.variables_validated

    def __prepare_and_validate_single_variable(self, variable):
        values = variable.strip().split(" ", 1)
        self.entity = values.pop(0)
        self.__prepare_entity()
        self.__validate_entity_name(values)

        self.__prepare_values(values[0])

    def __prepare_entity(self):
        self.__validate_entity()
        self.__add_entity()

    def __validate_entity(self):
        if self.entity not in self.CONTSTRUCTION_TO_BUILD.keys():
            raise InvalidVariablesException("#Niepoprawne polecenie w deklaracji")

    def __add_entity(self,):
        try:
            self.variables_validated[self.entity]
        except KeyError:
            self.variables_validated[self.entity] = []

    def __prepare_values(self, values):
        values_list = values.split(",")
        for value in values_list:
            value = value.strip()
            value = self.__validate_value(value)
            self.__add_variabe_to_entity(value)

    def __validate_value(self, value):
        if "" == value:
            raise InvalidVariablesException("#Niedozwolona znak")
        if not self.__validate_value_name(value):
            raise InvalidVariablesException("#Niedozwolona nazwa zmiennej")
        return value

    def __validate_entity_name(self, values):
        if len(values) == 0:
            raise InvalidVariablesException(f"#Brak nazwy w entity")

    def __add_variabe_to_entity(self, value):
        values_list = self.variables_validated[self.entity]
        if values_list:
            for var in values_list:
                if value == var.name:
                    raise InvalidVariablesException("#Zmienna o takiej nazwie już istnieje")

        value_obj = self.CONTSTRUCTION_TO_BUILD[self.entity](value)
        self.variables_validated[self.entity].append(value_obj)

    def __validate_value_name(self, value):
        return value not in KEY_WORDS and re.match(IDENT, value)
