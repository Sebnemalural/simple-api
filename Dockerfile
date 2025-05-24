FROM python:3.10-slim
WORKDIR /app

# 1) Bağımlılıkları kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Uygulama kodunu kopyala
COPY . .

# 3) Port’u expose et ve başlatma komutunu ayarla
EXPOSE 5000
CMD ["python", "app.py"]
