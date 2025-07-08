"""
Gas station filtering service for Gas Station Recommendation App
"""

from typing import List, Dict, Any, Optional
from models.schema import GasStation, Location
from config import Config

def filter_stations(stations: List[Dict[str, Any]], gas_needed: float, mpg: float, 
                   tank_remaining: float, speed: int = 40, fuel_grade: str = '87') -> List[Dict[str, Any]]:
    """
    Filter gas stations based on range, time, and other criteria
    
    Args:
        stations: List of gas station data
        gas_needed: Amount of gas needed in gallons
        mpg: Miles per gallon of the car
        tank_remaining: Remaining fuel in tank
        speed: Typical speed for time calculations (mph)
        fuel_grade: Fuel grade to use for price calculations ('87', '89', '91')
        
    Returns:
        List[Dict]: Filtered and ranked gas stations
    """
    recommended = []
    
    # Calculate maximum range based on remaining fuel
    max_range = tank_remaining * mpg
    
    # Calculate maximum travel time (20 minutes)
    max_travel_time = Config.MAX_TRAVEL_TIME_MINUTES
    
    for station in stations:
        distance = station.get('distance_miles', float('inf'))
        travel_time = station.get('travel_time_minutes', float('inf'))
        
        # Check if station is within range
        if distance <= max_range and travel_time <= max_travel_time:
            # Calculate costs using the selected fuel grade
            costs = calculate_station_costs(station, gas_needed, mpg, fuel_grade)
            
            # Add calculated costs to station data
            station.update(costs)
            
            # Add efficiency score
            station['efficiency_score'] = calculate_efficiency_score(station, gas_needed, mpg)
            
            recommended.append(station)
    
    # Sort by efficiency score (higher is better)
    recommended.sort(key=lambda x: x.get('efficiency_score', 0), reverse=True)
    
    return recommended

def calculate_station_costs(station: Dict[str, Any], gas_needed: float, mpg: float, fuel_grade: str = '87') -> Dict[str, float]:
    """
    Calculate total costs for a gas station
    
    Args:
        station: Gas station data
        gas_needed: Amount of gas needed in gallons
        mpg: Miles per gallon of the car
        fuel_grade: Fuel grade to use for price calculations ('87', '89', '91')
        
    Returns:
        Dict[str, float]: Cost breakdown
    """
    # Get the correct price for the selected fuel grade
    gas_prices = station.get('gas_prices', {})
    price_per_gallon = gas_prices.get(fuel_grade, station.get('price_per_gallon', 0))
    distance = station.get('distance_miles', 0)
    
    # Calculate fuel cost
    fuel_cost = gas_needed * price_per_gallon
    
    # Calculate travel cost (fuel used to get there and back)
    travel_gallons = (distance * 2) / mpg  # Round trip
    travel_cost = travel_gallons * price_per_gallon
    
    # Total cost
    total_cost = fuel_cost + travel_cost
    
    return {
        'fuel_cost': round(fuel_cost, 2),
        'travel_cost': round(travel_cost, 2),
        'total_cost': round(total_cost, 2),
        'cost_per_gallon_effective': round(total_cost / gas_needed, 2)
    }

def calculate_efficiency_score(station: Dict[str, Any], gas_needed: float, mpg: float) -> float:
    """
    Calculate efficiency score for ranking stations
    
    Args:
        station: Gas station data
        gas_needed: Amount of gas needed in gallons
        mpg: Miles per gallon of the car
        
    Returns:
        float: Efficiency score (higher is better)
    """
    # Base score starts with cost efficiency
    total_cost = station.get('total_cost', float('inf'))
    cost_score = 1000 / (total_cost + 1)  # Higher cost = lower score
    
    # Distance penalty (closer is better)
    distance = station.get('distance_miles', 0)
    distance_penalty = distance * 10
    
    # Time penalty (faster is better)
    travel_time = station.get('travel_time_minutes', 0)
    time_penalty = travel_time * 2
    
    # Rating bonus (if available)
    rating = station.get('rating', 3.0)
    if rating is not None:
        rating_bonus = (rating - 3.0) * 50  # Bonus for ratings above 3.0
    else:
        rating_bonus = 0  # No bonus for stations without ratings
    
    # Brand preference (major brands get small bonus)
    brand = station.get('brand', '').lower()
    brand_bonus = 0
    if brand in ['shell', 'chevron', 'exxon', 'mobil', 'bp']:
        brand_bonus = 20
    
    final_score = cost_score - distance_penalty - time_penalty + rating_bonus + brand_bonus
    
    return max(0, final_score)  # Ensure non-negative

