import requests
import html2text
from haystack import component
from haystack.dataclasses import Document
from typing import Optional, List

@component
class MastodonFetcher():    
    def __init__(self, last_k_posts: Optional[int] = 10):
        self.last_k_posts = last_k_posts
    
    @component.output_types(documents = List[Document])
    def run(self, username: str, last_k_posts: Optional[int] = None):
        if last_k_posts is None:
            last_k_posts = self.last_k_posts
        
        username, instance = username.split('@')
        
        url = f"https://{instance}/api/v1/accounts/lookup?acct={username}"
        try:
            id_response = requests.request("GET", url)
            id = id_response.json()["id"]
            get_status_url = f"https://{instance}/api/v1/accounts/{id}/statuses?limit={last_k_posts}"
            response = requests.request("GET", get_status_url)
            toot_stream = []
            for toot in response.json():
                toot_stream.append(Document(content=html2text.html2text(toot["content"])))
        except Exception as e:
            toot_stream = [Document(content="Please make sure you are providing a correct, publically accesible Mastodon account")]

        return {"documents": toot_stream}