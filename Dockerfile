# Menggunakan image Python resmi
FROM python:3.9-slim

# Tentukan folder kerja
WORKDIR .

# Salin file requirements.txt dan install library
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode aplikasi
COPY . .

# Ekspose port Flask (defaultnya 5000)
EXPOSE 5000

# Jalankan aplikasi Flask 
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "flask_api:app"]
