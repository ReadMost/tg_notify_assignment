import telebot
from django.core.management.base import BaseCommand
from telebot.types import Message

from notifications.models import Customer, CustomerNotificationSetting
from tg_notifier_assignment.config import BOT_TOKEN
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")


@bot.message_handler(commands=['start', 'help'])
def general_info(message: Message):
    bot.reply_to(message, "Welcome to the notifications bot. Please, use \n/subscribe `username` - to subscribe for notifications \n/unsubscribe `username` - to unsubscribe from notifications")


@bot.message_handler(commands=['subscribe'])
def subscribe(message: Message):
    args = message.text.split()[1:]
    if len(args) != 1:
        bot.reply_to(message, "Please, use /subscribe `username` command.")
        return
    try:
        customer_setting = CustomerNotificationSetting.objects.get(customer__username=args[0])
        if customer_setting.enable_telegram:
            bot.reply_to(message, "You are already subscribed.")
            return
        customer_setting.enable_telegram = True
        customer_setting.telegram_chat_id = message.chat.id
        customer_setting.save()
        bot.reply_to(message, "You have successfully subscribed.")
    except CustomerNotificationSetting.DoesNotExist:
        bot.reply_to(message, "User with such username does not exist.")
        return

@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message: Message):
    args = message.text.split()[1:]
    if len(args) != 1:
        bot.reply_to(message, "Please, use /unsubscribe `username` command.")
        return
    try:
        customer_setting = CustomerNotificationSetting.objects.get(customer__username=args[0])
        if not customer_setting.enable_telegram:
            bot.reply_to(message, "You are already unsubscribed.")
            return
        customer_setting.enable_telegram = False
        customer_setting.telegram_chat_id = None
        customer_setting.save()
        bot.reply_to(message, "You have successfully unsubscribed.")
    except CustomerNotificationSetting.DoesNotExist:
        bot.reply_to(message, "User with such username does not exist.")
        return

@bot.message_handler(func=lambda m: True)
def unsupported_msg(message: Message):
    bot.reply_to(message, "Sorry, I don't understand you. Please, use /start or /help commands.")


class Command(BaseCommand):
    help = "Run the bot"
    
    def handle(self, *args, **options):
        bot.polling()