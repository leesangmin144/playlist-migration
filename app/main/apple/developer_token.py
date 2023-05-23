import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError
import jwt, datetime

class AppleDeveloperToken():

    def __init__(self, teamId, keyId, keyPath):
        self.tokenUrl = "https://api.music.apple.com/v1/test"
        self.teamId = teamId
        self.keyId = keyId

        # Read RSA private key
        with open(keyPath, "r") as f:
            self.privateKey = f.read()

    def genDeveloperToken(self):

        payload = {
            "iss": self.teamId,
            "iat": datetime.datetime.utcnow(), # token generation time
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # token expiration time (e.g. valid in 30mins)
        }

        developerToken = jwt.encode(payload, self.privateKey, algorithm="ES256", headers={"alg": "ES256", "kid": self.keyId})

        headers = {
            "Authorization": f"Bearer {developerToken}"
        }

        try:
            res = requests.get(self.tokenUrl, headers=headers, timeout=1)
            res.raise_for_status()
            return f"Bearer {developerToken}"
        except Timeout:
            print("Request timed out")
        except ConnectionError:
            print("Could not connect to the server")
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")