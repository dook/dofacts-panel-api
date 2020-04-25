import requests

from .settings import API_URL, CHATBOT_API_KEY


class ApiClient:
    headers = {
        "x-api-key": CHATBOT_API_KEY,
    }

    def _send(self, path, data):
        response = requests.post(f"{API_URL}{path}", json=data, headers=self.headers,)

    def send_new_news_verdict(self, data):
        self._send("news", data)
