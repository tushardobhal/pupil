from files.logger import logger

import numpy as np
import cv2


class DoStuff:
    def __init__(self, glass_id, confidence_threshold, object_detect, debug):
        self.last_frmae_processed = 0
        self.glass_id = glass_id
        self.confidence_threshold = confidence_threshold
        self.object_detect = object_detect
        self.debug = debug

    def do_some_stuff(self, world_proxy, eye_0_proxy, eye_1_proxy, common_data_proxy):
        logger.info('Starting Do_Stuff...')

        while True:
            world = world_proxy.get_values()
            pupil_0 = eye_0_proxy.get_values()
            pupil_1 = eye_1_proxy.get_values()

            if world[0] is None or pupil_0[0] is None or pupil_1[0] is None or self.last_frmae_processed == world[0]:
                continue
            logger.info("Frame - {}, Timestamp - {}".format(world[0], world[2]))
            logger.info(
                "Eye_Id - {}, Norm_Pos - {}, Confidence - {}, Timestamp - {}".format(pupil_0[0], pupil_0[1], pupil_0[2],
                                                                                     pupil_0[3]))
            logger.info(
                "Eye_Id - {}, Norm_Pos - {}, Confidence - {}, Timestamp - {}".format(pupil_1[0], pupil_1[1], pupil_1[2],
                                                                                     pupil_1[3]))

            if pupil_0[2] > self.confidence_threshold and pupil_1[2] > self.confidence_threshold:
                pupil_loc = self.denormalize(np.mean([pupil_0[1], pupil_1[1]], axis=0), world[1].shape[:-1][::-1], True)
            elif pupil_0[2] > pupil_1[2]:
                pupil_loc = self.denormalize(pupil_0[1], world[1].shape[:-1][::-1], True)
            else:
                pupil_loc = self.denormalize(pupil_1[1], world[1].shape[:-1][::-1], True)

            try:
                detections = self.object_detect.perform_detect(world[1])
            except:
                raise

            if self.debug:
                self.display_image(detections, pupil_loc, world[1])

            self.last_frmae_processed = world[0]

            common_data_proxy.set_values(world[0], world[2])

    def display_image(self, detections, pupil_loc, frame):
        tmp = frame
        for detection in detections:
            bounds = detection[2]
            x1 = bounds[0] - bounds[2] / 2
            x2 = bounds[0] + bounds[2] / 2
            y1 = bounds[1] - bounds[3] / 2
            y2 = bounds[1] + bounds[3] / 2
            cv2.rectangle(tmp, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)

        cv2.imshow('frame.world_{}'.format(self.glass_id),
                   cv2.circle(tmp, (int(pupil_loc[0]), int(pupil_loc[1])), 5, (0, 0, 255), -1))
        cv2.waitKey(1)

    def denormalize(self, pos, size, flip_y=False):
        width, height = size
        x = pos[0]
        y = pos[1]
        x *= width
        if flip_y:
            y = 1 - y
        y *= height
        return x, y
