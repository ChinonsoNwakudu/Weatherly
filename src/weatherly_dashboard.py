import os
import json
import boto3
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WeatherDashboard:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.bucket_name = os.getenv('AWS_BUCKET_NAME')
        self.s3_client = boto3.client('s3')
        self.base_url = "http://api.openweathermap.org/data/2.5"

    def create_bucket_if_not_exists(self):
        """Create S3 bucket if it doesn't exist"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            print(f"Bucket {self.bucket_name} exists")
        except:
            print(f"Creating bucket {self.bucket_name}")
            try:
                self.s3_client.create_bucket(Bucket=self.bucket_name)
                print(f"Successfully created bucket {self.bucket_name}")
            except Exception as e:
                print(f"Error creating bucket: {e}")

    def fetch_weather(self, city):
        """Fetch current weather data from OpenWeather API"""
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "imperial"
        }
        
        try:
            response = requests.get(f"{self.base_url}/weather", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def fetch_forecast(self, city):
        """Fetch 5-day forecast from free OpenWeather API"""
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "imperial"
        }
        
        try:
            response = requests.get(f"{self.base_url}/forecast", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching forecast data: {e}")
            return None

    def save_to_s3(self, data, city, data_type="weather"):
        """Save weather or forecast data to S3 bucket"""
        if not data:
            return False
            
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        file_name = f"{data_type}-data/{city}-{timestamp}.json"
        
        try:
            data['timestamp'] = timestamp
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=json.dumps(data),
                ContentType='application/json'
            )
            print(f"Successfully saved {data_type} data for {city} to S3")
            return True
        except Exception as e:
            print(f"Error saving to S3: {e}")
            return False

def format_forecast_output(forecast_data):
    """Format 5-day forecast data for display"""
    if not forecast_data or 'list' not in forecast_data:
        return []
    
    # Group forecasts by day
    daily_forecasts = {}
    for forecast in forecast_data['list']:
        date = datetime.fromtimestamp(forecast['dt']).strftime('%Y-%m-%d')
        
        if date not in daily_forecasts:
            daily_forecasts[date] = {
                'temp_max': forecast['main']['temp_max'],
                'temp_min': forecast['main']['temp_min'],
                'descriptions': set([forecast['weather'][0]['description']]),
                'humidity_sum': forecast['main']['humidity'],
                'humidity_count': 1,
                'wind_speeds': [forecast['wind']['speed']]
            }
        else:
            daily_forecasts[date]['temp_max'] = max(daily_forecasts[date]['temp_max'], 
                                                  forecast['main']['temp_max'])
            daily_forecasts[date]['temp_min'] = min(daily_forecasts[date]['temp_min'], 
                                                  forecast['main']['temp_min'])
            daily_forecasts[date]['descriptions'].add(forecast['weather'][0]['description'])
            daily_forecasts[date]['humidity_sum'] += forecast['main']['humidity']
            daily_forecasts[date]['humidity_count'] += 1
            daily_forecasts[date]['wind_speeds'].append(forecast['wind']['speed'])

    # Format the daily forecasts
    formatted_forecast = []
    for date, data in daily_forecasts.items():
        forecast = {
            'date': date,
            'temp_max': round(data['temp_max']),
            'temp_min': round(data['temp_min']),
            'description': ', '.join(data['descriptions']),
            'humidity': round(data['humidity_sum'] / data['humidity_count']),
            'wind_speed': round(sum(data['wind_speeds']) / len(data['wind_speeds']), 1)
        }
        formatted_forecast.append(forecast)
    
    # Sort by date and return first 5 days
    return sorted(formatted_forecast, key=lambda x: x['date'])[:5]

def main():
    dashboard = WeatherDashboard()
    
    # Create bucket if needed
    dashboard.create_bucket_if_not_exists()
    
    cities = ["Lagos", "New York", "Doha"]

    # Option for users to add their city of choice
    print("Would you like to enter additional cities? (yes/no)")
    users_choice = input().strip().lower()
    
    if users_choice == "yes":
        print("Enter city names separated by commas (e.g., Tokyo, Berlin):")
        users_input = input().strip()
        additional_cities = [city.strip() for city in users_input.split(",") if city.strip()]
        cities.extend(additional_cities)
    
    for city in cities:
        print(f"\n=== Weather Report for {city} ===")
        
        # Fetch and display current weather
        print("\nCurrent Weather:")
        weather_data = dashboard.fetch_weather(city)
        if weather_data:
            temp = weather_data['main']['temp']
            feels_like = weather_data['main']['feels_like']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description']
            
            print(f"Temperature: {temp}°F")
            print(f"Feels like: {feels_like}°F")
            print(f"Humidity: {humidity}%")
            print(f"Conditions: {description}")
            
            # Save current weather to S3
            dashboard.save_to_s3(weather_data, city, "weather")
        else:
            print(f"Failed to fetch current weather data for {city}")
            continue
        
        # Fetch and display forecast
        print("\n5-Day Forecast:")
        forecast_data = dashboard.fetch_forecast(city)
        if forecast_data:
            formatted_forecast = format_forecast_output(forecast_data)
            for day in formatted_forecast:
                print(f"\n{day['date']}:")
                print(f"  High: {day['temp_max']}°F")
                print(f"  Low: {day['temp_min']}°F")
                print(f"  Conditions: {day['description']}")
                print(f"  Humidity: {day['humidity']}%")
                print(f"  Wind Speed: {day['wind_speed']} mph")
            
            # Save forecast to S3
            dashboard.save_to_s3(forecast_data, city, "forecast")
        else:
            print(f"Failed to fetch forecast data for {city}")

if __name__ == "__main__":
    main()