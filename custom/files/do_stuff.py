from files.logger import logger

import cv2

class DoStuff:
    def __init__(self):
        self.last_frmae_processed = 0
        pass

    def do_some_stuff(self, world_proxy, eye_0_proxy, eye_1_proxy):
        logger.info('Starting Do_Stuff...')

        while True:
            world = world_proxy.get_values()
            pupil_0 = eye_0_proxy.get_values()
            pupil_1 = eye_1_proxy.get_values()

            if world[0] == None or pupil_0[0] == None or pupil_1[0] == None or self.last_frmae_processed == world[0]:
                continue
            logger.info("Frame - {}, Timestamp - {}".format(world[0], world[2]))
            logger.info("Eye_Id - {}, Norm_Pos - {}, Confidence - {}, Timestamp - {}".format(pupil_0[0], pupil_0[1], pupil_0[2], pupil_0[3]))
            logger.info("Eye_Id - {}, Norm_Pos - {}, Confidence - {}, Timestamp - {}".format(pupil_1[0], pupil_1[1], pupil_1[2], pupil_1[3]))

            cv2.imshow('frame.world', world[1])
            cv2.waitKey(1)
            self.last_frmae_processed = world[0]

