from django.db import IntegrityError
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

User = get_user_model()

GET_PHONE, SAVE_DATA = range(2)

@sync_to_async
def get_user(telegram_id):
    try:
        return User.objects.filter(telegram_id=telegram_id).first()
    except User.DoesNotExist:
        return None

@sync_to_async
def create_user(phone_number, telegram_id):
    try:
        user = User.objects.create_user(
            phone_number=str(phone_number),
            password=str(telegram_id),
            telegram_id=telegram_id,
            is_active=False
        )
        return user
    except IntegrityError as e:
        print("IntegrityError:", e)
        return None
    except Exception as e:
        print("Error:", e)
        return None

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    user = await get_user(telegram_id)

    if user:
        await update.message.reply_text("Siz oldin ro'yxatdan o'tgansiz.", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    btn = [
        [KeyboardButton(text="Telefon raqamni yuborish", request_contact=True)]
    ]
    await update.message.reply_text(f"Salom, {update.effective_user.first_name}\n\nIltimos ro'yxatdan o'tish uchun telefon raqamingizni yuboring:", reply_markup=ReplyKeyboardMarkup(btn, resize_keyboard=True))
    return GET_PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    telegram_id = update.effective_user.id

    if not contact:
        await update.message.reply_text("Iltimos raqamni yuborish tugmasini bosing.")
        return GET_PHONE

    result = await create_user(contact.phone_number, telegram_id)
    if result:
        await update.message.reply_text("ro'yxatdan otdingiz", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    else:
        await update.message.reply_text("Malumotlaringiz saqlanmadi!\nAdmin bilan bog'laning.")

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("bekor qilindi")
    return ConversationHandler.END


register_conf_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start_handler)],
    states={
        GET_PHONE: [MessageHandler(filters.CONTACT, get_phone)]
    },
    fallbacks=[CommandHandler('cancel', cancel_command)]
)
