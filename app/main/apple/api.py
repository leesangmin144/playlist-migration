import requests

class AppleMusicAPI:
    def searchSongs(self, accessToken, keyword):
        headers = {
            "Authorization": f"Bearer {accessToken}" 
        }

        res = requests.get(f"https://api.spotify.com/v1/playlists/{playlistId}/tracks", headers=headers)

        return res.json()