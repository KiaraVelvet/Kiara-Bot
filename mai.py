import os
import logging
import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import requests

# Zmienne środowiskowe
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("MODEL", "mythomax-l2-13b")

# Konfiguracja logów
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Funkcja komunikacji z modelem AI
def query_openrouter(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": f"openrouter/{MODEL}",
        "messages": [
            {"role": "system", "content": "You are Kiara – a seductive, dominant woman who speaks both Polish and English. You always respond in the same language as the user. Your style is erotic, playful, confident, and feminine. If someone speaks Polish, you reply in Polish. If they write in English, you reply in English."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "Błąd w odpowiedzi AI."

# Obsługa wiadomości
async def handle_message(update, context):
    prompt = update.message.text
    reply = query_openrouter(prompt)
    await update.message.reply_text(reply)

# Start
async def start(update, context):
    await update.message.reply_text("Cześć, jestem Kiara 😈 Napisz do mnie coś niegrzecznego...")

# Uruchomienie bota
def main():
    application = Application.builder().token(TELEGRAM_API_KEY).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()
