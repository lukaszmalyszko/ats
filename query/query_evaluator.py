from query.query_preprocessor import QueryPreprocessor


class QueryEvaluator:
    def __init__(self, pkb):
        self.preprocessor = QueryPreprocessor(pkb)
        self.pkb = pkb

    def load(self):
        self.preprocessor.get_input()

    def get_result(self):
        tree = self.preprocessor.get_tree()
        tree.evaluate(self.pkb)
        result = tree.get_result()
        result = self.__parse_result(result)
        if len(result) == 0:
            result = 'none'
        return result

    def __parse_result(self, result):
        result_str = ""
        result_list = list(result)
        result_list.sort()
        for items in result_list:
            if len(items) > 1:
                single_result = ""
                for item in items:
                    single_result = f"{single_result}{item} "
                result_str = f"{result_str}{single_result[:-1]}, "
            else:
                result_str = f"{result_str}{items[0]}, "
        return result_str[:-2]
