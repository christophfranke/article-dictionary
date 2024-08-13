from flask import Blueprint, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from utils.mongo import get_collection
from smtplib import SMTPException
from users import User

from reset_password import create_password_link, send_reset_mail, get_email_from_token

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


@auth.route('/reset', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')

    if email is None:
        return jsonify({'message': 'Email required for password reset.'}), 400

    users = get_collection('users')

    existing_user = users.find_one({'email': email})
    if existing_user is None:
        return jsonify({'error': 'User does not exist'}), 400

    reset_link = create_password_link(email)
    print(f'Reset link is: {reset_link}')
    if not send_reset_mail(email, reset_link):
        return jsonify({'error': 'Internal error: Failed to send reset link'}), 500

    return jsonify({'success': True}), 200


@auth.route('/change-password', methods=['POST'])
def change_password():
    data = request.get_json()
    token = data.get('token')
    password = data.get('password')

    # Return 400 if no token or no password
    if not token or not password:
        return jsonify({'error': 'Token and password are required.'}), 400

    email, message = get_email_from_token(token)
    if email is None:
        return jsonify({'error': message}), 400

    # Check if the user exists
    users = get_collection('users')
    user = users.find_one({'email': email})
    if not user:
        return jsonify({'error': 'User does not exist.'}), 404

    # Hash the new password and update the user's password in the database
    hashed_password = generate_password_hash(password)
    users.update_one({'email': email}, {'$set': {'password': hashed_password}})

    return jsonify({'success': True}), 200


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
