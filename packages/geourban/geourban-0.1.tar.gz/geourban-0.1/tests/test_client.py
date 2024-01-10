# author: Jan Tschada
# SPDX-License-Identifer: Apache-2.0

from datetime import date, datetime
from georapid.client import GeoRapidClient
from georapid.factory import EnvironmentClientFactory
from geourban.services import aggregate, query, simulations, top
from geourban.types import GridType, VehicleType
import unittest

# Import errors during debug session: https://github.com/microsoft/vscode-python/issues/21648#issuecomment-1638365589
# Add the following in your user or workspace settings
"""
"python.experiments.optOutFrom": [
        "pythonTestAdapter"
    ]
"""



class TestConnect(unittest.TestCase):

    def setUp(self) -> None:
        self._latitudes = [51.83864, 50.73438]
        self._longitudes = [12.24555, 7.09549]

    def test_create(self):
        host = 'geourban.p.rapidapi.com'
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        self.assertIsNotNone(client, "Client must be initialized!")

    def test_list_simulations(self):
        host = 'geourban.p.rapidapi.com'
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        urban_simulations = simulations(client)
        self.assertIsNotNone(urban_simulations, "List of urban simulations must be initialized!")
        self.assertGreater(len(urban_simulations), 0, "List of urban simulations must not be emtpy!")

    def test_top_car_traffic_in_bonn(self):
        host = 'geourban.p.rapidapi.com'
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        simulation_date: date = date(2023, 8, 24)
        region_code: str = 'DEA22'
        vehicle_type: VehicleType = VehicleType.CAR
        grid_type: GridType = GridType.AGENT
        top_traffic_grid_cells = top(client, region_code, simulation_date, vehicle_type, grid_type)
        self.assertIsNotNone(top_traffic_grid_cells, "The traffic grid cells must be initialized!")
        self.assertTrue('features' in top_traffic_grid_cells, "The returned GeoJSON must have features!")

    def test_aggregate_car_traffic_in_bonn(self):
        host = 'geourban.p.rapidapi.com'
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        simulation_datetime: datetime = datetime(2023, 8, 24, 8, 0, 0)
        region_code: str = 'DEA22'
        vehicle_type: VehicleType = VehicleType.CAR
        grid_type: GridType = GridType.AGENT
        aggregated_traffic_grid_cells = aggregate(client, region_code, simulation_datetime, vehicle_type, grid_type)
        self.assertIsNotNone(aggregated_traffic_grid_cells, "The traffic grid cells must be initialized!")
        self.assertTrue('features' in aggregated_traffic_grid_cells, "The returned GeoJSON must have features!")

    def test_query_hotspot_in_bonn(self):
        host = 'geourban.p.rapidapi.com'
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        simulation_datetime: datetime = datetime(2023, 8, 24, 8, 45, 0)
        vehicle_type: VehicleType = VehicleType.CAR
        (latitude, longitude) = (50.746708, 7.074405)
        (seconds, meters) = (120, 1000)
        agent_positions = query(client, simulation_datetime, vehicle_type, latitude, longitude, seconds, meters)
        self.assertIsNotNone(agent_positions, "The agent poistions must be initialized!")
        self.assertTrue('features' in agent_positions, "The returned GeoJSON must have features!")