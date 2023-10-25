import os

import logging

logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')
TG_SHUTDOWN_DELAY_SECS = int(os.getenv('TG_SHUTDOWN_DELAY', 20))
TG_ACTIVE_USERS_CHECK_INTERVAL_HOURS = int(os.getenv('TG_ACTIVE_USERS_CHECK_INTERVAL_HOURS', 24))
TG_BALANCE_THRESHOLD = int(os.getenv('TG_BALANCE_THRESHOLD', 5000))