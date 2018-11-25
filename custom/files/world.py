class World:

    def __init__(self):
        self.index = None
        self.timestamp = None
        self.frame = None

    def set_values(self, index, frame, timestamp):
        self.index = index
        self.frame = frame
        self.timestamp = timestamp

    def get_values(self):
        return self.index, self.frame, self.timestamp

    def __repr__(self):
        return str(self.__dict__)