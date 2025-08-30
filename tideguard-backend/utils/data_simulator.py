import random
import time
import math

class DataSimulator:
    def __init__(self):
        self.base_wind_speed = 30  # Base wind speed in km/h
        self.base_wave_height = 1.5  # Base wave height in meters
        self.time_offset = time.time()
        
    def generate_data(self):
        """Generate simulated weather and tide data"""
        current_time = time.time() - self.time_offset
        
        # Generate wind speed with realistic patterns
        wind_speed = self._generate_wind_speed(current_time)
        
        # Generate wave height (correlated with wind speed)
        wave_height = self._generate_wave_height(wind_speed, current_time)
        
        # Add some random weather conditions
        weather_conditions = self._generate_weather_conditions(wind_speed)
        
        return {
            'timestamp': int(time.time()),
            'wind_speed': round(wind_speed, 1),
            'wave_height': round(wave_height, 1),
            'weather_condition': weather_conditions,
            'temperature': round(random.uniform(15, 25), 1),
            'humidity': round(random.uniform(60, 90), 1),
            'pressure': round(random.uniform(1010, 1020), 1)
        }
    
    def _generate_wind_speed(self, time_offset):
        """Generate realistic wind speed patterns"""
        # Base wind with daily cycle (stronger during day)
        daily_cycle = math.sin(time_offset / 86400 * 2 * math.pi) * 10
        
        # Add some gusty behavior
        gust_factor = random.uniform(0.8, 1.5)
        
        # Add seasonal variation
        seasonal_factor = 1 + math.sin(time_offset / 31536000 * 2 * math.pi) * 0.3
        
        # Random noise
        noise = random.uniform(-5, 5)
        
        wind_speed = (self.base_wind_speed + daily_cycle + noise) * gust_factor * seasonal_factor
        
        # Ensure wind speed is positive and realistic
        return max(0, min(120, wind_speed))
    
    def _generate_wave_height(self, wind_speed, time_offset):
        """Generate wave height based on wind speed and tide patterns"""
        # Wave height correlates with wind speed (Beaufort scale approximation)
        wind_wave_factor = wind_speed / 20  # Rough correlation
        
        # Add tidal variation (12.4 hour cycle)
        tidal_cycle = math.sin(time_offset / 44640 * 2 * math.pi) * 0.5
        
        # Add some swell from distant storms
        swell_factor = random.uniform(0.5, 1.5)
        
        wave_height = (self.base_wave_height + wind_wave_factor + tidal_cycle) * swell_factor
        
        # Ensure wave height is positive and realistic
        return max(0.1, min(8, wave_height))
    
    def _generate_weather_conditions(self, wind_speed=None):
        """Generate weather conditions based on wind and other factors"""
        conditions = [
            'Clear', 'Partly Cloudy', 'Cloudy', 'Light Rain', 
            'Heavy Rain', 'Stormy', 'Foggy', 'Misty'
        ]
        
        # If no wind_speed provided, use a default value
        if wind_speed is None:
            wind_speed = random.uniform(20, 60)
        
        # Weight conditions based on wind speed
        if wind_speed > 80:
            return 'Stormy'
        elif wind_speed > 50:
            return random.choice(['Heavy Rain', 'Stormy', 'Cloudy'])
        elif wind_speed > 30:
            return random.choice(['Light Rain', 'Cloudy', 'Partly Cloudy'])
        else:
            return random.choice(['Clear', 'Partly Cloudy', 'Cloudy', 'Foggy'])
