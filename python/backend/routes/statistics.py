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
    seven_days_ago = datetime.utcnow() - timedelta(days=7)

    # MongoDB Aggregation Pipeline
    pipeline = [
        {
            '$match': {
                'timestamp': {'$gte': seven_days_ago},
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
                'ignore_words': {'$first': '$ignore_words'}
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
                'ignore_words': 1
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

    # Modify the result to add 'total_words' and remove 'ignore_words'
    for entry in result:
        entry['total_words'] = entry['new_words'] + entry['seen_words'] + entry['known_words']
        del entry['ignore_words']

    # Fill in missing dates based on the latest available entry
    for i in range(1, 7):  # Loop through the next 6 days
        date = (datetime.utcnow() - timedelta(days=i)).strftime('%Y-%m-%d')

        # Check if an entry for the date already exists
        existing_entry = next((entry for entry in result if entry['date'] == date), None)

        if existing_entry is None:
            # Create a dummy entry if no entry exists for the date
            dummy_entry = {
                'date': date,
                'latest_timestamp': None,
                'new_words': 0,
                'seen_words': 0,
                'known_words': 0,
                'ignore_words': 0  # Assuming 'ignore_words' should also be present in the result
            }
            result.append(dummy_entry)

    return jsonify(result)
