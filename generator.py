# generator.py
from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    model_name = data.get('model_name')
    viewer_id = data.get('viewerid')
    random_number = random.randint(1, 100)  # Generate a random number
    return jsonify({
        "reason": model_name,
        "result": random_number
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
