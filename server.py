from flask import Flask, request, jsonify, send_file
import base64
from PIL import Image
import io
import struct

app = Flask(__name__)

current_image = None
current_pixels = None
new_message = False

@app.route('/')
def index():
    return send_file('draw.html')

@app.route('/send', methods=['POST'])
def send_image():
    global current_image, current_pixels, new_message
    data = request.get_json()
    current_image = data['image']
    
    # המרת התמונה ל-RGB565
    img_data = base64.b64decode(current_image.split(',')[1])
    img = Image.open(io.BytesIO(img_data)).convert('RGB')
    img = img.resize((128, 160))
    
    pixels = []
    for y in range(128):
        for x in range(160):
            r, g, b = img.getpixel((x, y))
            rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            pixels.append(rgb565)
    
    current_pixels = pixels
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
    global new_message, current_pixels
    new_message = False
    if current_pixels is None:
        return jsonify({'pixels': []})
    return jsonify({'pixels': current_pixels})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
