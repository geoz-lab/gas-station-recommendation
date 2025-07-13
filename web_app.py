#!/usr/bin/env python3
"""
Flask Web Application for Gas Station Recommendation App
"""

from flask import Flask, render_template, request, jsonify, session
import json
import os
from datetime import datetime
from services import fuel_calculator, location_service, map_service, gas_filter, llm_service
from models.schema import UserPreferences
from config import Config

app = Flask(__name__)
app.secret_key = 'gas_station_recommendation_secret_key_2024'

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', config=Config)

@app.route('/api/calculate-fuel', methods=['POST'])
def calculate_fuel():
    """Calculate fuel needs"""
    try:
        data = request.get_json()
        input_type = data.get('input_type')  # 'gallon' or 'percent'
        value = float(data.get('value'))
        tank_size = float(data.get('tank_size', 15.0))
        
        fuel_needed = fuel_calculator.calculate_gas_needed(input_type, value, tank_size)
        
        return jsonify({
            'success': True,
            'fuel_needed': fuel_needed,
            'tank_remaining': tank_size - fuel_needed
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/search-stations', methods=['POST'])
def search_stations():
    """Search for gas stations"""
    try:
        data = request.get_json()
        
        # Get user preferences
        mpg = float(data.get('mpg', 25.0))
        tank_size = float(data.get('tank_size', 15.0))
        fuel_needed = float(data.get('fuel_needed', 5.0))
        fuel_grade = data.get('fuel_grade', '87')  # Default to regular (87)
        
        # Validate inputs
        if not all([mpg, tank_size, fuel_needed]):
            return jsonify({
                'success': False, 
                'error': 'Invalid input values. Please check MPG, tank size, and fuel needed.'
            })
        
        # Get location with timeout handling
        location_type = data.get('location_type')  # 'current' or 'address'
        
        if location_type == 'current':
            # Check if coordinates were provided by the frontend
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            
            if latitude is not None and longitude is not None:
                # Use the coordinates provided by the browser
                location = (float(latitude), float(longitude))
            else:
                # Fallback to IP-based location
                location = location_service.use_current_location()
        else:
            address = data.get('address', 'San Francisco, CA')
            try:
                # Simple geocoding without signal timeout (which doesn't work well in web context)
                location = location_service.geocode_address(address)
                
                # Validate the location
                if not location or len(location) != 2:
                    raise Exception("Invalid location returned")
                    
            except Exception as e:
                return jsonify({
                    'success': False, 
                    'error': f'Could not find location for address: {address}. Please check the address or use current location.'
                })
        
        # Search for stations
        radius_miles = float(data.get('radius_miles', 10.0))
        stations = map_service.search_gas_stations(location, radius_miles)
        
        # Filter stations
        tank_remaining = max(0, tank_size - fuel_needed)  # Ensure non-negative
        filtered_stations = gas_filter.filter_stations(stations, fuel_needed, mpg, tank_remaining, fuel_grade=fuel_grade)
        
        # Get AI analysis
        if filtered_stations:
            analysis = llm_service.analyze_with_llm(filtered_stations[:10], fuel_grade)  # Pass fuel grade
        else:
            analysis = "No gas stations found within your range."
        
        return jsonify({
            'success': True,
            'location': location,
            'stations': filtered_stations,
            'analysis': analysis,
            'total_stations': len(stations),
            'filtered_stations': len(filtered_stations)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/geocode', methods=['POST'])
def geocode_address():
    """Geocode an address"""
    try:
        data = request.get_json()
        address = data.get('address')
        
        if not address:
            return jsonify({'success': False, 'error': 'Address is required'})
        
        location = location_service.geocode_address(address)
        
        return jsonify({
            'success': True,
            'latitude': location[0],
            'longitude': location[1]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/current-location', methods=['GET'])
def get_current_location():
    """Get current location using IP geolocation"""
    try:
        location = location_service.get_location_from_ip()
        
        return jsonify({
            'success': True,
            'latitude': location[0],
            'longitude': location[1]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/config')
def get_config():
    """Get app configuration"""
    return jsonify({
        'default_mpg': Config.DEFAULT_MPG,
        'default_tank_size': Config.DEFAULT_TANK_SIZE,
        'default_radius': Config.DEFAULT_SEARCH_RADIUS_MILES,
        'max_travel_time': Config.MAX_TRAVEL_TIME_MINUTES,
        'has_google_maps': bool(Config.GOOGLE_MAPS_API_KEY),
        'has_claude': bool(Config.CLAUDE_API_KEY),
        'has_openai': bool(Config.OPENAI_API_KEY)
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    print("🚀 Starting Gas Station Recommendation Web App...")
    print("📍 Access the app at: http://localhost:8080")
    print("🔧 API endpoints available at: http://localhost:8080/api/")
    
    app.run(debug=True, host='0.0.0.0', port=8080) 