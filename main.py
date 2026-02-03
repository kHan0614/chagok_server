# server.py
from flask import Flask, request, jsonify
import mysql.connector
from werkzeug.security import check_password_hash

app = Flask(__name__)

db = mysql.connector.connect(
    host='127.0.0.1',
    user='app_user',
    password='test_test',
    database='chagok_db',
    port=3306
)


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    pw = data.get('password')

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()
    cursor.close()

    if user and check_password_hash(user['password'], pw):
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

