class URLManager:
    def __init__(self):
        self.new_urls = set()
        self.visited = set()

    def add_url(self, url):
        if url not in self.new_urls and url not in self.visited:
            self.new_urls.add(url)

    def get_url(self):
        url = self.new_urls.pop()
        self.visited.add(url
        )
        return url

    def has_url(self):
        return len(self.new_urls) > 0
