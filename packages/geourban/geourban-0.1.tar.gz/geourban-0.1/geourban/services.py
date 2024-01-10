# author: Jan Tschada
# SPDX-License-Identifer: Apache-2.0

from datetime import date, datetime
from georapid.client import GeoRapidClient
from geourban.formats import OutFormat
from geourban.types import GridType, VehicleType
import requests



def aggregate(client: GeoRapidClient, region_code: str, simulation_datetime: datetime, vehicle_type: VehicleType, grid_type: GridType, out_format: OutFormat=OutFormat.GEOJSON):
    """
    Returns a spatially enabled traffic grid representing aggregated simulated movements of pedestrians, bikes and cars.

    :param client: The client instance to use for this query.
    :type client: :class:`georapid.client.GeoRapidClient`
    :param region_code: The simulations endpoint returns all available urban regions. 
        You have to use the region code, e.g. `DEA22` for the city of Bonn, Germany.
    :type region_code: str
    :param simulation_datetime: Represents the simulated start time.
        The simulations endpoint list the available urban regions with their simulation dates. 
        The time must be defined using the simulation date and the time being on the hour, e.g. `2023-08-24T07:00:00`.
    :type simulation_datetime: :class:`datetime.datetime`
    :param vehicle_type: Car, Bike and Pedestrian are possible vehicle types.
    :type vehicle_type: :class:`geourban.types.VehicleType`
    :param grid_type: The values agent, speed and emissions are supported grid types.
        agent: The number of unique agents is calculated.
        speed: The speed average of every agent is calculated.
        emissions: The sum of carbon dioxide emissions of every agent is calculated. This makes only sense for vehicle being cars!
    :type grid_type: :class:`geourban.types.GridType`
    :param out_format: The output format. Defaults to OutFormat.GEOJSON.
    :type out_format: :class:`geourban.formats.OutFormat`, optional

    :return: The JSON response from the geourban service.
    :rtype: :class:`dict`

    Example:
    
    .. code-block:: python
    
        from datetime import datetime
        from georapid.client import GeoRapidClient
        from georapid.factory import EnvironmentClientFactory
        from geourban.services import aggregate
        from geourban.types import GridType, VehicleType
        
        host = 'geourban.p.rapidapi.com'
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        simulation_datetime: datetime = datetime(2023, 8, 24, 8, 0, 0)
        region_code: str = 'DEA22'
        vehicle_type: VehicleType = VehicleType.CAR
        grid_type: GridType = GridType.AGENT
        aggregated_traffic_grid_cells = aggregate(client, region_code, simulation_datetime, vehicle_type, grid_type)
    
    """
    endpoint = '{0}/aggregate'.format(client.url)
    params = {
        'region': region_code,
        'time': simulation_datetime.isoformat(),
        'vehicle': str(vehicle_type),
        'grid': str(grid_type),
        'format': str(out_format)
    }
    response = requests.request('GET', endpoint, headers=client.auth_headers, params=params)
    response.raise_for_status()

    return response.json()

def query(client: GeoRapidClient, simulation_datetime: datetime, vehicle_type: VehicleType, latitude: float, longitude: float, seconds: int=60, meters: float=500, out_format: OutFormat=OutFormat.GEOJSON):
    """
    Queries the simulated agent positions in space and time.
    Returns all positions within a certain radius of a given location and within a certain time frame.

    :param client: The client instance to use for this query.
    :type client: :class:`georapid.client.GeoRapidClient`
    :param simulation_datetime: The datetime of the simulation.
    :type simulation_datetime: :class:`datetime.datetime`
    :param vehicle_type: Car, Bike and Pedestrian are possible vehicle types.
    :type vehicle_type: :class:`geourban.types.VehicleType`
    :param latitude: The latitude of the location to query.
    :type latitude: float
    :param longitude: The longitude of the location to query.
    :type longitude: float
    :param seconds: The time frame in seconds. Defaults to 60.
    :type seconds: int, optional
    :param meters: The radius in meters. Defaults to 500.
    :type meters: float, optional
    :param out_format: The output format. Defaults to OutFormat.GEOJSON.
    :type out_format: :class:`geourban.formats.OutFormat`, optional

    :raises ValueError: If latitude is not in the range of [-90.0, 90.0].
    :raises ValueError: If longitude is not in the range of [-180.0, 180.0].
    :raises ValueError: If seconds is not in the range of [1, 120].
    :raises ValueError: If meters is not in the range of [1.0, 1000.0].

    :return: The JSON response from the geourban service.
    :rtype: :class:`dict`

    Example:
    
    .. code-block:: python
    
        from datetime import datetime
        from georapid.client import GeoRapidClient
        from georapid.factory import EnvironmentClientFactory
        from geourban.services import query
        from geourban.types import VehicleType
        
        host = 'geourban.p.rapidapi.com'
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        simulation_datetime: datetime = datetime(2023, 8, 24, 8, 45, 0)
        vehicle_type: VehicleType = VehicleType.CAR
        (latitude, longitude) = (50.746708, 7.074405)
        (seconds, meters) = (120, 1000)
        agent_positions = query(client, simulation_datetime, vehicle_type, latitude, longitude, seconds, meters)
    
    """

    if latitude < -90.0 or 90.0 < latitude:
        raise ValueError(f'Invalid latitude value! {latitude} is not in the range of [-90.0, 90.0].')
    
    if longitude < -180.0 or 180.0 < longitude:
        raise ValueError(f'Invalid longitude value! {longitude} is not in the range of [-180.0, 180.0].')
    
    if seconds < 1 or 120 < seconds:
        raise ValueError(f'Invalid seconds value! {seconds} is not in the range of [1, 120].')
    
    if meters < 1.0 or 1000.0 < meters:
        raise ValueError(f'Invalid meters value! {meters} is not in the range of [1.0, 1000.0].')

    endpoint = '{0}/query'.format(client.url)
    params = {
        'datetime': simulation_datetime.isoformat(),
        'seconds': seconds,
        'vehicle': str(vehicle_type),
        'lat': latitude,
        'lon': longitude,
        'meters': meters,
        'format': str(out_format)
    }
    response = requests.request('GET', endpoint, headers=client.auth_headers, params=params)
    response.raise_for_status()

    return response.json()

