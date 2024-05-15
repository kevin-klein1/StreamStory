import json
import datetime
from requests import post, get
from dotenv import load_dotenv
import os
import base64
from flask import request, redirect





## Define Functions


## reads json object, stringfy's it and writes/creates json file in workspace. Used to read json server side. 

def write_json_file(object):
    json_str = json.dumps(object)
    with open('test.json', 'w') as file:
        file.write(json_str)



## Merging many Spotify Json files as one
def merge_json(files, output_file):
    merged_data = []

    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
            merged_data.extend(data)

    with open(output_file, 'w') as f:
        json.dump(merged_data, f)


def search_for_artist_info(spotify, artist):
    results = spotify.search(q='artist:' + artist, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        artist = items[0]
        id = artist['id']
        try:
            result = artist['images'][0]['url']
        except IndexError:  
            result = None
        uri = artist['uri']
        return result, id, uri 


def search_for_album(spotify, id, album): 
    artist_uri = "spotify:artist:" + id
    results = spotify.artist_albums(artist_uri, album_type='album')
    albums_list = results['items']
    for record in albums_list:
        current_album_name = record['name']
        ##print()
        ##print(f"{current_album_name} == {album}")
        ##print()
        current_album_name = current_album_name.lower()
        if album.lower() == current_album_name:
            return record['images'][0]['url'], record['uri'], record['id']
        elif album.lower() in current_album_name:
            if "live" or "deluxe" in current_album_name:
                continue
            return record['images'][0]['url'], record['uri'], record['id']
        else:
            continue
    return None



def search_song_uri(spotify, album_id, song):
    result = spotify.album_tracks(album_id)
    tracks = result['items']
    for track_object in tracks:
        track_name = track_object['name']
        if song.lower() == track_name.lower():
            return track_object['uri']
        else:
            continue
    return None


def spotify_callback():
    # Check if there's an error parameter in the request
    error = request.args.get('error')
    if error == 'access_denied':
        # User denied access, redirect to a different page
        return redirect('/')


## load enviroment varialbes
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

