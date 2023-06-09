from flask import Flask, abort, json, render_template, request
from spotify.client_credential import SpotifyOAuth
from spotify.api import SpotifyAPI
from apple.developer_token import AppleDeveloperToken
from apple.api import AppleMusicAPI

SPOTIFY_CLIENT_ID = b""
SPOTIFY_CLIENT_SECRET = b""

APPLE_TEAM_ID = b""
APPLE_KEY_ID = b""
APPLE_KEY_PATH = b""

app = Flask(__name__)

def getSpotifyAccessToken():
    so = SpotifyOAuth(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    accessToken = so.clientCredential()
    
    return accessToken
    
def getAppleAccessToken():
    adt = AppleDeveloperToken(APPLE_TEAM_ID, APPLE_KEY_ID, APPLE_KEY_PATH)
    developerToken = adt.genDeveloperToken()
    
    return developerToken
    
@app.route("/apple/write/playlist")
def writePlaylistToAppleMusic():
    accessToken = getAppleAccessToken()

    searchResults = AppleMusicAPI().searchSongs(accessToken, "You Make Me Feel Like Dancing - Remastered")
    return searchResults

@app.route("/spotify/fetch/playlist")
def fetchPlaylistFromSpotify():
    # TODO: Change to receive only playlistId from html 
    playlistId = request.args.get("playlistId").split('/')[4]

    accessToken = getSpotifyAccessToken()

    playlistItems = SpotifyAPI().getPlaylistItems(accessToken, playlistId)

    songs = {}
    try:
        for index, item in enumerate(playlistItems["items"], start=0):
            songs[index] = item["track"]["name"]
    except:
        return "fetch playlist error"

    return songs

@app.route('/')
def home():
    return render_template('index.html')

@app.errorhandler(404)
def pageNotFound(error):
    return render_template("page_not_found.html"), 404

if __name__ == '__main__':

    # Read Spotify's client_id and client_secret for OAuth
    try:
        with open("credentials.txt") as f:
            creds = json.loads(f.read().strip())   

            SPOTIFY_CLIENT_ID = creds["spotify"]["CLIENT_ID"]
            SPOTIFY_CLIENT_SECRET = creds["spotify"]["CLIENT_SECRET"]

            APPLE_TEAM_ID = creds["apple"]["TEAM_ID"]
            APPLE_KEY_ID = creds["apple"]["KEY_ID"] 
            APPLE_KEY_PATH = creds["apple"]["KEY_PATH"]

    except FileNotFoundError:
        print("The file does not exist.")
    except PermissionError:
        print("You do not have permission to access the file.")
    except IsADirectoryError:
        print("You are trying to open a directory, not a file.")
    except FileExistsError:
        print("The file already exists.")
    except Exception as e:
        print("An unexpected error occurred:", e)

    app.run(port=5000, debug=True)