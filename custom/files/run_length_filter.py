class RunLengthFilter:
    def __init__(self):
        self.cur_state = 1
        self.total_num_states = 6

    def update_run_length_filter(self, hit):
        if 1 <= self.cur_state <= (self.total_num_states / 2 - 1):
            if hit == 1:
                self.cur_state = self.cur_state + 1
                out = 0
            else:
                self.cur_state = 1
                out = 0

        elif self.cur_state == self.total_num_states / 2:
            if hit == 1:
                self.cur_state = self.cur_state + 1
                out = 1
            else:
                self.cur_state = 1
                out = 0

        elif self.total_num_states / 2 <= self.cur_state <= (self.total_num_states - 1):
            if hit == 0:
                self.cur_state = self.cur_state + 1
                out = 1
            else:
                self.cur_state = self.total_num_states / 2 + 1
                out = 1

        else:
            if hit == 0:
                self.cur_state = 1
                out = 0
            else:
                self.cur_state = self.total_num_states / 2 + 1
                out = 1

        return out
