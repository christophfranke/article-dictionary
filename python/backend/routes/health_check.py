from flask import Blueprint, jsonify

health_check = Blueprint('health_check', __name__)

@health_check.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200
