class World:

    def __init__(self):
        self.glass_id = None
        self.index = None
        self.timestamp = None
        self.frame = None

    def set_values(self, glass_id, timestamp, index, frame):
        self.glass_id = glass_id
        self.index = index
        self.frame = frame
        self.timestamp = timestamp

    def get_values(self):
        return self.glass_id, self.timestamp, self.index, self.frame

    def __repr__(self):
        return str(self.__dict__)
