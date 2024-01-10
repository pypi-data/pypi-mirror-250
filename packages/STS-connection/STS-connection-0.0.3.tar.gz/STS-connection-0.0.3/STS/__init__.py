name = "STS"
__version__ = "0.0.1"

import logging

debug = False
logger = logging.getLogger(__name__)
if debug:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
from .Serial import *
from .Telnet import *
from .SSH import *
