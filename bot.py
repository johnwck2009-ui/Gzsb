import json
import logging
import os
from pathlib import Path

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CONTENT_FILE = Path(__file__).with_name("content.json")


def load_content():
    try:
        with CONTENT_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError):
        logger.exception("Could not read content.json")
        return {"news": [], "standings": {}}


def home_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ព័ត៌មានបាល់ទាត់", callback_data="news"),
            InlineKeyboardButton("តារាងចំណាត់ថ្នាក់", callback_data="standings"),
        ]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "សូមស្វាគមន៍មកកាន់ GZSB24\n\n"
        "ប្រភពព័ត៌មានបាល់ទាត់ និងតារាងចំណាត់ថ្នាក់លីគ។\n"
        "សូមជ្រើសរើសមុខងារខាងក្រោម។"
    )
    await update.effective_message.reply_text(message, reply_markup=home_keyboard())


async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    items = load_content().get("news", [])
    if not items:
        text = "មិនទាន់មានព័ត៌មានបាល់ទាត់ទេ។ សូមពិនិត្យម្តងទៀតនៅពេលក្រោយ។"
    else:
        text = "ព័ត៌មានបាល់ទាត់\n\n" + "\n\n".join(
            f"• {item.get('title', 'ព័ត៌មាន')}\n{item.get('summary', '')}"
            for item in items
        )
    await update.effective_message.reply_text(text, reply_markup=home_keyboard())


async def standings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    leagues = load_content().get("standings", {})
    if not leagues:
        text = (
            "មិនទាន់មានតារាងចំណាត់ថ្នាក់ទេ។\n"
            "ទិន្នន័យនេះត្រូវបានធ្វើបច្ចុប្បន្នភាពដោយដៃ ហើយមិនមែនជាទិន្នន័យផ្ទាល់ទេ។"
        )
    else:
        sections = ["តារាងចំណាត់ថ្នាក់លីគ"]
        for league, rows in leagues.items():
            sections.append(f"\n{league}")
            sections.extend(
                f"{row.get('pos', i)}. {row.get('team', 'ក្រុម')} — "
                f"{row.get('points', 0)} ពិន្ទុ"
                for i, row in enumerate(rows, start=1)
            )
        sections.append("\nចំណាំ៖ តារាងត្រូវបានធ្វើបច្ចុប្បន្នភាពដោយដៃ មិនមែនជាទិន្នន័យផ្ទាល់ទេ។")
        text = "\n".join(sections)
    await update.effective_message.reply_text(text, reply_markup=home_keyboard())


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "news":
        await news_from_callback(query, context)
    elif query.data == "standings":
        await standings_from_callback(query, context)


async def news_from_callback(query, context):
    items = load_content().get("news", [])
    if not items:
        text = "មិនទាន់មានព័ត៌មានបាល់ទាត់ទេ។ សូមពិនិត្យម្តងទៀតនៅពេលក្រោយ។"
    else:
        text = "ព័ត៌មានបាល់ទាត់\n\n" + "\n\n".join(
            f"• {item.get('title', 'ព័ត៌មាន')}\n{item.get('summary', '')}"
            for item in items
        )
    await query.message.reply_text(text, reply_markup=home_keyboard())


async def standings_from_callback(query, context):
    leagues = load_content().get("standings", {})
    if not leagues:
        text = (
            "មិនទាន់មានតារាងចំណាត់ថ្នាក់ទេ។\n"
            "ទិន្នន័យនេះត្រូវបានធ្វើបច្ចុប្បន្នភាពដោយដៃ ហើយមិនមែនជាទិន្នន័យផ្ទាល់ទេ។"
        )
    else:
        sections = ["តារាងចំណាត់ថ្នាក់លីគ"]
        for league, rows in leagues.items():
            sections.append(f"\n{league}")
            sections.extend(
                f"{row.get('pos', i)}. {row.get('team', 'ក្រុម')} — "
                f"{row.get('points', 0)} ពិន្ទុ"
                for i, row in enumerate(rows, start=1)
            )
        sections.append("\nចំណាំ៖ តារាងត្រូវបានធ្វើបច្ចុប្បន្នភាពដោយដៃ មិនមែនជាទិន្នន័យផ្ទាល់ទេ។")
        text = "\n".join(sections)
    await query.message.reply_text(text, reply_markup=home_keyboard())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "ពាក្យបញ្ជា៖\n"
        "/start - បើកម៉ឺនុយដើម\n"
        "/news - ព័ត៌មានបាល់ទាត់\n"
        "/standings - តារាងចំណាត់ថ្នាក់លីគ\n"
        "/help - ជំនួយ",
        reply_markup=home_keyboard(),
    )


def main():
    if not BOT_TOKEN:
        raise RuntimeError("Set TELEGRAM_BOT_TOKEN in your environment before starting the bot.")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(CommandHandler("standings", standings))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    logger.info("GZSB24 Football bot is starting")
    app.run_polling()


if __name__ == "__main__":
    main()
