import requests
from datetime import datetime

class WeatherService:
    """Service to fetch weather data from OpenWeatherMap API"""
    
    def __init__(self, api_key, base_url):
        """
        Initialize weather service
        
        Args:
            api_key: OpenWeatherMap API key
            base_url: OpenWeatherMap API base URL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.cache = {}
        self.cache_duration = 600  # Cache for 10 minutes
    
    def get_weather(self, latitude, longitude, region_name=None):
        """
        Fetch weather data for coordinates
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            region_name: Optional region name for caching
            
        Returns:
            dict with weather information
        """
        try:
            # Check cache first
            cache_key = f"{latitude},{longitude}"
            if cache_key in self.cache:
                cached_data, timestamp = self.cache[cache_key]
                if (datetime.now() - timestamp).seconds < self.cache_duration:
                    return cached_data
            
            # Make API request
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': self.api_key,
                'units': 'metric'  # Use Celsius
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Parse weather data
            weather_data = {
                'temperature': round(data['main']['temp'], 1),
                'feels_like': round(data['main']['feels_like'], 1),
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': round(data['wind']['speed'], 1),
                'description': data['weather'][0]['main'],
                'detailed_description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'clouds': data['clouds'].get('all', 0),
                'visibility': data.get('visibility', 'N/A'),
                'sunrise': data['sys']['sunrise'],
                'sunset': data['sys']['sunset'],
                'country': data['sys']['country'],
                'city': data['name'],
                'timestamp': datetime.now().isoformat()
            }
            
            # Cache the result
            self.cache[cache_key] = (weather_data, datetime.now())
            
            return weather_data
            
        except requests.exceptions.Timeout:
            return {
                'error': 'API request timeout',
                'message': 'Weather service took too long to respond'
            }
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                return {
                    'error': 'Invalid API key',
                    'message': 'Please set a valid OpenWeatherMap API key'
                }
            return {
                'error': 'API error',
                'message': str(e)
            }
        except Exception as e:
            return {
                'error': 'Weather fetch failed',
                'message': str(e)
            }
    
    def get_weather_for_regions(self, regions):
        """
        Fetch weather for multiple regions
        
        Args:
            regions: List of region dicts with coordinates
            
        Returns:
            dict with weather for each region
        """
        result = {}
        for region in regions:
            name = region.get('name')
            lat = region.get('latitude')
            lon = region.get('longitude')
            
            result[name] = self.get_weather(lat, lon, name)
        
        return result
    
    def clear_cache(self):
        """Clear the weather cache"""
        self.cache = {}
    
    def get_weather_icon_emoji(self, icon_code):
        """
        Convert OpenWeatherMap icon code to emoji
        
        Args:
            icon_code: Icon code from API
            
        Returns:
            Emoji representation
        """
        icon_map = {
            '01d': '☀️',   # Clear sky day
            '01n': '🌙',   # Clear sky night
            '02d': '⛅',   # Few clouds day
            '02n': '🌤️',   # Few clouds night
            '03d': '☁️',   # Scattered clouds
            '03n': '☁️',   # Scattered clouds
            '04d': '☁️',   # Broken clouds
            '04n': '☁️',   # Broken clouds
            '09d': '🌧️',   # Shower rain
            '09n': '🌧️',   # Shower rain
            '10d': '🌦️',   # Rain day
            '10n': '🌧️',   # Rain night
            '11d': '⛈️',   # Thunderstorm
            '11n': '⛈️',   # Thunderstorm
            '13d': '❄️',   # Snow
            '13n': '❄️',   # Snow
            '50d': '🌫️',   # Mist
            '50n': '🌫️',   # Mist
        }
        return icon_map.get(icon_code, '🌤️')
