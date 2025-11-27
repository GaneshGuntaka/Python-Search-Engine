class Crawler:
    def __init__(self, url_manager, downloader):
        self.url_manager = url_manager
        self.downloader = downloader

    def crawl(self, start_url, max_pages=50):
        self.url_manager.add_url(start_url)
        crawled = 0

        while self.url_manager.has_url() and crawled < max_pages:
            url = self.url_manager.get_url()
            print(f"Crawling: {url}")

            html = self.downloader.download(url)
            if html:
                self.downloader.save_page(url, html)
                links = self.downloader.extract_links(html)
                for link in links:
                    self.url_manager.add_url(link)

            crawled += 1
