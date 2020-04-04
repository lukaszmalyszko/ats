from collections import defaultdict
from typing import Dict
from typing import List
from typing import Set

from ast import Node
from parser_ import StmtCall, StmtIf, StmtWhile, StmtAssign


class PKB:
    __calls_map: Dict[str, Set[str]]
    __calls_map_rev: Dict[str, Set[str]]
    __modifies_map: Dict[str, Set[str]]
    __modifies_map_rev: Dict[str, Set[str]]
    __follows_map: Dict[str, Set[str]]
    __follows_map_rev: Dict[str, Set[str]]

    def __init__(self, ast_tree):
        self.__ast_tree = ast_tree
        self.__node_map = {}
        self.__follows_map = {}
        self.__uses_map = {}
        self.__modifies_map = defaultdict(set)
        self.__modifies_map_rev = defaultdict(set)
        self.__calls_map = defaultdict(set)
        self.__calls_map_rev = defaultdict(set)
        self.__follows_map = defaultdict(set)
        self.__follows_map_rev = defaultdict(set)
        self.__traverse(ast_tree)

    def __traverse(self, ast):
        self.__index_calls(ast.stmt_lst, ast.proc_name)
        self.__index_modifies(ast.stmt_lst, ast.proc_name)
        self.__index_follows(ast.stmt_lst)
        print("Usage: file_name")

    def __index_calls(self, stmts: List[Node], proc_name):
        for stmt in stmts:
            if isinstance(stmt, StmtCall):
                self.__calls_map[proc_name].add(stmt.proc_name)
            if isinstance(stmt, StmtIf):
                self.__index_calls(stmt.then, proc_name)
                self.__index_calls(stmt.else_, proc_name)
            if isinstance(stmt, StmtWhile):
                self.__index_calls(stmt.stmt_lst, proc_name)

        for k, v in self.__calls_map.items():
            for item in v:
                self.__calls_map_rev[item].add(k)

    def __index_follows(self, stmts:List):
        stmts.sort(key=lambda stmt: stmt.line)
        prev = None
        for stmt in stmts:
            if prev is not None:
                # print(prev.line, ' -> ', stmt.line)
                self.__follows_map[prev.line].add(stmt.line)
                self.__follows_map_rev[stmt.line].add(prev.line)
            if isinstance(stmt, StmtIf):
                self.__index_follows(stmt.then)
                self.__index_follows(stmt.else_)
            if isinstance(stmt, StmtWhile):
                self.__index_follows(stmt.stmt_lst)
            prev = stmt

    def __index_uses(self):
        print("Usage: file_name")

    def __index_modifies(self, stmts, proc_name):
        for stmt in stmts:
            if isinstance(stmt, StmtAssign):
                self.__modifies_map[stmt.var_name].add(stmt.line)
                self.__modifies_map[stmt.var_name].add(proc_name)

        for k, v in self.__modifies_map.items():
            for item in v:
                self.__modifies_map_rev[item].add(k)
