# Menggunakan image Python resmi
FROM python:3.9-slim

# Tentukan folder kerja
WORKDIR .

# Salin file requirement.txt dan install library
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# Salin seluruh kode aplikasi
COPY . .

# Ekspose port Flask (defaultnya 5000)
EXPOSE 5000

# Jalankan aplikasi Flask 
CMD ["python", "flask_api.py"]
