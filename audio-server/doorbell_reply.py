import paho.mqtt.client as mqtt
import logging
import pyttsx3
import vlc
import time
import os
import requests

LOG_FILENAME = '/var/log/doorbell_logs.out'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

# Função para verificar a existência do arquivo e baixá-lo se necessário
def check_and_download_wav():
    filename = 'doorbell.wav'
    url = 'http://soundbible.com/grab.php?id=165&type=wav'
    if not os.path.isfile(filename):
        logging.info(f"{filename} not found. Downloading from {url}")
        try:
            r = requests.get(url, allow_redirects=True)
            with open(filename, 'wb') as f:
                f.write(r.content)
            logging.info(f"Downloaded {filename} successfully.")
        except Exception as e:
            logging.error(f"Failed to download {filename}: {e}")

# Verifica e baixa o arquivo .wav antes de inicializar o player VLC
check_and_download_wav()

player = vlc.MediaPlayer("doorbell.wav")

# Callback events
def on_connect(client, userdata, flags, rc):
    logging.debug(f'Connected with result code {rc}')
    client.subscribe("home/core/doorbell")  # Inscreve-se no tópico assim que a conexão é estabelecida

def on_message(client, userdata, msg):
    logging.debug(f'Received message on {msg.topic}: {msg.payload}')
    player.play()
    time.sleep(2)  # Aguarda o fim da reprodução do som
    engine = pyttsx3.init()
    engine.say("Someone is at the front door")
    engine.runAndWait()

# MQTT settings
client = mqtt.Client("piDoorbell-chime")
client.on_connect = on_connect
client.on_message = on_message

# Conectar ao broker MQTT
client.connect("broker_address", 1883, 60)  # Substitua "broker_address" pelo endereço IP do seu broker MQTT

client.loop_forever()