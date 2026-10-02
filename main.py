import os
import re

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")


def extract_data(text):
    if not text:
        return None

    # ID — ဥပမာ "65: Ayanokoji..."
    id_match = re.search(r"(?m)^\s*(\d+)\s*:", text)

    # Rarity — ဥပမာ "RARITY: Uncommon"
    rarity_match = re.search(
        r"RARITY\s*:\s*([^\n]+)",
        text,
        re.IGNORECASE
    )

    if not id_match or not rarity_match:
        return None

    character_id = id_match.group(1)
    rarity = rarity_match.group(1).strip()

    return character_id, rarity


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message

    if not message:
        return

    text = message.text or message.caption

    # Forward လုပ်ထားတဲ့ message ရဲ့ content ကိုဖတ်မယ်
    if message.forward_origin:
        text = message.text or message.caption

    result = extract_data(text)

    if not result:
        await message.reply_text(
            "❌ ID / Rarity မတွေ့ပါဘူး။\n\n"
            "Character Catcher message ကို ဒီ Bot ထဲ Forward လုပ်ပါ။"
        )
        return

    character_id, rarity = result
    gift = f".gift {character_id}"

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📋 Copy",
                callback_data=f"copy:{character_id}"
            )
        ]
    ])

    await message.reply_text(
        f"⭐ Rarity: {rarity}\n"
        f"🆔 ID: {character_id}\n\n"
        f"<code>{gift}</code>\n\n"
        f"Copy လုပ်ဖို့ အောက်က Button ကိုနှိပ်ပါ။",
        parse_mode="HTML",
        reply_markup=keyboard
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Card Gift Bot\n\n"
        "Character Catcher message ကို ဒီထဲ Forward လုပ်ပါ။\n"
        "ID + Rarity ကို အလိုအလျောက်ထုတ်ပေးပါမယ်။"
    )


def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN မရှိပါ")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(filters.COMMAND, start)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT | filters.CaptionRegex(".+"),
            handle_message
        )
    )

    print("Bot running...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
