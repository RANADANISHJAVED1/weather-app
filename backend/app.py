from flask import Flask, jsonify, request
from flask_cors import CORS
from config import DEBUG, HOST, PORT, REGIONS, WEATHER_API_URL, WEATHER_API_KEY
from time_service import TimeService
from weather_service import WeatherService
import traceback

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=['http://localhost:*', 'http://127.0.0.1:*'])

# Initialize services
time_service = TimeService()
weather_service = WeatherService(WEATHER_API_KEY, WEATHER_API_URL)

# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify server is running"""
    return jsonify({
        'status': 'ok',
        'service': 'World Time & Weather API',
        'version': '1.0.0'
    }), 200


# ============================================================================
# TIME ENDPOINTS
# ============================================================================

@app.route('/api/time', methods=['GET'])
def get_time():
    """Get current time for all regions"""
    try:
        times = time_service.get_all_region_times(REGIONS)
        
        # Combine with region info
        result = []
        for region in REGIONS:
            region_name = region['name']
            time_data = times.get(region_name, {})
            
            result.append({
                'name': region_name,
                'timezone': region['timezone'],
                'country': region['country'],
                'flag': region['flag'],
                'time': time_data
            })
        
        return jsonify({
            'success': True,
            'timestamp': __import__('datetime').datetime.utcnow().isoformat(),
            'regions': result
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to fetch time data',
            'details': str(e)
        }), 500


# ============================================================================
# WEATHER ENDPOINTS
# ============================================================================

@app.route('/api/weather', methods=['GET'])
def get_weather():
    """Get current weather for all regions"""
    try:
        weather_data = weather_service.get_weather_for_regions(REGIONS)
        
        # Combine with region info
        result = []
        for region in REGIONS:
            region_name = region['name']
            weather = weather_data.get(region_name, {})
            
            # Check for errors in weather data
            if 'error' in weather:
                # Use demo data if API fails (for testing without API key)
                weather = get_demo_weather(region_name)
            
            result.append({
                'name': region_name,
                'country': region['country'],
                'flag': region['flag'],
                'latitude': region['latitude'],
                'longitude': region['longitude'],
                'weather': weather
            })
        
        return jsonify({
            'success': True,
            'timestamp': __import__('datetime').datetime.utcnow().isoformat(),
            'regions': result
        }), 200
    
    except Exception as e:
        print(f"Error in get_weather: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': 'Failed to fetch weather data',
            'details': str(e)
        }), 500


# ============================================================================
# COMBINED ENDPOINT
# ============================================================================

@app.route('/api/regions', methods=['GET'])
def get_regions():
    """Get time and weather for all regions (main endpoint)"""
    try:
        # Get time data
        times = time_service.get_all_region_times(REGIONS)
        
        # Get weather data
        weather_data = weather_service.get_weather_for_regions(REGIONS)
        
        # Combine all data
        result = []
        for region in REGIONS:
            region_name = region['name']
            time_info = times.get(region_name, {})
            weather_info = weather_data.get(region_name, {})
            
            # Use demo data if weather API fails
            if 'error' in weather_info:
                weather_info = get_demo_weather(region_name)
            
            result.append({
                'name': region_name,
                'timezone': region['timezone'],
                'country': region['country'],
                'flag': region['flag'],
                'latitude': region['latitude'],
                'longitude': region['longitude'],
                'time': time_info,
                'weather': weather_info
            })
        
        return jsonify({
            'success': True,
            'timestamp': __import__('datetime').datetime.utcnow().isoformat(),
            'regions': result
        }), 200
    
    except Exception as e:
        print(f"Error in get_regions: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': 'Failed to fetch regions data',
            'details': str(e)
        }), 500


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_demo_weather(city):
    """Return demo weather data for testing without API key"""
    demo_data = {
        'New York': {
            'temperature': 22,
            'feels_like': 20,
            'humidity': 65,
            'pressure': 1013,
            'wind_speed': 12,
            'description': 'Partly Cloudy',
            'detailed_description': 'partly cloudy',
            'icon': '02d',
            'clouds': 40,
            'visibility': 10000,
            'sunrise': 1234567890,
            'sunset': 1234567891,
            'country': 'US',
            'city': 'New York'
        },
        'London': {
            'temperature': 15,
            'feels_like': 13,
            'humidity': 70,
            'pressure': 1015,
            'wind_speed': 8,
            'description': 'Cloudy',
            'detailed_description': 'overcast clouds',
            'icon': '04d',
            'clouds': 90,
            'visibility': 10000,
            'sunrise': 1234567890,
            'sunset': 1234567891,
            'country': 'GB',
            'city': 'London'
        },
        'Tokyo': {
            'temperature': 25,
            'feels_like': 24,
            'humidity': 60,
            'pressure': 1010,
            'wind_speed': 5,
            'description': 'Clear',
            'detailed_description': 'clear sky',
            'icon': '01d',
            'clouds': 10,
            'visibility': 10000,
            'sunrise': 1234567890,
            'sunset': 1234567891,
            'country': 'JP',
            'city': 'Tokyo'
        },
        'Sydney': {
            'temperature': 28,
            'feels_like': 27,
            'humidity': 55,
            'pressure': 1012,
            'wind_speed': 15,
            'description': 'Sunny',
            'detailed_description': 'clear sky',
            'icon': '01d',
            'clouds': 5,
            'visibility': 10000,
            'sunrise': 1234567890,
            'sunset': 1234567891,
            'country': 'AU',
            'city': 'Sydney'
        },
        'Dubai': {
            'temperature': 38,
            'feels_like': 42,
            'humidity': 30,
            'pressure': 1008,
            'wind_speed': 20,
            'description': 'Hot & Sunny',
            'detailed_description': 'clear sky',
            'icon': '01d',
            'clouds': 2,
            'visibility': 10000,
            'sunrise': 1234567890,
            'sunset': 1234567891,
            'country': 'AE',
            'city': 'Dubai'
        },
        'São Paulo': {
            'temperature': 26,
            'feels_like': 25,
            'humidity': 68,
            'pressure': 1011,
            'wind_speed': 10,
            'description': 'Partly Cloudy',
            'detailed_description': 'partly cloudy',
            'icon': '02d',
            'clouds': 45,
            'visibility': 10000,
            'sunrise': 1234567890,
            'sunset': 1234567891,
            'country': 'BR',
            'city': 'São Paulo'
        }
    }
    return demo_data.get(city, demo_data['New York'])


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'message': 'The requested endpoint does not exist'
    }), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    print('╔════════════════════════════════════════════╗')
    print('║   World Time & Weather API (Python)       ║')
    print('╠════════════════════════════════════════════╣')
    print(f'║ Server: http://{HOST}:{PORT}')
    print('║ Endpoints:')
    print('║   - GET /health              (health check)')
    print('║   - GET /api/time            (all times)')
    print('║   - GET /api/weather         (all weather)')
    print('║   - GET /api/regions         (combined data)')
    print('╚════════════════════════════════════════════╝')
    print()
    
    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG
    )
