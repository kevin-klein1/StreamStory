import json
from dotenv import load_dotenv
import os
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
    # Make the API call to search for artists by name
    results = spotify.search(q='artist:' + artist, type='artist')


    # Extract items (artists) from the response. Returns an object of potential artsts
    items = results['artists']['items']

    # This will hold the matches of potential artists of same name
    matches = []

    for artist_pot in items:

        ## Check if the artist's name exactly matches the input. the beatles == the beatles
        if artist_pot['name'].lower() == artist.lower():
            
            ## Assigns field we know will have data to dict
            artist_info = {
            'name': artist_pot['name'],
            'id': artist_pot['id'],
            'uri': artist_pot['uri'],
            }

            # Check if the artist has images. Sometimes field can come back empty
            if not artist_pot['images']:
                artist_info['picture'] = "static/photos/smilesqrblack.png"
            else:
                artist_info['picture'] = artist_pot['images'][0]['url']

            ## Append to list of potential artists
            matches.append(artist_info)

    # Return the list of matched artists {name, id, uri, photo}
    return matches


def verify_artist(spotify, matches, user_data):

    ## For each match, try to find by match by comparing user data with artist total songs 
    for artist in matches:
        artist_id = artist['id']
            
        ## Create empty list to store album ids
        album_ids = []

        ## Aggregate song bank of all artist's songs
        song_bank = []

        ## Fetch artist's albums
        artist_albums = spotify.artist_albums(artist_id=artist_id)['items']

        ## Append list of each album ids 
        for album in artist_albums:
            album_ids.append(album['id'])
        
        ## Fetch album info for all artist's albums
        albums_info = spotify.albums(album_ids)['albums']

        ## For each album, get all track names and append to song_bank
        for album in albums_info:
            for track in album['tracks']['items']:
                song_bank.append(track['name'])
        ## Check if song/artist stream in current user's data, is found in song bank + artist names match
        for user_song in user_data:
            if user_song[0] in song_bank and user_song[1].lower() == artist['name'].lower():
                return artist['picture'], artist['id'], artist['uri'], artist['name']    

    ## If none found, return None
    return None




def search_for_album(spotify, album, artist_uri): 

    ## If no uri is present return None
    if not artist_uri:
        return None
    
    ## Fetch Artist's albums
    results = spotify.artist_albums(artist_uri, album_type='album')
    albums_list = results['items']

    ## Search for album match in object
    for record in albums_list:

        ## Current record's name
        current_album_name = record['name']
        current_album_name = current_album_name.lower()

        ## If target album == our album, return
        if album.lower() == current_album_name:
            return record['images'][0]['url'], record['uri'], record['id']
        elif album.lower() in current_album_name:
            if "live" or "deluxe" in current_album_name:
                continue
            return record['images'][0]['url'], record['uri'], record['id']
        else:
            continue
    return None

def get_album_tracks(spotify, album_id):
    results = spotify.album_tracks(album_id)
    track_listing_info = results['items']
    return track_listing_info

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
# load_dotenv() -> development only 
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

