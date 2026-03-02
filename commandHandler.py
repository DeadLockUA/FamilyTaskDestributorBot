import DBHandler
from telegram import Update
from telegram.ext import ContextTypes
import messageHandler

async def show_users_handler(update: Update,context: ContextTypes.DEFAULT_TYPE):
    
    users = DBHandler.get_all_users()

    if not users:
        await update.message.reply_text("No users found.")
        return

    message = "👥 Users:\n\n"

    for user in users:
        message += f"ID: {user['id']}\n"
        message += f"Name: {user['name']}\n"
        message += f"Role: {user['role']}\n\n"

    await update.message.reply_text(message)

async def start_dialog_handler (update: Update,context: ContextTypes.DEFAULT_TYPE):
    await messageHandler.reset_dialog(update)

async def show_help_menu (update: Update,context: ContextTypes.DEFAULT_TYPE):
    

    await messageHandler.reset_dialog(update)
    
   