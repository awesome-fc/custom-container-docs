class FCContext:
    def __init__(self, access_key_id="", access_key_secret="", security_token="", account_id="", request_id="", region=""):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.security_token = security_token
        self.request_id = request_id
        self.region = region
        self.account_id = account_id

FC_CONTEXT = FCContext()