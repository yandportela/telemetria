import ssl
import time
import json
import random
from datetime import datetime
import paho.mqtt.client as mqtt

# Configurações MQTT
HOST      = "jaragua.lmq.cloudamqp.com"
PORT      = 8883
USERNAME  = "qhmqhsgs:qhmqhsgs"
PASSWORD  = "owm17UsNUz4Jcb7LtugOAELVgds2AxmX"
TOPIC     = "sequisersim"

# Inicializa Django para acessar o banco
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
django.setup()

from api_telemetria.models import Medicao, Veiculo

# Busca IDs válidos automaticamente do banco
VEICULOS = list(Veiculo.objects.values_list('id', flat=True))
MEDICOES = list(Medicao.objects.values_list('id', flat=True))

print(f"🔍 IDs de veículos encontrados: {VEICULOS}")
print(f"🔍 IDs de medições encontrados: {MEDICOES}")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"🔗 [PUB] Conectado ao broker {HOST}:{PORT}")
    else:
        print(f"❌ [PUB] Falha na conexão rc={rc}")

def on_publish(client, userdata, mid):
    print(f"📤 [PUB] Mensagem enviada (mid={mid})")

def build_payload():
    return json.dumps({
        "valor": round(random.uniform(10.0, 120.0), 2),
        "veiculo": random.choice(VEICULOS),
        "medicao": random.choice(MEDICOES),
        "data": datetime.now().isoformat(),
    })

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id="mqtt-publisher-teste")
    client.username_pw_set(USERNAME, PASSWORD)

    ctx = ssl.create_default_context()
    ctx.check_hostname = True
    ctx.verify_mode = ssl.CERT_REQUIRED
    client.tls_set_context(ctx)

    client.on_connect = on_connect
    client.on_publish = on_publish

    print(f"🔄 [PUB] Conectando em {HOST}:{PORT}...")
    client.connect(HOST, PORT, keepalive=60)
    client.loop_start()

    time.sleep(2)

    try:
        while True:
            payload = build_payload()
            client.publish(TOPIC, payload, qos=1)
            print(f"📡 [PUB] Publicado em '{TOPIC}': {payload}")
            time.sleep(60)
    except KeyboardInterrupt:
        print("🛑 [PUB] Publicador encerrado.")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()