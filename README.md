# OCR Paddle Project

A Python-based Optical Character Recognition (OCR) project using PaddleOCR and OpenAI/Groq API for intelligent document processing (resumes and receipts).

## Project Overview

This project uses **PaddleOCR** to extract text from images/documents and then leverages **OpenAI API** (via Groq) to intelligently parse and structure the extracted data into JSON format.

**Supported Document Types:**
- Resumes (extracts: nama, email, nomor_telepon)
- Receipts (extracts: vendor, tanggal, total)

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ocr
```

### 2. Create Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirement.txt
```

Or install packages individually:
```bash
pip install paddleocr>=2.6.0
pip install paddlepaddle
pip install openai
pip install python-dotenv
```

## Environment Setup

### 1. Create `.env` File
Create a `.env` file in the project root directory:
```bash
touch .env
```

### 2. Add API Keys
Edit `.env` and add your Groq API key:
```
GROQ_API_KEYS=your_groq_api_key_here
```

**How to get Groq API Key:**
1. Visit [Groq Console](https://console.groq.com)
2. Sign up or login
3. Generate an API key
4. Add it to your `.env` file

## Usage

### Processing a Single Document
```bash
python3 ocr_paddle.py path/to/document.pdf
```

**Example:**
```bash
python3 ocr_paddle.py Invoice-tokped.PDF
```

### Output
The script outputs JSON format:
- **Resume:** `{"nama": "...", "email": "...", "nomor_telepon": "..."}`
- **Receipt:** `{"vendor": "...", "tanggal": "YYYY-MM-DD", "total": 0}`

### Error Handling
If an error occurs, the output will be in format:
```json
{"error": "error message"}
```

## Project Structure
```
ocr/
├── ocr_paddle.py          # Main OCR processing script
├── requirement.txt        # Python dependencies
├── .env                   # Environment variables (create this)
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## Supported Files

The script processes the following file formats:
- PDF files
- Image files (PNG, JPG, JPEG, etc.)

## First Run

**Note:** On first run, PaddleOCR will automatically download the pre-trained models (~200MB). This may take a few minutes depending on your internet connection.

## Troubleshooting

### Issue: "GROQ_API_KEYS not found"
- **Solution:** Make sure `.env` file exists and contains `GROQ_API_KEYS=your_key`
- Verify the variable name is exactly `GROQ_API_KEYS`

### Issue: PaddleOCR download fails
- **Solution:** Check your internet connection
- Try running again, it will continue from where it stopped

### Issue: "ModuleNotFoundError" for paddleocr or openai
- **Solution:** Reinstall requirements:
  ```bash
  pip install --upgrade -r requirement.txt
  ```

### Issue: Out of memory on GPU
- The script uses `use_gpu=False` by default (CPU mode)
- If you have GPU, modify the script to use `use_gpu=True`

## License

Check the LICENSE file for details.
