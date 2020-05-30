class QueryTree:
    def __init__(self):
        self._select = None
        self._result = {}
        self._statements = {
            "such_that": [],
            "with": [],
            "pattern": [],
        }

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, node):
        self._result = node

    @property
    def select(self):
        return self._select

    def is_selected(self, node):
        return node in self._select.variables

    def set_select(self, node):
        node.set_parent(self)
        self._select = node

    def add_such_that(self, node):
        node.set_parent(self)
        self._statements["such_that"].append(node)

    def get_such_that_statements(self):
        return self._statements["such_that"]

    def add_with(self, node):
        node.set_parent(self)
        self._statements["with"].append(node)

    def get_with_statements(self):
        return self._statements["with"]

    def evaluate(self, pkb):
        self.__evaluate_relations(pkb)

    def get_result(self):
        result = {key: value for (key, value) in self.result.items() if key in self.select.variables}
        return set(zip(*result.values()))

    def __evaluate_relations(self, pkb):
        for node in self._statements["such_that"]:
            self._result.update(node.evaluate(pkb, self._statements["with"]))
