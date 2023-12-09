from flask import Blueprint, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from utils.mongo import get_collection

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    users = get_collection('users')

    existing_user = users.find_one({'email': email})
    if existing_user:
        return jsonify({'message': 'User already exists'}), 400

    # Hash the password before storing it in the database
    hashed_password = generate_password_hash(password, method='sha256')

    # Assuming 'users' is the collection storing user data
    user_id = users.insert_one({'email': email, 'password': hashed_password}).inserted_id

    return jsonify({'message': 'User registered successfully', 'user_id': str(user_id)})

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
        return jsonify({'message': 'Invalid credentials'}), 401

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'})

# Other routes and functionality for authentication can be added as needed

