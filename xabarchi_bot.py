from telegram import Update, InputMediaPhoto, InputMediaVideo, InputMedia, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import logging

# Logging sozlash
logging.basicConfig(format='%(asctime)s - %(name)s - %(levellevel)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram bot tokeni
API_TOKEN = '8014328569:AAE9rw2hNwsZ3fb1VCqOsC0tZHYDSERepuc'
CHANNEL_USERNAMES = ['@ellikqala_YI_agentligi', '@asos001']  # Asosiy kanallar ro'yxatini bu yerda kiritamiz
TARGET_GROUPS_AND_CHANNELS = ['@asos77' '@tozabog_yoshlari', '@Iftixoryoshlarii', '@Saxtiyon_yoshlari', '@Qilichinoq_city1', '@chopon_mfy', '@Koiot_yoshlari', '@dostlik-ofy-yoshlari', '@sharq_yulduzi_yoshlari', '@oq_oltin_yoshlari', '@navbaxor_mfy_yoshlar', '@guldursun_yoshlari', '@Burgutqala_yoshlari', '@gulistonofyyoshlari', '@Qizilqumofyyoshlari', '@akchakul_ofy_yoshlari', '@abaymfjjaslari', '@qiqqizobod_yoshlar', '@ellikqalaOfy_Yoshlari', '@AlisherNavoiy_yoshlari', '@ayozqala77', '@iqbolmfyyoshlari', '@kichik_guldursun', '@yangi_uzyosh', '@ibnsinoyoshlari', '@Paxtachimahallayoshlari', '@sarabiy_yoshlari', '@guruh3', 'https://t.me/joinchat/XXXXXXX', 'https://t.me/joinchat/XXXXXXX']  # Faqat @asos77 guruh username'ini kiritamiz
GROUP_USERNAME = '@bustonmfy1'  # Bu yerda tavsiya qilingan guruh username'ini kiritamiz
THANK_YOU_MESSAGE = "Rahmat, guruhingizga qo'shildim. Iltimos, menga admin huquqini bering."

# Botni ishga tushirish komandasi (shaxsiy xabarlarda)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private":
        keyboard = [
            [InlineKeyboardButton("Oldin shu guruh qo`shiling👆 ", url=f"tg://resolve?domain={GROUP_USERNAME.lstrip('@')}")],
            [InlineKeyboardButton("Botni guruhga qo'shish", url='http://t.me/your_bot_username?startgroup=new')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Botga xush kelibsiz! Iltimos, quyidagi tugmalarni bosing:", reply_markup=reply_markup)

# Bot guruhga qo'shilganda xabar yuborish (guruhda)
async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=THANK_YOU_MESSAGE)

# Kanaldan xabarlarni olish va guruhlarga yuborish
async def forward_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Xabarlar kanaldan guruhlarga yuborilmoqda")
    if update.channel_post and update.channel_post.chat.username in [channel.lstrip('@') for channel in CHANNEL_USERNAMES]:
        message = update.channel_post
        media_group = []

        if message.media_group_id:
            media_group = await collect_media_group(context, message.chat_id, message.media_group_id, message.caption or message.text)
        elif message.photo:
            media_group.append(InputMediaPhoto(media=message.photo[-1].file_id, caption=message.caption or message.text))

        for target in TARGET_GROUPS_AND_CHANNELS:
            try:
                if media_group:
                    await context.bot.send_media_group(chat_id=target, media=media_group)
                logger.info(f"Xabar {target} ga yuborildi")
            except Exception as e:
                logger.error(f"Xatolik yuz berdi: {e}")

async def collect_media_group(context, chat_id, media_group_id, caption):
    updates = await context.bot.get_updates(limit=100)
    media_group = []
    for update in updates:
        if update.channel_post and update.channel_post.media_group_id == media_group_id:
            if update.channel_post.photo:
                if len(media_group) == 0:
                    media_group.append(InputMediaPhoto(update.channel_post.photo[-1].file_id, caption=caption))
                else:
                    media_group.append(InputMediaPhoto(update.channel_post.photo[-1].file_id))
            elif update.channel_post.video:
                if len(media_group) == 0:
                    media_group.append(InputMediaVideo(update.channel_post.video.file_id, caption=caption))
                else:
                    media_group.append(InputMediaVideo(update.channel_post.video.file_id))
    return media_group

# Botni ishga tushirish
if __name__ == '__main__':
    app = ApplicationBuilder().token(API_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))
    app.add_handler(MessageHandler(filters.ChatType.CHANNEL, forward_messages))

    app.run_polling()
