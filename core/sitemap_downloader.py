from core.requester import Requester
import os

class SitemapDownloader():
    def __init__(self):
        self.requester = Requester()

    def download_mainsitemap(self, url, save_path):
        url = url + "/console/integration/execute/name/GoogleSitemap"
        try:
            response = self.requester.get(url)
            print(response.status_code)
        except:
            return False

        try:
            with open(save_path, "w") as file:
                file.write(response.text)
            return True
        except:
            return False