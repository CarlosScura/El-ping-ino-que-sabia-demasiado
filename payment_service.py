import requests
import random
import time
from datetime import datetime

SERVER_URL = "http://127.0.0.1:6039/logs"
TOKEN = "SERVICE2_TOKEN"   # distinto al del auth-service

SEVERITY_MESSAGES = {
    "INFO": [
        "Pago procesado correctamente",
        "Factura generada exitosamente"
    ],
    "DEBUG": [
        "Validación de tarjeta completada"
    ],
    "WARNING": [
        "Saldo insuficiente detectado"
    ],
    "ERROR": [
        "Error en la conexión con pasarela de pagos",
        "Transacción rechazada por el banco"
    ],
    "CRITICAL": [
        "Sistema de pagos caído"
    ]
}

def send_random_log():
    severity = random.choice(list(SEVERITY_MESSAGES.keys()))
    message = random.choice(SEVERITY_MESSAGES[severity])

    log = {
        "timestamp": datetime.now().isoformat(),
        "service": "payment-service",
        "severity": severity,
        "message": message
    }

    try:
        response = requests.post(
            SERVER_URL,
            json=log,
            headers={"Authorization": f"Token {TOKEN}"}
        )
        print("Log enviado:", log)
        print("Respuesta del servidor:", response.json())
    except Exception as e:
        print("Error al enviar log:", e)

if __name__ == "__main__":
    try:
        while True:
            send_random_log()
            time.sleep(random.uniform(1, 5))
    except KeyboardInterrupt:
        print("\nServicio de pagos detenido manualmente.")
