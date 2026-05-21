import requests
import random
import time
from datetime import datetime

SERVER_URL = "http://127.0.0.1:6039/logs"
TOKEN = "SERVICE1_TOKEN"

SEVERITIES = ["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]
MESSAGES = [
    "Usuario inició sesión",
    "Cache reconstruida correctamente",
    "Timeout en la conexión con base de datos",
    "Archivo de configuración no encontrado",
    "Servicio reiniciado automáticamente",
    "Token inválido detectado",
    "Operación completada con éxito"
]

def send_random_log():
    log = {
        "timestamp": datetime.now().isoformat(),
        "service": "auth-service",
        "severity": random.choice(SEVERITIES),
        "message": random.choice(MESSAGES)
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
        print("\nServicio detenido manualmente.")
