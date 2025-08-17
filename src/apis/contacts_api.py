
from config.settings import ACCOUNT_ID
from .base_client import BaseClient

class ContactClient:
    def __init__(self, base_client: BaseClient, account_id = ACCOUNT_ID):
        self.client = base_client
        self.account_id = account_id


    def create_contact(self, contact_name:str, contact_email:str, inbox_id: str):
        url = f"/api/v1/accounts/{self.account_id}/contacts"
        body = {
                "inbox_id": inbox_id,
                "name":contact_name,
                "email":contact_email
                }
        response = self.client.post(url, json=body)
        response.raise_for_status()
        return response.json()

    def delete_contact(self, contact_id: str):
        url = f"/api/v1/accounts/{self.account_id}/contacts/{contact_id}"
        response = self.client.delete(url)
        response.raise_for_status()
        return response

