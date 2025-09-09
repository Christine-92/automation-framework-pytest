from datetime import datetime
from enums import MessageType
from src.apis.messages_api import MessagesClient
from src.config.settings import ACCOUNT_ID
from tests.api_tests.conftest import auth_client


def test_in_out_messages(auth_client,contact, conversation):

    msg_client = MessagesClient(auth_client, ACCOUNT_ID)

    conv_id = conversation["id"]
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    golden_incoming_msg = f"{conv_id} This is incoming message{ts}"
    golden_outgoing_msg = f"{conv_id} This is outgoing message{ts}"
    golden_private_msg = f"{conv_id} This is private message{ts}"


    sent_in = msg_client.send_message(conv_id, golden_incoming_msg,MessageType.INCOMING)
    sent_out = msg_client.send_message(conv_id, golden_outgoing_msg,MessageType.OUTGOING)
    sent_private = msg_client.send_message(conv_id,golden_private_msg, MessageType.OUTGOING,private=True)

    assert sent_in["content"]   == golden_incoming_msg, "incoming message mismatch"
    assert sent_in["conversation_id"] == conv_id, "conversation id mismatch mismatch"
    assert sent_in["private"] == False, "Incoming Message is private"
    assert sent_out["conversation_id"] == conv_id, "conversation id mismatch mismatch"
    assert sent_out["private"] ==   False, "outgoing message is private"
    assert sent_out["content"] == golden_outgoing_msg, "outgoing message mismatch"
    assert sent_private["private"] == True, "Message is not private"
