# Menggunakan image Python resmi
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

ENV PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK=True
ENV PYTHONUNBUFFERED=1
ENV FLAGS_allocator_strategy=naive_best_fit
ENV FLAGS_fraction_of_gpu_memory_to_use=0

# Tentukan folder kerja
WORKDIR /app

# Salin file requirement.txt dan install library
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# Salin seluruh kode aplikasi
COPY . .

# Ekspose port Flask (defaultnya 5000)
EXPOSE 5000

# Tambahkan ini di bagian paling bawah Dockerfile
# Tambahkan log file agar error terlihat di dashboard Easypanel
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "flask_api:app"]