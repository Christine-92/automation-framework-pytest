from src.apis.base_client import BaseClient
from src.config.settings import *


class AuthClient(object):
    def __init__(self,  base_url=BASE_URL):
        self.base_url = base_url.rstrip('/')
        self.token_info = {} # store all auth headers
        # no token yes
        self.auth_client = BaseClient(self.base_url)

# This method logged in the user by given
    def  login(self)-> dict:
        req_body = {
            "email": USERNAME,
            "password": PASSWORD,
            "sso_auth_token": "",
            "impersonate": False,
            "check_active_sessions": False
        }
        url = "/auth/sign_in"
        resp = self.auth_client.post(url, json=req_body)
        resp.raise_for_status()

        # Save all needed headers
        self.token_info = {
            "token": resp.headers.get("Authorization"),
            "access-token": resp.headers.get("access-token"),
            "client": resp.headers.get("client"),
            "uid": resp.headers.get("uid")
        }
        return self.token_info
# This method logged-out user by the saved header upon login
    def logout(self):
        headers = self.token_info.copy()
        url ="/auth/sign_out"
        resp = self.auth_client.delete(url, headers=headers)
        resp.raise_for_status()
        return resp
