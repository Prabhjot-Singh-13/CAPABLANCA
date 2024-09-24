import requests
from bs4 import BeautifulSoup
import csv

# URL of the website
url = 'https://www.365chess.com/women-top-chess-players.php'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table containing the data
    table = soup.find('table', {'class': 'table'})

    # Initialize a list to hold player data
    players = []

    # Loop through table rows to extract player information
    for row in table.find_all('tr')[1:]:  # Skip the header row
        columns = row.find_all('td')
        if columns:
            rank = columns[0].text.strip()
            name = columns[1].find('a').text.strip()
            rating = columns[2].text.strip()
            title = columns[3].text.strip()
            fide_id = columns[4].text.strip()
            country = columns[5].text.strip()
            birth_year = columns[7].text.strip()

            players.append({
                'rank': rank,
                'name': name,
                'rating': rating,
                'title': title,
                'fide_id': fide_id,
                'country': country,
                'birth_year': birth_year
            })

    # Define CSV file name
    csv_file = 'top_women_chess_players.csv'

    # Write data to CSV
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=players[0].keys())
        writer.writeheader()  # Write the header
        writer.writerows(players)  # Write player data

    print(f'Data saved to {csv_file}')
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
