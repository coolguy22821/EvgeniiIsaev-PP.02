import os

class MaxBotAdapter:
    """Демонстрационный адаптер. Реальная отправка требует официального MAX API."""
    def __init__(self,mode="demo"):
        self.mode=mode
        self.token=os.getenv("MAX_BOT_TOKEN","")
        self.chat_id=os.getenv("MAX_CHAT_ID","")

    def build_message(self,data):
        return (f"Новая заявка на студенческий конкурс\\n"
                f"Участник: {data['full_name']}\\nГруппа: {data['group_name']}\\n"
                f"Конкурс: {data['competition_name']}\\nНомер заявки: {data['registration_id']}")

    def notify_class_representative(self,data):
        message=self.build_message(data)
        if self.mode!="live":
            print("[MAX BOT — DEMO MODE]"); print(message)
            return {"status":"demo","details":"Сообщение сформировано; реальная отправка отключена."}
        if not self.token or not self.chat_id:
            return {"status":"not_configured","details":"Не заданы MAX_BOT_TOKEN или MAX_CHAT_ID."}
        return {"status":"not_implemented","details":"Транспорт MAX API нужно реализовать по официальной документации; сообщение не отправлено."}
