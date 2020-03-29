import re
from abc import abstractmethod

from query.query_validator.exceptions import InvalidQueryException
from query.utils import REL_REF, IDENT, KEY_WORDS


class Element:
    def __init__(self):
        self.value = []
        self.error_message = "# Błąd w zapytaniu"
        self.next = Element

    def validate(self, value):
        element = [
            element
            for element in CONTSTRUCTION_TO_NEXT_MAPPING.keys()
            if element == value
        ]
        if not element:
            raise InvalidQueryException(self.error_message)
        self.next = CONTSTRUCTION_TO_NEXT_MAPPING[element[0]]
        return True


class Select(Element):
    def __init__(self):
        super().__init__()
        self.value = ["Select"]
        self.error_message = '# Zapytanie nie zaczyna się od "Select"'
        self.next = Variable

    def validate(self, value):
        if value not in self.value:
            raise InvalidQueryException(self.error_message)


class Variable(Element):
    def __init__(self):
        super().__init__()
        self.value = []
        self.error_message = "# Oczekiwana poprawna nazwa elementu"
        self.next = Element

    def validate(self, value):
        if not re.match(IDENT, value) or value in KEY_WORDS:
            raise InvalidQueryException(self.error_message)


class Such(Element):
    def __init__(self):
        super().__init__()
        self.value = ["such"]
        self.error_message = '# Oczekiwana klauzula "such that"'
        self.next = That

    def validate(self, value):
        if value not in self.value:
            raise InvalidQueryException(self.error_message)


class That(Element):
    def __init__(self):
        super().__init__()
        self.value = ["that"]
        self.error_message = '# Niepoprawna klauzula "such that"'
        self.next = Relation

    def validate(self, value):
        if value not in self.value:
            raise InvalidQueryException(self.error_message)


class Relation(Element):
    def __init__(self):
        super().__init__()
        self.value = []
        self.error_message = "# Niepoprawna składnia relacji"
        self.next = Element  # TODO w przyszłości zmiana na with

        self.first_param = ""
        self.second_param = ""

    def validate(self, value):
        relation = list(filter(value.startswith, RELATION_TO_MODEL.keys()))
        if not relation or not self._is_params_syntax_correct(value):
            raise InvalidQueryException(self.error_message)
        else:
            model = RELATION_TO_MODEL[relation[0]]()
            model.extract_params(value)
            model.validate_params()

    def extract_params(self, value):
        buffer = ""
        first_param = False
        second_param = False
        for char in value:
            if "(" in char:
                first_param = True
                continue
            if "," in char:
                self.first_param = buffer.strip(" ")
                buffer = ""
                first_param = False
                second_param = True
                continue
            if ")" in char:
                self.second_param = buffer.strip(" ")
                second_param = False
                continue
            if first_param is True or second_param is True:
                buffer = buffer + char

    @abstractmethod
    def validate_params(self):
        pass

    def _is_params_syntax_correct(self, value):
        return re.match(REL_REF, value)


class Modifies(Relation):
    def __init__(self):
        super().__init__()
        self.error_message = "# Niepoprawna składnia Modifies"
        self.next = Element

    def validate_params(self):
        # Modifies(stmtRef, entRef)

        pass


class Uses(Relation):
    def __init__(self):
        super().__init__()
        self.error_message = "# Niepoprawna składnia Uses"
        self.next = Element

    def validate_params(self):
        pass


class Parent(Relation):
    def __init__(self):
        super().__init__()
        self.error_message = "# Niepoprawna składnia Parent"
        self.next = Element

    def validate_params(self):
        pass


class ParentStar(Relation):
    def __init__(self):
        super().__init__()
        self.error_message = "# Niepoprawna składnia Parent*"
        self.next = Element

    def validate_params(self):
        pass


class Follows(Relation):
    def __init__(self):
        super().__init__()
        self.error_message = "# Niepoprawna składnia Follows"
        self.next = Element

    def validate_params(self):
        pass


class FollowsStar(Relation):
    def __init__(self):
        super().__init__()
        self.error_message = "# Niepoprawna składnia Follows*"
        self.next = Element

    def validate_params(self):
        pass


class Condition(Element):
    def __init__(self):
        super().__init__()
        self.error_message = "# Niepoprawna składnia warunku"
        self.next = Element


RELATION_TO_MODEL = {
    "Modifies": Modifies,
    "Uses": Uses,
    "Parent": Parent,
    "Parent*": ParentStar,
    "Follows": Follows,
    "Follows*": FollowsStar,
}

CONTSTRUCTION_TO_NEXT_MAPPING = {
    "Select": Variable,
    "such": That,
    "that": Relation,
    "pattern": None,
    "with": Condition,
}
