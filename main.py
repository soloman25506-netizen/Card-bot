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

    # Examples:
    # 65: Ayanokoji Kiyotaka
    # 330: Class 3-E
    match = re.search(
        r"(?m)^\s*(\d+)\s*:",
        text
    )

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

    # Message ထဲက text / caption ကိုယူမယ်
    text = message.text or message.caption

    if not text:
        await message.reply_text(
            "❌ စာသားကို မဖတ်နိုင်ပါဘူး။"
        )
        return

    # ID ရှာမယ်
    character_id = find_id(text)

    if not character_id:
        await message.reply_text(
            "❌ ID မတွေ့ပါဘူး။\n\n"
            "ဥပမာ:\n"
            "65: Character Name"
        )
        return

    # .cgift ID
    gift_code = f".cgift {character_id}"

    # Copy button
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


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "🤖 Card Gift Bot\n\n"
        "Character message ကို ဒီ Bot ထဲ ပို့ပါ။\n\n"
        "Bot က ID ကိုရှာပြီး\n"
        ".cgift ID အဖြစ် Copy လုပ်လို့ရအောင် ပြပေးပါမယ်။"
    )


def main():
    if not TOKEN:
        raise RuntimeError(
            "BOT_TOKEN မသတ်မှတ်ထားပါ။"
        )

    app = Application.builder().token(TOKEN).build()

    # /start
    app.add_handler(
        MessageHandler(
            filters.COMMAND,
            start
        )
    )

    # Normal text / caption
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
