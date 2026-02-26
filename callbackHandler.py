import DBHandler
from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from communication_handler import log,send_to_user


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    log("Entering button_handler")
    query = update.callback_query

    await query.answer()  

    data = query.data

    log(f"Button_Pressed: {data}")
    if data == "create_task":
        log("Starting to handle create_task button")
        user_id = update.effective_user.id
        user_states[user_id] = {
            "task": task_selection_states[0],           #CREATE_TASK
            "step": task_creation_states[0],            #WAITING_FOR_TASK_NAME
            "task_data": {}
        }
        await query.edit_message_text("Please enter task name:")

    elif data == "my_tasks":
        await query.edit_message_text("Here are your tasks 📋")

    elif data == "help":
        await query.edit_message_text("Help section ❓")