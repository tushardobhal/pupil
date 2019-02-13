from files.logger import logger, logger2, logger_run_length
from files.run_length_filter import RunLengthFilter

import time
import numpy as np
import cv2


class DoStuffTogether:

    def __init__(self, object_detect, num_objects, debug):
        self.last_frame_index_1 = 0
        self.last_frame_index_2 = 0
        self.prev_state = False
        self.objects = np.array(["cards", "dice", "key", "map", "ball", "face"])
        self.object_detect = object_detect
        self.num_objects = num_objects
        self.run_length_filter = []
        for i in range(self.num_objects):
            self.run_length_filter.append(RunLengthFilter())
        self.debug = debug

    def do_some_stuff_together(self, common_data_proxy_1, common_data_proxy_2):
        logger.info("Starting Do_Stuff_Together...")

        while True:
            common_data_1 = common_data_proxy_1.get_values()
            common_data_2 = common_data_proxy_2.get_values()
            if common_data_1[0] is None or common_data_2[0] is None:
                continue

            # if common_data_1[0] is None or common_data_2[0] is None or (
            #         common_data_1[2] == self.last_frame_index_1 and common_data_2[2] == self.last_frame_index_2):
            #     continue

            logger.info("Glass_1 Frame - {}, Glass_2 Frame - {}, Glass_1 Timestamp - {}, Glass_2 Timestamp - {}".format(
                common_data_1[2], common_data_2[2], common_data_1[1], common_data_2[1]))

            start = time.monotonic()
            concat_image = np.concatenate((common_data_1[3], common_data_2[3]), axis=0)
            logger.info("Time taken for concat - {}".format((time.monotonic() - start)))

            start = time.monotonic()
            try:
                detections = self.object_detect.perform_detect(concat_image)
                detections_glass1, detections_glass2 = self.split_detections(detections)
                denorm_detections_glass1 = denormalize_detections(detections_glass1, common_data_1[5], 0)
                denorm_detections_glass2 = denormalize_detections(detections_glass2, common_data_2[5], 1)
            except Exception as e:
                raise e
            logger.info("Time taken for getting detections - {}".format((time.monotonic() - start)))

            if self.debug:
                self.display_image(common_data_1[0], denorm_detections_glass1, common_data_1[4], common_data_1[3])
                self.display_image(common_data_2[0], denorm_detections_glass2, common_data_2[4], common_data_2[3])

            run_length_output_glass1 = self.perform_run_length(denorm_detections_glass1, common_data_1[4])
            run_length_output_glass2 = self.perform_run_length(denorm_detections_glass2, common_data_2[4])

            self.detect_joint_look(common_data_1, common_data_2, run_length_output_glass1, run_length_output_glass2)

            self.last_frame_index_1 = common_data_1[2]
            self.last_frame_index_2 = common_data_2[2]

    def detect_joint_look(self, common_data_1, common_data_2, run_length_output_glass1, run_length_output_glass2):
        common_look_time = int(time.time() * 1000)
        logger_run_length.info(
            ";time-{};Glass1_hit_scan_output-{};Glass2_hit_scan_output-{};Glass1_run_length_output-{};Glass2_run_length_output-{};Frame1-{};Frame2-{}".format(
                common_look_time, run_length_output_glass1[1], run_length_output_glass2[1], run_length_output_glass1[0], run_length_output_glass2[0],
                common_data_1[2], common_data_2[2]))

        # check if the runlength are same for the two glasses
        if run_length_output_glass1[0] == run_length_output_glass1[0] and sum(run_length_output_glass1[0]) != 0:
            if not self.prev_state:
                self.prev_state = True
                obj_idx = np.argmax(run_length_output_glass1[0])
                logger2.info("Look Detected;{}:{}".format(self.objects[obj_idx], common_look_time))

            play_sound()
        else:
            self.prev_state = False

    def perform_run_length(self, detections, pupil_loc):
        output = [0] * self.num_objects
        hit = [0] * self.num_objects
        x = pupil_loc[0]
        y = pupil_loc[1]

        for detection in detections:
            index = self.object_detect.get_alt_names().index(detection[0])
            bounds = detection[2]
            x1 = bounds[0] - bounds[2] / 2
            x2 = bounds[0] + bounds[2] / 2
            y1 = bounds[1] - bounds[3] / 2
            y2 = bounds[1] + bounds[3] / 2

            yin = (y1 <= y <= y2)
            xin = (x1 <= x <= x2)
            if xin and yin:
                hit[index] = 1
                break

        for i in range(0, self.num_objects):
            output[i] = self.run_length_filter[i].update_run_length_filter(hit[i])

        # logger.info("Run length output - {}".format(output))
        return output, hit

    def display_image(self, glass_id, detections, pupil_loc, frame):
        tmp = frame
        for detection in detections:
            bounds = detection[2]
            x1 = bounds[0] - bounds[2] / 2
            x2 = bounds[0] + bounds[2] / 2
            y1 = bounds[1] - bounds[3] / 2
            y2 = bounds[1] + bounds[3] / 2
            cv2.rectangle(tmp, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)

            label = detection[0] + ' - ' + str(round(detection[1], 4))
            cv2.putText(tmp, text=label, org=(int(x1), int(y1)), fontFace=3, fontScale=.5, color=(255, 0, 0), thickness=1)

        cv2.imshow('frame.world_{}'.format(glass_id),
                   cv2.circle(tmp, (int(pupil_loc[0]), int(pupil_loc[1])), 15, (0, 0, 255), -1))
        cv2.waitKey(1)

    @staticmethod
    def split_detections(detections):
        detections_glass1 = []
        detections_glass2 = []

        for detection in detections:
            if detection[2][1] < 208:
                detections_glass1.append(detection)
            else:
                detections_glass2.append(detection)

        return detections_glass1, detections_glass2


def play_sound():
    print('\a')


def denormalize_detections(detections, confidence, is_second):
    if detections is None or len(detections) == 0:
        return detections

    detections_new = []
    x_norm_base = 1280/416
    y_norm_base = 1440/416
    for detection in detections:
        bounds = detection[2]
        x1 = bounds[0] * x_norm_base
        y1 = bounds[1] * y_norm_base
        if is_second == 1:
            y1 = y1 - 720
        width = bounds[2] * x_norm_base
        height = bounds[3] * y_norm_base + (1-confidence/100)*25
        if detection[0] == 0 or detection[0] == 4 or detection[0] == 5:
            width = width + (1-confidence/100)*15
            height = height + (1-confidence/100)*15
        else:
            width = width + (1 - confidence / 100) * 30
            height = height + (1 - confidence / 100) * 30

        bounds_new = (x1, y1, width, height)

        detections_new.append((detection[0], detection[1], bounds_new))

    return detections_new
