import re

from query.query_parser.exceptions import InvalidQueryParamException
from query.utils import INTEGER, IDENT


class ParamsValidator:
    @staticmethod
    def get_variable_ref(ref, query_preprocessor):
        variable = query_preprocessor.symbols.get_symbol(ref)
        if not variable:
            raise InvalidQueryParamException("# Niepoprawne parametry")
        return variable

    @staticmethod
    def get_statement_ref(ref, query_preprocessor):
        if re.match(INTEGER, ref):
            # TODO check if program contains line with such number
            raise NotImplementedError
        if ref is "_":
            return "_"
        stmt_ref = query_preprocessor.symbols.get_symbol(ref)
        if not stmt_ref:
            raise InvalidQueryParamException("# Niepoprawne parametry")
        return stmt_ref

    @staticmethod
    def get_entity_ref(ref, query_preprocessor):
        if re.match(f"(['\"]{IDENT}['\"])", ref):
            # TODO check if program contains such variable
            return ref.strip("'")
        if ref is "_":
            return "_"
        entity_ref = query_preprocessor.symbols.get_symbol(ref)
        if not entity_ref or entity_ref.type != "ref":
            raise InvalidQueryParamException("# Niepoprawne parametry")
        return entity_ref

    @staticmethod
    def get_condition_variable(ref, query_preprocessor):
        if re.match(f"({IDENT}[.\"][a-zA-Z#]*)", ref):
            var, attr_name = ref.split(".")
            entity_ref = query_preprocessor.symbols.get_symbol(var)
            if not entity_ref:
                raise InvalidQueryParamException("# Niepoprawne parametry warunku")
            return entity_ref, attr_name
        raise InvalidQueryParamException("# Niepoprawne parametry warunku")

    @staticmethod
    def get_condition_value(ref):
        if re.match(f"(['\"]{IDENT}['\"])", ref):
            return ref.strip("'")
        return ref

