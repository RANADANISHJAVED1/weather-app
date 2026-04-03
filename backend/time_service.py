from datetime import datetime
import pytz

class TimeService:
    """Service to handle timezone and time conversions"""
    
    @staticmethod
    def get_region_time(timezone_str):
        """
        Get current time for a specific timezone
        
        Args:
            timezone_str: Timezone string (e.g., 'America/New_York')
            
        Returns:
            dict with formatted time and datetime object
        """
        try:
            tz = pytz.timezone(timezone_str)
            current_time = datetime.now(tz)
            
            return {
                'formatted': current_time.strftime('%H:%M:%S'),
                'date': current_time.strftime('%Y-%m-%d'),
                'datetime': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                'day': current_time.strftime('%A'),
                'hour': current_time.hour,
                'minute': current_time.minute,
                'second': current_time.second,
                'offset': current_time.strftime('%z')
            }
        except Exception as e:
            return {
                'error': f'Invalid timezone: {timezone_str}',
                'message': str(e)
            }
    
    @staticmethod
    def get_all_region_times(regions):
        """
        Get time for multiple regions
        
        Args:
            regions: List of region dicts with timezone info
            
        Returns:
            dict with times for each region
        """
        result = {}
        for region in regions:
            timezone = region.get('timezone')
            region_name = region.get('name')
            result[region_name] = TimeService.get_region_time(timezone)
        
        return result
    
    @staticmethod
    def get_time_difference(tz1, tz2):
        """
        Calculate time difference between two timezones
        
        Args:
            tz1: First timezone string
            tz2: Second timezone string
            
        Returns:
            Time difference in hours
        """
        try:
            timezone1 = pytz.timezone(tz1)
            timezone2 = pytz.timezone(tz2)
            
            now_utc = datetime.now(pytz.UTC)
            time1 = now_utc.astimezone(timezone1)
            time2 = now_utc.astimezone(timezone2)
            
            diff = (time2.hour - time1.hour) % 24
            return diff
        except Exception as e:
            return None
