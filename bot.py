from telegram import Update, ReplyKeyboardMarkup
from botToken import TOKEN #import token for your telegram bot. 
from telegram.ext import ApplicationBuilder, MessageHandler,CommandHandler, filters, ContextTypes
import DBHandler
import messageHandler
import commandHandler
import callbackHandler
from  supportTools import log
from telegram.ext import CallbackQueryHandler
from globalVariables import logger

#configuration section
DBHandler.create_tables()

#DBHandler.add_user(12345, "testName", "Admin")
#DBHandler.add_user(123456, "testName2", "Admin")


#main app loop
logger.info("Starting Bot")
app = ApplicationBuilder().token(TOKEN).build()
log("Bot is up and running. Waiting for user requests............")

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messageHandler.message_handler))
app.add_handler(CommandHandler("ShowUsers",commandHandler.show_users_handler ))
app.add_handler(CommandHandler("Start",commandHandler.start_dialog_handler ))
app.add_handler(CommandHandler("Help",commandHandler.show_help_menu ))
app.add_handler(CallbackQueryHandler(callbackHandler.button_handler))

app.run_polling()

