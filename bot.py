import discord, os, aiohttp
from discord.ext import commands
from dotenv import load_dotenv
from weidian import search_in_stores

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("❌ No se encontró DISCORD_TOKEN en el archivo .env")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

ALLOWED_CHANNELS: set[int] = set()
waiting_for_keyword: dict[int, int] = {}
PREFIX = "yiltec:"


@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user} (ID: {bot.user.id})")
    print(f"🔍 Escuchando mensajes con '{PREFIX}'")


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    if ALLOWED_CHANNELS and message.channel.id not in ALLOWED_CHANNELS:
        return

    await bot.process_commands(message)

    has_image = any(
        att.content_type and att.content_type.startswith("image/")
        for att in message.attachments
    )
    text = message.content.strip()

    # Solo foto → pedir nombre
    if has_image and not text:
        waiting_for_keyword[message.author.id] = message.channel.id
        await message.reply(
            f"📝 ¿Qué producto es? Escribe `{PREFIX} marca modelo` y lo busco.",
            mention_author=False,
        )
        return

    # Ignorar mensajes sin el prefijo
    if not text.lower().startswith(PREFIX):
        return

    # Extraer keyword
    keyword = text[len(PREFIX):].strip()
    if not keyword:
        await message.reply(
            f"📝 Escribe algo después de `{PREFIX}`, por ejemplo: `{PREFIX} nike air force`",
            mention_author=False,
        )
        return

    waiting_for_keyword.pop(message.author.id, None)
    await _do_search(message, keyword)


async def _do_search(message: discord.Message, keyword: str):
    thinking = await message.reply("🔍 Buscando…", mention_author=False)

    results = search_in_stores(keyword)
    items = results.get("results", [])

    if not items:
        await thinking.edit(
            content="❌ No lo encuentro, avisa a **Mario** y él te lo encontrará."
        )
        return

    lines = ["**🛒 Productos encontrados:**"]
    for item in items:
        price = f"💶 {item['price_eur']}€" if item.get('price_eur') else ""
        lines.append(f"• **{item['name']}** {price}\n  <{item['link']}>")

    await thinking.edit(content="\n".join(lines))


@bot.command(name="ping")
async def ping(ctx):
    await ctx.reply(f"🏓 Pong! Latencia: {round(bot.latency * 1000)}ms")


if __name__ == "__main__":
    bot.run(TOKEN)
