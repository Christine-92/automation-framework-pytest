from apis.contacts_api import ContactClient
from apis.channels_api import ChannelClient
import pytest
from config.settings import ACCOUNT_ID
from datetime import datetime


def test_create_contact(auth_client, channel):

    ts = datetime.now().strftime('%Y%m%d%H%M%S%f')
    golden_name =f"auto_contact_{ts}"
    golden_email = f"{golden_name}@example.com"
    inbox_id = channel["id"]

    contact = ContactClient(auth_client,ACCOUNT_ID)
    created_contact = None
    contact_id = None


    try:
        created_contact = contact.create_contact(golden_name, golden_email, inbox_id)
        contact_id = created_contact["payload"]["contact"]["id"]

        assert created_contact["payload"]["contact"]["name"] == golden_name, "contact name mismatch"

    finally:
        if contact_id:
            contact.delete_contact(contact_id)