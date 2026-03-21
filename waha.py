import os
import requests

def _auth_headers():
    headers = {"Content-Type": "application/json"}
    api_key = os.getenv("WAHA_API_KEY", "").strip()
    if api_key:
        # Padrão comum do WAHA
        headers["X-Api-Key"] = api_key
    return headers

def send_message(chat_id: str, text: str, session: str | None = None) -> dict:
    """
    Envia mensagem de texto via WAHA.
    Requer:
      - WAHA_BASE_URL (ex.: http://waha:3000 dentro do Docker)
      - WAHA_SESSION (opcional; default 'default')
      - WAHA_API_KEY (recomendado)
    """
    base_url = os.getenv("WAHA_BASE_URL", "http://waha:3000").rstrip("/")
    session = session or os.getenv("WAHA_SESSION", "default")

    url = f"{base_url}/api/sendText"
    payload = {
        "session": session,
        "chatId": chat_id,
        "text": text
    }

    r = requests.post(url, json=payload, headers=_auth_headers(), timeout=30)
    r.raise_for_status()
    return r.json() if r.content else {"status": "ok"}