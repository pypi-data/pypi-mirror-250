# author: Jan Tschada
# SPDX-License-Identifer: Apache-2.0

from enum import Enum, unique



@unique
class GridType(Enum):
    """
    Represents the supported grid types.
    agent: The number of unique agents is calculated.
    speed: The speed average of every agent is calculated.
    emissions: The sum of carbon dioxide emissions of every agent is calculated. This makes only sense for vehicle being cars!

    Example:

    .. code-block:: python
    
        from geourban.types import GridType

        # Returns traffic grid cells accumulating the number of unique agents
        grid_type = GridType.AGENT

        # Returns traffic grid cells accumulating the speed average or every agent
        grid_type = GridType.SPEED

        # Returns traffic grid cells accumulating the sum of carbon dioxide emissions (kg/km) of every agent
        # This makes only sense for vehicle being cars!
        grid_type = GridType.EMISSIONS

    """
    AGENT=0
    SPEED=1
    EMISSIONS=2

    def __str__(self) -> str:
        if 0 == self.value:
            return 'agent'
        elif 1 == self.value:
            return 'speed'
        elif 2 == self.value:
            return 'emissions'
        
        return self.name
    
@unique
class VehicleType(Enum):
    """
    Represents the supported vehicle types.
    Car, Bike and Pedestrian are possible vehicle types.

    Example:

    .. code-block:: python
    
        from geourban.types import VehicleType

        # Returns traffic grid cells from agents moving by car
        vehicle_type = VehicleType.CAR

        # Returns traffic grid cells from agents moving by bike
        vehicle_type = VehicleType.BIKE

        # Returns traffic grid cells from agents walking
        vehicle_type = VehicleType.PEDESTRIAN

    """
    CAR=0
    BIKE=1
    PEDESTRIAN=2

    def __str__(self) -> str:
        if 0 == self.value:
            return 'Car'
        elif 1 == self.value:
            return 'Bike'
        elif 2 == self.value:
            return 'Pedestrian'
        
        return self.name