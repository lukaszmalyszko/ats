

class QueryPreprocessor:
    ENTITY_LIST = [
        'stmt',
        'while',
        'assign',
        'prog_line',
        'constant',
        'variable',
    ]

    def get_input(self):
        variables_input = input('Podaj deklaracje: ')
        query_input = input('Podaj zapytanie: ')

        variables = self.__validate_variables(variables_input)

        return variables, query_input

    def __validate_variables(self, variables_input):
        variables = variables_input.split(';')

        if variables[-1].strip() == '':
            return variables_input
        else:
            raise InvalidVariablesException('Brak średnika na końcu deklaracji')


class InvalidVariablesException(Exception):
    def __init__(self, message):
        self.message = message
