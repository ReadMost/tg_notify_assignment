Steps to do:
1. Go to https://uvu.readmost.kz/admin/
2. Create own user by filling: Username, Email, Password, First name, Last name, Balance=10000
3. Go to Telegram bot via https://t.me/tg_notifier_assignment_bot
   1. Subscribe to bot by command: `/subscribe <your_username>`
4. Update created user balance less than 5000 (e.g. 1000)
To Resend message you need:
5. remove ur msg raw in `Telegram Message` or in https://uvu.readmost.kz/admin/notifications/telegrammessage/ (There is shutdown period, thus after sending msg u cannot resend it immediately)
If you want to update template and resend message:
6. Go to https://uvu.readmost.kz/admin/notifications/messagetemplate/ and update/create template and set is_active=True
7. Repeat (5) step to reproduce message sending
---
Criteria for sending message:
1. User balance < 5000
2. User balance should be decreased in last 24h
4. User should not be notified in last 24h
3. User should be subscribed to bot
