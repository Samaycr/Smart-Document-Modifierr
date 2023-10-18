from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/your_database_name'
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

@app.route('/register', methods=['POST'])
def register():
    users = mongo.db.users
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    existing_user = users.find_one({'username': username})
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user_id = users.insert({'username': username, 'password': hashed_password})
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    username = request.json.get('username')
    password = request.json.get('password')

    user = users.find_one({'username': username})
    if user and bcrypt.check_password_hash(user['password'], password):
        # Here, you can implement user session management or JWT for token-based authentication
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/protected', methods=['GET'])
def protected_resource():
    # Implement authentication check for protected resources here
    return jsonify({'message': 'This is a protected resource'}), 200

if __name__ == '__main__':
    app.run(debug=True)
