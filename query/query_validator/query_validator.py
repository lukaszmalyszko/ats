from query.query_validator.query_elements import Select


class QueryValidator:
    def __init__(self):
        self.next_element = Select()

    def validate_query(self, query_input):
        query = query_input.split(" ")
        for element in query:
            if self.next_element.validate(element):
                self.next_element = self.next_element.expected_element()
            else:
                raise InvalidQueryException(self.next_element.error_message)


class InvalidQueryException(Exception):
    def __init(self, message):
        self.message = message
