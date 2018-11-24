from files.logger import logger

class DoStuff:
    def __init__(self):
        pass

    def do_some_stuff(self, world_dest, eye_0_dest, eye_1_dest):
        logger.info('Starting Do_Stuff...')

        while True:
            world = world_dest.recv()
            pupil_0 = eye_0_dest.recv()
            pupil_1 = eye_1_dest.recv()
            logger.info(world.__repr__())
            logger.info(pupil_0.__repr__())
            logger.info(pupil_1.__repr__())

