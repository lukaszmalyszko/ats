from typing import Any, Dict, Set
from ast import AST, NodeType


class PKB:
    _ast = AST()

    _parent_map: Dict[int, int]
    _follows_map: Dict[int, int]
    _uses_map: Dict[int, Set[str]]
    _modifies_map: Dict[str, Set[int]]
    _calls_map: Dict[str, Set[str]]

    def __init__(self, ast_tree):
        self._ast_tree = ast_tree
        self._node_map = {}
        self._parent_map = {}
        self._follows_map = {}
        self._uses_map = {}
        self._modifies_map = {}
        self._calls_map = {}

        self.__index = 0

        self._traverse(ast_tree)

    def _traverse(self, ast):
        for procedure in ast:
            self.__create_node(procedure)
            self.__traverse_stmt_lst(
                self._ast.get_child(procedure, 0)
                , procedure)

        print("Usage: file_name")

    def __traverse_stmt_lst(self, stmt_lst, parent):
        for stmt in self._ast.get_children(stmt_lst):
            self.__create_node(stmt)
            self.__add_parent(stmt, parent)

            if self._ast.get_type(stmt) == NodeType.WHILE:
                self.__traverse_stmt_lst(self._ast.get_child(stmt, 1), stmt)
                self.__add_uses(stmt, self._ast.get_child(stmt, 0))

            if self._ast.get_type(stmt) == NodeType.IF:
                self.__traverse_stmt_lst(self._ast.get_child(stmt, 1), stmt)
                self.__add_uses(stmt, self._ast.get_child(stmt, 0))
                if len(self._ast.get_children(stmt)) > 2:
                    self.__traverse_stmt_lst(self._ast.get_child(stmt, 2), stmt)

            if self._ast.get_type(stmt) == NodeType.ASSIGN:
                self.__add_modifies(stmt)
                self.__add_uses_for_assign(stmt, self._ast.get_child(stmt, 1))

        self.__fill_follows(stmt_lst)

    def __create_node(self, node):
        self._node_map.update({self.__index: node})
        self.__index += 1
        return self.__index - 1

    def __get_node_index(self, node):
        for (key, value) in self._node_map.items():
            if value == node:
                return key
        raise Exception("Index not found")

    def __add_parent(self, node, parent):
        self._parent_map.update({
            self.__get_node_index(node): self.__get_node_index(parent)
        })

    def __add_modifies(self, node):
        self._modifies_map.update({
            self.__get_node_index(node): self._ast.get_node_value(self._ast.get_child(node, 0))
        })

    def __add_uses_for_assign(self, node, processed_node):
        if isinstance(processed_node,list):
            for child in processed_node:
                self.__add_uses_for_assign(node, child)

        else:
            child_type = self._ast.get_type(processed_node)
            if child_type == NodeType.VARIABLE:
                self.__add_uses(node, processed_node)
            elif child_type == NodeType.ARITHMETIC:
                self.__add_uses_for_assign(node, self._ast.get_children(processed_node))

        print("a")

    def __add_uses(self, node, var):
        self._uses_map.update({
            self.__get_node_index(node): self._ast.get_node_value(var)
        })

    def __fill_follows(self, stmt_lst):
        prev_node = None
        for stmt in self._ast.get_children(stmt_lst):
            if prev_node:
                self._follows_map.update({
                    self.__get_node_index(stmt): self.__get_node_index(prev_node)
                })
            prev_node = stmt
