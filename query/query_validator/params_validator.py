import re

from query.query_validator.exceptions import InvalidQueryException
from query.utils import INTEGER, IDENT


class ParamsValidator:
    @staticmethod
    def is_variable_ref_correct(ref, query_preprocessor):
        if not query_preprocessor.check_if_contains_variable(ref):
            return False
        return True

    @staticmethod
    def is_statement_ref_correct(ref, query_preprocessor):
        if re.match(INTEGER, ref):
            # TODO check if program contains line with such number
            return True
        if not query_preprocessor.check_if_contains_variable(ref) and ref is not "_":
            return False
        return True

    @staticmethod
    def is_entity_ref_correct(ref, query_preprocessor):
        if re.match(f"(['\"]{IDENT}['\"])", ref):
            # TODO check if program contains such variable
            return True
        if not query_preprocessor.check_if_contains_variable(ref) and ref is not "_":
            return False
        return True
