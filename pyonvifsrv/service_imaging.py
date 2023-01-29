import logging
from pyonvifsrv.context import Context

logger = logging.getLogger(__name__)

class ImagingService:
    def __init__(self, context: Context):
        self.context = context
