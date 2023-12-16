from flask import Blueprint, jsonify
from datetime import datetime, timedelta
from utils.mongo import get_collection
from flask_login import login_required, current_user
from bson import ObjectId


statistics = Blueprint('statistics', __name__)


@statistics.route('/daily', methods=['GET'])
@login_required
def get_statistics():
    statistics_collection = get_collection('statistics')

    # Calculate the date 7 days ago from today
    seven_days_ago = datetime.utcnow() - timedelta(days=8)

    # MongoDB Aggregation Pipeline
    pipeline = [
        {
            '$match': {
                'timestamp': {
                    '$gte': seven_days_ago,
                    '$lt': datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
                },
                'user_id': ObjectId(current_user.id)  # Filter by current user_id
            }
        },
        {
            '$sort': {
                'timestamp': -1
            }
        },
        {
            '$group': {
                '_id': {
                    '$dateToString': {
                        'format': '%Y-%m-%d',
                        'date': '$timestamp'
                    }
                },
                'latest_timestamp': {'$first': '$timestamp'},
                'new_words': {'$first': '$new_words'},
                'seen_words': {'$first': '$seen_words'},
                'known_words': {'$first': '$known_words'},
                'total_words': {'$first': '$total_words'},
                'new_cluster': {'$first': '$new_cluster'},
                'seen_cluster': {'$first': '$seen_cluster'},
                'known_cluster': {'$first': '$known_cluster'},
                'total_cluster': {'$first': '$total_cluster'}
            }
        },
        {
            '$project': {
                '_id': 0,
                'date': '$_id',
                'latest_timestamp': 1,
                'new_words': 1,
                'seen_words': 1,
                'known_words': 1,
                'total_words': 1,
                'new_cluster': 1,
                'seen_cluster': 1,
                'known_cluster': 1,
                'total_cluster': 1
            }
        },
        {
            '$sort': {
                'latest_timestamp': -1
            }
        }
    ]

    # Execute the aggregation pipeline
    result = list(statistics_collection.aggregate(pipeline))

    # Calculate today's statistics fresh
    today_date = datetime.utcnow().strftime('%Y-%m-%d')
    dictionary = get_collection('dictionary')
    cluster = get_collection('cluster')
    today_statistics = {
        'date': today_date,
        'latest_timestamp': None,  # Update this if needed based on your requirements
        'new_words': dictionary.count_documents({'status': 'new', 'user_id': ObjectId(current_user.id)}),
        'seen_words': dictionary.count_documents({'status': 'seen', 'user_id': ObjectId(current_user.id)}),
        'known_words': dictionary.count_documents({'status': 'known', 'user_id': ObjectId(current_user.id)}),
        'total_words': dictionary.count_documents({'user_id': ObjectId(current_user.id)}),
        'new_cluster': cluster.count_documents({'status': 'new', 'user_id': ObjectId(current_user.id)}),
        'seen_cluster': cluster.count_documents({'status': 'seen', 'user_id': ObjectId(current_user.id)}),
        'known_cluster': cluster.count_documents({'status': 'known', 'user_id': ObjectId(current_user.id)}),
        'total_cluster': cluster.count_documents({'user_id': ObjectId(current_user.id)}),
    }

    # Add today's statistics to the result
    result.append(today_statistics)

    return jsonify(result)
