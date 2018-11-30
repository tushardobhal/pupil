from files.logger import logger


class DoStuffTogether:

    def __init__(self):
        self.last_frame_index_1 = 0
        self.last_frame_index_2 = 0

    def do_some_stuff_together(self, common_data_proxy_1, common_data_proxy_2):
        logger.info("Starting Do_Stuff_Together...")

        while True:
            common_data_1 = common_data_proxy_1.get_values()
            common_data_2 = common_data_proxy_2.get_values()
            if common_data_1[0] is None or common_data_2[0] is None or (
                    common_data_1[2] == self.last_frame_index_1 and common_data_2[2] == self.last_frame_index_2):
                continue

            logger.info("Glass_1 Frame - {}, Glass_2 Frame - {}, Glass_1 Timestamp - {}, Glass_2 Timestamp - {}".format(
                common_data_1[2], common_data_2[2], common_data_1[1], common_data_2[1]))
            logger.info("Glass_1 output - {}, Glass_2 output - {}".format(common_data_1[3], common_data_2[3]))

            if common_data_1[3] == common_data_2[3] and sum(common_data_1[3]) != 0:
                logger.info("Look Detected")
                play_sound()

            self.last_frame_index_1 = common_data_1[0]
            self.last_frame_index_2 = common_data_2[0]


def play_sound():
    print('\a')
