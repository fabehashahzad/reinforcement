from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/greet', methods=['POST'])
def greet():
    data = request.get_json()
    name = data.get('name', '')
    age = data.get('age', '')
    greeting = f"Hello, {name}! You are {age} years old."
    return jsonify({'greeting': greeting})

if __name__ == '__main__':
    app.run(debug=True)