def filter_by_brand(stations: List[Dict[str, Any]], preferred_brands: List[str]) -> List[Dict[str, Any]]:
    """
    Filter stations by preferred brands
    
    Args:
        stations: List of gas station data
        preferred_brands: List of preferred brand names
        
    Returns:
        List[Dict]: Filtered stations
    """
    if not preferred_brands:
        return stations
    
    preferred_brands_lower = [brand.lower() for brand in preferred_brands]
    
    filtered = []
    for station in stations:
        brand = station.get('brand', '').lower()
        if brand in preferred_brands_lower:
            filtered.append(station)
    
    return filtered

def filter_by_price_range(stations: List[Dict[str, Any]], min_price: float, max_price: float) -> List[Dict[str, Any]]:
    """
    Filter stations by price range
    
    Args:
        stations: List of gas station data
        min_price: Minimum price per gallon
        max_price: Maximum price per gallon
        
    Returns:
        List[Dict]: Filtered stations
    """
    filtered = []
    for station in stations:
        price = station.get('price_per_gallon', 0)
        if min_price <= price <= max_price:
            filtered.append(station)
    
    return filtered

def filter_by_distance(stations: List[Dict[str, Any]], max_distance: float) -> List[Dict[str, Any]]:
    """
    Filter stations by maximum distance
    
    Args:
        stations: List of gas station data
        max_distance: Maximum distance in miles
        
    Returns:
        List[Dict]: Filtered stations
    """
    filtered = []
    for station in stations:
        distance = station.get('distance_miles', float('inf'))
        if distance <= max_distance:
            filtered.append(station)
    
    return filtered

def get_station_summary(stations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate summary statistics for gas stations
    
    Args:
        stations: List of gas station data
        
    Returns:
        Dict[str, Any]: Summary statistics
    """
    if not stations:
        return {
            'total_stations': 0,
            'avg_price': 0,
            'min_price': 0,
            'max_price': 0,
            'avg_distance': 0,
            'avg_travel_time': 0
        }
    
    prices = [s.get('price_per_gallon', 0) for s in stations]
    distances = [s.get('distance_miles', 0) for s in stations]
    travel_times = [s.get('travel_time_minutes', 0) for s in stations]
    
    return {
        'total_stations': len(stations),
        'avg_price': round(sum(prices) / len(prices), 2),
        'min_price': min(prices),
        'max_price': max(prices),
        'avg_distance': round(sum(distances) / len(distances), 1),
        'avg_travel_time': round(sum(travel_times) / len(travel_times), 0)
    }

def rank_by_criteria(stations: List[Dict[str, Any]], criteria: str = 'cost') -> List[Dict[str, Any]]:
    """
    Rank stations by different criteria
    
    Args:
        stations: List of gas station data
        criteria: Ranking criteria ('cost', 'distance', 'time', 'rating')
        
    Returns:
        List[Dict]: Ranked stations
    """
    if criteria == 'cost':
        return sorted(stations, key=lambda x: x.get('total_cost', float('inf')))
    elif criteria == 'distance':
        return sorted(stations, key=lambda x: x.get('distance_miles', float('inf')))
    elif criteria == 'time':
        return sorted(stations, key=lambda x: x.get('travel_time_minutes', float('inf')))
    elif criteria == 'rating':
        return sorted(stations, key=lambda x: x.get('rating', 0), reverse=True)
    else:
        return stations  # Return as-is for unknown criteria 