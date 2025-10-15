#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime

def scrape_avalanche_data():
    """Scrape avalanche data from Utah Avalalanche Center"""
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }
    
    all_data = []
    
    print("Starting avalanche data scraping...")
    
    for i in range(54):  # Scrape all pages
        if i == 0:
            URL = 'https://utahavalanchecenter.org/avalanches/salt-lake'
        else:
            URL = f'https://utahavalanchecenter.org/avalanches/salt-lake?page={i}'
        
        print(f"Scraping page {i+1}/54...")
        
        try:
            page = requests.get(URL, headers=headers, timeout=10)
            page.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching page {i+1}: {e}")
            continue
            
        soup = BeautifulSoup(page.content, 'html.parser')
        tables = soup.find_all('table')
        
        if not tables:
            print(f"No tables found on page {i+1}")
            continue
            
        table = tables[0]
        
        # Extract column names
        column_names = []
        header_row = table.find('tr')
        if header_row:
            th_tags = header_row.find_all('th')
            column_names = [th.get_text().strip() for th in th_tags]
        
        # Extract data rows
        rows = table.find_all('tr')[1:]  # Skip header row
        
        for row in rows:
            columns = row.find_all('td')
            if len(columns) > 0:
                row_data = []
                for index, column in enumerate(columns):
                    text = column.get_text().strip()
                    
                    # Clean up specific columns
                    if "Avalanche: " in text:
                        text = text[11:]  # Remove "Avalanche: " prefix
                    elif index == 4 or index == 5:
                        text = text[:-1] if text.endswith('°') else text  # Remove degree symbol
                    
                    row_data.append(text)
                
                if len(row_data) > 0:
                    all_data.append(row_data)
    
    print(f"Scraped {len(all_data)} avalanche records")
    
    # Create DataFrame
    if all_data:
        df = pd.DataFrame(all_data, columns=column_names)
        
        # Remove duplicates based on all columns
        initial_count = len(df)
        df = df.drop_duplicates()
        final_count = len(df)
        
        if initial_count != final_count:
            print(f"Removed {initial_count - final_count} duplicate records")
        
        # Save to CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f'avalanches_scraped_{timestamp}.csv'
        df.to_csv(output_file, index=False)
        
        print(f"Saved {final_count} unique records to {output_file}")
        return output_file
    else:
        print("No data scraped!")
        return None

if __name__ == "__main__":
    output_file = scrape_avalanche_data()
    if output_file:
        print(f"\nScraping complete! Output saved to: {output_file}")
    else:
        print("\nScraping failed!")
