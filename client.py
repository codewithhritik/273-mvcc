import requests

SERVER_URL = "http://127.0.0.1:5000"

def start_transaction():
    response = requests.post(f"{SERVER_URL}/start").json()
    transaction_id = response.get('transaction_id')
    print(f"Transaction {transaction_id} started.")
    return transaction_id

def write(transaction_id, key, value):
    response = requests.post(f"{SERVER_URL}/write", json={'transaction_id': transaction_id, 'key': key, 'value': value})
    print(response.json().get('message'))

def commit(transaction_id):
    response = requests.post(f"{SERVER_URL}/commit", json={'transaction_id': transaction_id})
    print(response.json().get('message'))

def read(transaction_id, key):
    try:
        response = requests.get(f"{SERVER_URL}/read", params={'transaction_id': transaction_id, 'key': key})
        response.raise_for_status()  # Check for HTTP errors
        json_response = response.json()
        print(f"Value: {json_response.get('value')}, Version: {json_response.get('version')}, Timestamp: {json_response.get('timestamp')}")
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.JSONDecodeError as json_err:
        print(f"JSON decode error: {json_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

def rollback(transaction_id):
    response = requests.post(f"{SERVER_URL}/rollback", json={'transaction_id': transaction_id})
    print(response.json().get('message'))

def main():
    transaction_id = None
    while True:
        option = input("\nOptions: start, read, write, commit, rollback, exit\nEnter option: ").strip().lower()

        if option == 'exit':
            break
        elif option == 'start':
            transaction_id = start_transaction()
        elif option == 'read':
            if transaction_id is None:
                print("Please start a transaction first.")
            else:
                key = input("Enter key: ")
                read(transaction_id, key)
        elif option in ['write', 'commit', 'rollback']:
            if transaction_id is None:
                print("Please start a transaction first.")
                continue
            if option == 'write':
                key = input("Enter key: ")
                value = input("Enter value: ")
                write(transaction_id, key, value)
            elif option == 'commit':
                commit(transaction_id)
                transaction_id = None  # Reset transaction_id after commit
            elif option == 'rollback':
                rollback(transaction_id)
                transaction_id = None  # Reset transaction_id after rollback
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()