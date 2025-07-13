"""
Helper utilities for Gas Station Recommendation App
"""

import os
import sys
from typing import List, Dict, Any, Optional

def print_banner(title: str, width: int = 60) -> None:
    """
    Print a formatted banner with title
    
    Args:
        title: Banner title
        width: Banner width
    """
    print("\n" + "=" * width)
    print(f"  {title.center(width - 4)}")
    print("=" * width)

def display_icons() -> None:
    """
    Display app icons and branding
    """
    icons = """
    ⛽ Gas Station Recommendation App ⛽
    
    🚗 Find the best gas stations near you
    📍 Get location-based recommendations  
    💰 Save money with smart cost analysis
    🤖 AI-powered insights and rankings
    
    """
    print(icons)

def format_currency(amount: float) -> str:
    """
    Format amount as currency
    
    Args:
        amount: Amount to format
        
    Returns:
        str: Formatted currency string
    """
    return f"${amount:.2f}"

def format_distance(distance: float) -> str:
    """
    Format distance for display
    
    Args:
        distance: Distance in miles
        
    Returns:
        str: Formatted distance string
    """
    if distance < 1:
        return f"{distance * 5280:.0f} ft"
    else:
        return f"{distance:.1f} miles"

def format_time(minutes: int) -> str:
    """
    Format time for display
    
    Args:
        minutes: Time in minutes
        
    Returns:
        str: Formatted time string
    """
    if minutes < 60:
        return f"{minutes} min"
    else:
        hours = minutes // 60
        mins = minutes % 60
        if mins == 0:
            return f"{hours} hr"
        else:
            return f"{hours} hr {mins} min"

def display_station(station: Dict[str, Any], index: Optional[int] = None) -> None:
    """
    Display a single gas station in a formatted way
    
    Args:
        station: Gas station data
        index: Optional index number
    """
    name = station.get('name', 'Unknown Station')
    brand = station.get('brand', 'Unknown')
    price = station.get('price_per_gallon', 0)
    distance = station.get('distance_miles', 0)
    travel_time = station.get('travel_time_minutes', 0)
    total_cost = station.get('total_cost', 0)
    rating = station.get('rating', 'N/A')
    
    prefix = f"#{index}: " if index is not None else ""
    
    print(f"{prefix}🏪 {name}")
    print(f"   🏷️  Brand: {brand}")
    print(f"   💰 Price: {format_currency(price)}/gallon")
    print(f"   📍 Distance: {format_distance(distance)}")
    print(f"   ⏱️  Travel Time: {format_time(travel_time)}")
    print(f"   💵 Total Cost: {format_currency(total_cost)}")
    if rating != 'N/A':
        print(f"   ⭐ Rating: {rating}")
    print()

def display_stations_list(stations: List[Dict[str, Any]], title: str = "Gas Stations") -> None:
    """
    Display a list of gas stations
    
    Args:
        stations: List of gas station data
        title: Display title
    """
    if not stations:
        print("❌ No gas stations found.")
        return
    
    print_banner(title)
    
    for i, station in enumerate(stations, 1):
        display_station(station, i)

def display_summary(stations: List[Dict[str, Any]]) -> None:
    """
    Display summary statistics for gas stations
    
    Args:
        stations: List of gas station data
    """
    if not stations:
        print("❌ No stations to summarize.")
        return
    
    prices = [s.get('price_per_gallon', 0) for s in stations]
    distances = [s.get('distance_miles', 0) for s in stations]
    costs = [s.get('total_cost', 0) for s in stations]
    
    print_banner("📊 Summary Statistics")
    print(f"🏪 Total Stations: {len(stations)}")
    print(f"💰 Price Range: {format_currency(min(prices))} - {format_currency(max(prices))}/gallon")
    print(f"📍 Distance Range: {format_distance(min(distances))} - {format_distance(max(distances))}")
    print(f"💵 Cost Range: {format_currency(min(costs))} - {format_currency(max(costs))}")
    print(f"📈 Average Price: {format_currency(sum(prices)/len(prices))}/gallon")
    print(f"📉 Average Cost: {format_currency(sum(costs)/len(costs))}")

def get_user_confirmation(prompt: str = "Continue? (y/n): ") -> bool:
    """
    Get user confirmation
    
    Args:
        prompt: Confirmation prompt
        
    Returns:
        bool: True if user confirms
    """
    while True:
        response = input(prompt).strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' or 'n'.")

def clear_screen() -> None:
    """
    Clear the terminal screen
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def show_loading_animation(message: str = "Loading...", duration: int = 3) -> None:
    """
    Show a simple loading animation
    
    Args:
        message: Loading message
        duration: Animation duration in seconds
    """
    import time
    import threading
    
    def animate():
        chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        i = 0
        start_time = time.time()
        
        while time.time() - start_time < duration:
            print(f"\r{chars[i]} {message}", end='', flush=True)
            time.sleep(0.1)
            i = (i + 1) % len(chars)
        
        print(f"\r✅ {message} Complete!")
    
    # Run animation in a separate thread
    thread = threading.Thread(target=animate)
    thread.start()
    thread.join()

def validate_numeric_input(prompt: str, min_value: Optional[float] = None, max_value: Optional[float] = None) -> float:
    """
    Get and validate numeric input from user
    
    Args:
        prompt: Input prompt
        min_value: Minimum allowed value
        max_value: Maximum allowed value
        
    Returns:
        float: Validated numeric value
    """
    while True:
        try:
            value = float(input(prompt))
            
            if min_value is not None and value < min_value:
                print(f"❌ Value must be at least {min_value}")
                continue
                
            if max_value is not None and value > max_value:
                print(f"❌ Value must be at most {max_value}")
                continue
                
            return value
            
        except ValueError:
            print("❌ Please enter a valid number.")

def create_progress_bar(current: int, total: int, width: int = 40) -> str:
    """
    Create a progress bar string
    
    Args:
        current: Current progress value
        total: Total value
        width: Progress bar width
        
    Returns:
        str: Progress bar string
    """
    if total == 0:
        return "[" + " " * width + "] 0%"
    
    progress = current / total
    filled = int(width * progress)
    bar = "█" * filled + "░" * (width - filled)
    percentage = int(progress * 100)
    
    return f"[{bar}] {percentage}%"

def display_error(message: str) -> None:
    """
    Display an error message
    
    Args:
        message: Error message
    """
    print(f"❌ Error: {message}")

def display_success(message: str) -> None:
    """
    Display a success message
    
    Args:
        message: Success message
    """
    print(f"✅ {message}")

def display_warning(message: str) -> None:
    """
    Display a warning message
    
    Args:
        message: Warning message
    """
    print(f"⚠️  Warning: {message}")

def display_info(message: str) -> None:
    """
    Display an info message
    
    Args:
        message: Info message
    """
    print(f"ℹ️  {message}") 