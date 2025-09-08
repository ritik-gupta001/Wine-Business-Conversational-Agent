import requests
import os
from typing import Dict, Any
from duckduckgo_search import DDGS
from datetime import datetime

class WeatherTool:
    """Tool for getting current weather information"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")  # Make sure this is set in your .env
        
    def _get_coordinates(self, city_name):
        """Convert city name to coordinates using OpenWeather Geocoding API"""
        geocoding_url = (
            f"http://api.openweathermap.org/geo/1.0/direct"
            f"?q={city_name}&limit=1&appid={self.api_key}"
        )
        response = requests.get(geocoding_url)
        if response.status_code == 200:
            results = response.json()
            if results:
                return results[0]['lat'], results[0]['lon']
        return None, None

    def get_weather(self, location, exclude="minutely,hourly"):
        """Get weather data for a given location (city name or lat,lon)."""
        try:
            # For Napa, CA use hardcoded coordinates since it's our primary location
            if location.lower().strip() == "napa, ca":
                lat, lon = 38.2975, -122.2869
            # Check if location is already in lat,lon format
            elif isinstance(location, tuple) and len(location) == 2:
                lat, lon = location
            else:
                # Convert city name to coordinates
                lat, lon = self._get_coordinates(location)
                if lat is None or lon is None:
                    return f"Sorry, I couldn't find the coordinates for {location}. Please try another nearby city."

            # Use the current weather API endpoint instead of onecall
            url = (
                f"https://api.openweathermap.org/data/2.5/weather"
                f"?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
            )
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                temp = data.get('main', {}).get('temp', 'N/A')
                description = data.get('weather', [{}])[0].get('description', 'N/A').capitalize()
                humidity = data.get('main', {}).get('humidity', 'N/A')
                
                weather_info = (
                    f"Current weather in {location}: {temp}°C, {description}. "
                    f"Humidity: {humidity}%"
                )
                return weather_info
            else:
                return f"Sorry, I'm having trouble getting the weather information right now. Error code: {response.status_code}"
                
        except Exception as e:
            return f"I apologize, but I'm having trouble accessing the weather information. Please try again later. Error: {str(e)}"

class WebSearchTool:
    """Tool for performing web searches"""
    
    def __init__(self):
        self.ddg = DDGS()
    
    def search_web(self, query: str, max_results: int = 3) -> str:
        """Perform a web search and return results"""
        try:
            results = list(self.ddg.text(query, max_results=max_results))
            
            if not results:
                return "No search results found."
            
            formatted_results = []
            for i, result in enumerate(results, 1):
                formatted_results.append(
                    f"{i}. {result['title']}\n"
                    f"   {result['body'][:200]}...\n"
                    f"   Source: {result['href']}\n"
                )
            
            return "Web Search Results:\n" + "\n".join(formatted_results)
            
        except Exception as e:
            return f"Web search error: {str(e)}"

class WineKnowledgeBase:
    """Tool for accessing wine business information"""
    
    def __init__(self, knowledge_file: str = "wine_business_info.txt"):
        self.knowledge_file = knowledge_file
        self.knowledge_content = self._load_knowledge()
    
    def _load_knowledge(self) -> str:
        """Load wine business knowledge from file"""
        try:
            with open(self.knowledge_file, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return "Wine business information file not found."
        except Exception as e:
            return f"Error loading wine business information: {str(e)}"
    
    def get_business_info(self, query: str = "") -> str:
        """Get wine business information"""
        if not self.knowledge_content:
            return "Wine business information is not available."
        
        return self.knowledge_content
    
    def search_knowledge(self, query: str) -> str:
        """Search within the wine business knowledge base"""
        if not self.knowledge_content:
            return "Wine business information is not available."
        
        # Simple keyword search (you could enhance this with semantic search)
        query_lower = query.lower()
        lines = self.knowledge_content.split('\n')
        relevant_lines = [line for line in lines if query_lower in line.lower()]
        
        if relevant_lines:
            return '\n'.join(relevant_lines[:10])  # Return first 10 matching lines
        else:
            return f"No specific information found for '{query}' in our wine business database."