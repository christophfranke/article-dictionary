from flask import Blueprint, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from utils.mongo import get_collection
from users import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    name = data.get('name', '')
    source_language = data.get('sourceLanguage')
    target_language = data.get('targetLanguage')
    password = data.get('password')

    if not email or not password or not source_language or not target_language:
        return jsonify({'error': 'Email and password are required'}), 400

    users = get_collection('users')

    existing_user = users.find_one({'email': email})
    if existing_user:
        return jsonify({'error': 'User already exists'}), 400

    # Hash the password before storing it in the database
    hashed_password = generate_password_hash(password)
    user_id = users.insert_one({
        'email': email,
        'name': name,
        'password': hashed_password,
        'source_language': source_language,
        'target_language': target_language,
    }).inserted_id

    user_data = users.find_one({'email': email})
    user_obj = User(user_data)
    login_user(user_obj)

    return jsonify({'message': 'User registered successfully'}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    users = get_collection('users')

    user_data = users.find_one({'email': email})

    if user_data and check_password_hash(user_data['password'], password):
        user_obj = User(user_data)
        login_user(user_obj)
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 403

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'})

# Other routes and functionality for authentication can be added as needed

