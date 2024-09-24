import requests
import csv
import re

# List of top players with their details
top_players = [
    {"rank": 1, "name": "Magnus Carlsen", "rating": 2832, "title": "GM", "fide_id": "1503014", "country": "Norway"},
    {"rank": 2, "name": "Hikaru Nakamura", "rating": 2802, "title": "GM", "fide_id": "2016192", "country": "United States"},
    {"rank": 3, "name": "Fabiano Caruana", "rating": 2798, "title": "GM", "fide_id": "2020009", "country": "United States"},
    {"rank": 4, "name": "Erigaisi Arjun", "rating": 2778, "title": "GM", "fide_id": "35009192", "country": "India"},
    {"rank": 5, "name": "Alireza Firouzja", "rating": 2767, "title": "GM", "fide_id": "12573981", "country": "France"},
    {"rank": 6, "name": "Nodirbek Abdusattorov", "rating": 2766, "title": "GM", "fide_id": "14204118", "country": "Uzbekistan"},
    {"rank": 7, "name": "Gukesh D", "rating": 2764, "title": "GM", "fide_id": "46616543", "country": "India"},
    {"rank": 8, "name": "Yi Wei", "rating": 2762, "title": "GM", "fide_id": "8603405", "country": "China"},
    {"rank": 9, "name": "Ian Nepomniachtchi", "rating": 2755, "title": "GM", "fide_id": "4168119", "country": "Russian Federation"},
    {"rank": 10, "name": "Wesley So", "rating": 2752, "title": "GM", "fide_id": "5202213", "country": "United States"},
    {"rank": 11, "name": "Viswanathan Anand", "rating": 2751, "title": "GM", "fide_id": "5000017", "country": "India"},
    {"rank": 12, "name": "Praggnanandhaa R", "rating": 2750, "title": "GM", "fide_id": "25059530", "country": "India"},
    {"rank": 13, "name": "Leinier Dominguez Perez", "rating": 2748, "title": "GM", "fide_id": "3503240", "country": "United States"},
    {"rank": 14, "name": "Quang Liem Le", "rating": 2741, "title": "GM", "fide_id": "12401137", "country": "Viet Nam"},
    {"rank": 15, "name": "Liren Ding", "rating": 2736, "title": "GM", "fide_id": "8603677", "country": "China"},
    {"rank": 16, "name": "Shakhriyar Mamedyarov", "rating": 2733, "title": "GM", "fide_id": "13401319", "country": "Azerbaijan"},
    {"rank": 17, "name": "Hans Moke Niemann", "rating": 2733, "title": "GM", "fide_id": "2093596", "country": "United States"},
    {"rank": 18, "name": "Jan Krzysztof Duda", "rating": 2732, "title": "GM", "fide_id": "1170546", "country": "Poland"},
    {"rank": 19, "name": "Maxime Vachier Lagrave", "rating": 2731, "title": "GM", "fide_id": "623539", "country": "France"},
    {"rank": 20, "name": "Vincent Keymer", "rating": 2730, "title": "GM", "fide_id": "12940690", "country": "Germany"},
    {"rank": 21, "name": "Levon Aronian", "rating": 2729, "title": "GM", "fide_id": "13300474", "country": "United States"},
    {"rank": 22, "name": "Anish Giri", "rating": 2724, "title": "GM", "fide_id": "24116068", "country": "Netherlands"},
    {"rank": 23, "name": "Parham Maghsoodloo", "rating": 2723, "title": "GM", "fide_id": "12539929", "country": "Iran"},
    {"rank": 24, "name": "Santosh Gujrathi Vidit", "rating": 2720, "title": "GM", "fide_id": "5029465", "country": "India"},
    {"rank": 25, "name": "Richard Rapport", "rating": 2715, "title": "GM", "fide_id": "738590", "country": "Hungary"},
    {"rank": 26, "name": "M. Amin Tabatabaei", "rating": 2714, "title": "GM", "fide_id": "12521213", "country": "Iran"},
    {"rank": 27, "name": "Alexey Sarana", "rating": 2713, "title": "GM", "fide_id": "24133795", "country": "Serbia"},
    {"rank": 28, "name": "Hao Wang", "rating": 2703, "title": "GM", "fide_id": "8602883", "country": "China"},
    {"rank": 29, "name": "Yangyi Yu", "rating": 2703, "title": "GM", "fide_id": "8603820", "country": "China"},
    {"rank": 30, "name": "Vladislav Artemiev", "rating": 2701, "title": "GM", "fide_id": "24101605", "country": "Russian Federation"},
    {"rank": 31, "name": "Teimour Radjabov", "rating": 2700, "title": "GM", "fide_id": "13400924", "country": "Azerbaijan"},
    {"rank": 32, "name": "Ray Robson", "rating": 2700, "title": "GM", "fide_id": "2023970", "country": "United States"},
    {"rank": 33, "name": "Chithambaram VR Aravindh", "rating": 2698, "title": "GM", "fide_id": "5072786", "country": "India"},
    {"rank": 34, "name": "Peter Svidler", "rating": 2698, "title": "GM", "fide_id": "4102142", "country": "FIDE"},
    {"rank": 35, "name": "Jorden Van Foreest", "rating": 2696, "title": "GM", "fide_id": "1039784", "country": "Netherlands"},
    {"rank": 36, "name": "Xiangzhi Bu", "rating": 2693, "title": "GM", "fide_id": "8601445", "country": "China"},
    {"rank": 37, "name": "Daniil Dubov", "rating": 2693, "title": "GM", "fide_id": "24126055", "country": "Russian Federation"},
    {"rank": 38, "name": "Vladimir Fedoseev", "rating": 2692, "title": "GM", "fide_id": "24130737", "country": "Slovenia"},
    {"rank": 39, "name": "Alexander Grischuk", "rating": 2689, "title": "GM", "fide_id": "4126025", "country": "Russian Federation"},
    {"rank": 40, "name": "Samuel Sevian", "rating": 2689, "title": "GM", "fide_id": "2040506", "country": "United States"},
]

def get_player_games(username):
    url = f'https://lichess.org/api/games/user/{username}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.text  # Get raw PGN text
    else:
        print(f"Failed to retrieve games for {username}. Status code: {response.status_code}")
        return None

def parse_pgn(games):
    game_entries = []
    games_split = games.strip().split('\n\n')  # Split games by double newlines