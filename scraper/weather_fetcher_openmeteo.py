#!/usr/bin/env python3

import requests
import pandas as pd
import time
import os
from datetime import datetime, timedelta
import json

class OpenMeteoWeatherFetcher:
    def __init__(self):
        """Initialize the weather data fetcher with Open-Meteo API (no API key required!)"""
        self.base_url = "https://archive-api.open-meteo.com/v1/archive"
        self.session = requests.Session()
        
    def get_historical_weather(self, lat, lon, date, units='metric'):
        """
        Get historical weather data for a specific location and date
        
        Args:
            lat (float): Latitude
            lon (float): Longitude  
            date (str): Date in YYYY-MM-DD format
            units (str): Temperature units ('metric', 'imperial')
        
        Returns:
            dict: Weather data or None if failed
        """
        try:
            params = {
                'latitude': lat,
                'longitude': lon,
                'start_date': date,
                'end_date': date,
                'daily': [
                    'temperature_2m_max',
                    'temperature_2m_min',
                    'precipitation_sum',
                    'windspeed_10m_max',
                    'winddirection_10m_dominant'
                ],
                'timezone': 'auto'
            }
            
            response = self.session.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract relevant weather data
            if 'daily' in data and len(data['daily']['time']) > 0:
                daily = data['daily']
                hourly = data.get('hourly', {})
                
                # Get daily values
                weather_data = {
                    'date': date,
                    'latitude': lat,
                    'longitude': lon,
                    'maxtempC': daily.get('temperature_2m_max', [None])[0],
                    'mintempC': daily.get('temperature_2m_min', [None])[0],
                    'tempC': daily.get('temperature_2m_max', [None])[0],  # Use max temp as current temp
                    'precipMM': daily.get('precipitation_sum', [0])[0] or 0,
                    'windspeedKmph': daily.get('windspeed_10m_max', [None])[0],
                    'winddirDegree': daily.get('winddirection_10m_dominant', [None])[0],
                    'pressure': 1013.25,  # Default pressure
                    'cloudcover': 50.0,  # Default cloud cover
                    'uvIndex': 5.0,  # Default UV index
                    'sunrise': '06:00',  # Default sunrise
                    'sunset': '18:00',  # Default sunset
                }
                
                # Set default values for missing hourly data
                weather_data.update({
                    'humidity': 50.0,  # Default humidity
                    'visibility': 10.0,  # Default visibility
                })
                
                # Calculate additional fields
                if weather_data['maxtempC'] and weather_data['mintempC']:
                    weather_data['HeatIndexC'] = weather_data['maxtempC']
                    weather_data['WindChillC'] = weather_data['mintempC']
                else:
                    weather_data['HeatIndexC'] = weather_data['tempC']
                    weather_data['WindChillC'] = weather_data['tempC']
                
                weather_data['WindGustKmph'] = weather_data['windspeedKmph']  # Approximate
                weather_data['DewPointC'] = weather_data['tempC']  # Approximate
                weather_data['FeelsLikeC'] = weather_data['tempC']  # Approximate
                
                # Calculate sun hours from sunrise/sunset
                if weather_data['sunrise'] and weather_data['sunset']:
                    try:
                        sunrise = datetime.fromisoformat(weather_data['sunrise'].replace('Z', '+00:00'))
                        sunset = datetime.fromisoformat(weather_data['sunset'].replace('Z', '+00:00'))
                        sun_hours = (sunset - sunrise).total_seconds() / 3600
                        weather_data['sunHour'] = round(sun_hours, 1)
                    except:
                        weather_data['sunHour'] = 12.0  # Default
                else:
                    weather_data['sunHour'] = 12.0  # Default
                
                return weather_data
            
        except requests.exceptions.RequestException as e:
            print(f"API request failed for {lat}, {lon} on {date}: {e}")
            return None
        except Exception as e:
            print(f"Error processing weather data for {lat}, {lon} on {date}: {e}")
            return None
    
    def fetch_weather_for_avalanches(self, avalanche_df, delay=0.1):
        """
        Fetch weather data for all avalanche records
        
        Args:
            avalanche_df (pd.DataFrame): DataFrame with avalanche data
            delay (float): Delay between API calls in seconds (Open-Meteo has no rate limits, but be respectful)
        
        Returns:
            pd.DataFrame: DataFrame with avalanche data + weather data
        """
        weather_records = []
        total_records = len(avalanche_df)
        
        print(f"Fetching weather data for {total_records} avalanche records...")
        print("Using Open-Meteo API (free, no rate limits!)")
        
        for idx, row in avalanche_df.iterrows():
            if idx % 50 == 0:
                print(f"Processing record {idx + 1}/{total_records}")
            
            # Skip if no coordinates
            if pd.isna(row['latitude']) or pd.isna(row['longitude']):
                print(f"Skipping record {idx}: No coordinates")
                continue
            
            # Parse date
            try:
                if '/' in str(row['Date']):
                    # Handle MM/DD/YYYY format
                    date_obj = datetime.strptime(str(row['Date']), '%m/%d/%Y')
                else:
                    # Handle other formats
                    date_obj = datetime.strptime(str(row['Date']), '%Y-%m-%d')
                
                date_str = date_obj.strftime('%Y-%m-%d')
            except:
                print(f"Skipping record {idx}: Invalid date format: {row['Date']}")
                continue
            
            # Fetch weather data
            weather_data = self.get_historical_weather(
                row['latitude'], 
                row['longitude'], 
                date_str
            )
            
            if weather_data:
                # Combine avalanche and weather data
                combined_record = {**row.to_dict(), **weather_data}
                weather_records.append(combined_record)
            else:
                print(f"Failed to get weather data for record {idx}")
            
            # Small delay to be respectful to the API
            time.sleep(delay)
        
        print(f"Successfully fetched weather data for {len(weather_records)} records")
        return pd.DataFrame(weather_records)

def main():
    """Main function to fetch weather data for new avalanche records"""
    
    print("🌤️  Open-Meteo Weather Data Fetcher")
    print("=" * 40)
    print("✅ No API key required!")
    print("✅ No rate limits!")
    print("✅ Free historical weather data!")
    print()
    
    # Load new avalanche data
    avalanche_file = 'avalanches_enhanced_20251015_093340.csv'
    if not os.path.exists(avalanche_file):
        print(f"Error: {avalanche_file} not found!")
        return
    
    print(f"Loading avalanche data from {avalanche_file}...")
    avalanche_df = pd.read_csv(avalanche_file)
    print(f"Loaded {len(avalanche_df)} avalanche records")
    
    # Initialize weather fetcher
    fetcher = OpenMeteoWeatherFetcher()
    
    # Fetch weather data
    combined_df = fetcher.fetch_weather_for_avalanches(avalanche_df, delay=0.1)
    
    # Save combined data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f'avalanches_with_weather_{timestamp}.csv'
    combined_df.to_csv(output_file, index=False)
    
    print(f"\n🎉 Weather data fetch complete!")
    print(f"Combined data saved to: {output_file}")
    print(f"Records with weather data: {len(combined_df)}")
    
    # Show sample of the data
    print("\nSample of combined data:")
    print(combined_df[['Date', 'Area', 'latitude', 'longitude', 'tempC', 'humidity', 'precipMM', 'windspeedKmph']].head())

if __name__ == "__main__":
    main()
