"""
Адаптер уведомлений MAX.

В первой версии используется режим-заглушка: сообщение выводится в консоль.
Для реальной отправки необходимо получить доступ к официальному API/платформе
ботов MAX, настроить токен и идентификаторы чатов старост.
"""


def notify_class_representatives(registration):
    message = (
        "Новая заявка на студенческий конкурс!\n"
        f"Участник: {registration['full_name']}\n"
        f"Группа: {registration['group_name']}\n"
        f"Конкурс: {registration['competition_name']}\n"
        f"Номер заявки: {registration['registration_id']}"
    )
    print("[MAX BOT — DEMO]")
    print(message)
    return True
