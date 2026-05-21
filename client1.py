import requests
from datetime import datetime

# URL del servidor central
SERVER_URL = "http://127.0.0.1:6039/logs"

# Token válido para este servicio
TOKEN = "SERVICE1_TOKEN"

def send_log():
    # Armar un log falso
    log = {
        "timestamp": datetime.now().isoformat(),
        "service": "auth-service",
        "severity": "ERROR",
        "message": "Intento de login fallido"
    }

    # Enviar el log al servidor
    response = requests.post(
        SERVER_URL,
        json=log,
        headers={"Authorization": f"Token {TOKEN}"}
    )

    print("Respuesta del servidor:", response.json())

if __name__ == "__main__":
    send_log()
