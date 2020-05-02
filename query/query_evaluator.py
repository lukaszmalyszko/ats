from query.query_preprocessor import QueryPreprocessor


class QueryEvaluator:
    def __init__(self, pkb):
        self.preprocessor = QueryPreprocessor()
        self.pkb = pkb

    def load(self):
        self.preprocessor.get_input()

    def get_result(self):
        tree = self.preprocessor.get_tree()
        tree.evaluate(self.pkb)
        result = tree.result
        return self.__parse_result(result)

    def __parse_result(self, result):
        result_str = ""
        for item in result:
            result_str = f"{result_str}{item}, "
        return result_str[:-2]
