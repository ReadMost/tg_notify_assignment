from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from notifications.models import Customer, BalanceHistory, CustomerNotificationSetting
from tg_notifier_assignment.config import logger


@receiver(pre_save, sender=Customer)
def save_customer_balance_change(sender, instance, **kwargs):
    try:
        old_instance = Customer.objects.get(id=instance.id)
        if old_instance.balance != instance.balance:
            BalanceHistory.objects.create(
                customer=instance,
                new_balance=instance.balance,
                old_balance=old_instance.balance
            )
            pass
    except Customer.DoesNotExist:  # to handle initial object creation
        # logger.error("save_customer_balance_change: Customer does not exist")
        return
    except Exception as e:
        logger.error(e)

@receiver(post_save, sender=Customer)
def save_customer_setting(sender, instance, created, **kwargs):
    if created:
        CustomerNotificationSetting.objects.create(
            customer=instance
        )