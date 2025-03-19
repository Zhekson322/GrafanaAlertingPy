FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .env .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python3", "-u", "main.py"]