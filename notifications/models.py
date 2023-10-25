from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser

class Customer(AbstractUser):
    balance = models.IntegerField(default=0)

class CustomerNotificationSetting(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='notification_setting')
    enable_telegram = models.BooleanField(default=False)
    telegram_chat_id = models.CharField(max_length=255, null=True, blank=True)
    enable_email = models.BooleanField(default=False)
    # enable_discord = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Customer Notification Settings"
        index_together = [
            ["customer", "enable_telegram"],
        ]
'''
    These history business logic is implemented via signals, do not mess it up
'''
class BalanceHistory(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    new_balance = models.IntegerField()
    old_balance = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Balance Histories"
    
    
'''
save send telegram messages
'''
class TelegramMessage(models.Model):
    SENT = 'sent'
    FAILED = 'failed'
    STATUS_CHOICES = (
        (SENT, 'Sent'),
        (FAILED, 'Failed'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    chat_id = models.CharField(max_length=55, null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True, choices=STATUS_CHOICES)
    
    def __str__(self):
        return f"{self.customer} - {self.message}"
    

class MessageTemplate(models.Model):
    is_active = models.BooleanField(default=True) # is_active must be single true in db and at least 1
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.is_active:
            try:
                temp = MessageTemplate.objects.get(is_active=True)
                if self != temp:
                    temp.is_active = False
                    temp.save()
            except MessageTemplate.DoesNotExist:
                pass
        super(MessageTemplate, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.message}"
    
    @classmethod
    def get_active_template(cls):
        try:
            return cls.objects.get(is_active=True)
        except cls.DoesNotExist:
            obj = MessageTemplate.objects.create(message="Your balance is less than threshold, please top up your balance")
            return obj