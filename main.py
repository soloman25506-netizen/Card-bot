import os
import re

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CopyTextButton
from telegram.ext import Application, MessageHandler, ContextTypes, filters


TOKEN = os.getenv("BOT_TOKEN")


def parse_character(text):
    # Rarity
    rarity_match = re.search(
        r"RARITY\s*:\s*([A-Za-z]+)",
        text,
        re.IGNORECASE
    )

    if not rarity_match:
        return None

    rarity = rarity_match.group(1).strip()

    # ID
    # Example: 330: Class 3-E
    id_match = re.search(
        r"(?:^|\n|\s)(\d+)\s*:",
        text
    )

    if not id_match:
        return None

    character_id = id_match.group(1)

    return rarity, character_id


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message

    if not message or not message.text:
        return

    result = parse_character(message.text)

    if not result:
        return

    rarity, character_id = result

    gift_command = f".gift {character_id}"

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text="📋 Copy .gift",
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


def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN is not set")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
