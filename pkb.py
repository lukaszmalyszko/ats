
class PKB:

    def __init__(self, ast_tree):
        self.__ast_tree = ast_tree
        self.__node_map = {}
        self.__follows_map = {}
        self.__uses_map = {}
        self.__modifies_map = {}

        self.__traverse(ast_tree)

    def __traverse(self, ast):
        print("Usage: file_name")
