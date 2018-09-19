import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

# get username from terminal from arg

username = sys.argv[1]

# Erase cache and prompt for user permission access

try:
    token = util.prompt_for_user_token(username)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)

# Create our spotipy object

spotify = spotipy.Spotify(auth=token)

user = spotify.current_user()
print(json.dumps(user, sort_keys=True, indent=4))

display_name = user["display_name"]
followers = user["followers"]["total"]

while True:
    print()
    print(">>> Welcome to Spotify CLI " + display_name + "!")
    print(">>> You have %s followers" % followers)
    print()
    print("0 - Search for an artist")
    print("1 - exit")

    print()
    choice = input("Your choice: ")

    if choice == "0":
        print()
        search_query = input("Who would like to search for?: ")
        print()

        # search result
        search_result = spotify.search(search_query, 2, 0, "artist")

        # artist details
        artist = search_result['artists']['items'][0]
        artist_id = artist['id']
        print(artist['name'])
        print("%s followers" % artist['followers']['total'])
        print(artist['genres'][0])
        print()

        webbrowser.open(artist['images'][0]['url'])

        # album and track details
        track_uris = []
        track_art = []
        z = 0

        # extract album data
        album_results = spotify.artist_albums(artist_id)['items']

        for item in album_results:
            print("ALBUM: %s" % item['name'])
            album_id = item['id']
            album_art = item['images'][0]['url']

            track_results = spotify.album_tracks(album_id)['items']

            for track in track_results:
                print("%s: %s" % (z, track['name']))
                track_uris.append(item['uri'])
                track_art.append(album_art)
                z+=1

            print()

        while True:
            song_selection = input("Enter a song number to view its album art: ")

            webbrowser.open(track_art[int(song_selection)])

    if choice == "1":
        break

# print(json.dumps(VARIABLE, sort_keys=True, indent=4))


