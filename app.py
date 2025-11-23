# Class for connecting to backend
from flask import Flask, request, jsonify
from flask_cors import CORS
from predict_helps_hurts import helps_hurts_classifier

app = Flask(__name__)
CORS(app)

@app.route('/ping') # dummy test
def ping():
    return "pong"

@app.route('/process', methods=['POST'])
def process_data():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400

    # Validate required fields
    missing_fields = []

    if 'name' not in data:
        missing_fields.append('name')

    if 'is_common' not in data:
        missing_fields.append('is_common')

    if missing_fields:
        return jsonify({'error': f"Missing required fields: {', '.join(missing_fields)}"}), 400

    name = data['name']
    is_common = data['is_common']

    # Call backend logic
    result = classifier.predict_from_name(name, is_common=is_common)
    json = result.to_json(orient='index')
    print(f'received target word: {name}, giving result')

    return json, 200 



if __name__ == '__main__':
    classifier = helps_hurts_classifier()
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
