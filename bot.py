from telegram import Update, ParseMode
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Токен берётся из переменной среды

async def mention_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    me = await context.bot.get_chat_member(chat.id, context.bot.id)
    if me.status not in ['administrator', 'creator']:
        await update.message.reply_text("Я должен быть админом, чтобы упоминать участников.")
        return

    admins = await context.bot.get_chat_administrators(chat.id)
    mentions = []
    for admin in admins:
        user = admin.user
        if user.username:
            mentions.append(f"@{user.username}")
        else:
            mentions.append(f"[{user.first_name}](tg://user?id={user.id})")

    await update.message.reply_text(" ".join(mentions), parse_mode=ParseMode.MARKDOWN)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("all", mention_all))
app.add_handler(MessageHandler(filters.Regex(r"@all"), mention_all))
app.run_polling()
