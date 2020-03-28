from query.query_validator.query_elements import Select


class QueryValidator:
    def __init__(self):
        self.elements = QueryValidator.ElementsContainer()
        self.expected_element = self.elements.SELECT

    def validate_query(self, query_input):
        query = query_input.split(" ")
        for element in query:
            if element not in self.expected_element.value:
                raise InvalidQueryException(self.expected_element.error_message)
            else:
                return

    class ElementsContainer:
        def __init__(self):
            self.SELECT = Select()


class InvalidQueryException(Exception):
    def __init(self, message):
        self.message = message
