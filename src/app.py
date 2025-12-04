from flask import Flask
from flask import request, jsonify

app = Flask(__name__)

def validate_post_data(data: dict) -> bool:
    if not isinstance(data, dict):
        return False
    if not data.get('name') or not isinstance(data['name'], str):
        return False
    if data.get('age') and not isinstance(data['age'], int):
        return False
    return True

@app.route('/', methods=['GET'])
def hello():
    return 'Hello World!'

@app.route('/add', methods=['GET'])
def add():
    try:
        a = float(request.args.get('a'))
        b = float(request.args.get('b'))
    except (TypeError, ValueError):
        return 'a и b - НЕ числа'
    return str(a + b)

@app.route('/max_number', methods=['GET'])
def max_number():
    try:
        a = float(request.args.get('a'))
        b = float(request.args.get('b'))
    except (TypeError, ValueError):
        return 'a и b - НЕ числа'
    return max(a, b)


@app.route('/api', methods=['GET', 'POST'])
def api():
    """
    /api entpoint
    GET - returns json= {'status': 'test'}
    POST -  {
            name - str not null
            age - int optional
            }
    :return:
    """
    if request.method == 'GET':
        return jsonify({'status': 'test'})
    elif request.method == 'POST':
        if validate_post_data(request.json):
            return jsonify({'status': 'OK'})
        else:
            return jsonify({'status': 'bad input'}), 400

def main():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    main()
