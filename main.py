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

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def find_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message

    if not message:
        return

    # Text / Photo Caption
    text = message.text or message.caption

    if not text:
        return

    # Rarity ပါရမယ်
    rarity = re.search(
        r"\bRARITY\s*:\s*(?:Legendary|Mystical|Mythical|Rare|Uncommon|Common)\b",
        text,
        re.IGNORECASE
    )

    if not rarity:
        return

    # Card ID ရှာမယ်
    # ဥပမာ - 6969: Nishikigi Chisato
    id_match = re.search(
        r"(?<!\d)(\d{2,10})\s*:",
        text
    )

    if not id_match:
        return

    card_id = id_match.group(1)
    gift = f".gift {card_id}"

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=f"📋 Copy {gift}",
                copy_text=CopyTextButton(text=gift)
            )
        ]
    ])

    await message.reply_text(
        f"🎴 Card ID: `{card_id}`\n"
        f"⭐ Rarity: `{rarity.group(0)}`\n\n"
        f"`{gift}`",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT | filters.PHOTO,
            find_card
        )
    )

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
