import requests


class TelegramRequests:
    def __init__(self, token: str, chat_id: int = None):
        self.token = token
        self.chat_id = chat_id

    def get_updates(self, offset: int = None, timeout: int = 100):
        url = f"https://api.telegram.org/bot{self.token}/getUpdates"
        params = {'offset': offset, 'timeout': timeout}
        response = requests.get(url, params=params)
        return response.json()

    def send_message(self, text: str):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        data = {'chat_id': self.chat_id, 'text': text}
        response = requests.post(url, data=data)
        return response.json()