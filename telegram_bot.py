import os, logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from weidian import search_in_stores

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("❌ No se encontró TELEGRAM_TOKEN en el archivo .env")

logging.basicConfig(level=logging.INFO)

# Usuarios esperando que escriban el nombre tras mandar foto
waiting_for_keyword: dict[int, bool] = {}


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return

    user_id = message.from_user.id
    text = (message.text or "").strip()
    has_photo = bool(message.photo)

    # Solo foto → pedir nombre
    if has_photo and not text:
        waiting_for_keyword[user_id] = True
        await message.reply_text("📝 ¿Qué producto es? Escribe la marca y el modelo y lo busco.")
        return

    # Foto + caption → buscar directamente
    if has_photo and message.caption:
        keyword = message.caption.strip()
        waiting_for_keyword.pop(user_id, None)
        await _do_search(message, keyword)
        return

    # Texto → buscar directamente (en Telegram no hace falta prefijo)
    if text:
        waiting_for_keyword.pop(user_id, None)
        await _do_search(message, text)
        return


async def _do_search(message, keyword: str):
    thinking = await message.reply_text("🔍 Buscando…")

    results = search_in_stores(keyword)
    items = results.get("results", [])

    if not items:
        await thinking.edit_text("❌ No lo encuentro, avisa a *Mario* y él te lo encontrará.", parse_mode="Markdown")
        return

    lines = ["*🛒 Productos encontrados:*"]
    for item in items:
        price = f"💶 {item['price_eur']}€" if item.get("price_eur") else ""
        # En Telegram los links entre <> no hacen falta, no genera previews
        lines.append(f"• *{item['name']}* {price}\n  {item['link']}")

    await thinking.edit_text("\n".join(lines), parse_mode="Markdown", disable_web_page_preview=True)


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_message))
    print("✅ Bot de Telegram arrancado")
    app.run_polling()


if __name__ == "__main__":
    main()
