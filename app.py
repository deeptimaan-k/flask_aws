from flask import Flask, jsonify, render_template
import mysql.connector
from mysql.connector import Error
from config import db_config

app = Flask(__name__)

def get_db_connection():
    """Establish a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/')
def home():
    """Render a home page."""
    return render_template('index.html')

@app.route('/fetch-data', methods=['GET'])
def fetch_data():
    """Fetch data from the MySQL database."""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users")  # Change 'users' to your table name
            rows = cursor.fetchall()
            return jsonify(rows)
        finally:
            cursor.close()
            connection.close()
    else:
        return jsonify({"error": "Failed to connect to the database."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
