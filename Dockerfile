# Menggunakan image Python resmi
FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Tentukan folder kerja
WORKDIR .

# Salin file requirement.txt dan install library
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# Salin seluruh kode aplikasi
COPY . .

# Ekspose port Flask (defaultnya 5000)
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "flask_api:app"]