from flask import Flask, request, jsonify
import threading
import time
import pickle
import os

app = Flask(__name__)
data_lock = threading.Lock()
data_file = 'data.pkl'

def load_data():
    if os.path.exists(data_file):
        with open(data_file, 'rb') as file:
            return pickle.load(file)
    return {"data": {}, "transactions": {}}

def dump_data(data):
    with open(data_file, 'wb') as file:
        pickle.dump(data, file)

@app.route('/start', methods=['POST'])
def start_transaction():
    with data_lock:
        current_data = load_data()
        transaction_id = int(time.time())  # Simplified transaction ID
        current_data['transactions'][transaction_id] = {'start_time': time.time(), 'changes': {}}
        dump_data(current_data)
    return jsonify({'transaction_id': transaction_id}), 200

@app.route('/write', methods=['POST'])
def write():
    transaction_id = request.json.get('transaction_id')
    key = request.json.get('key')
    value = request.json.get('value')
    with data_lock:
        current_data = load_data()
        current_data['transactions'][transaction_id]['changes'][key] = value
        dump_data(current_data)
    return jsonify({'message': 'Write successful'}), 200

@app.route('/commit', methods=['POST'])
def commit_transaction():
    transaction_id = request.json.get('transaction_id')
    with data_lock:
        current_data = load_data()
        transaction = current_data['transactions'].pop(transaction_id, None)
        if transaction:
            for key, value in transaction['changes'].items():
                if key not in current_data['data']:
                    current_data['data'][key] = []
                version_number = len(current_data['data'][key]) + 1
                current_data['data'][key].append((value, version_number, transaction['start_time']))
            dump_data(current_data)
    return jsonify({'message': 'Commit successful'}), 200

# @app.route('/read', methods=['GET'])
# def read():
#     transaction_id = int(request.args.get('transaction_id'))
#     key = request.args.get('key')
#     with data_lock:
#         current_data = load_data()
#         print(current_data)
#         transactions = current_data['transactions']
#         data = current_data['data']

#         transaction = transactions.get(transaction_id, {'changes': {}, 'start_time': time.time()})
#         if key in transaction['changes']:
#             value = transaction['changes'][key]
#             version = len(data.get(key, [])) + 1
#             timestamp = transaction['start_time']
#         else:
#             if key in data:
#                 versions = data[key]
#                 # Get the latest version
#                 value, version, timestamp = max(versions, key=lambda x: x[2])
#             else:
#                 value, version, timestamp = None, None, None

#         readable_timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp)) if timestamp else None
#     return jsonify({'value': value, 'version': version, 'timestamp': readable_timestamp}), 200

@app.route('/read', methods=['GET'])
def read():
    transaction_id = int(request.args.get('transaction_id'))
    key = request.args.get('key')
    with data_lock:
        current_data = load_data()
        transactions = current_data['transactions']
        data = current_data['data']

        transaction = transactions.get(transaction_id, {'changes': {}, 'start_time': time.time()})
        if key in transaction['changes']:
            # If the key has been modified in the current transaction, return the modified value
            value = transaction['changes'][key]
            version = len(data.get(key, [])) + 1
            timestamp = transaction['start_time']
        else:
            if key in data:
                versions = data[key]
                # Get the latest committed version (excluding the current transaction changes)
                committed_versions = [v for v in versions if v[2] < transaction['start_time']]
                if committed_versions:
                    value, version, timestamp = max(committed_versions, key=lambda x: x[2])
                else:
                    value, version, timestamp = (None, None, None)
            else:
                value, version, timestamp = (None, None, None)

        readable_timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp)) if timestamp else None
    return jsonify({'value': value, 'version': version, 'timestamp': readable_timestamp}), 200

@app.route('/rollback', methods=['POST'])
def rollback_transaction():
    transaction_id = request.json.get('transaction_id')
    with data_lock:
        current_data = load_data()
        current_data['transactions'].pop(transaction_id, None)
        dump_data(current_data)
    return jsonify({'message': 'Rollback successful'}), 200

if __name__ == '__main__':
    app.run(debug=True)