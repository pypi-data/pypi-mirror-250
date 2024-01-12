import logging
from georeader.handlers.general_handler import GeneralHandler

LOGGER = logging.getLogger("__name__")


class JSONHandler(GeneralHandler):

    handler_type = "GeoJSON"
    source_type = "file"

    def __init__(self, file_name: str, *args, **kwargs):
        self.GDAL_drivers = ["GEOJSON", "ESRIJSON"]
        super(JSONHandler, self).__init__(
            source=file_name,
            gdal_drivers=self.GDAL_drivers
        )
