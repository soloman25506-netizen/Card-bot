import os
import re

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CopyTextButton,
)
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")


def parse_character(text):
    if not text:
        return None

    # Rarity
    rarity_match = re.search(
        r"RARITY\s*:\s*([^\n]+)",
        text,
        re.IGNORECASE
    )

    # ID
    # Example:
    # 330: Class 3-E
    id_match = re.search(
        r"(?m)^\s*(\d+)\s*:",
        text
    )

    if not rarity_match or not id_match:
        return None

    rarity = rarity_match.group(1).strip()
    character_id = id_match.group(1)

    return rarity, character_id


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    message = update.effective_message

    if not message:
        return

    # User က Reply ထားတဲ့ message ကို အရင်ဖတ်မယ်
    source_text = None

    if message.reply_to_message:
        replied = message.reply_to_message

        source_text = (
            replied.text
            or replied.caption
        )

    # Reply မဟုတ်ရင် ကိုယ်ပို့တဲ့စာကို ဖတ်မယ်
    if not source_text:
        source_text = message.text or message.caption

    result = parse_character(source_text)

    if not result:
        return

    rarity, character_id = result

    gift_command = f".gift {character_id}"

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📋 Copy .gift",
                copy_text=CopyTextButton(
                    text=gift_command
                )
            )
        ]
    ])

    await message.reply_text(
        f"⭐ Rarity: {rarity}\n"
        f"🆔 ID: {character_id}\n\n"
        f"<code>{gift_command}</code>",
        parse_mode="HTML",
        reply_markup=keyboard
    )


async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):
    print("ERROR:", context.error)


def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN is not set")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.ALL,
            handle_message
        )
    )

    app.add_error_handler(error_handler)

    print("Bot running...")

    app.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
