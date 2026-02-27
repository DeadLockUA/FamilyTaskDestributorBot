from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler,CommandHandler, filters, ContextTypes
import DBHandler
import messageHandler
import commandHandler
import callbackHandler
from  supportTools import log
from telegram.ext import CallbackQueryHandler

#configuration section
TOKEN = "8601111376:AAHfAgJ7HAsm6zO2RqTIeeyysE0YGnp7CUM"
DBHandler.create_tables()

#DBHandler.add_user(12345, "testName", "Admin")


#main app loop

log("Starting Bot")
app = ApplicationBuilder().token(TOKEN).build()
log("Bot is up and running. Waiting for user requests............")

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messageHandler.message_handler))
app.add_handler(CommandHandler("ShowUsers",commandHandler.show_users_handler ))
app.add_handler(CallbackQueryHandler(callbackHandler.button_handler))

app.run_polling()

