from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__)

# Your OpenAI API key
OPENAI_API_KEY = ''  # Replace with your actual OpenAI API key
OPENAI_API_URL = 'https://api.openai.com/v1/chat/completions'

def generate_response(prompt):
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-3.5-turbo',  # Use the desired model
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 100,
        'temperature': 0.7
    }

    response = requests.post(OPENAI_API_URL, headers=headers, json=data)
    response_json = response.json()

    # Check if the response contains an error
    if response.status_code != 200:
        return f"Error: {response_json.get('error', {}).get('message', 'Unknown error')}"

    return response_json['choices'][0]['message']['content']

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = generate_response(user_input)
    return jsonify({'response': response})

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')  # Serve the index.html file

if __name__ == '__main__':
    app.run(debug=True)