import logging
import logging.handlers as handlers
from datetime import datetime

# Application Logger

# create logger
logger = logging.getLogger("first_logger")
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = handlers.RotatingFileHandler('gaze_glasses.log', maxBytes=1*1024*1024*1024, backupCount=50)
fh.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s | [%(processName)s] | [%(filename)s %(funcName)s] | [%(levelname)s] - %(message)s')
fh.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)

# Looks Logger

# create logger
logger2 = logging.getLogger("second_logger")
logger2.setLevel(logging.INFO)

# create file handler which logs even debug messages
fh2 = handlers.RotatingFileHandler('looks.log', maxBytes=1*1024*1024*1024, backupCount=50)
fh2.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter2 = logging.Formatter('%(asctime)s | [%(processName)s] | [%(filename)s %(funcName)s] | [%(levelname)s] - %(message)s')
fh2.setFormatter(formatter)

# add the handlers to the logger
logger2.addHandler(fh2)

# Run Length Logger

# create logger
logger_run_length = logging.getLogger("third_logger")
logger_run_length.setLevel(logging.INFO)

# create file handler which logs even debug messages
fh2 = handlers.RotatingFileHandler('run_length_{:%Y-%m-%d_%H-%M-%S}.log'.format(datetime.now()), maxBytes=1*1024*1024*1024, backupCount=50)
fh2.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter2 = logging.Formatter('%(asctime)s | [%(processName)s] | [%(filename)s %(funcName)s] | [%(levelname)s] - %(message)s')
fh2.setFormatter(formatter)

# add the handlers to the logger
logger_run_length.addHandler(fh2)