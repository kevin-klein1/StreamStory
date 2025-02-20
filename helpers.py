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

    ## For each match, try to find by match by comparing user data with artist top songs or albums
    for artist in matches:
        artist_id = artist['id']
            
        ## API Call. Get the artist's top tracks
        top_tracks = spotify.artist_top_tracks(artist_id)['tracks']
    
        top_track_names = [track['name'].lower() for track in top_tracks]
        
        ## Get the artist's albums
        albums = spotify.artist_albums(artist_id, album_type='album')['items']
        album_names = [album['name'].lower() for album in albums]
        
        ## Check if any of the user's songs from top tracks
        for user_song in user_data:
            ## If song found and artist name matches, return 
            if user_song[0].lower() in top_track_names and user_song[1].lower() == matches[0]['name'].lower():
                return artist['picture'], artist['id'], artist['uri'], artist['name']

        ## If user data isn't found in song compare, search for album match
        for user_album in user_data:

            ## Check if album name in API list
            if user_album[2].lower() in album_names:

                ## Get album info from helper func
                album_data = search_for_album(spotify, user_album[2], artist['uri'])[2]
                album_tracks_info = get_album_tracks(spotify, album_data)

                for song in album_tracks_info:

                    ## Formatting
                    song_id = f"spotify:track:" + song['id']

                    ## If the uri match. Bug here though - sometimes
                    if user_album[3] == song_id:
                        return artist['picture'], artist['id'], artist['uri'], artist['name']
                    
    # If no good matches found, return original top list match from potential matches
    fallback = ("static/photos/smilesqrblack.png", None, None, matches[0]['name'])

    return fallback


def search_for_album(spotify, album, artist_uri): 

    if not artist_uri:
        return None
    results = spotify.artist_albums(artist_uri, album_type='album')
    albums_list = results['items']
    for record in albums_list:
        current_album_name = record['name']
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
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

