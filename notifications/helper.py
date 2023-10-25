from copy import copy

from notifications.models import Customer
from tg_notifier_assignment.config import TG_BALANCE_THRESHOLD


def get_message_template_fill_dict(customer: Customer = None):
    if customer is None:
        customer = Customer()
    fill_dict = copy(customer.__dict__)
    fill_dict['threshold_balance'] = TG_BALANCE_THRESHOLD
    return fill_dict