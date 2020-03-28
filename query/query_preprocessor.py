from query.query_validator.query_elements import KEY_WORDS
from query.query_validator.query_validator import QueryValidator


class QueryPreprocessor:
    variables = ''
    query = ''

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
        variables = self.__validate_variables(variables_input)
        return variables

    def __validate_variables(self, variables_input):
        variables = variables_input.split(";")
        if variables[-1].strip() == "":
            variables.pop()
            for variable in variables:
                self.__validate_single_variable(variable)
            return variables_input
        else:
            raise InvalidVariablesException("#Brak średnika na końcu deklaracji")

    def __validate_single_variable(self, variable):
        values = variable.strip().split(" ")
        entity = values.pop(0)
        self.__validate_entity(entity)
        self.__validate_values(values)

    def __validate_entity(self, entity):
        if entity not in KEY_WORDS:
            raise InvalidVariablesException("#Niepoprawne polecenie w deklaracji")

    def __validate_values(self, values):
        if len(values) == 0:
            raise InvalidVariablesException(f"#Brak nazwy w entity")
        for value in values:
            if value.replace(",", "") in KEY_WORDS:
                raise InvalidVariablesException("#Niedozwolona nazwa zmiennej")

    def __validate_query(self, query_input):
        query_validator = QueryValidator()
        query_validator.validate_query(query_input)
        return query_input


class InvalidVariablesException(Exception):
    def __init__(self, message):
        self.message = message
