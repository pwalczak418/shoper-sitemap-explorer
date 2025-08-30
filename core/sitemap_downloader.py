from core.requester import Requester
import os
import xml.etree.ElementTree as ET
import re
import time

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
        
    def download_single_child(self, singlelink, childmap_iteration, trans, index, save_path):

        childmap_iteration = childmap_iteration.replace("GoogleSitemap/list/", "")

        ## TO DO ##

        try:
            response = self.requester.get()
            print(response.status_code)
        except:
            return False

        try:
            with open(save_path, "w") as file:
                file.write(response.text)
            return True
        except:
            return False
        
    def download_childsitemaps(self, url, save_path, selected_childs):
        print("Rozpoczynamy pobieranie podsitemap")
        print(f"url: {url}, save_path: {save_path}, childs: {selected_childs}")

        main_save_path = os.path.join(save_path, "sitemap.xml")
        try:
            self.download_mainsitemap(url, main_save_path)
        except:
            return False
        
        sitemaps_url = {
            "Produkty": "GoogleSitemap/list/products",
            "Kategorie": "GoogleSitemap/list/categories",
            "Producenci": "GoogleSitemap/list/producers",
            "Blog": "GoogleSitemap/list/news",
            "Strony informacyjne": "GoogleSitemap/list/info",
            "Kolekcje": "GoogleSitemap/list/collections"
        }

        selected_urls = []

        for i in selected_childs:
            if i in sitemaps_url:
                selected_urls.append(sitemaps_url[i])

        print(selected_urls)

        try:
            xml_tree = ET.parse(main_save_path)
            xml_root = xml_tree.getroot()
            links = []
            for sitemap in xml_root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap"):
                    loc_element = sitemap.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
                    if loc_element is not None:
                        link = loc_element.text
                        links.append(link)
        except Exception as e:
            print("Wystąpił błąd z odczytaniem Sitemap")
            return False
        
        print(links)

        for index, singlelink in enumerate(links, start=1):
            for singlechildmap in selected_urls:
                if singlechildmap in singlelink:
                    trans_pattern = re.compile(r'\b[a-z]{2}_[A-Z]{2}\b')
                    trans_found = trans_pattern.search(singlelink)
                    trans = trans_found.group(0)
                    print(trans)
                    singlechildmap_iteration = singlechildmap
                    print("singlechild:", singlelink)
                    print("current index", index)
                    self.download_single_child(singlelink, singlechildmap_iteration, trans, index, save_path)
            
        print("Zakończono")