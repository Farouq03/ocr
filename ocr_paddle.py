from paddleocr import PaddleOCR
import json
from openai import OpenAI
import os
import base64
import sys
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Inisialisasi model (akan download model di awal)
# use_angle_cls=True membantu mendeteksi jika teks terbalik/miring
ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False) # 'en' mencakup karakter Indonesia juga
groq_api_key = os.getenv('GROQ_API_KEY')
client = OpenAI(
    api_key=groq_api_key, 
    base_url="https://api.groq.com/openai/v1",
)

def process_with_paddle(image_path):
    # print(f"Memproses {image_path} dengan PaddleOCR...")
    
    # Ekstraksi teks
    result = ocr.ocr(image_path)
    
    # Gabungkan semua teks yang terdeteksi
    full_text = []
    for idx in range(len(result)):
        res = result[idx]
        if res: # Pastikan hasil tidak kosong
            for line in res:
                text_content = line[1][0] # Mengambil teksnya saja
                full_text.append(text_content)
    
    raw_text = "\n".join(full_text)

    prompt = f"""
    Periksa raw text yang telah diekstrak dan ikuti 2 set aturan di bawah ini sesuai konteks dokumen (resume atau receipt).
    
    Raw Text:
    {raw_text}

    Aturan Resume:
    Tugas: Ubah teks resume di bawah ini menjadi sebuah JSON yang rapi.
    1. Output HARUS berupa JSON murni, tanpa penjelasan, tanpa kata pengantar, dan tanpa markdown block (seperti ```json).
    2. Hanya berikan 3 field berikut dalam JSON dengan format:
       - nama : nama lengkap pelamar
       - email : alamat email pelamar
       - nomor_telepon : nomor telepon/HP pelamar
    3. Jika salah satu field tidak ditemukan, isikan dengan null.
    
    Jangan menambahkan field lain selain yang diminta di atas.

    Aturan Receipt:
    Tugas: Ubah teks resi di bawah ini menjadi JSON yang rapi.
    1. Output HARUS berupa JSON murni, tanpa penjelasan, tanpa kata pengantar, dan tanpa markdown block (seperti ```json).
    2. Bersihkan angka dari simbol "Rp", titik, atau koma (ubah menjadi integer).
    3. Ubah format tanggal menjadi YYYY-MM-DD.
    4. Jika terdapat angka yang tertukar dengan o huruf (misalnya "O" menjadi "0"), perbaiki sesuai konteks.
    5. Setiap angka yang diawali dengan rp harus diubah menjadi integer.
    6. total diambil dari "Total tagihan", "Total pembayaran", atau "Total" pada receipt.
    7. Hanya berikan 3 field berikut dalam JSON:
       - vendor: nama toko atau penjual
       - tanggal: tanggal pembelian dalam format YYYY-MM-DD
       - total: total pembayaran sebagai integer tanpa titik dan koma (gunakan titik desimal jika ada)
    8. Jika salah satu field tidak ditemukan, isikan dengan null.

    Jangan menambahkan field lain selain yang diminta di atas.

    """
    
    # print("Merapikan data dengan AI Lokal...")

    response = client.responses.create(
        input=prompt,
        model="openai/gpt-oss-20b",
    )
    return response.output_text

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        try:
            # Panggil fungsi tanpa mencetak progres di dalamnya
            output = process_with_paddle(file_path)
            
            # PASTIKAN: Hanya print output JSON saja di sini
            print(output) 
        except Exception as e:
            # Jika error, kirim JSON berisi pesan error agar Odoo tidak crash
            print(json.dumps({"error": str(e)}))

# # Contoh eksekusi
# output, raw_text = process_with_paddle("Invoice-tokped.PDF")
# print("\n--- HASIL OCR Paddle---")
# print(raw_text)
# print("\n--- HASIL JSON GROQ ---")
# print(output)