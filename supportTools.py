from globalVariables import logger
from datetime import datetime, timedelta
from telegram import Update
import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def log(someText):
    print(f"{datetime.now()} {someText}")

async def send_to_user(update: Update, text: str, reply_markup = None):
    logger.warning(f"send_to_user tex={text}, markup = {reply_markup}")
    await update.effective_chat.send_message(text,reply_markup=reply_markup)

def parse_deadline(user_input: str):
    user_input = user_input.strip().lower()
    now = datetime.now()

    # --- RELATIVE FORMAT (1h, 2d, 3m, 4y) ---
    match = re.match(r"^(\d+)([hdmy])$", user_input)

    if match:
        value = int(match.group(1))
        unit = match.group(2)

        if unit == "h":
            return now + timedelta(hours=value)

        elif unit == "d":
            return now + timedelta(days=value)

        elif unit == "m":
            # 1 month ≈ 30 days
            return now + timedelta(days=value * 30)

        elif unit == "y":
            # 1 year ≈ 365 days
            return now + timedelta(days=value * 365)

    # --- ABSOLUTE DATE (dd-mm-yyyy) ---
    try:
        return datetime.strptime(user_input, "%d-%m-%Y")
    except ValueError:
        pass

    # --- INVALID FORMAT ---
    return None


def get_support_menu_markup():
    #Returns just the support/help part of the menu
    keyboard = [
        [
            InlineKeyboardButton("🏠 Main Menu", callback_data="/start"),
            InlineKeyboardButton("ℹ️ Help/Info", callback_data="/help")            
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_main_menu_markup():
    #Returns the full main menu, including support row
    keyboard = [
        [
            InlineKeyboardButton("➕ New task", callback_data="create_task"),
            InlineKeyboardButton("📋 My Tasks",      callback_data="get_my_tasks_menu")
        ],
        # Reuse the support row upacked
        *get_support_menu_markup().inline_keyboard 
    ]
    
    return InlineKeyboardMarkup(keyboard)

def get_priority_markup():
    #Returns the full main menu, including support row
    keyboard = [
        [
            InlineKeyboardButton("🔴 0 - Super Urgent", callback_data="set_priority/0"),
        ],
        [
            InlineKeyboardButton("🟠 1 - High", callback_data="set_priority/1"),
        ],
        [
            InlineKeyboardButton("🟡 2 - Medium", callback_data="set_priority/2"),
        ],
        [
            InlineKeyboardButton("🟢 3 - Low", callback_data="set_priority/3"),
        ],
        [
            InlineKeyboardButton("🔵 4 - Relaxed", callback_data="set_priority/4")
        ],
        # Reuse the support row upacked
        *get_support_menu_markup().inline_keyboard 
    ]
    
    return InlineKeyboardMarkup(keyboard)


def get_task_menu_markup():
    #Returns the full main menu, including support row
    keyboard = [
        [
            InlineKeyboardButton("📋Task history", callback_data="show_my_task_history"),
            InlineKeyboardButton("✍️Active tasks", callback_data="show_my_task_list")
        ],
        # Reuse the support row upacked
        *get_support_menu_markup().inline_keyboard 
    ]

    return InlineKeyboardMarkup(keyboard)

