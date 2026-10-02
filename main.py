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


def find_id(text):
    if not text:
        return None

    # 65: Character Name
    # 330: Class 3-E
    match = re.search(r"(?m)^\s*(\d+)\s*:", text)

    if match:
        return match.group(1)

    return None


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    message = update.effective_message

    if not message:
        return

    text = message.text or message.caption

    if not text:
        return

    character_id = find_id(text)

    if not character_id:
        await message.reply_text(
            "❌ ID မတွေ့ပါဘူး။"
        )
        return

    gift_code = f".gift {character_id}"

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📋 Copy",
                copy_text=CopyTextButton(
                    text=gift_code
                )
            )
        ]
    ])

    await message.reply_text(
        f"🆔 ID: {character_id}\n\n"
        f"<code>{gift_code}</code>",
        parse_mode="HTML",
        reply_markup=keyboard
    )


def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN မရှိပါ")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT | filters.CAPTION,
            handle_message
        )
    )

    print("Bot running...")

    app.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
