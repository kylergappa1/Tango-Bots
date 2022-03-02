# log.py

import logging

LOG_LEVEL = logging.DEBUG
# LOG_LEVEL = logging.INFO

logging.basicConfig(format='%(levelname)s: %(message)s', level=LOG_LEVEL)

log = logging

# END
