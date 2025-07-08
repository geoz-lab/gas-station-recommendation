"""
Map service for Gas Station Recommendation App
"""

import json
import random
import time
from typing import List, Dict, Any, Tuple, Optional
import requests
from models.schema import GasStation, Location
from config import Config
from .gas_price_service import gas_price_service

class MapService:
    """Service for handling map-related operations and gas station searches"""
    
    def __init__(self):
        self.api_key = Config.GOOGLE_MAPS_API_KEY
        self.base_url = "https://maps.googleapis.com/maps/api"
        self.cache = {}  # Simple cache for API responses
    
    def search_gas_stations(self, location: Tuple[float, float], radius_miles: float = 5) -> List[Dict[str, Any]]:
        """
        Search for gas stations near the given location
        
        Args:
            location: (latitude, longitude) tuple
            radius_miles: Search radius in miles
            
        Returns:
            List[Dict]: List of gas station data
        """
        if self.api_key:
            return self._search_with_google_maps(location, radius_miles)
        else:
            return self._get_mock_stations(location, radius_miles)
    
    def _search_with_google_maps(self, location: Tuple[float, float], radius_miles: float) -> List[Dict[str, Any]]:
        """
        Search using Google Maps Places API
        
        Args:
            location: (latitude, longitude) tuple
            radius_miles: Search radius in miles
            
        Returns:
            List[Dict]: List of gas station data
        """
        try:
            # Convert miles to meters
            radius_meters = int(radius_miles * 1609.34)
            
            url = f"{self.base_url}/place/nearbysearch/json"
            params = {
                'location': f"{location[0]},{location[1]}",
                'radius': radius_meters,
                'type': 'gas_station',
                'key': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') == 'OK':
                stations = []
                for place in data.get('results', []):
                    station = self._parse_google_place(place, location)
                    if station:
                        stations.append(station)
                return stations
            else:
                print(f"⚠️  Google Maps API error: {data.get('status')}")
                return self._get_mock_stations(location, radius_miles)
                
        except Exception as e:
            print(f"⚠️  Google Maps API error: {e}")
            return self._get_mock_stations(location, radius_miles)
    
    def _parse_google_place(self, place: Dict[str, Any], user_location: Tuple[float, float]) -> Optional[Dict[str, Any]]:
        """
        Parse Google Places API response into our format
        
        Args:
            place: Google Places API place object
            user_location: User's location for distance calculation
            
        Returns:
            Optional[Dict]: Parsed gas station data
        """
        try:
            # Extract location
            lat = place['geometry']['location']['lat']
            lng = place['geometry']['location']['lng']
            
            # Calculate distance
            distance = self._calculate_distance(user_location, (lat, lng))
            
            # Estimate travel time (assuming 40 mph average)
            travel_time = int((distance / 40) * 60)
            
            # Get gas prices for different grades
            gas_prices = gas_price_service.get_gas_prices(lat, lng, place.get('name', ''))
            price = gas_prices.get('87', 3.80)  # Use regular (87) as default price
            
            return {
                'name': place.get('name', 'Unknown Station'),
                'location': {
                    'latitude': lat,
                    'longitude': lng,
                    'address': place.get('vicinity', '')
                },
                'price_per_gallon': price,
                'gas_prices': gas_prices,  # Include all fuel grades
                'distance_miles': round(distance, 1),
                'travel_time_minutes': travel_time,
                'brand': self._extract_brand(place.get('name', '')),
                'rating': place.get('rating'),
                'address': place.get('vicinity', ''),
                'place_id': place.get('place_id')
            }
        except Exception as e:
            print(f"⚠️  Error parsing place: {e}")
            return None
    
    def _get_mock_stations(self, location: Tuple[float, float], radius_miles: float) -> List[Dict[str, Any]]:
        """
        Generate mock gas station data for testing
        
        Args:
            location: (latitude, longitude) tuple
            radius_miles: Search radius in miles
            
        Returns:
            List[Dict]: Mock gas station data
        """
        brands = ['Shell', 'Chevron', 'Exxon', 'Mobil', 'BP', 'Texaco', 'Arco', '76']
        
        stations = []
        for i in range(random.randint(5, 12)):
            # Generate random location within radius
            angle = random.uniform(0, 2 * 3.14159)
            distance = random.uniform(0.5, radius_miles)
            
            # Convert polar to cartesian
            lat_offset = distance * 0.014  # Rough conversion
            lng_offset = distance * 0.014 / abs(location[0] / 90)
            
            station_lat = location[0] + lat_offset * random.uniform(-1, 1)
            station_lng = location[1] + lng_offset * random.uniform(-1, 1)
            
            # Calculate actual distance
            actual_distance = self._calculate_distance(location, (station_lat, station_lng))
            
            if actual_distance <= radius_miles:
                brand = random.choice(brands)
                station_name = f"{brand} Station #{i+1}"
                
                # Get realistic gas prices
                gas_prices = gas_price_service.get_gas_prices(station_lat, station_lng, station_name)
                price = gas_prices.get('87', 3.80)  # Use regular (87) as default price
                
                travel_time = int((actual_distance / 40) * 60)  # Assume 40 mph
                
                stations.append({
                    'name': station_name,
                    'location': {
                        'latitude': station_lat,
                        'longitude': station_lng,
                        'address': f"Mock Address {i+1}"
                    },
                    'price_per_gallon': price,
                    'gas_prices': gas_prices,  # Include all fuel grades
                    'distance_miles': round(actual_distance, 1),
                    'travel_time_minutes': travel_time,
                    'brand': brand,
                    'rating': round(random.uniform(3.5, 5.0), 1),
                    'address': f"Mock Address {i+1}",
                    'place_id': f"mock_place_{i}"
                })
        
        return stations
    
    def _calculate_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """
        Calculate distance between two points using Haversine formula
        
        Args:
            point1: (lat1, lon1) tuple
            point2: (lat2, lon2) tuple
            
        Returns:
            float: Distance in miles
        """
        import math
        
        lat1, lon1 = point1
        lat2, lon2 = point2
        
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Earth's radius in miles
        r = 3956
        
        return c * r
    

    
    def _extract_brand(self, station_name: str) -> str:
        """
        Extract brand name from station name
        
        Args:
            station_name: Full station name
            
        Returns:
            str: Brand name
        """
        brands = ['Shell', 'Chevron', 'Exxon', 'Mobil', 'BP', 'Texaco', 'Arco', '76']
        for brand in brands:
            if brand.lower() in station_name.lower():
                return brand
        return 'Unknown'
    
    def get_directions(self, origin: Tuple[float, float], destination: Tuple[float, float]) -> Dict[str, Any]:
        """
        Get directions between two points
        
        Args:
            origin: Starting location (lat, lng)
            destination: Ending location (lat, lng)
            
        Returns:
            Dict: Directions data
        """
        if not self.api_key:
            return self._get_mock_directions(origin, destination)
        
        try:
            url = f"{self.base_url}/directions/json"
            params = {
                'origin': f"{origin[0]},{origin[1]}",
                'destination': f"{destination[0]},{destination[1]}",
                'key': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') == 'OK' and data.get('routes'):
                route = data['routes'][0]['legs'][0]
                return {
                    'distance_miles': route['distance']['text'],
                    'duration_minutes': int(route['duration']['value'] / 60),
                    'duration_text': route['duration']['text']
                }
            else:
                return self._get_mock_directions(origin, destination)
                
        except Exception as e:
            print(f"⚠️  Directions API error: {e}")
            return self._get_mock_directions(origin, destination)
    
    def _get_mock_directions(self, origin: Tuple[float, float], destination: Tuple[float, float]) -> Dict[str, Any]:
        """
        Generate mock directions data
        
        Args:
            origin: Starting location
            destination: Ending location
            
        Returns:
            Dict: Mock directions data
        """
        distance = self._calculate_distance(origin, destination)
        duration = int((distance / 40) * 60)  # Assume 40 mph
        
        return {
            'distance_miles': f"{distance:.1f} mi",
            'duration_minutes': duration,
            'duration_text': f"{duration} mins"
        }

# Global instance
map_service = MapService()

# Convenience functions
def search_gas_stations(location: Tuple[float, float], radius_miles: float = 5) -> List[Dict[str, Any]]:
    """Convenience function for searching gas stations"""
    return map_service.search_gas_stations(location, radius_miles)

def get_directions(origin: Tuple[float, float], destination: Tuple[float, float]) -> Dict[str, Any]:
    """Convenience function for getting directions"""
    return map_service.get_directions(origin, destination) 