from flask import Flask, request, send_file
from flask_cors import CORS
from rembg import remove, new_session
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# সেশন তৈরি করে রাখা যাতে বারবার মডেল লোড না হয়
session = new_session()

@app.route('/api/remove-bg', methods=['POST'])
def remove_bg():
    try:
        if 'image' not in request.files:
            return {"error": "No image uploaded"}, 400
        
        file = request.files['image']
        input_image = Image.open(file.stream)
        
        # সেশন ব্যবহার করে ব্যাকগ্রাউন্ড রিমুভ
        output_image = remove(input_image, session=session)

        img_io = io.BytesIO()
        output_image.save(img_io, format='PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    except Exception as e:
        return {"error": str(e)}, 500

def handler(request):
    return app(request)
