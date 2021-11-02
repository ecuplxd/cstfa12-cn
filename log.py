import logging

from colorlog import ColoredFormatter

LOG_LEVEL = logging.DEBUG
LOGFORMAT = "  %(log_color)s%(levelname)-4s%(reset)s | %(log_color)s%(message)s%(reset)s"

logging.root.setLevel(LOG_LEVEL)

formatter = ColoredFormatter(LOGFORMAT)

stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)

log = logging.getLogger('PdfTransformer')
log.setLevel(LOG_LEVEL)
log.addHandler(stream)
