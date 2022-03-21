# log.py

import logging
import inspect

LOG_LEVEL = logging.INFO
LOG_LEVEL = logging.DEBUG

logging.basicConfig(format='%(levelname)s: %(message)s', level=LOG_LEVEL)

log = logging

def log_method_call(obj, stack = 1):
    log.debug("%s::%s()", obj.__class__.__name__, inspect.stack()[stack][3])


# END
