import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError
import json

class SpotifyOAuth():

    def __init__(self, clientId, clientSecret):
        self.tokenUrl = "https://accounts.spotify.com/api/token"
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
        
        try:
            res = requests.post(self.tokenUrl, headers=headers, data=data)
            res.raise_for_status()

            resJson = res.json()
            if (resJson["token_type"] != "Bearer"):
                raise ValueError("Spotify Access Token is wrong")
            else:    
                return resJson["access_token"]

        except Timeout:
            print("Request timed out")
        except ConnectionError:
            print("Could not connect to the server")
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Python 3.6 이상
        except Exception as err:
            print(f"An error occurred: {err}")  # Python 3.6 이상