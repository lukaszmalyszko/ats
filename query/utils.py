KEY_WORDS = [
    "Select",
    "such",
    "that",
    "with",
    "stmt",
    "while",
    "assign",
    "prog_line",
    "constant",
    "variable",
]

IDENT = "[a-zA-Z][a-zA-Z0-9#]*"
INTEGER = "[0-9]+"
STMT_REF = f"({IDENT})|[_]|{INTEGER}+"
ENT_REF = f"({IDENT})|[_]|['\"]({IDENT}['\"])"
PARAM_REF = f"({IDENT})|[_]|[0-9]+|['\"]({IDENT}['\"])"
REL_REF = f"[a-zA-Z]+[*]?[(]({PARAM_REF})+[ ]*[,][ ]*({PARAM_REF})+[)]"
