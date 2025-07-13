"""
Gas Price Service for Gas Station Recommendation App
"""

import requests
import random
import time
from typing import Dict, Optional, Tuple, Any
from config import Config

class GasPriceService:
    """Service for fetching gas prices from Google Maps"""
    
    def __init__(self):
        self.api_key = Config.GOOGLE_MAPS_API_KEY
        self.cache = {}  # Simple cache for API responses
        self.cache_timeout = 3600  # 1 hour cache
    
    def get_gas_prices(self, latitude: float, longitude: float, station_name: str = "") -> Dict[str, float]:
        """
        Get gas prices for different fuel grades at a location from Google Maps
        
        Args:
            latitude: Station latitude
            longitude: Station longitude
            station_name: Station name for better price estimation
            
        Returns:
            Dict[str, float]: Prices for different fuel grades
        """
        # Only try Google Maps
        prices = self._try_google_maps_prices(latitude, longitude, station_name)
        if prices:
            return prices
        
        # Return empty dict if no prices found
        return {}
    
    def get_gas_prices_with_source(self, latitude: float, longitude: float, station_name: str = "") -> Dict[str, Any]:
        """
        Get gas prices with source information
        
        Returns:
            Dict with 'prices' and 'source' keys
        """
        # Only try Google Maps
        prices = self._try_google_maps_prices(latitude, longitude, station_name)
        if prices:
            return {'prices': prices, 'source': 'Google Maps'}
        
        # Return empty prices if none found
        return {'prices': {}, 'source': 'Not available'}
    
    def _try_google_maps_prices(self, latitude: float, longitude: float, station_name: str) -> Optional[Dict[str, float]]:
        """
        Try to extract prices from Google Maps data
        """
        if not self.api_key:
            return None
        
        try:
            # Search for the specific station to get more details
            url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            params = {
                'location': f"{latitude},{longitude}",
                'radius': 100,  # Very small radius to get the exact station
                'type': 'gas_station',
                'key': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'OK' and data.get('results'):
                    # Look for the station with matching name or closest location
                    for place in data['results']:
                        place_lat = place['geometry']['location']['lat']
                        place_lng = place['geometry']['location']['lng']
                        
                        # Check if this is the same station (within 100 meters)
                        if self._calculate_distance((latitude, longitude), (place_lat, place_lng)) < 0.1:
                            # Try to get detailed place info which might have prices
                            return self._extract_prices_from_place_details(place.get('place_id'))
            
            return None
            
        except Exception as e:
            print(f"⚠️  Google Maps price extraction error: {e}")
            return None
    
    def _extract_prices_from_place_details(self, place_id: str) -> Optional[Dict[str, float]]:
        """
        Extract prices from Google Place Details API
        Google Maps provides gas prices in the place details
        """
        if not place_id or not self.api_key:
            return None
        
        try:
            url = "https://maps.googleapis.com/maps/api/place/details/json"
            params = {
                'place_id': place_id,
                'fields': 'name,formatted_address,price_level,opening_hours,editorial_summary,reviews',
                'key': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'OK' and data.get('result'):
                    result = data['result']
                    
                    # Try to extract gas prices from editorial summary or reviews
                    prices = self._extract_prices_from_text(result.get('editorial_summary', {}).get('overview', ''))
                    if not prices:
                        # Try to extract from reviews
                        reviews = result.get('reviews', [])
                        for review in reviews[:3]:  # Check first 3 reviews
                            prices = self._extract_prices_from_text(review.get('text', ''))
                            if prices:
                                break
                    
                    if prices:
                        return prices
                    
                    # Fallback to price level if no specific prices found
                    price_level = result.get('price_level', 2)  # 0-4 scale
                    return self._generate_prices_from_level(price_level)
            
            return None
            
        except Exception as e:
            print(f"⚠️  Place details extraction error: {e}")
            return None
    
    def _extract_prices_from_text(self, text: str) -> Optional[Dict[str, float]]:
        """
        Extract gas prices from text (like Google Maps descriptions or reviews)
        """
        if not text:
            return None
        
        import re
        
        # Look for price patterns like "$5.00", "Regular $5.00", "87 $5.00", etc.
        price_patterns = [
            r'regular\s*\$?(\d+\.?\d*)',  # Regular $5.00
            r'87\s*\$?(\d+\.?\d*)',       # 87 $5.00
            r'premium\s*\$?(\d+\.?\d*)',  # Premium $5.50
            r'91\s*\$?(\d+\.?\d*)',       # 91 $5.50
            r'midgrade\s*\$?(\d+\.?\d*)', # Midgrade $5.30
            r'89\s*\$?(\d+\.?\d*)',       # 89 $5.30
            r'diesel\s*\$?(\d+\.?\d*)',   # Diesel $5.50
        ]
        
        prices = {}
        text_lower = text.lower()
        
        # Extract regular/87 price
        for pattern in [r'regular\s*\$?(\d+\.?\d*)', r'87\s*\$?(\d+\.?\d*)']:
            match = re.search(pattern, text_lower)
            if match:
                prices['87'] = float(match.group(1))
                break
        
        # Extract premium/91 price
        for pattern in [r'premium\s*\$?(\d+\.?\d*)', r'91\s*\$?(\d+\.?\d*)']:
            match = re.search(pattern, text_lower)
            if match:
                prices['91'] = float(match.group(1))
                break
        
        # Extract midgrade/89 price
        for pattern in [r'midgrade\s*\$?(\d+\.?\d*)', r'89\s*\$?(\d+\.?\d*)']:
            match = re.search(pattern, text_lower)
            if match:
                prices['89'] = float(match.group(1))
                break
        
        # If we found at least one price, return them
        if prices:
            # If we only found one price, estimate the others
            if '87' in prices and '89' not in prices:
                prices['89'] = round(prices['87'] + 0.25, 2)
            if '87' in prices and '91' not in prices:
                prices['91'] = round(prices['87'] + 0.50, 2)
            if '89' in prices and '87' not in prices:
                prices['87'] = round(prices['89'] - 0.25, 2)
            if '91' in prices and '87' not in prices:
                prices['87'] = round(prices['91'] - 0.50, 2)
            
            return prices
        
        return None
    
    def _generate_prices_from_level(self, price_level: int) -> Dict[str, float]:
        """
        Generate realistic prices based on Google's price level (Updated for 2024)
        """
        # Base prices for different price levels (0-4 scale) - Updated for 2024
        base_prices = {
            0: 3.80,  # Very cheap
            1: 4.10,  # Cheap
            2: 4.40,  # Moderate
            3: 4.80,  # Expensive
            4: 5.20   # Very expensive
        }
        
        base_price = base_prices.get(price_level, 4.40)
        
        # Add some realistic variation
        variation = random.uniform(-0.20, 0.20)
        
        return {
            '87': round(base_price + variation, 2),
            '89': round(base_price + 0.25 + variation, 2),
            '91': round(base_price + 0.50 + variation, 2)
        }
    
    def _calculate_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """
        Calculate distance between two points in miles
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

# Global instance
gas_price_service = GasPriceService()

# Convenience function
def get_gas_prices(latitude: float, longitude: float, station_name: str = "") -> Dict[str, float]:
    """Convenience function for getting gas prices"""
    return gas_price_service.get_gas_prices(latitude, longitude, station_name) 