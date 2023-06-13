# main.py
import requests
import json

def get_string_from_server():
    response = requests.get('http://localhost:5000/get_string')
    if response.status_code == 200:
        print(response.json()['message'])
    else:
        print("Error getting string from server.")

def post_string_to_server(message):
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({'message': message})
    response = requests.post('http://localhost:5000/post_string', headers=headers, data=data)
    if response.status_code == 200:
        print(response.json()['message'])
    else:
        print("Error posting string to server.")

if __name__ == "__main__":
    get_string_from_server()
    post_string_to_server('This is a test string.')
