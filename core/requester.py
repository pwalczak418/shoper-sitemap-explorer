import requests

class Requester():
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-agent": "SSE"})

    def get(self, url):
        print(f"Requesting: {url}")
        response = self.session.get(url)
        return response