from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Tokens válidos
VALID_TOKENS = {"SERVICE1_TOKEN", "SERVICE2_TOKEN","SERVICE3_TOKEN"}

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
        return jsonify({"error": "Tu no eres mi bro, bro"}), 401

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

@app.route("/logs", methods=["GET"])
def get_logs():
    # Parámetros opcionales
    timestamp_start = request.args.get("timestamp_start")
    timestamp_end = request.args.get("timestamp_end")
    received_start = request.args.get("received_at_start")
    received_end = request.args.get("received_at_end")

    conn = sqlite3.connect("logs.db")
    c = conn.cursor()

    query = "SELECT id, timestamp, service, severity, message, received_at FROM logs WHERE 1=1"
    params = []

    # Filtros dinámicos
    if timestamp_start:
        query += " AND timestamp >= ?"
        params.append(timestamp_start)
    if timestamp_end:
        query += " AND timestamp <= ?"
        params.append(timestamp_end)
    if received_start:
        query += " AND received_at >= ?"
        params.append(received_start)
    if received_end:
        query += " AND received_at <= ?"
        params.append(received_end)

    query += " ORDER BY received_at DESC"

    c.execute(query, params)
    rows = c.fetchall()
    conn.close()

    # Convertir a lista de diccionarios
    logs = [
        {
            "id": row[0],
            "timestamp": row[1],
            "service": row[2],
            "severity": row[3],
            "message": row[4],
            "received_at": row[5]
        }
        for row in rows
    ]

    return jsonify(logs)


if __name__ == "__main__":
    init_db()
    app.run(port=6039, debug=True)
