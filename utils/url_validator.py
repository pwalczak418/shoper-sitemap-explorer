from urllib.parse import urlparse
from core.requester import Requester

class Validator():
    def __init__(self):
        pass

    def validate_url(self, url):
        print(f"Podano URL: {url}")
        try:
            result = urlparse(url)
        except AttributeError:
            print("Nie udało się sparsować podanego URL")
            return False
        
        print(result.scheme)

        if result.scheme != "https":
            url = "https://" + url
        
        result = urlparse(url)

        if url.endswith("/"):
            url = url[:-1]

        if not all([result.netloc, '.' in result.netloc]):
            print("Nie podano prawidłowego URL")
            return False
        else:
            print("Struktura URL prawidłowa.")
            return url

    def connect(self, url):

        self.requester = Requester()
        print(f"Rozpoczynam próbę połączenia z {url}")
        try:
            response = self.requester.get(url)
        except:
            print(f"Nie odnaleziono podanej strony: {url}.")
            return False
        response_headers = response.headers
        status = response.status_code
        
        if "DCSaaS" in response_headers.values() and status == 200:
            print(f"Połączono ze sklepem Shoper: {url}")
            return True
        elif status == 200:
            print("Nie znaleziono sklepu Shoper pod podanym adresem")
            return False
        else:
            print(f"Program nie mógł się połączyć z adresem: {url}. Otrzymany status HTTP: {status}")
            return False