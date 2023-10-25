
from celery import shared_task
from django.db.models import F, Q
from django.utils import timezone

from notifications.helper import get_message_template_fill_dict
from notifications.management.commands.bot import bot
from notifications.models import TelegramMessage, CustomerNotificationSetting, BalanceHistory, MessageTemplate
from tg_notifier_assignment.celery import app
from tg_notifier_assignment.config import logger, TG_SHUTDOWN_DELAY_SECS, TG_ACTIVE_USERS_CHECK_INTERVAL_HOURS, \
    TG_BALANCE_THRESHOLD


@shared_task(name="send_tg_message")
def send_tg_message(chat_ids, messages, customer_ids):
    tg_msgs = []
    for chat_id, message, customer_id in zip(chat_ids, messages, customer_ids):
        msg_obj = TelegramMessage(
            customer_id=customer_id,
            chat_id=chat_id,
            message=message,
        )
        try:
            bot.send_message(chat_id, message)
            msg_obj.sent_at = timezone.now()
            msg_obj.status = TelegramMessage.SENT
        except Exception as e:
            logger.error(e)
            msg_obj.status = TelegramMessage.FAILED
        tg_msgs.append(msg_obj)
    TelegramMessage.objects.bulk_create(tg_msgs)

def _get_telegram_message(customer, message_template):
    fill_dict = get_message_template_fill_dict(customer)
    return message_template.format(**fill_dict)

@app.task(name='tg_notification_periodic_check_task')
def tg_notification_periodic_check_task():
    active_time_start = timezone.now() - timezone.timedelta(hours=TG_ACTIVE_USERS_CHECK_INTERVAL_HOURS)
    print("1111")
    alr_sent_customers = TelegramMessage.objects.filter(
        Q(created_at__gte=active_time_start), # message sent in last 24 hours
        Q(status=TelegramMessage.SENT) # message sent successfully
    ).values_list('customer_id', flat=True)
    print("222")
    
    # todo-improvement: we can use among Token to get recent active users
    need_notify_customers = BalanceHistory.objects.filter(
        Q(customer__notification_setting__enable_telegram=True), # customer has enabled telegram notification
        Q(created_at__gte=active_time_start), # balance changed in last 24 hours
        Q(new_balance__lt=F('old_balance')), # balance decreased
        Q(new_balance__lt=TG_BALANCE_THRESHOLD), # balance less than threshold,
        ~Q(customer_id__in=alr_sent_customers) # customer has been notified already
    ).values_list('customer_id', flat=True)
    print("3333")

    customer_settings = CustomerNotificationSetting.objects.filter(
        Q(customer_id__in=need_notify_customers),
        Q(enable_telegram=True),
    ).select_related('customer')
    print("4444")
    msg_template = MessageTemplate.get_active_template()

    chat_ids, messages, customer_ids = [], [], []
    print(customer_settings)
    for customer_setting in customer_settings:
        chat_ids.append(customer_setting.telegram_chat_id)
        messages.append(_get_telegram_message(customer_setting.customer, msg_template.message))
        customer_ids.append(customer_setting.customer_id)
    print("5000")

    res = send_tg_message.delay(chat_ids, messages, customer_ids)
    res.forget()
    
    
    
        