import streamlit as st
import chess
import chess.svg
import chess.engine
import pandas as pd
import joblib
import numpy as np
from PIL import Image
from io import BytesIO

# Initialize the Stockfish engine
engine_path = r"C:\Users\hiddensardar\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"
engine = chess.engine.SimpleEngine.popen_uci(engine_path)

# Load your chess player dataset
df = pd.read_csv(r"C:\Users\hiddensardar\Downloads\ches.csv")

# Load your trained model
model = joblib.load(r"C:\Users\hiddensardar\Downloads\chess_model.pkl")  # Replace with your actual model path

# Function to select a player and get their games
def select_player(player_name):
    player_games = df[(df['White'] == player_name) | (df['Black'] == player_name)]
    if player_games.empty:
        st.write(f"No games found for player: {player_name}")
        return None
    return player_games

# Function to get Stockfish's top moves for a given board position
def get_stockfish_top_moves(board, depth=10):
    result = engine.analyse(board, chess.engine.Limit(depth=depth))
    top_moves = [move.uci() for move in result["pv"][:10]]
    return top_moves

# Function to preprocess the board into a feature vector
def preprocess_board(board):
    piece_mapping = {
        'P': 1, 'N': 2, 'B': 3, 'R': 4, 'Q': 5, 'K': 6,
        'p': -1, 'n': -2, 'b': -3, 'r': -4, 'q': -5, 'k': -6,
        '.': 0
    }
    board_matrix = []
    for row in range(8):
        board_matrix.append([piece_mapping[board.piece_at(chess.square(col, row))] for col in range(8)])
    return np.array(board_matrix).flatten()  # Flatten the board matrix for model input

# Function to get the model's predicted move
def get_model_prediction(board):
    board_features = preprocess_board(board)
    board_features_array = board_features.reshape(1, -1)  # Reshape for a single sample
    predicted_move = model.predict(board_features_array)
    return predicted_move[0]  # Assuming your model returns a valid UCI move

# Function to convert the chess board to an image using cairosvg
def board_to_image(board):
    board_svg = chess.svg.board(board)
    png_data = cairosvg.svg2png(bytestring=board_svg.encode('utf-8'))
    image = Image.open(BytesIO(png_data))
    return image

# Streamlit App Interface
st.title("Chess Game Player & Model Visualization")

# Select a player from the dataset
player_name = st.text_input("Enter the player's name (e.g., 'Donchenko, Alexander'):")

if player_name:
    # Fetch and display games for the selected player
    player_games = select_player(player_name)
    if player_games is not None:
        st.write(f"Games found for player: {player_name}")
        st.dataframe(player_games)

# Play the game with user interaction
if st.button("Start New Game"):
    board = chess.Board()
    while not board.is_game_over():
        st.write("## Current Board Position")
        st.image(board_to_image(board), use_column_width=True)

        # Get user's move input
        user_move = st.text_input("Enter your move (in UCI format, e.g., 'e2e4'):", key="user_move")
        if user_move:
            try:
                board.push_uci(user_move)
            except ValueError:
                st.write("Invalid move. Please enter a valid move.")
                continue

            # Get Stockfish's top moves and model prediction
            stockfish_moves = get_stockfish_top_moves(board)
            model_prediction = get_model_prediction(board)

            st.write(f"### Model Prediction: {model_prediction}")
            st.write(f"### Stockfish's Top Moves: {stockfish_moves}")

            # Check if the model's prediction is in Stockfish's top moves
            if model_prediction in stockfish_moves:
                st.write(f"Model prediction {model_prediction} is in Stockfish's top moves.")
                board.push_uci(model_prediction)
            else:
                st.write(f"Model prediction {model_prediction} is NOT in Stockfish's top moves.")
                st.write("Showing Stockfish's top 15 moves...")
                additional_moves = get_stockfish_top_moves(board, depth=15)
                st.write(f"### Stockfish's Next Best Moves: {additional_moves}")
                board.push_uci(additional_moves[0])  # Pick the first one as a fallback

            # Display the board after AI's move
            st.write("### Board after AI's Move:")
            st.image(board_to_image(board), use_column_width=True)

            # Check if the game is over
            if board.is_game_over():
                st.write("### Game Over!")
                st.write(f"Game Result: {board.result()}")
                break

# Close the Stockfish engine when done
engine.quit()
