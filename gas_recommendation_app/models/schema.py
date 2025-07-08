"""
Data models for Gas Station Recommendation App
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime

@dataclass
class UserPreferences:
    """User car preferences"""
    mpg: float
    tank_size: float
    current_fuel_level: Optional[float] = None
    
    def __post_init__(self):
        if self.current_fuel_level is None:
            self.current_fuel_level = self.tank_size * 0.25  # Assume 25% full

@dataclass
class Location:
    """Geographic location"""
    latitude: float
    longitude: float
    address: Optional[str] = None
    
    def __str__(self) -> str:
        if self.address:
            return f"{self.address} ({self.latitude:.4f}, {self.longitude:.4f})"
        return f"({self.latitude:.4f}, {self.longitude:.4f})"

@dataclass
class GasStation:
    """Gas station information"""
    name: str
    location: Location
    price_per_gallon: float
    distance_miles: float
    travel_time_minutes: int
    brand: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    rating: Optional[float] = None
    total_cost: Optional[float] = None
    travel_cost: Optional[float] = None
    fuel_types: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.fuel_types is None:
            self.fuel_types = ["Regular", "Premium"]
    
    def calculate_total_cost(self, gallons_needed: float, mpg: float, 
                           current_price: Optional[float] = None) -> Dict[str, float]:
        """Calculate total cost including travel cost"""
        price = current_price or self.price_per_gallon
        fuel_cost = gallons_needed * price
        travel_gallons = self.distance_miles / mpg
        travel_cost = travel_gallons * price
        total_cost = fuel_cost + travel_cost
        
        self.total_cost = round(total_cost, 2)
        self.travel_cost = round(travel_cost, 2)
        
        return {
            "fuel_cost": round(fuel_cost, 2),
            "travel_cost": self.travel_cost,
            "total_cost": self.total_cost
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "name": self.name,
            "brand": self.brand,
            "address": self.address,
            "location": {
                "latitude": self.location.latitude,
                "longitude": self.location.longitude,
                "address": self.location.address
            },
            "price_per_gallon": self.price_per_gallon,
            "distance_miles": self.distance_miles,
            "travel_time_minutes": self.travel_time_minutes,
            "rating": self.rating,
            "total_cost": self.total_cost,
            "travel_cost": self.travel_cost,
            "fuel_types": self.fuel_types
        }

@dataclass
class RecommendationRequest:
    """Request for gas station recommendations"""
    user_preferences: UserPreferences
    fuel_needed: float
    location: Location
    search_radius_miles: float = 10.0
    max_travel_time_minutes: int = 20

@dataclass
class RecommendationResponse:
    """Response with gas station recommendations"""
    stations: List[GasStation]
    analysis: str
    timestamp: datetime
    request: RecommendationRequest
    
    def __post_init__(self):
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)
    
    def get_top_stations(self, limit: int = 5) -> List[GasStation]:
        """Get top stations sorted by total cost"""
        sorted_stations = sorted(
            self.stations, 
            key=lambda x: x.total_cost or float('inf')
        )
        return sorted_stations[:limit]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "stations": [station.to_dict() for station in self.stations],
            "analysis": self.analysis,
            "timestamp": self.timestamp.isoformat(),
            "top_stations": [station.to_dict() for station in self.get_top_stations()]
        } 