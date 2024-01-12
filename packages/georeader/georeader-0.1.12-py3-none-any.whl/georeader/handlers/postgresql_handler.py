import logging
from georeader.handlers.general_handler import GeneralHandler

LOGGER = logging.getLogger("__name__")


class PostgreSQLHandler(GeneralHandler):

    handler_type = "PostgreSQL"
    source_type = "db"

    def __init__(self, connection_str: str, *args, **kwargs):
        self.GDAL_drivers = ["PostgreSQL"]
        super(PostgreSQLHandler, self).__init__(
            source=connection_str, gdal_drivers=self.GDAL_drivers
        )
        LOGGER.debug(f"initializing {self.handler_type}")
        LOGGER.debug(vars(self))


