from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Tokens válidos
VALID_TOKENS = {"SERVICE1_TOKEN", "SERVICE2_TOKEN"}

# Inicializar base de datos
def init_db():
    conn = sqlite3.connect("logs.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            service TEXT,
            severity TEXT,
            message TEXT,
            received_at TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route("/logs", methods=["POST"])
def receive_logs():
    # 1. Verificar token
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Token ") or auth_header.split()[1] not in VALID_TOKENS:
        return jsonify({"error": "Tu no sos mi bro, bro"}), 401

    # 2. Recibir logs (puede ser uno o varios)
    logs = request.get_json()
    if not isinstance(logs, list):
        logs = [logs]

    conn = sqlite3.connect("logs.db")
    c = conn.cursor()

    for log in logs:
        c.execute("""
            INSERT INTO logs (timestamp, service, severity, message, received_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            log.get("timestamp"),
            log.get("service"),
            log.get("severity"),
            log.get("message"),
            datetime.now().isoformat()
        ))
    conn.commit()
    conn.close()

    return jsonify({"status": "ok", "received": len(logs)})

if __name__ == "__main__":
    init_db()
    app.run(port=6039, debug=True)
