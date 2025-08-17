
from .base_client import BaseClient
from config.settings import ACCOUNT_ID

class ConversationClient:
    def __init__(self,base_client: BaseClient, account_id = ACCOUNT_ID):
        self.account_id = account_id
        self.client= base_client

    def create_conversation(self,source_id: str, contact_id: str,inbox_id: str ):
        url = f"/api/v1/accounts/{self.account_id}/conversations"
        body = {
            "source_id": source_id,
            "inbox_id": inbox_id,
            "contact_id": contact_id,
            "additional_attributes": {},
            "custom_attributes": {
                "attribute_key": "attribute_value",
                "priority_conversation_number": 3
            },
            "status": "open",
            "assignee_id": 396
        }
        response = self.client.post(url, json=body)
        response.raise_for_status()
        return response.json()