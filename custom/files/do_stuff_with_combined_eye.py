from files.logger import logger

import numpy as np
import cv2


class DoStuffWithCombinedEye:
    def __init__(self, glass_id, confidence_threshold):
        self.last_frmae_processed = 0
        self.glass_id = glass_id
        self.confidence_threshold = confidence_threshold

    def do_some_stuff(self, world_proxy, eye_0_proxy, common_data_proxy):
        logger.info('Starting Do_Stuff...')

        while True:
            world = world_proxy.get_values()
            pupil_0 = eye_0_proxy.get_values()

            if world[0] is None or pupil_0[0] is None or self.last_frmae_processed == world[0]:
                continue
            logger.info("Frame - {}, Timestamp - {}".format(world[0], world[2]))
            logger.info(
                "Eye_Id - {}, Norm_Pos - {}, Confidence - {}, Timestamp - {}".format(pupil_0[0], pupil_0[1], pupil_0[2],
                                                                                     pupil_0[3]))

            pupil_loc = self.denormalize(pupil_0[1], world[1].shape[:-1][::-1], True)

            cv2.imshow('frame.world_{}'.format(self.glass_id),
                       cv2.circle(world[1], (int(pupil_loc[0]), int(pupil_loc[1])), 5, (0, 0, 255), -1))
            cv2.waitKey(1)
            self.last_frmae_processed = world[0]

            common_data_proxy.set_values(world[0], world[2])

    def denormalize(self, pos, size, flip_y=False):
        width, height = size
        x = pos[0]
        y = pos[1]
        x *= width
        if flip_y:
            y = 1 - y
        y *= height
        return x, y
