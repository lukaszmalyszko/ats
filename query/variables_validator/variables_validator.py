import re

from query.query_validator.query_elements import IDENT
from query.variables_validator.exceptions import InvalidVariablesException


class VariablesValidator:
    ENTITY_LIST = [
        "stmt",
        "while",
        "assign",
        "prog_line",
        "constant",
        "variable",
    ]
    entity = ""
    validated_variables = {}

    def validate_variables(self, variables_input):
        variables = variables_input.split(";")
        if variables[-1].strip() == "":
            variables.pop()
            for variable in variables:
                self.__prepare_and_validate_single_variable(variable)
        else:
            raise InvalidVariablesException("#Brak średnika na końcu deklaracji")

        return self.validated_variables

    def __prepare_and_validate_single_variable(self, variable):
        values = variable.strip().split(" ")
        self.entity = values.pop(0)
        self.__prepare_entity()
        self.__prepare_values(values)

    def __prepare_entity(self):
        self.__validate_entity()
        self.__add_entity()

    def __validate_entity(self):
        if self.entity not in self.ENTITY_LIST:
            raise InvalidVariablesException("#Niepoprawne polecenie w deklaracji")

    def __add_entity(self,):
        try:
            self.validated_variables[self.entity]
        except KeyError:
            self.validated_variables[self.entity] = []

    def __prepare_values(self, values):
        self.__validate_entity_name(values)
        for i, value in enumerate(values):
            value = self.__validate_value(i, value, values)
            self.__add_variabe_to_entity(value)

    def __validate_value(self, i, value, values):
        if "," in value:
            try:
                values[i + 1]
            except IndexError:
                raise InvalidVariablesException("#Niedozwolona znak")
        value = value.replace(",", "")
        if value in self.ENTITY_LIST:
            raise InvalidVariablesException("#Niedozwolona nazwa zmiennej")
        if not self.__validate_value_name(value):
            raise InvalidVariablesException("#Niedozwolona nazwa zmiennej")
        return value

    def __validate_entity_name(self, values):
        if len(values) == 0:
            raise InvalidVariablesException(f"#Brak nazwy w entity")

    def __add_variabe_to_entity(self, value):
        self.validated_variables[self.entity].append(value)

    def __validate_value_name(self, value):
        return re.match(IDENT, value)
