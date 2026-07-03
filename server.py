from flask import Flask, request, jsonify, send_file
import base64

app = Flask(__name__)

current_image = None
new_message = False

@app.route('/')
def index():
    return send_file('draw.html')

@app.route('/send', methods=['POST'])
def send_image():
    global current_image, new_message
    data = request.get_json()
    current_image = data['image']
    new_message = True
    return jsonify({'status': 'ok'})

@app.route('/check', methods=['GET'])
def check_message():
    global new_message
    if new_message:
        return jsonify({'new_message': True})
    return jsonify({'new_message': False})

@app.route('/image', methods=['GET'])
def get_image():
    global new_message
    new_message = False
    return jsonify({'image': current_image})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
