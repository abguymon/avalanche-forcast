import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}

for i in range(54):
    if i == 0:
        URL = 'https://utahavalanchecenter.org/avalanches/salt-lake'
    else:
        URL = f'https://utahavalanchecenter.org/avalanches/salt-lake?page={i}'
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find_all('table')[0]

    n_columns = 0
    n_rows=0
    column_names = []

    # Find number of rows and columns
    # we also find the column titles if we can
    for row in table.find_all('tr'):
        
        # Determine the number of rows in the table
        td_tags = row.find_all('td')
        if len(td_tags) > 0:
            n_rows+=1
            if n_columns == 0:
                # Set the number of columns for our table
                n_columns = len(td_tags)
                
        # Handle column names if we find them
        th_tags = row.find_all('th') 
        if len(th_tags) > 0 and len(column_names) == 0:
            for th in th_tags:
                column_names.append(th.get_text())

    # Safeguard on Column Titles
    if len(column_names) > 0 and len(column_names) != n_columns:
        raise Exception("Column titles do not match the number of columns")

    columns = column_names if len(column_names) > 0 else range(0,n_columns)
    df = pd.DataFrame(columns = columns,
                        index= range(0,n_rows))
    row_marker = 0
    for row in table.find_all('tr'):
        column_marker = 0
        columns = row.find_all('td')
        for index, column in enumerate(columns):
            if "Avalanche: " in column.get_text():
                df.iat[row_marker,column_marker] = column.get_text().strip()[11:]
            elif index == 1:
                pass
            elif index == 4 or index == 5:
                df.iat[row_marker,column_marker] = column.get_text().strip()[:-1]
            else:
                df.iat[row_marker,column_marker] = column.get_text().strip()
            column_marker += 1
        if len(columns) > 0:
            row_marker += 1


    df.to_csv('out.csv', index=False, mode='a')