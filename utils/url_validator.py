from urllib.parse import urlparse
from core.requester import Requester

class Validator():
    def __init__(self, log):
        self.log = log

    def validate_url(self, url):
        self.log(f"Podano URL: {url}")
        try:
            result = urlparse(url)
        except AttributeError:
            self.log("ERROR: Nie udało się sparsować podanego URL")
            return False
        
        print(result.scheme)

        if result.scheme != "https":
            url = "https://" + url
        
        result = urlparse(url)

        if url.endswith("/"):
            url = url[:-1]

        if not all([result.netloc, '.' in result.netloc]):
            self.log("ERROR: Nie podano prawidłowego URL")
            return False
        else:
            self.log("Struktura URL prawidłowa.")
            return url

    def connect(self, url):

        self.requester = Requester()
        self.log(f"Rozpoczynam próbę połączenia z {url}")
        try:
            response = self.requester.get(url)
        except:
            self.log(f"ERROR: Nie odnaleziono podanej strony: {url}.")
            return False
        if response and response.headers is not None:
            response_headers = response.headers
        else:
            self.log(f"ERROR: Nie udało się nawiązać połączenia: {url}")
            return False
        status = response.status_code
        
        if "DCSaaS" in response_headers.values() and status == 200:
            self.log(f"Połączono ze sklepem Shoper: {url}")
            return True
        elif status == 200:
            self.log("ERROR: Nie znaleziono sklepu Shoper pod podanym adresem")
            return False
        else:
            self.log(f"ERROR: Program nie mógł się połączyć z adresem: {url}. Otrzymany status HTTP: {status}")
            return False