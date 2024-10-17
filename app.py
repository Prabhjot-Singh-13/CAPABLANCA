from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Load your model
with open('chess_model.pkl', 'rb') as model_file:
    model = joblib.load(model_file)

@app.route('/')
def home():
    return "Hello, Flask is running!"

@app.route('/predict', methods=['POST'])
def predict():
    # Get the JSON data from the request
    data = request.json
    board_state = data.get('board_state')  # assuming the board state is sent in the request
    
    # Validate input
    if not board_state:
        return jsonify({'error': 'No board state provided'}), 400

    # Use the model to predict the next move
    predicted_move = model.predict(board_state)  # Adjust this based on your model's API
    
    return jsonify({'predicted_move': predicted_move})

if __name__ == '__main__':
    app.run(port=5000)  # Ensure this matches the ngrok port
