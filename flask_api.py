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
        file_data = file_data.strip()
        
        # Remove data URI prefix if present (e.g., data:image/pdf;base64,...)
        if "," in file_data and len(file_data) > 100:
            file_data = file_data.split(",")[-1]

        # Robust base64 detection: 
        # 1. Very long strings (> 500 chars) are almost certainly NOT paths
        # 2. If it's not an existing absolute path, treat as base64
        is_base64 = len(file_data) > 500 or (not os.path.exists(file_data) and not os.path.isabs(file_data))

        if is_base64:
            try:
                # Validate it's actually base64 by trying to decode a small piece
                base64.b64decode(file_data[:100], validate=False)
                
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                    temp_file.write(base64.b64decode(file_data))
                    temp_path = temp_file.name
                path_to_process = temp_path
            except Exception as b64_err:
                return jsonify({"error": f"Failed to decode base64 data: {str(b64_err)}"}), 400
        else:
            path_to_process = file_data

        if not os.path.exists(path_to_process):
            return jsonify({"error": f"File not found: {path_to_process}"}), 404

        result = process_with_paddle(path_to_process)
        return jsonify({"result": result})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=False)