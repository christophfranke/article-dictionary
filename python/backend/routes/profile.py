from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from utils.mongo import get_collection


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
            'name': user_data.get('name', user.email),
            'from_language': user_data.get('from_language', ''),
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
    new_data = {key: data[key] for key in data if key in ['name', 'email', 'from_language', 'to_language']}

    # Hash the password if provided in the data
    if 'password' in data:
        new_data['password'] = generate_password_hash(data['password'])

    users.update_one({'email': user['email']}, {'$set': new_data})
    updated_user = users.find_one({'email': user['email']})

    return jsonify(updated_user), 200


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
        'from_language': user_data.get('from_language', ''),
        'to_language': user_data.get('to_language', ''),
        # Add more settings as needed
    }

    return jsonify(settings_data), 200
