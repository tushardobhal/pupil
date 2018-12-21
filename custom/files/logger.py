import logging
import logging.handlers as handlers

# create logger
logger = logging.getLogger("first_logger")
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = handlers.RotatingFileHandler('gaze_glasses.log', maxBytes=20*1024*1024, backupCount=5)
fh.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s | [%(processName)s] | [%(filename)s %(funcName)s] | [%(levelname)s] - %(message)s')
fh.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)

# create logger
logger2 = logging.getLogger("second_logger")
logger2.setLevel(logging.INFO)

# create file handler which logs even debug messages
fh2 = handlers.RotatingFileHandler('looks.log', maxBytes=20*1024*1024, backupCount=5)
fh2.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter2 = logging.Formatter('%(asctime)s | [%(processName)s] | [%(filename)s %(funcName)s] | [%(levelname)s] - %(message)s')
fh2.setFormatter(formatter)

# add the handlers to the logger
logger2.addHandler(fh2)