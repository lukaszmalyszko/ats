import re
from abc import abstractmethod

from query.query_validator.exceptions import InvalidQueryException
from query.query_validator.params_validator import ParamsValidator
from query.utils import REL_REF


class Element:
    def __init__(self, query_preprocessor):
        self.query_preprocessor = query_preprocessor
        self.value = []
        self.error_message = "# Błąd w zapytaniu"
        self.next = Element

    def validate(self, value):
        element = [
            element
            for element in CONSTRUCTION_TO_NEXT_MAPPING.keys()
            if element == value
        ]
        if not element:
            raise InvalidQueryException(self.error_message)
        self.next = CONSTRUCTION_TO_NEXT_MAPPING[element[0]]
        return True

    def can_query_be_finished(self):
        return True

    @abstractmethod
    def create_node(self, value):
        pass


class Select(Element):
    def __init__(self, query_preprocessor):
        super().__init__(query_preprocessor)
        self.value = ["Select"]
        self.error_message = '# Zapytanie nie zaczyna się od "Select"'
        self.next = Variable

    def validate(self, value):
        if value not in self.value:
            raise InvalidQueryException(self.error_message)

    def can_query_be_finished(self):
        return False

    def create_node(self, value):
        pass


class Variable(Element):
    def __init__(self, query_preprocessor):
        super().__init__(query_preprocessor)
        self.value = []
        self.error_message = "# Oczekiwana poprawna nazwa elementu"
        self.next = Element

    def validate(self, value):
        does_variable_exist = ParamsValidator.is_variable_ref_correct(
            value, self.query_preprocessor
        )
        if not does_variable_exist:
            raise InvalidQueryException(self.error_message)

    def can_query_be_finished(self):
        return False

    def create_node(self, value):
        # TODO
        pass


class Such(Element):
    def __init__(self, query_preprocessor):
        super().__init__(query_preprocessor)
        self.value = ["such"]
        self.error_message = '# Oczekiwana klauzula "such that"'
        self.next = That

    def validate(self, value):
        if value not in self.value:
            raise InvalidQueryException(self.error_message)

    def can_query_be_finished(self):
        return False

    def create_node(self, value):
        # TODO
        pass


class That(Element):
    def __init__(self, query_preprocessor):
        super().__init__(query_preprocessor)
        self.value = ["that"]
        self.error_message = '# Niepoprawna klauzula "such that"'
        self.next = Relation

    def validate(self, value):
        if value not in self.value:
            raise InvalidQueryException(self.error_message)

    def can_query_be_finished(self):
        return False

    def create_node(self, value):
        # TODO
        pass


class Relation(Element):
    def __init__(self, query_preprocessor):
        super().__init__(query_preprocessor)
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
            model = RELATION_TO_MODEL[relation[-1]](self.query_preprocessor)
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

    def can_query_be_finished(self):
        return False

    def _is_params_syntax_correct(self, value):
        return re.match(REL_REF, value)

    def create_node(self, value):
        # TODO
        pass


class Modifies(Relation):
    def __init__(self, query_preprocessor):
        super().__init__(query_preprocessor)
        self.error_message = "# Niepoprawna składnia Modifies"
        self.next = Element

    def validate_params(self):
        # Modifies(stmtRef, entRef)
        is_first_param_correct = ParamsValidator.is_statement_ref_correct(
            self.first_param, self.query_preprocessor
        )
        is_second_param_correct = ParamsValidator.is_entity_ref_correct(
            self.second_param, self.query_preprocessor
        )
        if not is_first_param_correct or not is_second_param_correct:
            raise InvalidQueryException("# Niepoprawne parametry w Modifies")


class Uses(Relation):
    def __init__(self, query_preprocessor):
        super().__init__(query_preprocessor)
        self.error_message = "# Niepoprawna składnia Uses"
        self.next = Element

    def validate_params(self):
        # Uses(stmtRef, entRef)
        is_first_param_correct = ParamsValidator.is_statement_ref_correct(
            self.first_param, self.query_preprocessor
        )
        is_second_param_correct = ParamsValidator.is_entity_ref_correct(
            self.second_param, self.query_preprocessor
        )
        if not is_first_param_correct or not is_second_param_correct:
            raise InvalidQueryException("# Niepoprawne parametry w Uses")


class Parent(Relation):
    def __init__(self, query_preprocessor):
        super().__init__(query_preprocessor)
        self.error_message = "# Niepoprawna składnia Parent"
        self.next = Element

    def validate_params(self):
        # Parent(stmtRef, stmtRef)
        is_first_param_correct = ParamsValidator.is_statement_ref_correct(
            self.first_param, self.query_preprocessor
        )
        is_second_param_correct = ParamsValidator.is_statement_ref_correct(
            self.second_param, self.query_preprocessor
        )
        if not is_first_param_correct or not is_second_param_correct:
            raise InvalidQueryException("# Niepoprawne parametry w Parent")


class ParentStar(Relation):
    def __init__(self, query_preprocessor):
        super().__init__(query_preprocessor)
        self.error_message = "# Niepoprawna składnia Parent*"
        self.next = Element

    def validate_params(self):
        # Parent*(stmtRef, stmtRef)
        is_first_param_correct = ParamsValidator.is_statement_ref_correct(
            self.first_param, self.query_preprocessor
        )
        is_second_param_correct = ParamsValidator.is_statement_ref_correct(
            self.second_param, self.query_preprocessor
        )
        if not is_first_param_correct or not is_second_param_correct:
            raise InvalidQueryException("# Niepoprawne parametry w Parent*")


class Follows(Relation):
    def __init__(self, query_preprocessor):
        super().__init__(query_preprocessor)
        self.error_message = "# Niepoprawna składnia Follows"
        self.next = Element

    def validate_params(self):
        # Follows(stmtRef, stmtRef)
        is_first_param_correct = ParamsValidator.is_statement_ref_correct(
            self.first_param, self.query_preprocessor
        )
        is_second_param_correct = ParamsValidator.is_statement_ref_correct(
            self.second_param, self.query_preprocessor
        )
        if not is_first_param_correct or not is_second_param_correct:
            raise InvalidQueryException("# Niepoprawne parametry w Follows")


class FollowsStar(Relation):
    def __init__(self, query_preprocessor):
        super().__init__(query_preprocessor)
        self.error_message = "# Niepoprawna składnia Follows*"
        self.next = Element

    def validate_params(self):
        # Follows*(stmtRef, stmtRef)
        is_first_param_correct = ParamsValidator.is_statement_ref_correct(
            self.first_param, self.query_preprocessor
        )
        is_second_param_correct = ParamsValidator.is_statement_ref_correct(
            self.second_param, self.query_preprocessor
        )
        if not is_first_param_correct or not is_second_param_correct:
            raise InvalidQueryException("# Niepoprawne parametry w Follows*")


class Condition(Element):
    def __init__(self, query_preprocessor):
        super().__init__(query_preprocessor)
        self.error_message = "# Niepoprawna składnia warunku"
        self.next = Element

    def validate(self, value):
        if not re.match(REL_REF, value):
            raise InvalidQueryException(self.error_message)
        # TODO attributes validation

    def can_query_be_finished(self):
        return False

    def create_node(self, value):
        # TODO
        pass


RELATION_TO_MODEL = {
    "Modifies": Modifies,
    "Uses": Uses,
    "Parent": Parent,
    "Parent*": ParentStar,
    "Follows": Follows,
    "Follows*": FollowsStar,
}

CONSTRUCTION_TO_NEXT_MAPPING = {
    "Select": Variable,
    "such": That,
    "that": Relation,
    "pattern": None,
    "with": Condition,
}
