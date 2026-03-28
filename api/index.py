from flask import Flask, request, send_file
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

@app.route('/api/remove-bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return {"error": "No image uploaded"}, 400
    
    file = request.files['image']
    input_image = Image.open(file.stream)
    output_image = remove(input_image)

    img_io = io.BytesIO()
    output_image.save(img_io, format='PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

# Vercel এর জন্য এটি দরকার
def handler(request):
    return app(request)