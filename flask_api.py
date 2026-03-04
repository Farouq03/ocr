from flask import Flask, request, jsonify
from ocr_paddle import process_with_paddle
import traceback
from dotenv import load_dotenv
import os
load_dotenv()
ip = os.getenv("IP_ADDRESS")

app = Flask(__name__)

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "status": "online",
        "message": "OCR API is running. Use /ocr (POST) for processing."
    })

@app.route('/ocr', methods=['POST'])
def ocr_post():
    incoming_data = request.get_json()
    
    file_data = incoming_data.get("file_data")
    if not file_data:
        return jsonify({"error": "No file data provided"}), 400

    try:
        result = process_with_paddle(file_data)
        return jsonify({"result": result})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=False)