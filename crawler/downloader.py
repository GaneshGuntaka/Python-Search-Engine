import requests
from bs4 import BeautifulSoup
import os
import hashlib

class Downloader:

    def download(self, url):
        try:
            response = requests.get(url, timeout=5)
            return response.text
        except:
            return None

    def save_page(self, url, content):
        filename = hashlib.md5(url.encode()).hexdigest() + ".html"
        path = f"data/pages/{filename}"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def extract_links(self, html):
        soup = BeautifulSoup(html, "html.parser")
        links = []
        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            if href.startswith("http"):
                links.append(href)
        return links
