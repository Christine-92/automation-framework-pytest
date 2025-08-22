from src.apis.base_client import BaseClient
from src.config.settings import ACCOUNT_ID
class ChannelClient:
    def __init__(self, base_client: BaseClient, account_id:str =  ACCOUNT_ID):
        self.client = base_client
        self.account_id = account_id

# This method creates channel

    def create_channel(self, name: str, website_url: str, widget_color: str = "#009CE0", greeting_enabled: bool = False,
                       greeting_message: str = ""):
        data = {
            "name": name,
            "greeting_enabled": str(greeting_enabled).lower(),  # convert to "true"/"false"
            "greeting_message": greeting_message,
            "channel[type]": "web_widget",
            "channel[website_url]": website_url,
            "channel[widget_color]": widget_color
        }

        endpoint = f"/api/v1/accounts/{self.account_id}/inboxes"
        response = self.client.post(endpoint, params=data)
        response.raise_for_status()
        return response.json()
# This method gets channel by given id
    def get_channels_by_id(self, channel_id: str):
        endpoint = f"/api/v1/accounts/{self.account_id}/inboxes/{channel_id}"
        response = self.client.get(endpoint)
        response.raise_for_status()
        return response.json()

# This method deletes the channel
    def delete_channel(self, channel_id):
        endpoint = f"/api/v1/accounts/{self.account_id}/inboxes/{channel_id}"
        resp = self.client.delete(endpoint)
        resp.raise_for_status()
        return resp
