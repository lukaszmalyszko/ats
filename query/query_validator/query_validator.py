from query.query_validator.query_elements import Select


class QueryValidator:
    def __init__(self):
        self.next_element = Select()

    def validate_query(self, query_string):
        query_elements = self.__get_query_elements(query_string)
        for element in query_elements:
            if self.next_element.validate(element):
                self.next_element = self.next_element.expected_element()
            else:
                raise InvalidQueryException(self.next_element.error_message)

    def __get_query_elements(self, query_string):
        elements = []
        buffer = ""
        relation = False
        for char in query_string:
            if char == "(":
                relation = True
            if char == ")":
                relation = False
            if buffer.endswith(" ") and relation is False:
                elements.append(buffer)
                buffer = ""
            buffer = buffer + char
        elements.append(buffer)
        elements = [element.strip(" ") for element in elements]
        return elements


class InvalidQueryException(Exception):
    def __init(self, message):
        self.message = message
