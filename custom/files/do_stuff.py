from files.logger import logger

import numpy as np


class DoStuff:
    def __init__(self, glass_id, confidence_threshold):
        self.last_frame_processed = 0
        self.glass_id = glass_id
        self.confidence_threshold = confidence_threshold

    def do_some_stuff(self, world_proxy, eye_0_proxy, eye_1_proxy, common_data_proxy):
        logger.info('Starting Do_Stuff...')

        while True:
            world = world_proxy.get_values()
            pupil_0 = eye_0_proxy.get_values()
            pupil_1 = eye_1_proxy.get_values()

            if world[0] is None or pupil_0[0] is None or pupil_1[0] is None or self.last_frame_processed == world[2]:
                continue
            # logger.info("Frame - {}, Timestamp - {}".format(world[2], world[1]))
            # logger.info(
            #     "Eye_Id - {}, Norm_Pos - {}, Confidence - {}, Timestamp - {}".format(pupil_0[2], pupil_0[3], pupil_0[4],
            #                                                                          pupil_0[1]))
            # logger.info(
            #     "Eye_Id - {}, Norm_Pos - {}, Confidence - {}, Timestamp - {}".format(pupil_1[2], pupil_1[3], pupil_1[4],
            #                                                                          pupil_1[1]))

            if pupil_0[4] > self.confidence_threshold and pupil_1[4] > self.confidence_threshold:
                pupil_loc = np.mean([pupil_0[3], pupil_1[3]], axis=0)
                confidence = np.mean([pupil_0[4], pupil_1[4]])
            elif pupil_0[4] > pupil_1[4]:
                pupil_loc = pupil_0[3]
                confidence = pupil_0[4]
            else:
                pupil_loc = pupil_1[3]
                confidence = pupil_1[4]

            self.last_frame_processed = world[2]

            common_data_proxy.set_values(self.glass_id, world[1], world[2], world[3], pupil_loc, confidence)
