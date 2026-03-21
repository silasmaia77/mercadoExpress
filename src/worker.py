import os
import json
import time
import redis

from src.agent import get_agent
from src.database import init_db
from waha import send_message

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
QUEUE_KEY = "queue:incoming"

# DB init
init_db()

rdb = redis.Redis.from_url(REDIS_URL, decode_responses=True)

# Cache de agentes por cliente (memória do processo)
active_agents: dict[str, object] = {}

def get_or_create_agent(sender_id: str):
    if sender_id not in active_agents:
        print(f"🧠 Criando novo cérebro para: {sender_id}")
        active_agents[sender_id] = get_agent()
    return active_agents[sender_id]

def already_processed(message_id: str | None) -> bool:
    """
    Idempotência simples usando Redis SET.
    """
    if not message_id:
        return False
    key = "processed:message_ids"
    added = rdb.sadd(key, message_id)
    # added == 1 se inseriu agora; 0 se já existia
    return added == 0

def main():
    print("⚙️ Worker iniciado. Aguardando jobs...")

    while True:
        try:
            item = rdb.blpop(QUEUE_KEY, timeout=30)
            if not item:
                continue

            _, raw_job = item
            job = json.loads(raw_job)

            sender = job.get("sender")
            text = job.get("text", "")
            message_id = job.get("message_id")

            if not sender or not text:
                continue

            if already_processed(message_id):
                print(f"🔁 Ignorado (duplicado) message_id={message_id}")
                continue

            print(f"📩 Job de {sender}: {text}")

            agent = get_or_create_agent(sender)
            response = agent.chat(text)
            reply_text = str(response)

            print(f"🤖 Resposta para {sender}: {reply_text}")
            send_message(chat_id=sender, text=reply_text)

        except Exception as e:
            print(f"❌ Erro no worker: {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()