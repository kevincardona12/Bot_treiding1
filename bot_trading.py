import os
from flask import Flask
app = Flask(__name__)
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)

# Variables de entorno
TOKEN = os.getenv("TELEGRAM_TOKEN")
URL = os.getenv("RENDER_EXTERNAL_URL")

# Crear aplicación Flask y bot
app = Flask(__name__)
bot_app = ApplicationBuilder().token(TOKEN).build()

# Comandos del bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 ¡Bot activo! Usa /senal")

async def senal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Señal: 🟢 COMPRA (ejemplo)")

# Añadir comandos
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CommandHandler("senal", senal))

# Ruta webhook para Telegram
@app.route("/webhook", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    await bot_app.process_update(update)
    return "OK"

# Ejecutar en local o entorno con gunicorn
if __name__ == "__main__":
    import asyncio
    async def main():
        await bot_app.initialize()
        await bot_app.bot.set_webhook(f"{URL}/webhook")
        print("✅ Webhook conectado")
        await bot_app.start()
    asyncio.run(main())
