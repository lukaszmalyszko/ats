class QueryTree:
    def __init__(self):
        self._select = None
        self._result = None
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

    def set_select(self, node):
        self._select = node

    def add_such_that(self, node):
        self._statements["such_that"].append(node)

    def get_such_that_statements(self):
        return self._statements["such_that"]
