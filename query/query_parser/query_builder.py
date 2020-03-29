from query.query_parser.query_parser import QueryParser
from query.query_tree.query_tree import QueryTree
from query.query_tree.tree_nodes import Root


class QueryBuilder(QueryParser):
    def __init__(self, query_preprocessor):
        super().__init__(query_preprocessor)

    def build_query(self, query_string):
        query_elements = self.parse_query(query_string)
        tree = QueryTree()
        tree.root = Root()
        for element in query_elements:
            self.expected_element.create_node(element, tree)
            self.expected_element = self.expected_element.next(self.query_preprocessor)
        return tree
