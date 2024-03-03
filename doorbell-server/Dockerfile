# Criar um serviço systemd para iniciar o container Docker na inicialização,
# doorbell.service em /etc/systemd/system/, com ExecStart apontando para o comando Docker:
# sudo nano /etc/systemd/system/doorbell.service
# sudo systemctl daemon-reload
# sudo systemctl enable doorbell.service
# sudo systemctl start doorbell.service

FROM arm32v7/python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libraspberrypi-bin \
    python3-pygame \
    libsdl1.2-dev \
    libsdl-image1.2-dev \
    libsdl-mixer1.2-dev \
    libsdl-ttf2.0-dev \
    libsmpeg-dev \
    libportmidi-dev \
    libavformat-dev \
    libswscale-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt

COPY requirements.txt /app/
COPY doorbell.py /app/doorbell.py

CMD ["python", "/app/doorbell.py"]
