# Gas Station Recommendation App

A smart gas station recommendation system that helps you find the best gas stations near you based on cost, distance, and travel time. The app uses AI-powered analysis to provide personalized recommendations.

## Features

- 🚗 **Car Setup**: Configure your car's MPG and fuel tank size
- ⛽ **Fuel Needs**: Input specific gallons or percentage of tank needed
- 📍 **Location Services**: Use GPS or enter address manually
- 🗺️ **Smart Search**: Find gas stations within your range
- 💰 **Cost Analysis**: Calculate total cost including travel expenses
- 🤖 **AI Recommendations**: Get AI-powered rankings and insights
- ⏱️ **Time Optimization**: Consider travel time in recommendations

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd gas_station_recommendation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (optional):
```bash
export GOOGLE_MAPS_API_KEY="your_google_maps_api_key"
export CLAUDE_API_KEY="your_claude_api_key"
export OPENAI_API_KEY="your_openai_api_key"
```

## Usage

Run the application:
```bash
python main.py
```

The app will guide you through:
1. Setting up your car preferences (MPG, tank size)
2. Specifying fuel needs (gallons or percentage)
3. Choosing location (GPS or manual address)
4. Getting AI-powered recommendations

## Configuration

### API Keys

- **Google Maps API**: For real gas station data and directions
- **Claude API**: For AI analysis and recommendations
- **OpenAI API**: Alternative LLM provider

### Default Settings

- Search radius: 10 miles
- Maximum travel time: 20 minutes
- Default location: San Francisco (when GPS unavailable)

## Project Structure

```
gas_recommendation_app/
│
├── main.py                  # Entry point
├── config.py                # Configuration settings
├── requirements.txt         # Dependencies
├── README.md               # This file
│
├── services/
│   ├── fuel_calculator.py   # Fuel needs calculation
│   ├── location_service.py  # Geolocation functions
│   ├── map_service.py       # Google Maps integration
│   ├── llm_service.py       # AI analysis
│   └── gas_filter.py        # Station filtering logic
│
├── models/
│   └── schema.py            # Data models
│
├── utils/
│   └── helpers.py           # Utility functions
│
└── data/
    └── icons/               # App icons (placeholder)
```

## How It Works

1. **Input Processing**: User provides car specs and fuel needs
2. **Location Detection**: GPS or geocoded address
3. **Station Search**: Find nearby gas stations
4. **Cost Calculation**: Include travel costs in total price
5. **AI Analysis**: LLM ranks stations by efficiency
6. **Recommendations**: Present top 5 options with reasoning

## Cost Calculation

The app calculates total cost as:
```
Total Cost = Fuel Cost + Travel Cost
Fuel Cost = Gallons Needed × Price per Gallon
Travel Cost = (Distance × 2 / MPG) × Price per Gallon
```

## API Integration

### Google Maps API
- Places API for gas station search
- Directions API for travel time
- Geocoding for address conversion

### LLM APIs
- Claude API (primary)
- OpenAI API (fallback)
- Mock analysis when APIs unavailable

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
```

### Type Checking
```bash
mypy .
```

### Linting
```bash
flake8
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation
- Review the code comments

## Roadmap

- [ ] Web interface
- [ ] Mobile app
- [ ] Real-time gas prices
- [ ] Route optimization
- [ ] User preferences storage
- [ ] Integration with car APIs
- [ ] Fuel loyalty programs
- [ ] Environmental impact analysis 