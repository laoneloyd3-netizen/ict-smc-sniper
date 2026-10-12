import os, hmac, requests
from flask import Flask, request, abort, jsonify
app = Flask(__name__)
BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "").strip()
PUBLIC_URL = os.environ.get("RENDER_EXTERNAL_URL", "").rstrip("/")

def api(method, payload):
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not configured")
    r = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/{method}", json=payload, timeout=15)
    r.raise_for_status()
    return r.json()

def send(chat_id, text):
    return api("sendMessage", {"chat_id": chat_id, "text": text})

@app.get("/")
def home():
    return jsonify({"service":"ICT SMC Sniper Telegram connector","status":"running",
                    "note":"Test connector only; live Deriv analysis is not connected."})

@app.get("/health")
def health():
    return jsonify({"ok": True})

@app.post("/webhook")
def webhook():
    supplied = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
    if not WEBHOOK_SECRET or not hmac.compare_digest(supplied, WEBHOOK_SECRET):
        abort(403)
    update = request.get_json(silent=True) or {}
    msg = update.get("message") or update.get("edited_message") or {}
    chat_id = (msg.get("chat") or {}).get("id")
    text = (msg.get("text") or "").strip()
    if chat_id and text:
        if text.startswith("/start"):
            reply = ("ICT SMC Sniper bot is connected!\n\nCommands: /status, /help\n\n"
                     "Important: live Deriv data and ICT/SMC analysis are NOT connected yet. "
                     "This is only a Telegram connection test.")
        elif text.startswith("/status"):
            reply = "Telegram connector is online. Live market analysis is not connected yet."
        elif text.startswith("/help"):
            reply = "Available commands: /start, /status, /help"
        else:
            reply = "Message received. Telegram connector works; live trading analysis is not connected yet."
        send(chat_id, reply)
    return jsonify({"ok": True})

@app.get("/setup-webhook")
def setup_webhook():
    setup_key = os.environ.get("SETUP_KEY", "").strip()
    if not setup_key or not hmac.compare_digest(request.args.get("key", ""), setup_key):
        abort(403)
    if not BOT_TOKEN or not WEBHOOK_SECRET or not PUBLIC_URL:
        return jsonify({"ok":False,"error":"Set BOT_TOKEN, WEBHOOK_SECRET and wait for Render service URL."}), 400
    return jsonify(api("setWebhook", {"url":PUBLIC_URL+"/webhook","secret_token":WEBHOOK_SECRET,
                                     "drop_pending_updates":True}))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT","10000")))
