from django.contrib import admin

# Register your models here.
from notifications.helper import get_message_template_fill_dict
from notifications.models import Customer, BalanceHistory, MessageTemplate, TelegramMessage


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass

@admin.register(BalanceHistory)
class BalanceHistoryAdmin(admin.ModelAdmin):
    list_display = ('customer', 'new_balance', 'old_balance', 'created_at')

@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ('message', 'updated_at', 'created_at', 'is_active')
    list_editable = ('is_active',)
    def get_form(self, request, obj=None, **kwargs):
        fill_dict = ", ".join(get_message_template_fill_dict().keys())
        help_texts = {'message': f'Please use this keys in format {{username}}\nKeys: {fill_dict}'}
        kwargs.update({'help_texts': help_texts})
        return super(MessageTemplateAdmin, self).get_form(request, obj, **kwargs)

@admin.register(TelegramMessage)
class TelegramMessageAdmin(admin.ModelAdmin):
    list_display = ('customer', 'chat_id', 'message', 'created_at', 'sent_at', 'status')