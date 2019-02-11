class CommonData:

    def __init__(self):
        self.glass_id = None
        self.timestamp = None
        self.index = None
        self.image = None
        self.pupil_loc = None
        self.confidence = None

    def set_values(self, glass_id, timestamp, index, image, pupil_loc, confidence):
        self.glass_id = glass_id
        self.timestamp = timestamp
        self.index = index
        self.image = image
        self.pupil_loc = pupil_loc
        self.confidence = confidence

    def get_values(self):
        return self.glass_id, self.timestamp, self.index, self.image, self.pupil_loc, self.confidence

    def __repr__(self):
        return str(self.__dict__)
