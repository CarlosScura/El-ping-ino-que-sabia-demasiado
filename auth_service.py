import requests
import random
import time
from datetime import datetime

SERVER_URL = "http://127.0.0.1:6039/logs"
TOKEN = "SERVICE1_TOKEN"

SEVERITY_MESSAGE = {
    "INFO": ["Usuario inició sesión",
            "Operación completada con éxito"],
    "DEBUG":["Cache reconstruida correctamente"],
    "WARNING":["Servicio reiniciado automáticamente"],
    "ERROR":["Timeout en la conexión con base de datos",
            "Token inválido detectado"],
    "CRITICAL":["Archivo de configuración no encontrado"]
}

def send_random_log():
    severity = random.choice(list(SEVERITY_MESSAGE.keys()))
    message = random.choice(SEVERITY_MESSAGE[severity])

    log = {
        "timestamp": datetime.now().isoformat(),
        "service": "auth-service",
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
        print("\nServicio detenido manualmente.")
