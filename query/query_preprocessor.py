from query.query_validator.query_validator import QueryValidator


class QueryPreprocessor:
    ENTITY_LIST = [
        "stmt",
        "while",
        "assign",
        "prog_line",
        "constant",
        "variable",
    ]

    def get_input(self):
        variables_input = input("Podaj deklaracje: ")
        query_input = input("Podaj zapytanie: ")

        variables = self.__validate_variables(variables_input)
        query = self.__validate_query(query_input)

        return variables, query

    def __validate_variables(self, variables_input):
        variables = variables_input.split(";")
        if variables[-1].strip() == '':
            variables.pop()
            self.__validate_single_variable(variables)
            return variables_input
        else:
            raise InvalidVariablesException('#Brak średnika na końcu deklaracji')

    def __validate_single_variable(self, variables):
        for variable in variables:
            variable_values = variable.strip().split(" ")
            entity_from_variable = variable_values.pop(0)
            if entity_from_variable not in self.ENTITY_LIST:
                raise InvalidVariablesException('#Niepoprawne polecenie w deklaracji')
            self.__validate_variable_values(variable_values)

    def __validate_variable_values(self, variable_values):
        for value in variable_values:
            if value.replace(',', '') in self.ENTITY_LIST:
                raise InvalidVariablesException('#Nazwa taka sama jak nazwa polecenia')

    def __validate_query(self, query_input):
        query_validator = QueryValidator()
        query_validator.validate_query(query_input)
        return query_input


class InvalidVariablesException(Exception):
    def __init__(self, message):
        self.message = message
