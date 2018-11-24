class Pupil:

    def __init__(self, eye_id, norm_pos, confidence, timestamp):
        self.eye_id = eye_id
        self.norm_pos = norm_pos
        self.confidence = confidence
        self.timestamp = timestamp

    def __repr__(self):
        return str(self.__dict__)