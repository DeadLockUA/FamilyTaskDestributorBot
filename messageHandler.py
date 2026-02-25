import DBHandler
from telegram import Update,ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

requests = ["Show my tasks", "Assign task"]

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not DBHandler.get_user_by_telegram_id(user_id):
        print("User is not registered")
        print(f"Registering new user: {user_id}, {update.effective_user.full_name} as regular user")
        DBHandler.add_user(user_id, update.effective_user.full_name, "User")
    
    user_text = update.message.text

    if not user_text in requests:
        await show_menu (update,context)
        #await update.message.reply_text("Request is not clear")
    else:
        await update.message.reply_text(f"Request is: {user_text}")



async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("👥 Show Users", callback_data="show_users"),
            InlineKeyboardButton("📋 My Tasks", callback_data="my_tasks")
        ],
        [
            InlineKeyboardButton("❓ Help", callback_data="help")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Choose an option:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()  

    data = query.data

    if data == "show_users":
        await query.edit_message_text("Here are all users 👥")
        

    elif data == "my_tasks":
        await query.edit_message_text("Here are your tasks 📋")

    elif data == "help":
        await query.edit_message_text("Help section ❓")

    

    