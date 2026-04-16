# -*- coding: utf-8 -*-
import os
import json
import ssl
import time
from datetime import datetime

import paho.mqtt.client as mqtt

from django.db import IntegrityError
from django.utils import timezone

# Inicializa o Django
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
django.setup()

from django.conf import settings
from api_telemetria.models import MedicaoVeiculo, Medicao, Veiculo


def inserir_medicao_veiculo(veiculo_id, medicao_id, valor, data_field):
    """
    Insere uma medição de veículo no banco de dados.
    """
    try:
        veiculo = Veiculo.objects.get(pk=veiculo_id)
    except Veiculo.DoesNotExist:
        raise ValueError(f"Veiculo com id {veiculo_id} não existe")

    try:
        medicao = Medicao.objects.get(pk=medicao_id)
    except Medicao.DoesNotExist:
        raise ValueError(f"Medicao com id {medicao_id} não existe")

    try:
        MedicaoVeiculo.objects.create(
            veiculo=veiculo,
            medicao=medicao,
            data=data_field,
            valor=valor,
        )
    except IntegrityError as e:
        raise ValueError(f"Falha de integridade ao gravar MedicaoVeiculo: {e}")


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        topic = settings.MQTT.get("TOPIC", "sequisersim")
        client.subscribe(topic)
        print(f"🔗 [MQTT] Conectado e inscrito em '{topic}'")
    else:
        erros = {
            1: "Vers�o de protocolo recusada",
            2: "Identificador de cliente inv�lido",
            3: "Servidor indispon�vel",
            4: "Usu�rio ou senha incorretos",
            5: "N�o autorizado",
        }
        print(f"❌ [MQTT] Falha na conexão: rc={rc} - {erros.get(rc, 'Erro desconhecido')}")


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"🔌 [MQTT] Desconectado inesperadamente: rc={rc}. Tentando reconectar...")


def publish_notification(veiculo_id, medicao_id, valor, timestamp):
    cache_key = f"notif:{veiculo_id}:{medicao_id}:{valor}"
    if cache.get(cache_key):
        print(
            f"🔄 [MQTT] Notificação deduplicada ignorada: "
            f"veiculo={veiculo_id} medicao={medicao_id} valor={valor}"
        )
        return

    cache.set(cache_key, 1, 60)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "telemetria_all",
        {
            "type": "telemetria_event",
            "veiculo_id": veiculo_id,
            "valor": valor,
            "medicao_id": medicao_id,
            "timestamp": timestamp,
        },
    )
    print(f"📡 [MQTT] Notificação enviada: veiculo={veiculo_id} medicao={medicao_id}")


def validate_payload(data):
    if not isinstance(data, dict):
        raise ValueError("Payload MQTT deve ser um objeto JSON")

    required = ["valor"]
    missing = [key for key in required if key not in data]
    if missing:
        raise KeyError(missing[0])

    return data


def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode(errors="ignore")
        data = json.loads(payload)
        data = validate_payload(data)

        # Verificar se o payload é uma lista ou um objeto único
        if isinstance(data, list):
            for item in data:
                processar_item(item)
        else:
            processar_item(data)

    except KeyError as e:
        print(f"❌ [ERRO] Campo obrigatório ausente na mensagem: {e}")
    except ValueError as e:
        print(f"⚠️ [ERRO] Payload inválido: {e}")
    except json.JSONDecodeError as e:
        print(f"🔍 [ERRO] JSON inválido: {e}")
    except Exception as e:
        print(f"💥 [ERRO] Falha ao processar mensagem: {e}")


def processar_item(item):
    valor = float(item["valor"])
    veiculo_id = int(item.get("veiculo", item.get("motorid", 0)))
    medicao_id = int(item.get("medicao", item.get("medicaoid", 0)))

    if veiculo_id <= 0 or medicao_id <= 0:
        raise ValueError("veiculo_id e medicao_id devem ser inteiros positivos")

    data_value = item.get("data")
    if data_value:
        try:
            data_field = timezone.make_aware(datetime.fromisoformat(data_value))
        except Exception:
            data_field = timezone.now()
    else:
        data_field = timezone.now()

    inserir_medicao_veiculo(veiculo_id, medicao_id, valor, data_field)

    print(
        f"✅ [MQTT] Salvo: veiculo={veiculo_id} medicao={medicao_id} valor={valor}"
    )

    publish_notification(
        veiculo_id,
        medicao_id,
        valor,
        data_field.isoformat(),
    )


def create_mqtt_client():
    mqtt_cfg = settings.MQTT
    client_id = mqtt_cfg.get("CLIENT_ID")
    client = mqtt.Client(client_id=client_id) if client_id else mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    user = mqtt_cfg.get("USERNAME")
    password = mqtt_cfg.get("PASSWORD")
    if user and password:
        client.username_pw_set(user, password)

    port = mqtt_cfg.get("PORT", 8883)
    if port == 8883:
        ctx = ssl.create_default_context()
        ctx.check_hostname = True
        ctx.verify_mode = ssl.CERT_REQUIRED
        client.tls_set_context(ctx)
        print("🔒 [MQTT] TLS configurado com ssl.create_default_context()")

    return client


def main():
    mqtt_cfg = settings.MQTT
    host = mqtt_cfg.get("HOST", "127.0.0.1")
    port = mqtt_cfg.get("PORT", 8883)
    keepalive = mqtt_cfg.get("KEEPALIVE", 60)

    client = create_mqtt_client()
    reconnect_delay = 1

    while True:
        try:
            print(f"🔄 [MQTT] Conectando em {host}:{port}...")
            client.connect(host, port, keepalive)
            client.loop_forever()
        except KeyboardInterrupt:
            print("🛑 [MQTT] Interrompido pelo usuário")
            break
        except ssl.SSLError as e:
            print(f"🔒 [ERRO] Falha TLS/SSL: {e}")
        except ConnectionRefusedError:
            print(f"🚫 [ERRO] Conexão recusada em {host}:{port}. Verifique host e porta.")
        except TimeoutError:
            print(f"⏰ [ERRO] Timeout ao conectar em {host}:{port}.")
        except Exception as e:
            print(f"💥 [ERRO] Falha na conexão MQTT: {e}")
        print(f"🔄 [MQTT] Tentando reconectar em {reconnect_delay}s...")
        time.sleep(reconnect_delay)
        reconnect_delay = min(reconnect_delay * 2, 60)


if __name__ == "__main__":
    main()
