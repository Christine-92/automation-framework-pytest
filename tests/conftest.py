import os
import pytest

# 1) Load .env early (before importing config)
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=False)  # will read your project-root .env


import pytest
from datetime import datetime
from src.apis.auth_client import AuthClient
from src.apis.base_client import BaseClient
from src.apis.channels_api import ChannelClient
from src.config.settings import BASE_URL, ACCOUNT_ID

# Fixture scops
# function (default): runs before/after each test.
# class: runs once per test class.
# module: runs once per test file.
# session: runs once for the whole test run.
@pytest.fixture(scope = "session")
def auth_client():
    """Login only,(once per session) return BaseClient with token."""
    auth = AuthClient(base_url=BASE_URL)
    token_info = auth.login()
    client = BaseClient(base_url=BASE_URL, token=token_info["token"])
    yield client
    # logout at the very end of the whole run
    auth.logout()


@pytest.fixture(scope="module")
def channel(auth_client):
    """Create one channel per test module with a unique name/URL."""
    channel_client = ChannelClient(auth_client, ACCOUNT_ID)

    ts = datetime.now().timestamp()
    name = f"auto_test_channel_{ts}"
    website_url = f"https://autotest.com/{ts}"

    resp_json = channel_client.create_channel(
        name=name,
        website_url=website_url,
        greeting_enabled=False
    )
    # Yield the whole response so tests can use id/name/etc.
    yield resp_json

# @pytest.fixture(scope="module")
# def conversation(contact):
#     """Create one conversation per test module with a unique name/URL."""
# @pytest.fixture(scope="module")
#
# def contact()