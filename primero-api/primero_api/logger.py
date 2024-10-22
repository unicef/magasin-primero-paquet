import logging
from logging import NullHandler

# setup logging
logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())
logger.setLevel(logging.DEBUG)
