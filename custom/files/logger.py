import logging

# create logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('gaze_glasses.log')
fh.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s | [%(processName)s] | [%(filename)s %(funcName)s] | [%(levelname)s] - %(message)s')
fh.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)