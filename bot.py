from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler,CommandHandler, filters, ContextTypes
import datetime
import sqlite3
import DBHandler
import messageHandler
import commandHandler
from telegram.ext import CallbackQueryHandler

#configuration section
TOKEN = "8601111376:AAHfAgJ7HAsm6zO2RqTIeeyysE0YGnp7CUM"
DBHandler.create_tables()

#DBHandler.add_user(12345, "testName", "Admin")

user = DBHandler.get_user_by_telegram_id(123456)



#main app loop


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messageHandler.message_handler_default))
app.add_handler(CommandHandler("ShowUsers",commandHandler.show_users_handler ))
app.add_handler(CallbackQueryHandler(messageHandler.button_handler))

app.run_polling()

