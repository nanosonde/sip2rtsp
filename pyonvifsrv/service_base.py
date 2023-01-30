import logging

from pyonvifsrv.context import Context

logger = logging.getLogger(__name__)

class ServiceBase:
    def __init__(self, context: Context):
        self.context = context
