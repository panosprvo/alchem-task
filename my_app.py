from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime

from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/status": {"origins": "http://localhost:4200"}})
DATABASE = 'events.db'


def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                object_id TEXT NOT NULL,
                status TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')


@app.route('/status', methods=['GET'])
def get_status():
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM events ORDER BY timestamp DESC')
        rows = cur.fetchall()
    statuses = [{'object_id': row[1], 'status': row[2], 'timestamp': row[3]} for row in rows]
    return jsonify(statuses)


@app.route('/simulate', methods=['POST'])
def simulate_event():
    object_id = request.json.get('object_id')
    status = request.json.get('status')
    timestamp = datetime.now().isoformat()

    with sqlite3.connect(DATABASE) as conn:
        conn.execute('INSERT INTO events (object_id, status, timestamp) VALUES (?, ?, ?)',
                     (object_id, status, timestamp))
    return jsonify({'message': 'Event simulated successfully'})


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
