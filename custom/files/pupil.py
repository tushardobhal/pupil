class Pupil:

    def __init__(self):
        self.eye_id = None
        self.norm_pos = None
        self.confidence = None
        self.timestamp = None

    def set_values(self, eye_id, norm_pos, confidence, timestamp):
        self.eye_id = eye_id
        self.norm_pos = norm_pos
        self.confidence = confidence
        self.timestamp = timestamp

    def get_values(self):
        return self.eye_id, self.norm_pos, self.confidence, self.timestamp

    def __repr__(self):
        return str(self.__dict__)