from kfsd.apps.endpoints.handlers.relations.base import BaseHRelHandler
from kfsd.apps.core.common.logger import Logger, LogLevel

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class BasePermHandler(BaseHRelHandler):
    def __init__(self, **kwargs):
        BaseHRelHandler.__init__(self, **kwargs)
