class CommonData:

    def __init__(self):
        self.glass_id = None
        self.timestamp = None
        self.index = None
        self.run_length_output = None
        self.hit_scan_output = None

    def set_values(self, glass_id, timestamp, index, run_length_output, hit_scan_output):
        self.glass_id = glass_id
        self.timestamp = timestamp
        self.index = index
        self.run_length_output = run_length_output
        self.hit_scan_output = hit_scan_output

    def get_values(self):
        return self.glass_id, self.timestamp, self.index, self.run_length_output, self.hit_scan_output

    def __repr__(self):
        return str(self.__dict__)