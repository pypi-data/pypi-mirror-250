# author: Jan Tschada
# SPDX-License-Identifer: Apache-2.0

from enum import Enum, unique



@unique
class OutFormat(Enum):
    """
    Represents the supported output formats.

    Example:

    .. code-block:: python
    
        from geourban.formats import OutFormat

        # Returns the geospatial features as GeoJSON
        out_format = OutFormat.GEOJSON

        # Returns the geospatial features as Esri FeatureSet
        out_format = OutFormat.ESRI

        # Returns the result as JSON dict
        # This is only for results not representing geospatial features
        out_format = OutFormat.JSON
        
    """
    ESRI=0
    GEOJSON=1
    JSON=2

    def __str__(self) -> str:
        if 0 == self.value:
            return 'esri'
        elif 1 == self.value:
            return 'geojson'
        elif 2 == self.value:
            return 'json'
        
        return self.name