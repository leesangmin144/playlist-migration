import requests
import json

class SpotifyOAuth():

    def __init__(self, clientId, clientSecret):
        self.token_url = "https://accounts.spotify.com/api/token"
        self.clientId = clientId
        self.clientSecret = clientSecret

    def clientCredential(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": self.clientId,
            "client_secret": self.clientSecret
        }
        res = requests.post(self.token_url, headers=headers, data=data)
        return res.json()