import logging
from georeader.handlers.general_handler import GeneralHandler


LOGGER = logging.getLogger("__name__")


class GeoPackageHandler(GeneralHandler):

    handler_type = "GeoPackage"
    source_type = "file"

    def __init__(self, file_name, *args, **kwargs):
        self.GDAL_drivers = ["GPKG"]
        super(GeoPackageHandler, self).__init__(
            source=file_name,
            gdal_drivers=self.GDAL_drivers,
        )
        LOGGER.debug("initializing GeoPackageHandler")
        LOGGER.debug(vars(self))
