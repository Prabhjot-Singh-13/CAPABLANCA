import os
import pandas as pd
import chess.pgn

# Specify the correct path to the folder containing the PGN files
pgn_folder = '/Users/kalyani/Desktop/AIP/chesscom/top_20_women_players'

# Path to the output CSV file
output_csv_file = '/Users/kalyani/Desktop/AIP/chesscom/clock_data.csv'

# List to store the game data
games_data = []

# Loop through each subfolder and each file in the folder
for folder in os.listdir(pgn_folder):
    folder_path = os.path.join(pgn_folder, folder)
    
    if os.path.isdir(folder_path):
        for file in os.listdir(folder_path):
            # Check if the file is a PGN file
            if file.endswith('.pgn'):
                file_path = os.path.join(folder_path, file)
                
                # Open the PGN file
                with open(file_path, 'r') as infile:
                    while True:
                        # Parse the PGN file
                        game = chess.pgn.read_game(infile)
                        if game is None:
                            break
                        
                        # Extract relevant game information
                        game_info = {
                            'Event': game.headers.get('Event', ''),
                            'Date': game.headers.get('Date', ''),
                            'White': game.headers.get('White', ''),
                            'Black': game.headers.get('Black', ''),
                            'Result': game.headers.get('Result', ''),
                            'Round': game.headers.get('Round', ''),
                            'TimeControl': game.headers.get('TimeControl', ''),
                            'WhiteFideId': game.headers.get('WhiteFideId', ''),
                            'BlackFideId': game.headers.get('BlackFideId', ''),
                            'WhiteElo': game.headers.get('WhiteElo', ''),
                            'BlackElo': game.headers.get('BlackElo', ''),
                            'WhiteClock': game.headers.get('WhiteClock', ''),
                            'BlackClock': game.headers.get('BlackClock', ''),
                        }
                        
                        # To store the moves along with clock values
                        moves_with_clocks = []
                        
                        for move in game.mainline():
                            # Extract the move
                            move_san = move.san()
                            # Extract the clock time from the comment if it exists
                            clock_time = move.comment if move.comment else ''
                            # Combine move and clock time
                            moves_with_clocks.append(f"{move_san} {clock_time}")
                        
                        # Join all the moves with clocks into a single string
                        game_info['Moves'] = ' '.join(moves_with_clocks)
                        
                        # Append the game information to the list
                        games_data.append(game_info)

# Create a DataFrame from the game data
df = pd.DataFrame(games_data)

# Save the DataFrame to a CSV file
df.to_csv(output_csv_file, index=False)

print(f"All PGN files have been converted and saved to {output_csv_file}")