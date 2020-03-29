from query.query_validator.query_validator import QueryValidator
from query.variables_validator.variables_validator import VariablesValidator


class QueryPreprocessor:
    variables = ""
    query = ""
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
        variables_validator = VariablesValidator()
        self.entities = variables_validator.validate_variables(variables_input)

        return variables_input

    def __validate_query(self, query_input):
        query_validator = QueryValidator()
        query_validator.validate_query(query_input)
        return query_input
