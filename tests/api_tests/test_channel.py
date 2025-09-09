import pytest
from datetime import datetime
from src.apis.channels_api import ChannelClient
from src.config.settings import  ACCOUNT_ID


def test_create_channel(auth_client):
    # Golden data for test
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    golden_channel_name = f"auth_web_channel_{ts}"
    golden_url = f"https://{golden_channel_name}"

    channel_client = ChannelClient(auth_client, ACCOUNT_ID)
    channel_id = None

    try:
        # Create channel
        actual_channel = channel_client.create_channel(golden_channel_name, golden_url)
        channel_id = actual_channel.get("id")

        # Get channel details
        get_channel = channel_client.get_channels_by_id(channel_id)

        # Assertions
        assert golden_channel_name == get_channel["name"]
        assert channel_id == get_channel["id"]

    except Exception as e:
        pytest.fail(f"Test failed due to error: {e}")

    finally:
        # Cleanup
        if channel_id:
            channel_client.delete_channel(channel_id)
