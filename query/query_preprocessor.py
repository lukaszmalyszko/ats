from query.query_parser.query_builder import QueryBuilder
from query.query_parser.query_validator import QueryValidator
from query.variables_validator.declarations import Declarations
from query.variables_validator.variables_validator import VariablesValidator


class QueryPreprocessor:
    def __init__(self):
        self.variables = ""
        self.query = ""
        self.declarations = Declarations()
        self.tree = None

    def get_input(self):
        self.variables = self._get_variables()
        self.query = self._get_query()

        return self.variables, self.query

    def build_tree(self):
        query_builder = QueryBuilder(self)
        self.tree = query_builder.build_query(self.query)

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
        self.declarations.entities = variables_validator.validate_variables(
            variables_input
        )

        return variables_input

    def __validate_query(self, query_input):
        query_validator = QueryValidator(self)
        query_validator.validate_query(query_input)
        return query_input
