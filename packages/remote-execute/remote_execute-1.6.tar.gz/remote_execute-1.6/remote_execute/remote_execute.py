import requests
import threading
from typing import List, Tuple, Optional, Callable

class RemoteExecutor:
    def __init__(self, save_path: Optional[str] = None):
        self.running_urls = {}
        self.save_path = save_path

    def execute_request(self, url: str, name: Optional[str] = None, headers: Optional[dict] = None, on_fetch: Optional[Callable] = None):
        try:
            response = requests.get(url, headers=headers)
            # Add your logic to process the response as needed
            print(f"URL: {url}, Response Code: {response.status_code}")

            # Run user-provided function if provided
            if on_fetch:
                on_fetch(response)

            # Save to server if save_path is provided
            if self.save_path:
                self._save_to_server(url, response.text)

            # Store the response or other information if needed
            # self.running_urls[name] = {"response": response, ...}
        except Exception as e:
            print(f"Error accessing {url}: {e}")

    def _save_to_server(self, url, content):
        filename = url.split("/")[-1]
        filepath = f"{self.save_path}/{filename}"
        with open(filepath, "w") as file:
            file.write(content)
        print(f"Saved content from {url} to {filepath}")

    def fetch(self, urls: List[Union[str, Tuple[str, Optional[str], Optional[dict], Optional[Callable]]]]):
        for url_info in urls:
            if isinstance(url_info, tuple):
                url, name, headers, on_fetch = url_info
                self.execute_request(url, name=name, headers=headers, on_fetch=on_fetch)
            else:
                self.execute_request(url_info)