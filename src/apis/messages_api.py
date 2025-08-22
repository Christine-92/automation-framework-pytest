from src.apis.base_client import BaseClient
from src.config.settings import ACCOUNT_ID
from src.enums import MessageType, ContentType


class MessagesClient:

    def __init__(self, base_client:BaseClient,account_id = ACCOUNT_ID):
        self.client = base_client
        self.account_id = account_id


    def send_message(self, conversation_id, content: str, message_type: MessageType, private:bool =  False):
        url= f"/api/v1/accounts/{self.account_id}/conversations/{conversation_id}/messages"
        body = {
      "content": content,
      "message_type":message_type.value,
      "private": bool(private),
      "content_type": "text",
      "content_attributes": {}
                }
        response = self.client.post(url, json=body)
        response.raise_for_status()
        return response.json()

    def get_messages(self, conversation_id):
        url = f"/api/v1/accounts/{self.account_id}/conversations/{conversation_id}/messages"
        response = self.client.get(url)
        response.raise_for_status()
        return response.json()