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
        self._stmt_map = {}
        self._variables_map = {}
        self._while_map = {}
        self._if_map = {}
        self._assign_map = {}

        self._traverse(ast_tree)

    def get_nodes_map(self):
        return self._node_map

    def get_stmt_map(self):
        return self._stmt_map

    def get_if_map(self):
        return self._if_map

    def get_while_map(self):
        return self._while_map

    def get_assign_map(self):
        return self._assign_map

    def get_variables_map(self):
        return self._variables_map

    def isParent(self, parent, child):
        return self._parent_map.get(child) == parent

    def isFollowing(self, curr, prev):
        return self._follows_map.get(curr) == prev

    def isUsing(self, variable, line):
        return variable in self._parent_map.get(line)

    def isModifing(self, variable, line):
        return line in self._modifies_map.get(variable)

    # def isCalling(self, line, proc):
    #     return False;

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
            self.__add_to_stmt_list(stmt)

            if self._ast.get_type(stmt) == NodeType.WHILE:
                self.__traverse_stmt_lst(self._ast.get_child(stmt, 1), stmt)
                self.__add_uses(stmt, self._ast.get_child(stmt, 0))
                self.__add_to_while_list(stmt)

            if self._ast.get_type(stmt) == NodeType.IF:
                self.__traverse_stmt_lst(self._ast.get_child(stmt, 1), stmt)
                self.__add_uses(stmt, self._ast.get_child(stmt, 0))
                if len(self._ast.get_children(stmt)) > 2:
                    self.__traverse_stmt_lst(self._ast.get_child(stmt, 2), stmt)
                self.__add_to_if_list(stmt)

            if self._ast.get_type(stmt) == NodeType.ASSIGN:
                self.__create_node(self._ast.get_child(stmt, 0))
                self.__add_modifies(stmt)
                self.__add_uses_for_assign(stmt, self._ast.get_child(stmt, 1))
                self.__add_to_assign_list(stmt)

        self.__fill_follows(stmt_lst)

    def __create_node(self, node):
        if self._ast.get_type(node) == NodeType.VARIABLE:
            if self.__get_node_index(node) == -1:
                self._node_map.update({self.__index: node})
                self.__index += 1
                self.__add_to_variables_list(node)
            else:
                return
        else:
            self._node_map.update({self.__index: node})
            self.__index += 1
        return self.__index - 1

    def __get_node_index(self, node):
        for (key, value) in self._node_map.items():
            if self._ast.get_type(node) == NodeType.VARIABLE:
                if self._ast.get_node_value(value) == self._ast.get_node_value(node):
                    return key
            else:
                if value == node:
                    return key
        return -1

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

    def __add_to_stmt_list(self, stmt):
        self._stmt_map.update({
        self.__get_node_index(stmt) : stmt
        })

    def __add_to_if_list(self, if_node):
        self._if_map.update({
        self.__get_node_index(if_node) : if_node
        })

    def __add_to_while_list(self, while_node):
        self._while_map.update({
        self.__get_node_index(while_node) : while_node
        })

    def __add_to_assign_list(self, assign_node):
        self._assign_map.update({
        self.__get_node_index(assign_node) : assign_node
        })

    def __add_to_variables_list(self, node):
        self._variables_map.update({
        self.__get_node_index(node) : node
        })
