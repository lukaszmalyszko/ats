class Element:
    def __init__(self):
        self.value = []
        self.error_message = ""


class Select(Element):
    def __init__(self):
        super().__init__()
        self.value = ["Select"]
        self.error_message = '# Zapytanie nie zaczyna się od "Select"'
