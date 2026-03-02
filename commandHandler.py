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

async def start_dialog_handler (update: Update, context: ContextTypes.DEFAULT_TYPE = None):
    await messageHandler.reset_dialog(update)

async def show_help_menu(update: Update, context: ContextTypes.DEFAULT_TYPE = None):
    help_text = (
        "📋 <b>Family Task Distributor Bot — Help</b>\n\n"
        "This bot helps your family share, assign and track tasks easily.\n"
        "Create tasks, mark progress, review what needs to be done — all in one place.\n\n"
        
        "<b>Main commands & features:</b>\n"
        "• /start — start the bot and see the main menu\n"
        "• Main menu buttons:\n"
        "  👥 Assign new task — create a new task for someone in the family\n"
        "  📋 My Tasks — show your current tasks (open / in progress)\n"
        "  ❓ Help — show this help message\n\n"
        
        "<b>How to work with tasks:</b>\n"
        "1. Press «Assign new task» → follow the steps to create a task\n"
        "2. In «My Tasks» you can:\n"
           "   • Review details of any task\n"
           "   • Change status (mark as done, cancelled, etc.)\n"
           "   • Go back to the list or main menu\n\n"
        
        "<b>Task statuses (current system):</b>\n"
        "🆕 New / Open\n"
        "✅ Completed\n"
        "❌ Cancelled\n"
        "(more statuses can be added later)\n\n"
        
        "<b>Tips:</b>\n"
        "• Long task titles are shortened in lists — open the task to see full text\n"
        "• Deadlines are shown when you review a task\n"
        "• Creator and owner/assigned person are displayed in task details\n\n"
        
        "Have questions or ideas? Feel free to tell the bot creator 😊\n\n"
        
        "<i>Bot version: early development (March 2026)</i>"
    )   

    await messageHandler.reset_dialog(update,help_text)
    
   