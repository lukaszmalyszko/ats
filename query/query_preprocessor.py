import re

from query.query_validator.query_elements import KEY_WORDS, IDENT
from query.query_validator.query_validator import QueryValidator


class QueryPreprocessor:
    variables = ""
    query = ""
    entity = ""
    entities = {}

    def get_input(self):
        self.variables = self._get_variables()
        self.query = self._get_query()

        return self.variables, self.query

    def _get_query(self):
        query_input = input("Podaj zapytanie: ")
        query = self.__validate_query(query_input)
        return query

    def _get_variables(self):
        variables_input = input("Podaj deklaracje: ")
        variables = self.__prepare_and_validate_variables(variables_input)
        return variables

    def __prepare_and_validate_variables(self, variables_input):
        variables = variables_input.split(";")
        if variables[-1].strip() == "":
            variables.pop()
            for variable in variables:
                self.__prepare_and_validate_single_variable(variable)
            return variables_input
        else:
            raise InvalidVariablesException("#Brak średnika na końcu deklaracji")

    def __prepare_and_validate_single_variable(self, variable):
        values = variable.strip().split(" ")
        self.entity = values.pop(0)
        self.__prepare_and_validate_entity()
        self.__prepare_and_validate_values(values)

    def __prepare_and_validate_entity(self):
        if self.entity not in KEY_WORDS:
            raise InvalidVariablesException("#Niepoprawne polecenie w deklaracji")
        else:
            self.__add_or_create_entity()

    def __add_or_create_entity(self,):
        try:
            self.entities[self.entity]
        except KeyError:
            self.entities[self.entity] = []

    def __prepare_and_validate_values(self, values):
        if len(values) == 0:
            raise InvalidVariablesException(f"#Brak nazwy w entity")
        for i, value in enumerate(values):
            if ',' in value:
                try:
                    values[i+1]
                except IndexError:
                    raise InvalidVariablesException("#Niedozwolona znak")
            value = value.replace(",", "")
            if value in KEY_WORDS:
                raise InvalidVariablesException("#Niedozwolona nazwa zmiennej")
            if not self.__validate_value_name(value):
                raise InvalidVariablesException("#Niedozwolona nazwa zmiennej")
            self.__add_variabe_to_entity(value)

    def __add_variabe_to_entity(self, value):
        self.entities[self.entity].append(value)

    def __validate_value_name(self, value):
        return re.match(IDENT, value)

    def __validate_query(self, query_input):
        query_validator = QueryValidator()
        query_validator.validate_query(query_input)
        return query_input


class InvalidVariablesException(Exception):
    def __init__(self, message):
        self.message = message
