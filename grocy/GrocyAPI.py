import requests


class GrocyAPI:
    def __init__(self, url, api_key):
        self.url = url
        self.session = requests.session()
        self.session.headers = {'GROCY-API-KEY': api_key}
        self.api_key = api_key
        self.session.verify = False

    def get(self, url):
        if url[0] == '/':
            url = self.url + url

        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
