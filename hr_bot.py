import logging
import settings
import requests

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(settings.HELP_MESSAGE)


async def text_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    logger.info("Incoming message: " + text)

    reply = get_reply(text)

    logger.info("Outgoing message: " + reply)
    await update.message.reply_text(reply)


def get_reply(text):
    words = text.split(" ")
    if len(words) == 2:
        amount = float(words[0].rstrip(','))
        currency = words[1].upper()
        gross = amount / 100 * 113
        result = convert(gross, words[1])
        return f"{amount} net RUB\n" \
               f"{gross} gross RUB\n" \
               f"{result} {currency}"

    return settings.DEFAULT_ANSWER


def convert(amount: float, currency: str):
    logger.info('Call convert API')

    url = rf"https://api.apilayer.com/exchangerates_data/convert?to={currency}&from=RUB&amount={amount}"
    payload = {}
    headers = {
        "apikey": settings.CURRENCY_API_TOKEN
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()['result']


def main() -> None:
    application = Application.builder().token(settings.TG_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_command))

    application.run_polling()


if __name__ == "__main__":
    main()
