import requests
import random
import time
from datetime import datetime

SERVER_URL = "http://127.0.0.1:6039/logs"
TOKEN = "SERVICE3_TOKEN"

SEVERITY_MESSAGES = {
    "INFO": [
        "Inventario actualizado correctamente",
        "Nuevo producto agregado al stock"
    ],
    "DEBUG": [
        "Consulta de stock ejecutada"
    ],
    "WARNING": [
        "Stock bajo detectado en producto"
    ],
    "ERROR": [
        "Error al sincronizar inventario con base de datos",
        "Producto no encontrado en el sistema"
    ],
    "CRITICAL": [
        "Fallo crítico en el sistema de inventario"
    ]
}

def send_random_log():
    severity = random.choice(list(SEVERITY_MESSAGES.keys()))
    message = random.choice(SEVERITY_MESSAGES[severity])

    log = {
        "timestamp": datetime.now().isoformat(),
        "service": "inventory-service",
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
        print("\nServicio de inventario detenido manualmente.")
