#!/usr/bin/env python3

import pandas as pd
import os
from datetime import datetime

def merge_weather_data():
    """Merge the new weather data with existing avalanche data"""
    
    print("🔄 Merging Weather Data with Existing Dataset")
    print("=" * 50)
    
    # Load the new weather data
    weather_file = 'avalanches_with_weather_20251015_100341.csv'
    if not os.path.exists(weather_file):
        print(f"❌ Error: {weather_file} not found!")
        return
    
    print(f"Loading weather data from {weather_file}...")
    weather_df = pd.read_csv(weather_file)
    print(f"Loaded {len(weather_df)} records with weather data")
    
    # Load existing dataset
    existing_file = '../allData.csv'
    if not os.path.exists(existing_file):
        print(f"❌ Error: {existing_file} not found!")
        return
    
    print(f"Loading existing dataset from {existing_file}...")
    existing_df = pd.read_csv(existing_file)
    print(f"Loaded {len(existing_df)} existing records")
    
    # Check what columns we have
    print(f"\nWeather data columns: {list(weather_df.columns)}")
    print(f"Existing data columns: {list(existing_df.columns)}")
    
    # Prepare the new weather data for merging
    # We need to match the format of the existing dataset
    weather_columns = {
        'Date': 'Date',
        'Area': 'Area', 
        'latitude': 'latitude',
        'longitude': 'longitude',
        'Dangerous': 'Dangerous',
        'Depth': 'Depth',
        'tempC': 'tempC',
        'maxtempC': 'maxtempC',
        'mintempC': 'mintempC',
        'precipMM': 'precipMM',
        'windspeedKmph': 'windspeedKmph',
        'winddirDegree': 'winddirDegree',
        'pressure': 'pressure',
        'cloudcover': 'cloudcover',
        'humidity': 'humidity',
        'visibility': 'visibility',
        'uvIndex': 'uvIndex',
        'sunHour': 'sunHour',
        'HeatIndexC': 'HeatIndexC',
        'WindChillC': 'WindChillC',
        'WindGustKmph': 'WindGustKmph',
        'DewPointC': 'DewPointC',
        'FeelsLikeC': 'FeelsLikeC'
    }
    
    # Select and rename columns from weather data
    weather_clean = weather_df[list(weather_columns.keys())].copy()
    weather_clean = weather_clean.rename(columns=weather_columns)
    
    # Add missing columns that exist in the original dataset
    missing_columns = set(existing_df.columns) - set(weather_clean.columns)
    print(f"\nAdding missing columns: {missing_columns}")
    
    for col in missing_columns:
        if col in ['Location', 'Region']:
            # These are categorical columns, we'll need to map them
            weather_clean[col] = weather_clean['Area']  # Use Area as Location/Region
        else:
            # For numeric columns, use default values
            weather_clean[col] = 0
    
    # Ensure all columns are in the same order as existing dataset
    weather_clean = weather_clean[existing_df.columns]
    
    # Combine the datasets
    print(f"\nCombining datasets...")
    combined_df = pd.concat([existing_df, weather_clean], ignore_index=True)
    
    # Remove duplicates based on Date, Area, latitude, longitude
    print(f"Removing duplicates...")
    initial_count = len(combined_df)
    combined_df = combined_df.drop_duplicates(subset=['Date', 'Area', 'latitude', 'longitude'], keep='first')
    final_count = len(combined_df)
    print(f"Removed {initial_count - final_count} duplicate records")
    
    # Save the combined dataset
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f'allData_updated_{timestamp}.csv'
    combined_df.to_csv(output_file, index=False)
    
    print(f"\n🎉 Data merge complete!")
    print(f"Combined dataset saved to: {output_file}")
    print(f"Total records: {len(combined_df)}")
    print(f"Original records: {len(existing_df)}")
    print(f"New records: {len(weather_clean)}")
    
    # Show sample of the combined data
    print(f"\nSample of combined data:")
    print(combined_df[['Date', 'Area', 'tempC', 'humidity', 'precipMM', 'windspeedKmph', 'Dangerous']].head(10))
    
    # Show statistics
    print(f"\nDataset Statistics:")
    print(f"Dangerous avalanches: {combined_df['Dangerous'].sum()}")
    print(f"Safe avalanches: {(~combined_df['Dangerous']).sum()}")
    print(f"Date range: {combined_df['Date'].min()} to {combined_df['Date'].max()}")
    
    return output_file

if __name__ == "__main__":
    merge_weather_data()