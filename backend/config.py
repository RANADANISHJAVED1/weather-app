import os
from dotenv import load_dotenv

load_dotenv()

# Flask Configuration
DEBUG = os.getenv('DEBUG', True)
HOST = '0.0.0.0'
PORT = 5000

# Weather API Configuration
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'demo_key')  # Get free key from openweathermap.org
WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'

# Regions Configuration with coordinates
REGIONS = [
    {
        'name': 'New York',
        'timezone': 'America/New_York',
        'latitude': 40.7128,
        'longitude': -74.0060,
        'country': 'USA',
        'flag': '🇺🇸'
    },
    {
        'name': 'London',
        'timezone': 'Europe/London',
        'latitude': 51.5074,
        'longitude': -0.1278,
        'country': 'UK',
        'flag': '🇬🇧'
    },
    {
        'name': 'Tokyo',
        'timezone': 'Asia/Tokyo',
        'latitude': 35.6762,
        'longitude': 139.6503,
        'country': 'Japan',
        'flag': '🇯🇵'
    },
    {
        'name': 'Sydney',
        'timezone': 'Australia/Sydney',
        'latitude': -33.8688,
        'longitude': 151.2093,
        'country': 'Australia',
        'flag': '🇦🇺'
    },
    {
        'name': 'Dubai',
        'timezone': 'Asia/Dubai',
        'latitude': 25.2048,
        'longitude': 55.2708,
        'country': 'UAE',
        'flag': '🇦🇪'
    },
    {
        'name': 'São Paulo',
        'timezone': 'America/Sao_Paulo',
        'latitude': -23.5505,
        'longitude': -46.6333,
        'country': 'Brazil',
        'flag': '🇧🇷'
    }
]

# CORS Configuration
CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:*']
