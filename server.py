from flask import Flask, request, jsonify, send_file, Response
import base64
from PIL import Image
import io
import struct

app = Flask(__name__)

current_image = None
current_bmp = None
new_message = False

@app.route('/')
def index():
    return send_file('draw.html')

@app.route('/send', methods=['POST'])
def send_image():
    global current_image, current_bmp, new_message
    data = request.get_json()
    current_image = data['image']
    
    img_data = base64.b64decode(current_image.split(',')[1])
    img = Image.open(io.BytesIO(img_data)).convert('RGB')
    img = img.resize((160, 128), Image.LANCZOS)
    
    # שמירה כ-BMP
    bmp_buffer = io.BytesIO()
    img.save(bmp_buffer, format='BMP')
    current_bmp = bmp_buffer.getvalue()
    
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
    global new_message, current_bmp
    new_message = False
    if current_bmp is None:
        return jsonify({'error': 'no image'})
    return Response(current_bmp, mimetype='image/bmp')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
