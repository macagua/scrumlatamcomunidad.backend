"""Init and utils."""
from zope.i18nmessageid import MessageFactory

import logging


PACKAGE_NAME = "slc_web"

_ = MessageFactory("slc_web")

logger = logging.getLogger("slc_web")
