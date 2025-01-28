from flask import Flask, jsonify, render_template, request
import mysql.connector
from mysql.connector import Error
from config import db_config

app = Flask(__name__)

def get_db_connection():
    """Establish a connection to the RDS database."""
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/')
def home():
    """Display the home page with user list."""
    return render_template('index.html')

@app.route('/users', methods=['GET'])
def get_users():
    """Fetch all users from the database."""
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return jsonify(users)
    
    except Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

@app.route('/add_user', methods=['POST'])
def add_user():
    """Add a new user to the database."""
    connection = None
    cursor = None
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        
        if not username or not email:
            return jsonify({"error": "Username and email are required"}), 400
        
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = connection.cursor()
        query = "INSERT INTO users (username, email) VALUES (%s, %s)"
        cursor.execute(query, (username, email))
        connection.commit()
        
        return jsonify({"message": "User added successfully", "id": cursor.lastrowid})
    
    except Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
