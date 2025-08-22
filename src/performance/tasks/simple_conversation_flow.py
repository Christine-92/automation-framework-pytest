# src/performance/tasks/simple_conversation_flow.py
from locust import HttpUser, task, between
from datetime import datetime
import uuid

from src.apis.channels_api import ChannelClient
from src.apis.contacts_api import ContactClient
from src.apis.conversations_api import ConversationClient
from src.apis.messages_api import MessagesClient
from src.apis.base_client import BaseClient
from src.apis.auth_client import AuthClient
from src.config.settings import ACCOUNT_ID
from src.enums import MessageType


class LocustClientAdapter(BaseClient):
    """
    BaseClient-compatible adapter that routes requests through Locust's HTTP session,
    so every API call is recorded in Locust metrics.
    """
    def __init__(self, locust_http_session, base_url: str, token_headers: dict | None = None):
        super().__init__(base_url, token=None)
        self._session = locust_http_session
        # copy auth headers from AuthClient.login()
        if token_headers:
            if token_headers.get("token"):
                self.headers["Authorization"] = token_headers["token"]
            for k in ("access-token", "client", "uid"):
                if token_headers.get(k):
                    self.headers[k] = token_headers[k]

    def get(self, endpoint: str, params=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        merged = {**self.headers, **(headers or {})}
        return self._session.get(url, params=params, headers=merged, name=endpoint)

    def post(self, endpoint: str, params=None, json=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        merged = {**self.headers, **(headers or {})}
        return self._session.post(url, data=params, json=json, headers=merged, name=endpoint)

    def delete(self, endpoint: str, params=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        merged = {**self.headers, **(headers or {})}
        return self._session.delete(url, params=params, headers=merged, name=endpoint)


class ChannelConversationUser(HttpUser):
    """
    One channel per user.
    Each iteration: create 1 contact → create 1 conversation (using source_id from contact)
    → send incoming, outgoing, and private messages.
    """
    wait_time = between(1, 2)

    # (optional) placeholders for linters
    channel_api = None
    contact_api = None
    conversation_api = None
    messages_api = None
    channel_id = None

    def on_start(self):
        # 1) login to get headers
        auth = AuthClient(base_url=self.host)
        token_headers = auth.login()

        # 2) route API calls through Locust session (for proper metrics)
        client = LocustClientAdapter(self.client, base_url=self.host, token_headers=token_headers)

        # 3) wire API clients
        self.channel_api = ChannelClient(client, account_id=ACCOUNT_ID)
        self.contact_api = ContactClient(client, account_id=ACCOUNT_ID)
        self.conversation_api = ConversationClient(client, account_id=ACCOUNT_ID)
        self.messages_api = MessagesClient(client, account_id=ACCOUNT_ID)

        # 4) create one channel per user and reuse it
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        created = self.channel_api.create_channel(
            name=f"perf_channel_{ts}",
            website_url=f"perf-{ts}.example.com",  # must be a full URL
            widget_color="#009CE0",
            greeting_enabled=False,
            greeting_message=""
        )
        self.channel_id = str(created["id"])

    @task
    def contact_conversation_and_messages(self):
        # A) create contact in this channel
        contact = self.contact_api.create_contact(
            contact_name=f"PerfUser_{uuid.uuid4().hex[:6]}",
            contact_email=f"perf_{uuid.uuid4().hex[:8]}@example.com",
            inbox_id=self.channel_id
        )

        # B) extract IDs from contact payload (your API shape)
        payload = contact["payload"]
        contact_id = str(payload["contact"]["id"])
        source_id = payload["contact_inbox"]["source_id"]
        channel_id = str(payload["contact_inbox"]["inbox"]["id"])

        # C) create conversation (use source_id from contact)
        conv = self.conversation_api.create_conversation(
            source_id=source_id,
            contact_id=contact_id,
            inbox_id=channel_id
        )
        conv_id = str(conv["id"])

        # D) send messages: incoming → outgoing → private
        self.messages_api.send_message(
            conversation_id=conv_id,
            content="Hello from visitor (incoming)",
            message_type=MessageType.INCOMING,
            private=False
        )
        self.messages_api.send_message(
            conversation_id=conv_id,
            content="Hello from agent (outgoing)",
            message_type=MessageType.OUTGOING,
            private=False
        )
        self.messages_api.send_message(
            conversation_id=conv_id,
            content="Internal note (private)",
            message_type=MessageType.OUTGOING,  # private notes are typically outgoing + private=True
            private=True
        )

    def on_stop(self):
        # no cleanup (as requested)
        pass
