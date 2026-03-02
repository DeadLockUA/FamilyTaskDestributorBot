from typing import Optional

from telegram import Bot, InlineKeyboardMarkup
from telegram.error import TelegramError
from telegram.constants import ParseMode
from globalVariables import logger

# Adjust import to your project structure
from botToken import TOKEN      

# Lazy-loaded bot instance
_bot: Optional[Bot] = None


def get_bot() -> Bot:
    """Lazy initialization of Bot instance."""
    global _bot
    if _bot is None:
        _bot = Bot(token=TOKEN)
    return _bot


# ──────────────────────────────────────────────────────────────────────────────
# Core low-level send function (by chat_id)
# ──────────────────────────────────────────────────────────────────────────────

async def send_notification(
    chat_id: int,
    text: str,
    parse_mode: str = ParseMode.HTML,
    disable_web_page_preview: bool = True,
    disable_notification: bool = False,
    reply_markup: Optional[InlineKeyboardMarkup] = None,
) -> bool:
    """
    Send a message/notification to a specific Telegram chat_id.

    Returns True if successful, False otherwise.
    """
    bot = get_bot()

    try:
        await bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            reply_markup=reply_markup,
        )
        logger.info(f"Message sent to chat_id={chat_id}")
        return True

    except TelegramError as e:
        logger.error(f"Failed to send message to chat_id={chat_id}: {e}")
        return False


# ──────────────────────────────────────────────────────────────────────────────
# High-level: send by internal user_id (your owner_id / user_id)
# ──────────────────────────────────────────────────────────────────────────────

async def send_message_by_user_id(
    user_id: int,
    text: str,
    parse_mode: str = ParseMode.HTML,
    disable_notification: bool = False,
    reply_markup: Optional[InlineKeyboardMarkup] = None,
) -> bool:
    """
    Send a message to a user by their INTERNAL user_id (from your database).

    Looks up the corresponding telegram_id (chat_id) and sends the message.

    Returns:
        bool: True if message was sent successfully
    """
    chat_id = user_id

    if chat_id is None:
        logger.warning(f"Cannot send message: no telegram_id found for user_id={user_id}")
        return False

    return await send_notification(
        chat_id=chat_id,
        text=text,
        parse_mode=parse_mode,
        disable_notification=disable_notification,
        reply_markup=reply_markup,
    )
