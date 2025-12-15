from telegram.ext import Application
from telegram import Update, BotCommand


from handlers.start import register_conf_handler
from handlers.error import error_handler
from config.settings import BOT_TOKEN

Commands = [
    BotCommand('start', description='Botni qayta ishga tushurish')
]

async def post_init(application: Application):
    await application.bot.set_my_commands(Commands)
    print("Bot commands have been set.")


def main():
    bot = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    bot.add_handler(register_conf_handler)
    bot.add_error_handler(error_handler)

    bot.run_polling(allowed_updates=Update.ALL_TYPES)