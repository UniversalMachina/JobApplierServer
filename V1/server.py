from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def handle_request():
    if request.method == 'GET':
        return "Hello, this is a GET request"
    elif request.method == 'POST':
        return "Hello, this is a POST request"

if __name__ == "__main__":
    app.run(port=5000)
