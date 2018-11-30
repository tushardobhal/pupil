from files.logger import logger
from files.run_length_filter import RunLengthFilter

import numpy as np
import cv2


class DoStuff:
    def __init__(self, glass_id, confidence_threshold, num_objects, object_detect, debug):
        self.last_frame_processed = 0
        self.glass_id = glass_id
        self.confidence_threshold = confidence_threshold
        self.object_detect = object_detect
        self.num_objects = num_objects
        self.run_length_filter = []
        for i in range(self.num_objects):
            self.run_length_filter.append(RunLengthFilter())
        self.debug = debug

    def do_some_stuff(self, world_proxy, eye_0_proxy, eye_1_proxy, common_data_proxy):
        logger.info('Starting Do_Stuff...')

        while True:
            world = world_proxy.get_values()
            pupil_0 = eye_0_proxy.get_values()

            if world[0] is None or pupil_0[0] is None or self.last_frame_processed == world[2]:
                continue
            logger.info("Frame - {}, Timestamp - {}".format(world[2], world[1]))
            logger.info(
                "Eye_Id - {}, Norm_Pos - {}, Confidence - {}, Timestamp - {}".format(pupil_0[2], pupil_0[3], pupil_0[4],
                                                                                     pupil_0[1]))

            pupil_loc = pupil_0[3]

            try:
                detections = self.object_detect.perform_detect(world[3])

            except Exception as e:
                raise e

            if self.debug:
                self.display_image(detections, pupil_loc, world[3])

            self.last_frame_processed = world[2]

            run_length_output = self.perform_run_length(detections, pupil_loc)
            common_data_proxy.set_values(self.glass_id, world[1], world[2], run_length_output)

    def perform_run_length(self, detections, pupil_loc):
        output = [0] * self.num_objects
        hit = [0] * self.num_objects
        x = pupil_loc[0]
        y = pupil_loc[1]

        for detection in detections:
            label = detection[0]
            x1 = detection[2][0] - detection[2][2] / 2
            x2 = detection[2][0] + detection[2][2] / 2
            y1 = detection[2][1] - detection[2][3] / 2
            y2 = detection[2][1] + detection[2][3] / 2

            yin = (y1 <= y <= y2)
            xin = (x1 <= x <= x2)
            if xin and yin:
                hit[label] = 1
                break

        for i in range(0, self.num_objects):
            output[i] = self.run_length_filter[i].update_run_length_filter(hit[i])
        return output

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
                   cv2.circle(tmp, (int(pupil_loc[0]), int(pupil_loc[1])), 15, (0, 0, 255), -1))
        cv2.waitKey(1)
