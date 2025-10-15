#!/usr/bin/env python3

import pandas as pd
import csv
from datetime import datetime

def merge_new_avalanche_data():
    """Merge new avalanche data with existing coordinate data"""
    
    print("Loading existing coordinate mappings...")
    
    # Load existing coordinate data from the original dataset
    existing_data = pd.read_csv('../allData.csv')
    
    # Create a mapping of Area names to coordinates
    coord_mapping = {}
    for _, row in existing_data.iterrows():
        if pd.notna(row['Area']) and pd.notna(row['longitude']) and pd.notna(row['latitude']):
            coord_mapping[row['Area']] = {
                'longitude': row['longitude'],
                'latitude': row['latitude'],
                'altitude': row['altitude'] if pd.notna(row['altitude']) else 0.0
            }
    
    print(f"Found coordinate mappings for {len(coord_mapping)} locations")
    
    # Load new avalanche data
    print("Loading new avalanche data...")
    new_data = pd.read_csv('avalanches_scraped_20251015_092953.csv')
    
    print(f"Loaded {len(new_data)} new avalanche records")
    
    # Process new data and add coordinates
    enhanced_records = []
    
    for _, row in new_data.iterrows():
        location = row.iloc[1] if len(row) > 1 else None  # Region column
        
        if location and location in coord_mapping:
            coords = coord_mapping[location]
            enhanced_records.append({
                'Date': row.iloc[0],  # Date
                'Area': location,
                'Region': location,
                'Trigger': row.iloc[3] if len(row) > 3 else None,  # Trigger
                'Depth': row.iloc[4] if len(row) > 4 else None,  # Depth
                'Width': row.iloc[5] if len(row) > 5 else None,  # Width
                'longitude': coords['longitude'],
                'latitude': coords['latitude'],
                'altitude': coords['altitude'],
                'Dangerous': True  # All scraped avalanches are dangerous by definition
            })
        else:
            print(f"No coordinates found for location: {location}")
    
    print(f"Enhanced {len(enhanced_records)} records with coordinates")
    
    # Save enhanced data
    if enhanced_records:
        enhanced_df = pd.DataFrame(enhanced_records)
        output_file = f'avalanches_enhanced_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        enhanced_df.to_csv(output_file, index=False)
        print(f"Saved enhanced data to {output_file}")
        
        # Show sample of new data
        print("\nSample of new avalanche data:")
        print(enhanced_df.head())
        
        return output_file
    else:
        print("No enhanced records created")
        return None

if __name__ == "__main__":
    output_file = merge_new_avalanche_data()
    if output_file:
        print(f"\nData enhancement complete! Output: {output_file}")
    else:
        print("\nData enhancement failed!")
