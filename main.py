# server.py
from flask import Flask, request, jsonify
import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash

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
    cursor.execute("SELECT * FROM user_list WHERE email=%s", (email,))
    user = cursor.fetchone()
    cursor.close()

    if user and check_password_hash(user['password'], pw):
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user_name = data.get('user_name')
    nickname = data.get('nickname')  # <-- 추가

    hashed_pw = generate_password_hash(password)

    db_conn = mysql.connector.connect(
        host='127.0.0.1',
        user='app_user',
        password='test_test',
        database='chagok_db'
    )
    cursor = db_conn.cursor(dictionary=True)

    # 이메일 중복 체크
    cursor.execute("SELECT id FROM user_list WHERE email=%s", (email,))
    if cursor.fetchone():
        cursor.close()
        db_conn.close()
        return jsonify(success=False, message='이미 존재하는 이메일')

    # 닉네임 추가 저장
    cursor.execute(
        "INSERT INTO user_list (email, password, user_name, nickname) VALUES (%s, %s, %s, %s)",
        (email, hashed_pw, user_name, nickname)
    )
    db_conn.commit()
    cursor.close()
    db_conn.close()

    return jsonify(success=True)


@app.route('/warehouse', methods=['POST'])
def create_warehouse():
    data = request.json
    user_id = data.get('user_id')
    name = data.get('name')

    cursor = db.cursor(dictionary=True)

    # 중복 체크
    cursor.execute(
        "SELECT id FROM warehouse WHERE user_id=%s AND name=%s",
        (user_id, name)
    )
    if cursor.fetchone():
        return jsonify(success=False, message='이미 존재하는 창고')

    cursor.execute(
        "INSERT INTO warehouse (user_id, name) VALUES (%s, %s)",
        (user_id, name)
    )
    db.commit()

    return jsonify(success=True, warehouse_id=cursor.lastrowid)


@app.route('/warehouse', methods=['GET'])
def get_warehouses():
    user_id = request.args.get('user_id')

    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, name FROM warehouse WHERE user_id=%s ORDER BY created_at",
        (user_id,)
    )
    warehouses = cursor.fetchall()

    return jsonify(success=True, warehouses=warehouses)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
