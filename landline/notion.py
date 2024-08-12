import datetime
import pathlib
import requests

from landline.config import Config


class NotionController:
    def __init__(self, cfg: Config) -> None:       
        self.cfg = cfg
        self.session = requests.Session()
        self.session.headers["Content-Type"] = "application/json"
        self.session.headers["Authorization"] = f"Bearer {cfg.notion.token}"
        self.session.headers["Notion-Version"] = cfg.notion.version

    def build_url(self, path: str) -> str:
        return f"{self.cfg.notion.base_url}/{path}"

    def initialize_database(self, root_id: str) -> str:
        response = self.session.post(self.build_url("databases"), json={
            "parent": {
                "page_id": root_id,
            },
             'title': [
                 {
                    'type': 'text',
                    'text': {'content': 'Recordings', 'link': None},
                    'annotations': {
                        'bold': False,
                        'italic': False,
                        'strikethrough': False,
                        'underline': False,
                        'code': False,
                        'color': 'default',
                    },
                    'plain_text': 'Recordings',
                    'href': None,
                }
            ],
            "properties": {
                "Name": {"id": "name", "name": "Name", "type": "title", "title": {}},
                "Date": {"id": "date", "name": "Date", "type": "date", "date": {}},
                "Text": {"id": "text", "name": "Text", "type": "rich_text", "rich_text": {}},
                "File": {"id": "file", "name": "File", "type": "rich_text", "rich_text": {}},
            },
            "icon": {
                "type": "external",
                "external": {
                    "url": "https://www.notion.so/icons/database_gray.svg",
                },
            },
        })
        print(response, response.json())
        response.raise_for_status()
        return response.json()['id']
    
    def insert(self, name: str, date: datetime.datetime, file: pathlib.Path, text: str) -> str:
        response = self.session.post(self.build_url("pages"), json={
            "parent": {
                "database_id": self.cfg.notion.database_id,
            },
            "properties": {
                "Name": {"title": [{"text": {"content": name}}]},
                "Date": {"date": {"start": date.isoformat()}},
                "Text": {"rich_text": [{"text": {"content": text}}]},
                "File": {"rich_text": [{"text": {"content": file.name}}]},
            },
        })
        print(response, response.json())
        response.raise_for_status()
        return response.json()['id']
    
    def records(self):
        response = self.session.post(self.build_url(f"databases/{self.cfg.notion.database_id}/query"), json={})
        print(response, response.json())
        response.raise_for_status()
        yield from response.json()['results']
