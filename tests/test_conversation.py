from src.apis.conversations_api import ConversationClient
from src.config.settings import ACCOUNT_ID

def test_create_conversation(auth_client,contact):

    conv_client = ConversationClient(auth_client, ACCOUNT_ID)
    contact_id = contact["payload"]["contact"]["id"]
    source_id = contact["payload"]["contact_inbox"]["source_id"]
    channel_id = contact["payload"]["contact_inbox"]["inbox"]["id"]
    created_conv = conv_client.create_conversation(source_id, contact_id, channel_id)
    try:
        assert created_conv is not None
        assert created_conv["meta"]["sender"]["id"] == contact_id
        assert created_conv["inbox_id"] == channel_id
    except AssertionError:
        print(created_conv)