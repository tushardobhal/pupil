class Pupil:

    def __init__(self):
        self.glass_id = None
        self.eye_id = None
        self.norm_pos = None
        self.confidence = None
        self.timestamp = None

    def set_values(self, glass_id, timestamp, eye_id, norm_pos, confidence):
        self.glass_id = glass_id
        self.eye_id = eye_id
        self.norm_pos = norm_pos
        self.confidence = confidence
        self.timestamp = timestamp

    def get_values(self):
        return self.glass_id, self.timestamp, self.eye_id, self.norm_pos, self.confidence

    def __repr__(self):
        return str(self.__dict__)
