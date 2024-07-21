from flask import Flask, request, jsonify, render_template, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD')
    )
    return conn

# Create table if it doesn't exist
def create_table_if_not_exists():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS greetings (
            id SERIAL PRIMARY KEY,
            message TEXT NOT NULL
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

# Homepage route
@app.route('/')
def home():
    return render_template('index.html')

# Retrieve all messages and render them in HTML
@app.route('/messages', methods=['GET'])
def get_messages():
    try:
        create_table_if_not_exists()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM greetings;')
        messages = cur.fetchall()
        cur.close()
        conn.close()

        # Format the results as a list of dictionaries
        result = [{"id": row[0], "message": row[1]} for row in messages]
        return render_template('messages.html', messages=result)
    except Exception as e:
        return jsonify({"error": "An error occurred: " + str(e)}), 500

# Add a new message
@app.route('/messages', methods=['POST'])
def add_message():
    new_message = request.json.get('message')

    if not new_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        create_table_if_not_exists()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO greetings (message) VALUES (%s) RETURNING id;', (new_message,))
        message_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"id": message_id, "message": new_message}), 201
    except Exception as e:
        return jsonify({"error": "An error occurred: " + str(e)}), 500

# Route to render the update form
@app.route('/update/<int:message_id>', methods=['GET'])
def update_message_form(message_id):
    try:
        create_table_if_not_exists()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM greetings WHERE id = %s;', (message_id,))
        message = cur.fetchone()
        cur.close()
        conn.close()

        if message:
            message_data = {"id": message[0], "message": message[1]}
            return render_template('update_message.html', message=message_data)
        else:
            return jsonify({"error": "Message not found"}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred: " + str(e)}), 500

# Update an existing message
@app.route('/messages/<int:message_id>', methods=['PUT'])
def update_message(message_id):
    new_message = request.json.get('message')

    if not new_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        create_table_if_not_exists()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('UPDATE greetings SET message = %s WHERE id = %s;', (new_message, message_id))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"id": message_id, "message": new_message}), 200
    except Exception as e:
        return jsonify({"error": "An error occurred: " + str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
