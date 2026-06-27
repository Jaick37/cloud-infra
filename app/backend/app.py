from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os
import time

app = Flask(__name__)
CORS(app)

def get_db_connection():
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host="db",
                database="tododb",
                user="postgres",
                password="secret"
            )
            return conn
        except psycopg2.OperationalError:
            retries -= 1
            time.sleep(2)
    raise Exception("Could not connect to database")

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            task TEXT NOT NULL,
            done BOOLEAN DEFAULT FALSE
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/todos', methods=['GET'])
def get_todos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, task, done FROM todos')
    todos = [{'id': r[0], 'task': r[1], 'done': r[2]} for r in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO todos (task) VALUES (%s)', (data['task'],))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Todo added'}), 201

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
