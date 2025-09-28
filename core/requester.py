import requests
import time

class Requester():
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-agent": "shoper-sitemap-explorer/1.0 (+https://github.com/pwalczak418/shoper-sitemap-explorer)"})

    def get(self, url):
        attempts_limit = 3

        for attempt in range(attempts_limit):

            try:
                print(f"Rozpoczynam próbę połączenia z {url}")
                response = self.session.get(url)
                response.raise_for_status()
                return response
            except:
                print(f"Próba połączenia nie powiodła się z {url}")
                if attempt < attempts_limit - 1:
                    print("Wykonuję kolejną próbę połączenia")
                    time.sleep(1)
                else:
                    print(f"Żadna próba połączenia się z {url} się nie powiodła.")
                    return None