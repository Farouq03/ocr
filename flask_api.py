from flask import Flask, request, jsonify
import base64
import tempfile
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

    temp_path = None
    try:
        # Check if file_data is likely a base64 string
        # If it doesn't look like a path and is long, treat as base64
        if not file_data.startswith('/') and len(file_data) > 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                temp_file.write(base64.b64decode(file_data))
                temp_path = temp_file.name
            path_to_process = temp_path
        else:
            path_to_process = file_data

        result = process_with_paddle(path_to_process)
        return jsonify({"result": result})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        # Clean up the temp file if we created one
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=False)