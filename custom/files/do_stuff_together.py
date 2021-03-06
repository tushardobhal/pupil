from files.logger import logger, logger2, logger_run_length

import time
import numpy as np


class DoStuffTogether:

    def __init__(self):
        self.last_frame_index_1 = 0
        self.last_frame_index_2 = 0
        self.prev_state = False
        self.objects = np.array(["cards", "dice", "key", "map", "phone", "ball"])

    def do_some_stuff_together(self, common_data_proxy_1, common_data_proxy_2):
        logger.info("Starting Do_Stuff_Together...")

        while True:
            common_data_1 = common_data_proxy_1.get_values()
            common_data_2 = common_data_proxy_2.get_values()
            if common_data_1[0] is None or common_data_2[0] is None or (
                    common_data_1[2] == self.last_frame_index_1 and common_data_2[2] == self.last_frame_index_2):
                continue

            # logger.info("Glass_1 Frame - {}, Glass_2 Frame - {}, Glass_1 Timestamp - {}, Glass_2 Timestamp - {}".format(
            #     common_data_1[2], common_data_2[2], common_data_1[1], common_data_2[1]))
            # logger.info("Glass_1 output - {}, Glass_2 output - {}".format(common_data_1[3], common_data_2[3]))

            common_look_time = int(time.time() * 1000)
            logger_run_length.info(
                ";time-{};Glass1_hit_scan_output-{};Glass2_hit_scan_output-{};Glass1_run_length_output-{};Glass2_run_length_output-{};Frame1-{};Frame2-{}".format(
                    common_look_time, common_data_1[4], common_data_2[4], common_data_1[3], common_data_2[3], common_data_1[2], common_data_2[2]))

            if common_data_1[3] == common_data_2[3] and sum(common_data_1[3]) != 0:
                if not self.prev_state:
                    self.prev_state = True
                    obj_idx = np.argmax(common_data_1[3])
                    logger2.info("Look Detected;{}:{}".format(self.objects[obj_idx], common_look_time))

                play_sound()
            else:
                self.prev_state = False

            self.last_frame_index_1 = common_data_1[2]
            self.last_frame_index_2 = common_data_2[2]


def play_sound():
    print('\a')
