class World:

    def __init__(self, index, timestamp, frame):
        self.index = index
        self.timestamp = timestamp
        self.frame = frame

    def __repr__(self):
        return str(self.__dict__)