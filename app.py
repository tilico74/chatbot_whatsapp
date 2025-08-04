from flask import Flask, request
import os
from dotenv import load_dotenv
import requests

load_dotenv()



app = Flask(__name__)

VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')


@app.route("/", methods=["GET"])
def home():
    return "🚀 Servidor Flask do Chatbot WhatsApp está rodando!", 200

# Rota GET /webhook → usada para verificação inicial
@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("✅ Webhook verificado com sucesso!")
        return challenge, 200
    else:
        print("❌ Falha na verificação do webhook")
        return "Erro de verificação", 403

# Rota POST /webhook → usada para receber mensagens
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📩 Nova mensagem recebida:")
    print(data)

    try:
        entry = data["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        messages = value.get("messages")

        if messages:
            message = messages[0]
            phone_number_id = value["metadata"]["phone_number_id"]
            from_number = message["from"]  # número do remetente
            text = message["text"]["body"]  # texto da mensagem recebida

            print(f"📥 Mensagem de {from_number}: {text}")

            resposta = "👋 Olá! Sua mensagem foi recebida com sucesso!"

            url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"

            headers = {
                "Authorization": f"Bearer {os.getenv('TOKEN_WHATSAPP')}",
                "Content-Type": "application/json"
            }

            payload = {
                "messaging_product": "whatsapp",
                "to": from_number,
                "text": {"body": resposta}
            }

            r = requests.post(url, headers=headers, json=payload)
            print(f"📤 Resposta enviada: {r.status_code} - {r.text}")

    except Exception as e:
        print("❌ Erro ao processar mensagem:", e)

    return "EVENT_RECEIVED", 200

if __name__ == "__main__":    
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)