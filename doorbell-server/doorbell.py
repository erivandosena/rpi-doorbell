import os
import sys
import time
import logging
import logging.handlers
import argparse
from gpiozero import Button
import pygame
import paho.mqtt.publish as publish
import pyaudio
import wave
from picamera import PiCamera

# Configurações do ambiente SDL para o Pygame
os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_VIDEODRIVER"] = "fbcon"

# Configurações de log
LOG_FILENAME = "/tmp/doorbell.log"
LOG_LEVEL = logging.INFO

# Configuração do parser de argumentos de linha de comando
parser = argparse.ArgumentParser(description="Doorbell Service")
parser.add_argument("-l", "--log", help=f"file to write log to (default '{LOG_FILENAME}')")

args = parser.parse_args()
if args.log:
    LOG_FILENAME = args.log

# Configuração de logging
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Definindo os pinos e inicializando o GPIO
button = Button(26)

# Definições para captura de áudio e imagem
AUDIO_OUTPUT_FILENAME = "visitor_audio.wav"
IMAGE_OUTPUT_FILENAME = "visitor_image.jpg"

def record_audio(duration=5):
    audio_format = pyaudio.paInt16
    channels = 1
    rate = 44100
    chunk = 1024
    p = pyaudio.PyAudio()
    stream = p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    frames = []
    for i in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    with wave.open(AUDIO_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(audio_format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

def capture_image():
    with PiCamera() as camera:
        camera.start_preview()
        time.sleep(2)  # Camera warm-up time
        camera.capture(IMAGE_OUTPUT_FILENAME)
        camera.stop_preview()

def main():
    pygame.init()
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode((160, 128))

    while True:
        if button.is_pressed:
            print('Button Pressed')
            # Captura áudio e imagem do visitante
            record_audio()
            capture_image()
            # Publica uma mensagem MQTT
            try:
                publish.single("home/core/doorbell", "ON", hostname="mqtt_broker_address")
            except Exception as e:
                print(f"Failed to publish MQTT message: {e}")

        time.sleep(1)

if __name__ == '__main__':
    main()