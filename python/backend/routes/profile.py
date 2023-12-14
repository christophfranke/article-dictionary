from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from utils.mongo import get_collection
from utils.casing import camel_to_snake


profile = Blueprint('profile', __name__)


@profile.route('/preview')
def preview():
    # Assuming you have the current_user object available
    user = current_user

    if user.is_authenticated:
        users = get_collection('users')
        user_data = users.find_one({'email': user.email})

        if not user_data:
            return jsonify({'isLoggedIn': False}), 200

        response_data = {
            'isLoggedIn': True,
            'name': user_data.get('name', ''),
            'email': user_data.get('email'),
            'sourceLanguage': user_data.get('source_language', ''),
        }

        return jsonify(response_data), 200
    else:
        return jsonify({'isLoggedIn': False}), 200


@profile.route('/update', methods=['POST'])
@login_required
def update():
    user = current_user
    data = request.get_json()

    users = get_collection('users')

    # Only include fields that are provided in the data
    new_data = {camel_to_snake(key): data[key] for key in data if key in ['name', 'email', 'sourceLanguage', 'targetLanguage']}

    if 'source_language' in new_data or 'target_language' in new_data:
        return jsonify({'message': 'Source and target language cannot be updated'}), 400

    # Hash the password if provided in the data
    if 'password' in data:
        new_data['password'] = generate_password_hash(data['password'])

    users.update_one({'email': user.email}, {'$set': new_data})
    updated_user = users.find_one({'email': user.email})

    response_data = {
        'email': updated_user['email'],
        'name': updated_user.get('name', ''),
        'sourceLanguage': updated_user.get('source_language', ''),
        'targetLanguage': updated_user.get('target_language', ''),
    }
    return jsonify(response_data), 200


@profile.route('/settings')
@login_required
def settings():
    user = current_user

    users = get_collection('users')
    user_data = users.find_one({'email': user.email})

    if not user_data:
        return jsonify({'message': 'User not found'}), 404

    settings_data = {
        'email': user_data['email'],
        'name': user_data.get('name', ''),
        'sourceLanguage': user_data.get('source_language', ''),
        'targetLanguage': user_data.get('target_language', ''),
    }

    return jsonify(settings_data), 200
