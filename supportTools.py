from datetime import datetime, timedelta
from telegram import Update
import re

def log(someText):
    print(f"{datetime.now()} {someText}")


async def send_to_user(update: Update, text: str):
    if update.message:
        await update.message.reply_text(text)
    elif update.callback_query:
        await update.callback_query.message.reply_text(text)


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