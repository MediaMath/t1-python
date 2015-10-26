class ParserException(Exception):
    def __init__(self, caught):
        self.caught = caught
