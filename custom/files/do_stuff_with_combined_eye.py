from files.logger import logger
from files.run_length_filter import RunLengthFilter

import numpy as np
import cv2


class DoStuffWithCombinedEye:
    def __init__(self, glass_id, confidence_threshold):
        self.last_frame_processed = 0
        self.glass_id = glass_id
        self.confidence_threshold = confidence_threshold

    def do_some_stuff(self, world_proxy, eye_0_proxy, common_data_proxy):
        logger.info('Starting Do_Stuff...')

        while True:
            world = world_proxy.get_values()
            pupil_0 = eye_0_proxy.get_values()

            if world[0] is None or pupil_0[0] is None or self.last_frame_processed == world[2]:
                continue
            # logger.info("Frame - {}, Timestamp - {}".format(world[2], world[1]))
            # logger.info(
            #     "Eye_Id - {}, Norm_Pos - {}, Confidence - {}, Timestamp - {}".format(pupil_0[2], pupil_0[3], pupil_0[4],
            #                                                                          pupil_0[1]))
            # logger.info(
            #     "Eye_Id - {}, Norm_Pos - {}, Confidence - {}, Timestamp - {}".format(pupil_1[2], pupil_1[3], pupil_1[4],
            #                                                                          pupil_1[1]))

            pupil_loc = pupil_0[3]
            confidence = pupil_0[4]

            self.last_frame_processed = world[2]

            common_data_proxy.set_values(self.glass_id, world[1], world[2], world[3], pupil_loc, confidence)
