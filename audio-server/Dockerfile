FROM arm32v7/python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    vlc \
    espeak \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# COPY doorbell.wav /app/doorbell.wav
COPY doorbell_reply.py /app/doorbell_reply.py

CMD ["python", "/app/doorbell_reply.py"]