"""
LLM service for Gas Station Recommendation App
"""

import json
import time
from typing import List, Dict, Any, Optional
import requests
from config import Config

class LLMService:
    """Service for handling LLM interactions and analysis"""
    
    def __init__(self):
        self.claude_api_key = Config.CLAUDE_API_KEY
        self.openai_api_key = Config.OPENAI_API_KEY
        self.model = Config.LLM_MODEL
        self.max_tokens = Config.MAX_TOKENS
        self.temperature = Config.TEMPERATURE
    
    def analyze_with_llm(self, station_data: List[Dict[str, Any]], fuel_grade: str = "87") -> str:
        """
        Analyze gas station data with LLM and provide recommendations
        
        Args:
            station_data: List of gas station data
            fuel_grade: Fuel grade to consider (87, 89, 91)
            
        Returns:
            str: LLM analysis and recommendations
        """
        if not station_data:
            return "No gas stations found to analyze."
        
        # Format input for LLM
        input_prompt = self._format_station_data(station_data, fuel_grade)
        
        # Try Claude first, then OpenAI, then fallback
        try:
            if self.claude_api_key:
                return self._call_claude_api(input_prompt)
            elif self.openai_api_key:
                return self._call_openai_api(input_prompt)
            else:
                return self._generate_mock_analysis(station_data, fuel_grade)
        except Exception as e:
            print(f"⚠️  LLM API error: {e}")
            return self._generate_mock_analysis(station_data, fuel_grade)
    
    def _format_station_data(self, stations: List[Dict[str, Any]], fuel_grade: str = "87") -> str:
        """
        Format station data for LLM input
        
        Args:
            stations: List of gas station data
            fuel_grade: Fuel grade to consider (87, 89, 91)
            
        Returns:
            str: Formatted prompt
        """
        prompt = f"""You are an expert gas station recommendation assistant. Analyze the following gas stations and provide a detailed recommendation ranking the top 5 stations.

IMPORTANT: The user is looking for {fuel_grade} octane fuel. Consider the specific price for {fuel_grade} octane when available, not just the lowest price.

Consider these factors in your analysis:
1. Total cost (fuel cost + travel cost) for {fuel_grade} octane fuel
2. Distance and travel time
3. Brand reputation and ratings
4. Overall value for money
5. Fuel grade availability and pricing

Please provide your analysis in this exact format:

**BRIEF ANALYSIS:**
[Provide 2-3 sentences about the overall options and market conditions]

**TOP 5 RECOMMENDATIONS:**
Please list your top 5 recommendations in this format:
1. [Station Name] - [Brief reason]
2. [Station Name] - [Brief reason]
3. [Station Name] - [Brief reason]
4. [Station Name] - [Brief reason]
5. [Station Name] - [Brief reason]

Then provide a brief summary paragraph of your recommendations.

**ADDITIONAL CONSIDERATIONS:**
[Any important warnings, tips, or additional information]

Here are the gas station options:

"""
        
        for idx, station in enumerate(stations[:10], 1):  # Limit to top 10 for analysis
            # Get the correct price for the selected fuel grade
            gas_prices = station.get('gas_prices', {})
            selected_price = gas_prices.get(fuel_grade, station.get('price_per_gallon', 0))
            
            prompt += f"""Gas Station #{idx}: {station.get('name', 'Unknown')}
- Brand: {station.get('brand', 'Unknown')}
- {fuel_grade} Octane Price: ${selected_price:.2f}/gallon
- Distance: {station.get('distance_miles', 0):.1f} miles
- Travel Time: {station.get('travel_time_minutes', 0)} minutes
- Fuel Cost: ${station.get('fuel_cost', 0):.2f}
- Travel Cost: ${station.get('travel_cost', 0):.2f}
- Total Cost: ${station.get('total_cost', 0):.2f}
- Rating: {station.get('rating', 'N/A')}
- Address: {station.get('address', 'N/A')}
- All Fuel Grades: {gas_prices}

"""
        
        prompt += "\nPlease provide your analysis and top 5 recommendations:"
        
        return prompt
    
    def _call_claude_api(self, prompt: str) -> str:
        """
        Call Claude API for analysis
        
        Args:
            prompt: Formatted prompt for Claude
            
        Returns:
            str: Claude's response
        """
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.claude_api_key,
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['content'][0]['text']
    
    def _call_openai_api(self, prompt: str) -> str:
        """
        Call OpenAI API for analysis
        
        Args:
            prompt: Formatted prompt for OpenAI
            
        Returns:
            str: OpenAI's response
        """
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.openai_api_key}"
        }
        
        data = {
            "model": "gpt-4",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert gas station recommendation assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content']
    
    def _generate_mock_analysis(self, stations: List[Dict[str, Any]], fuel_grade: str = "87") -> str:
        """
        Generate mock analysis when LLM APIs are unavailable
        
        Args:
            stations: List of gas station data
            fuel_grade: Fuel grade to consider (87, 89, 91)
            
        Returns:
            str: Mock analysis
        """
        if not stations:
            return "No gas stations found to analyze."
        
        # Sort by total cost
        sorted_stations = sorted(stations, key=lambda x: x.get('total_cost', float('inf')))
        
        analysis = f"🤖 AI Analysis (Mock Mode) - {fuel_grade} Octane Fuel\n\n"
        analysis += "Based on the available gas stations, here are my top 5 recommendations:\n\n"
        
        for i, station in enumerate(sorted_stations[:5], 1):
            name = station.get('name', 'Unknown Station')
            brand = station.get('brand', 'Unknown')
            gas_prices = station.get('gas_prices', {})
            selected_price = gas_prices.get(fuel_grade, station.get('price_per_gallon', 0))
            distance = station.get('distance_miles', 0)
            travel_time = station.get('travel_time_minutes', 0)
            total_cost = station.get('total_cost', 0)
            rating = station.get('rating', 'N/A')
            
            analysis += f"#{i}: {name} ({brand})\n"
            analysis += f"   💰 {fuel_grade} Octane Price: ${selected_price:.2f}/gallon | Total Cost: ${total_cost:.2f}\n"
            analysis += f"   📍 Distance: {distance:.1f} miles | ⏱️  Time: {travel_time} min\n"
            analysis += f"   ⭐ Rating: {rating}\n\n"
        
        # Add summary
        avg_price = sum(s.get('price_per_gallon', 0) for s in stations) / len(stations)
        min_cost = min(s.get('total_cost', float('inf')) for s in stations)
        max_cost = max(s.get('total_cost', 0) for s in stations)
        
        analysis += f"📊 Summary:\n"
        analysis += f"   • Average price: ${avg_price:.2f}/gallon\n"
        analysis += f"   • Cost range: ${min_cost:.2f} - ${max_cost:.2f}\n"
        analysis += f"   • Stations analyzed: {len(stations)}\n\n"
        
        analysis += "💡 Recommendation: Choose the station with the lowest total cost that fits your time constraints."
        
        return analysis
    
    def summarize_stations(self, stations: List[Dict[str, Any]]) -> str:
        """
        Generate a brief summary of gas stations
        
        Args:
            stations: List of gas station data
            
        Returns:
            str: Summary text
        """
        if not stations:
            return "No gas stations found."
        
        prices = [s.get('price_per_gallon', 0) for s in stations]
        distances = [s.get('distance_miles', 0) for s in stations]
        
        summary = f"Found {len(stations)} gas stations:\n"
        summary += f"• Price range: ${min(prices):.2f} - ${max(prices):.2f}/gallon\n"
        summary += f"• Distance range: {min(distances):.1f} - {max(distances):.1f} miles\n"
        summary += f"• Average price: ${sum(prices)/len(prices):.2f}/gallon"
        
        return summary
    
    def get_quick_recommendation(self, stations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get quick recommendation without full LLM analysis
        
        Args:
            stations: List of gas station data
            
        Returns:
            Dict: Quick recommendation data
        """
        if not stations:
            return {"error": "No stations found"}
        
        # Find best by different criteria
        cheapest = min(stations, key=lambda x: x.get('total_cost', float('inf')))
        closest = min(stations, key=lambda x: x.get('distance_miles', float('inf')))
        fastest = min(stations, key=lambda x: x.get('travel_time_minutes', float('inf')))
        
        return {
            "cheapest": cheapest,
            "closest": closest,
            "fastest": fastest,
            "total_stations": len(stations)
        }

# Global instance
llm_service = LLMService()

# Convenience functions
def analyze_with_llm(station_data: List[Dict[str, Any]], fuel_grade: str = "87") -> str:
    """Convenience function for LLM analysis"""
    return llm_service.analyze_with_llm(station_data, fuel_grade)

def summarize_stations(stations: List[Dict[str, Any]]) -> str:
    """Convenience function for station summary"""
    return llm_service.summarize_stations(stations)

def get_quick_recommendation(stations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Convenience function for quick recommendation"""
    return llm_service.get_quick_recommendation(stations) 