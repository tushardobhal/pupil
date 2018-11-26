class CommonData:

    def __init__(self):
        self.index = None
        self.timestamp = None

    def set_values(self, index, timestamp):
        self.index = index
        self.timestamp = timestamp

    def get_values(self):
        return self.index, self.timestamp

    def __repr__(self):
        return str(self.__dict__)