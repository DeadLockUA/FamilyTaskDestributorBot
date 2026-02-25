from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import datetime

#configuration section
TOKEN = "8601111376:AAHfAgJ7HAsm6zO2RqTIeeyysE0YGnp7CUM"

#Menu
keyboard = [
    ["Кнопка 1"],
    ["Кнопка 2"],
    ["Кнопка 3"]
]

reply_markup = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True
)






# message handler
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"UserId_{user.id}_activity_log.txt"
    with open(filename, "a", encoding="utf-8") as file:
        file.write(
            f"{timestamp} | {user.id} | {user.first_name} | {text}\n"
        )

    await update.message.reply_text(
    f"Привет, {user.first_name}!"
    f"Твой UserID, {user.id}!"
)

    await context.bot.send_message(
    chat_id=user.id,  # вставить ID другого пользователя
    text=f"{user.first_name} только что написал боту!"
)
    
    

    if text == "Кнопка 1":
        await update.message.reply_text("Ты нажал кнопку 1")
    elif text == "Кнопка 2":
        await update.message.reply_text("Это ответ для кнопки 2")
    elif text == "Кнопка 3":
        await update.message.reply_text("Вот сообщение для кнопки 3")
    else:
        await update.message.reply_text(
            "Выбери кнопку:",
            reply_markup=reply_markup
        )






#main app loop
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu))

app.run_polling()