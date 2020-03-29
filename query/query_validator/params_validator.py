import re

from query.query_validator.exceptions import InvalidQueryException
from query.utils import INTEGER, IDENT


class ParamsValidator:
    @staticmethod
    def validate_statement_ref(ref, query_preprocessor):
        if re.match(INTEGER, ref):
            # TODO check if program contains line with such number
            pass
        if re.match(IDENT, ref):
            if not query_preprocessor.check_if_contains_variable(ref):
                raise InvalidQueryException("# Niepoprawny parametr statement")

    @staticmethod
    def validate_entity_ref(ref, query_preprocessor):
        pass
