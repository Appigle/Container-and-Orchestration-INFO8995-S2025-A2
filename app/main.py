import os
import logging
from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

# Logging setup
LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'app.log')
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

# Flask app
app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('MYSQL_HOST', 'db'),
        user=os.environ.get('MYSQL_USER', 'user'),
        password=os.environ.get('MYSQL_PASSWORD', 'password'),
        database=os.environ.get('MYSQL_DATABASE', 'userdb')
    )


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    if not first_name or not last_name:
        logging.info(f"POST /user - Missing fields: {data}")
        return jsonify({'error': 'first_name and last_name required'}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user (first_name, last_name) VALUES (%s, %s)",
            (first_name, last_name)
        )
        conn.commit()
        user_id = cursor.lastrowid
        cursor.close()
        conn.close()
        response = {'id': user_id, 'first_name': first_name,
                    'last_name': last_name}
        logging.info(f"POST /user - Created: {response}")
        return jsonify(response), 201
    except Error as e:
        logging.error(f"POST /user - DB Error: {e}")
        return jsonify({'error': 'Database error'}), 500


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, first_name, last_name FROM user WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            logging.info(f"GET /user/{user_id} - Found: {user}")
            return jsonify(user), 200
        else:
            logging.info(f"GET /user/{user_id} - Not found")
            return jsonify({'error': 'User not found'}), 404
    except Error as e:
        logging.error(f"GET /user/{user_id} - DB Error: {e}")
        return jsonify({'error': 'Database error'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
