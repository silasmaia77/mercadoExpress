import os
import json
from flask import Flask, request, jsonify
import redis

from src.database import init_db

app = Flask(__name__)

# Inicializa DB (cria tabelas se não existirem)
init_db()

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
rdb = redis.Redis.from_url(REDIS_URL, decode_responses=True)

QUEUE_KEY = "queue:incoming"

def _unauthorized():
    return jsonify({"status": "unauthorized"}), 401

@app.route("/webhook", methods=["POST"])
def webhook():
    expected = os.getenv("WEBHOOK_TOKEN", "").strip()
    got = request.headers.get("X-Webhook-Token", "").strip()

    if expected and got != expected:
        return _unauthorized()

    data = request.json or {}
    payload = data.get("payload", {}) if isinstance(data, dict) else {}

    sender = payload.get("from")
    message_body = payload.get("body")
    from_me = payload.get("fromMe", False)

    # Id (depende da versão; tentamos vários)
    message_id = payload.get("id") or payload.get("messageId") or payload.get("message_id")

    # Ignorar vazios, status, ou mensagens do próprio bot
    if not sender or not message_body or from_me:
        return jsonify({"status": "ignored"}), 200

    job = {
        "sender": sender,
        "text": message_body,
        "message_id": message_id,
        "raw": payload,
    }

    # Enfileira (rápido)
    rdb.rpush(QUEUE_KEY, json.dumps(job, ensure_ascii=False))

    return jsonify({"status": "queued"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)