"""
Location service for Gas Station Recommendation App
"""

import time
import requests
from typing import Tuple, Optional, Dict, Any
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from models.schema import Location
from config import Config

class LocationService:
    """Service for handling location-related operations"""
    
    def __init__(self):
        self.geolocator = Nominatim(user_agent="gas-station-recommendation-app")
        self.cache = {}  # Simple cache for geocoding results
    
    def geocode_address(self, address: str) -> Tuple[float, float]:
        """
        Convert address to coordinates using multiple geocoding services
        
        Args:
            address: Address string to geocode
            
        Returns:
            Tuple[float, float]: (latitude, longitude)
            
        Raises:
            Exception: If geocoding fails
        """
        # Check cache first
        if address in self.cache:
            return self.cache[address]
        
        # Try multiple address variations
        address_variations = self._generate_address_variations(address)
        
        # Try Google Maps API first if available
        if Config.GOOGLE_MAPS_API_KEY:
            for variation in address_variations:
                try:
                    coords = self._geocode_with_google(variation)
                    if coords:
                        self.cache[address] = coords
                        print(f"✅ Successfully geocoded: {variation}")
                        return coords
                except Exception as e:
                    print(f"⚠️  Google geocoding failed for '{variation}': {e}")
        
        # Fallback to Nominatim with better error handling
        for variation in address_variations:
            try:
                coords = self._geocode_with_nominatim(variation)
                if coords:
                    self.cache[address] = coords
                    print(f"✅ Successfully geocoded: {variation}")
                    return coords
            except Exception as e:
                print(f"⚠️  Nominatim geocoding failed for '{variation}': {e}")
        
        # Final fallback to default location
        print(f"⚠️  Could not geocode address: {address}. Using default location.")
        return (Config.DEFAULT_LATITUDE, Config.DEFAULT_LONGITUDE)
    
    def _generate_address_variations(self, address: str) -> list:
        """Generate multiple variations of an address to try"""
        variations = []
        
        # Original address
        variations.append(address)
        
        # Cleaned address
        cleaned = self._clean_address(address)
        if cleaned != address:
            variations.append(cleaned)
        
        # Try with just street name and city/state
        import re
        # Extract street name (remove house number)
        street_match = re.search(r'\d+\s+(.+?)(?:,|$)', address)
        if street_match:
            street_name = street_match.group(1).strip()
            city_state = self._extract_city_state(address)
            if city_state:
                variations.append(f"{street_name}, {city_state}")
        
        # Try just city/state
        city_state = self._extract_city_state(address)
        if city_state and city_state not in variations:
            variations.append(city_state)
        
        # Try with "Street" suffix
        if not address.lower().endswith(('street', 'st', 'avenue', 'ave', 'road', 'rd')):
            street_match = re.search(r'(\d+\s+[^,]+?)(?:,|$)', address)
            if street_match:
                street_part = street_match.group(1).strip()
                city_state = self._extract_city_state(address)
                if city_state:
                    variations.append(f"{street_part} St, {city_state}")
        
        return variations
    
    def _clean_address(self, address: str) -> str:
        """Clean and normalize address string"""
        import re
        
        # Store original address for fallback
        original_address = address
        
        # Remove common apartment/unit indicators that can confuse geocoding
        address = address.replace('Unit', '').replace('unit', '')
        address = address.replace('Suite', '').replace('suite', '')
        address = address.replace('Apt', '').replace('apt', '')
        address = address.replace('Apartment', '').replace('apartment', '')
        address = address.replace('Floor', '').replace('floor', '')
        address = address.replace('Fl', '').replace('fl', '')
        
        # Remove extra spaces and normalize
        address = ' '.join(address.split())
        
        # If the cleaned address is too short or doesn't contain city/state, try to add context
        if len(address.split()) < 3 or not re.search(r',\s*[A-Z]{2}', address):
            # Try to extract city/state from the original address
            city_state = self._extract_city_state(original_address)
            if city_state:
                # If address doesn't already have city/state, add it
                if not re.search(r',\s*[A-Z]{2}', address):
                    address = f"{address}, {city_state}"
        
        return address
    
    def _extract_city_state(self, address: str) -> Optional[str]:
        """Extract city and state from address"""
        # Look for common patterns like "City, State ZIP"
        import re
        
        # Pattern for "City, State ZIP" or "City, State"
        pattern = r'([A-Za-z\s]+),\s*([A-Z]{2})\s*(\d{5})?'
        match = re.search(pattern, address)
        
        if match:
            city = match.group(1).strip()
            state = match.group(2).strip()
            return f"{city}, {state}"
        
        return None
    
    def _geocode_with_google(self, address: str) -> Optional[Tuple[float, float]]:
        """Geocode using Google Maps API"""
        try:
            url = "https://maps.googleapis.com/maps/api/geocode/json"
            params = {
                'address': address,
                'key': Config.GOOGLE_MAPS_API_KEY
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') == 'OK' and data.get('results'):
                location = data['results'][0]['geometry']['location']
                return (location['lat'], location['lng'])
            
            return None
            
        except Exception as e:
            print(f"⚠️  Google geocoding error: {e}")
            return None
    
    def _geocode_with_nominatim(self, address: str) -> Optional[Tuple[float, float]]:
        """Geocode using Nominatim with timeout"""
        try:
            location = self.geolocator.geocode(address, timeout=5)
            if location:
                return (location.latitude, location.longitude)
            return None
        except Exception as e:
            print(f"⚠️  Nominatim geocoding error: {e}")
            return None
    
    def reverse_geocode(self, latitude: float, longitude: float) -> Optional[str]:
        """
        Convert coordinates to address
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            Optional[str]: Address string or None if reverse geocoding fails
        """
        try:
            location = self.geolocator.reverse((latitude, longitude), timeout=10)
            return location.address if location else None
        except Exception as e:
            print(f"⚠️  Reverse geocoding error: {e}")
            return None
    
    def use_current_location(self) -> Tuple[float, float]:
        """
        Get current location using IP-based geolocation as fallback
        
        Returns:
            Tuple[float, float]: (latitude, longitude)
        """
        # Try IP-based geolocation first
        try:
            ip_location = self.get_location_from_ip()
            if ip_location != (Config.DEFAULT_LATITUDE, Config.DEFAULT_LONGITUDE):
                print(f"📍 Using IP-based location: {ip_location}")
                return ip_location
        except Exception as e:
            print(f"⚠️  IP geolocation failed: {e}")
        
        # Fallback to default location
        print("📍 Using default location (San Francisco)")
        return (Config.DEFAULT_LATITUDE, Config.DEFAULT_LONGITUDE)
    
    def get_location_from_ip(self) -> Tuple[float, float]:
        """
        Get approximate location from IP address
        
        Returns:
            Tuple[float, float]: (latitude, longitude)
        """
        try:
            response = requests.get('http://ip-api.com/json/', timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    lat = data.get('lat')
                    lon = data.get('lon')
                    if lat and lon:
                        return (lat, lon)
        except Exception as e:
            print(f"⚠️  IP geolocation error: {e}")
        
        # Fallback to default location
        return (Config.DEFAULT_LATITUDE, Config.DEFAULT_LONGITUDE)
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two points using Haversine formula
        
        Args:
            lat1, lon1: First point coordinates
            lat2, lon2: Second point coordinates
            
        Returns:
            float: Distance in miles
        """
        import math
        
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
    
    def validate_coordinates(self, latitude: float, longitude: float) -> bool:
        """
        Validate coordinate values
        
        Args:
            latitude: Latitude value
            longitude: Longitude value
            
        Returns:
            bool: True if coordinates are valid
        """
        return -90 <= latitude <= 90 and -180 <= longitude <= 180
    
    def create_location_object(self, latitude: float, longitude: float, 
                             address: Optional[str] = None) -> Location:
        """
        Create a Location object
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            address: Optional address string
            
        Returns:
            Location: Location object
        """
        if not self.validate_coordinates(latitude, longitude):
            raise ValueError("Invalid coordinates")
        
        return Location(
            latitude=latitude,
            longitude=longitude,
            address=address
        )

# Global instance
location_service = LocationService()

# Convenience functions
def geocode_address(address: str) -> Tuple[float, float]:
    """Convenience function for geocoding"""
    return location_service.geocode_address(address)

def use_current_location() -> Tuple[float, float]:
    """Convenience function for current location"""
    return location_service.use_current_location()

def reverse_geocode(latitude: float, longitude: float) -> Optional[str]:
    """Convenience function for reverse geocoding"""
    return location_service.reverse_geocode(latitude, longitude)

def get_location_from_ip() -> Tuple[float, float]:
    """Convenience function for IP-based geolocation"""
    return location_service.get_location_from_ip() 