#!/usr/bin/env python3
"""
Gas Station Recommendation App
Main entry point for the application
"""

import sys
import os
from typing import Optional, Tuple
from services import fuel_calculator, location_service, map_service, gas_filter, llm_service
from models.schema import UserPreferences, GasStation
from utils.helpers import display_icons, print_banner

def get_user_preferences() -> UserPreferences:
    """Get user preferences for car settings"""
    print_banner("🚗 Car Setup")
    print("Let's set up your car preferences:")
    
    try:
        mpg = float(input("Enter your car's MPG (miles per gallon): "))
        tank_size = float(input("Enter your fuel tank size (gallons): "))
        
        return UserPreferences(mpg=mpg, tank_size=tank_size)
    except ValueError:
        print("❌ Invalid input. Please enter valid numbers.")
        return get_user_preferences()

def get_fuel_needs(tank_size: float) -> Tuple[str, float]:
    """Get fuel needs from user"""
    print_banner("⛽ Fuel Needs")
    print("How much fuel do you need?")
    print("1. Enter specific amount (e.g., 5 gallons)")
    print("2. Enter percentage of tank (e.g., 20% of tank)")
    
    choice = input("Choose option (1 or 2): ").strip()
    
    if choice == "1":
        try:
            gallons = float(input("Enter gallons needed: "))
            return "gallon", gallons
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")
            return get_fuel_needs(tank_size)
    
    elif choice == "2":
        try:
            percentage = float(input("Enter percentage (e.g., 20 for 20%): "))
            return "percent", percentage
        except ValueError:
            print("❌ Invalid input. Please enter a valid percentage.")
            return get_fuel_needs(tank_size)
    
    else:
        print("❌ Invalid choice. Please select 1 or 2.")
        return get_fuel_needs(tank_size)

def get_location() -> Tuple[float, float]:
    """Get user location"""
    print_banner("📍 Location")
    print("1. Use current location (GPS)")
    print("2. Enter address manually")
    
    choice = input("Choose option (1 or 2): ").strip()
    
    if choice == "1":
        print("📍 Getting current location...")
        location = location_service.use_current_location()
        print(f"📍 Location: {location[0]:.4f}, {location[1]:.4f}")
        return location
    
    elif choice == "2":
        address = input("Enter your address: ").strip()
        print("📍 Geocoding address...")
        try:
            location = location_service.geocode_address(address)
            print(f"📍 Location: {location[0]:.4f}, {location[1]:.4f}")
            return location
        except Exception as e:
            print(f"❌ Error geocoding address: {e}")
            print("📍 Falling back to current location...")
            return location_service.use_current_location()
    
    else:
        print("❌ Invalid choice. Using current location...")
        return location_service.use_current_location()

def run_recommendation(preferences: UserPreferences, fuel_input_type: str, 
                      fuel_value: float, location: Tuple[float, float]) -> str:
    """Run the complete recommendation process"""
    print_banner("🔍 Processing")
    
    # Calculate fuel needed
    print("⛽ Calculating fuel needs...")
    fuel_needed = fuel_calculator.calculate_gas_needed(fuel_input_type, fuel_value, preferences.tank_size)
    tank_remaining = preferences.tank_size - fuel_needed
    
    print(f"⛽ Fuel needed: {fuel_needed:.1f} gallons")
    print(f"⛽ Tank remaining: {tank_remaining:.1f} gallons")
    
    # Search for gas stations
    print("🗺️  Searching for gas stations...")
    stations = map_service.search_gas_stations(location)
    print(f"🗺️  Found {len(stations)} gas stations")
    
    # Filter stations
    print("🔍 Filtering stations based on range and time...")
    filtered = gas_filter.filter_stations(stations, fuel_needed, preferences.mpg, tank_remaining)
    print(f"🔍 {len(filtered)} stations meet criteria")
    
    if not filtered:
        print("❌ No gas stations found within your range!")
        return "No suitable gas stations found."
    
    # Get LLM analysis
    print("🤖 Analyzing with AI...")
    recommendation = llm_service.analyze_with_llm(filtered)
    
    return recommendation

def main():
    """Main application entry point"""
    print_banner("Gas Station Recommendation App")
    display_icons()
    
    try:
        # Get user preferences
        preferences = get_user_preferences()
        
        # Get fuel needs
        fuel_input_type, fuel_value = get_fuel_needs(preferences.tank_size)
        
        # Get location
        location = get_location()
        
        # Run recommendation
        result = run_recommendation(preferences, fuel_input_type, fuel_value, location)
        
        # Display results
        print_banner("🎯 Recommendations")
        print(result)
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 