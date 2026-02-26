from datetime import datetime
from telegram import Update

def log(someText):
    print(f"{datetime.now()} {someText}")

async def send_to_user (update: Update,text:str):
    await update.message.reply_text(text)
