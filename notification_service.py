from max_bot import MaxBotAdapter
import os

def send_registration_notification(registration):
    adapter=MaxBotAdapter(mode=os.getenv("NOTIFICATION_MODE","demo"))
    return adapter.notify_class_representative(registration)