def simulations(client: GeoRapidClient):
    """
    Returns all the available simulations using the urban region and the simulation date.
    The client instance must refer to a valid geourban services host like 'geourban.p.rapidapi.com'.

    :param client: The client instance to use for this query.
    :type client: :class:`georapid.client.GeoRapidClient`

    :return: The JSON response from the geourban service.
    :rtype: :class:`list`

    Example:
    
    .. code-block:: python
    
        from georapid.client import GeoRapidClient
        from georapid.factory import EnvironmentClientFactory
        from geourban.services import simulations
        
        host = 'geourban.p.rapidapi.com'
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        urban_simulations = simulations(client)
    
    """
    
    endpoint = '{0}/simulations'.format(client.url)
    response = requests.request('GET', endpoint, headers=client.auth_headers)
    response.raise_for_status()

    return response.json()

def top(client: GeoRapidClient, region_code: str, simulation_date: date, vehicle_type: VehicleType, grid_type: GridType, limit: int=10, out_format: OutFormat=OutFormat.GEOJSON):
    """
    Returns the top most accumulated traffic grid cells for an urban region.

    :param client: The client instance to use for this query.
    :type client: :class:`georapid.client.GeoRapidClient`
    :param region_code: The simulations endpoint returns all available urban regions. 
        You have to use the region code, e.g. `DEA22` for the city of Bonn, Germany.
    :type region_code: str
    :param simulation_date: Represents the simulated date. 
        The simulations endpoint list the available urban regions with their simulation dates. 
        The date must be defined using ISO format, e.g. `2023-08-24`.
    :type simulation_date: :class:`datetime.date`
    :param vehicle_type: Car, Bike and Pedestrian are possible vehicle types.
    :type vehicle_type: :class:`geourban.types.VehicleType`
    :param grid_type: The values agent, speed and emissions are supported grid types.
        agent: The number of unique agents is calculated.
        speed: The speed average of every agent is calculated.
        emissions: The sum of carbon dioxide emissions of every agent is calculated. This makes only sense for vehicle being cars!
    :type grid_type: :class:`geourban.types.GridType`
    :param limit: The maximum number of returned features. Defaults to 10.
    :type limit: int, optional
    :param out_format: The output format. Defaults to OutFormat.GEOJSON.
    :type out_format: :class:`geourban.formats.OutFormat`, optional

    :return: The JSON response from the geourban service.
    :rtype: :class:`dict`

    Example:
    
    .. code-block:: python
    
        from datetime import date
        from georapid.client import GeoRapidClient
        from georapid.factory import EnvironmentClientFactory
        from geourban.services import top
        from geourban.types import GridType, VehicleType
        
        host = 'geourban.p.rapidapi.com'
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        simulation_date: date = date(2023, 8, 24)
        region_code: str = 'DEA22'
        vehicle_type: VehicleType = VehicleType.CAR
        grid_type: GridType = GridType.AGENT
        top_traffic_grid_cells = top(client, region_code, simulation_date, vehicle_type, grid_type)
    
    """
    endpoint = '{0}/top'.format(client.url)
    params = {
        'region': region_code,
        'date': simulation_date.strftime('%Y-%m-%d'),
        'vehicle': str(vehicle_type),
        'grid': str(grid_type),
        'limit': limit,
        'format': str(out_format)
    }
    response = requests.request('GET', endpoint, headers=client.auth_headers, params=params)
    response.raise_for_status()

    return response.json()