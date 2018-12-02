import logging
import logging.handlers as handlers

# create logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = handlers.RotatingFileHandler('gaze_glasses.log', maxBytes=20*1024*1024, backupCount=5)
fh.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s | [%(processName)s] | [%(filename)s %(funcName)s] | [%(levelname)s] - %(message)s')
fh.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)