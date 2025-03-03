# backend/app.py
from flask import Flask, jsonify

app = Flask(__name__)

# Маршрут /api/data, который возвращает список данных в формате JSON
@app.route('/api/data', methods=['GET'])
def get_data():
    data = [
        {"id": 1, "name": "Item 1", "description": "This is the first item."},
        {"id": 2, "name": "Item 2", "description": "This is the second item."},
        {"id": 3, "name": "Item 3", "description": "This is the third item."}
    ]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
