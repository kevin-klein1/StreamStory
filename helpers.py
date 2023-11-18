import json
import datetime
from requests import post, get
from dotenv import load_dotenv
import os
import base64


## Define Functions


## Merging many Spotify Json files as one
def merge_json(files, output_file):
    merged_data = []

    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
            merged_data.extend(data)

    with open(output_file, 'w') as f:
        json.dump(merged_data, f)

'''
## Get Token from Spotify API
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base_64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base_64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}

    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

## Get the request format with token
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


## Function that searches the image of a given artist using API - Returns a http pic
def search_for_artist_pic(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=1"
    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items']
    print(json_result[0]['images'][0]['url'])

def search_for_artist_id(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=1"
    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items']
    print(json_result[0]['id'])




##Function that takes the field as a parameter so you don't have to create different functions
## something to beware of here - some values are inside lists and other dictionaries etc. 

def search_for_artist(token, artist_name, field):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=1"
    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items']
    print(json_result[0][field])


## load enviroment varialbes
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

token = get_token()
print(token)
'''


# Merge JSON files
# Replace with actual file names
##input_files = ['json_files/Spotify_History_Audio_2016-2018_1.json']
##output_file = 'merged_file.json'
##merge_json(input_files, output_file)


## Create file variable
##f = open('merged_file.json')

##Load file into a data object
##data = json.load(f)


## Set up empty dictionaries
favs = {}
songs = {}

'''
while True: 
    try: 
        year = int(input("Please enter a year: "))
        if year > 2010 and year <= 2023:
            break
    except ValueError:
        print("Please Enter A Valid Year")

print()
'''


'''
for i in data:
    time_string = i['ts']
    date_object = datetime.datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%SZ')

    
    

    if year != date_object.year:
        continue
    
    song = i['master_metadata_track_name']
    date = i['ts']
    artist = i['master_metadata_album_artist_name']
    if artist == None or artist == "Valleyheart":
        continue

    if artist in favs:
        favs[artist] += 1
    else: 
        favs[artist] = 1

    if (song, artist) in songs:
        songs[(song, artist)] += 1
    else:
        songs[(song, artist)] = 1

    
## Sort Artists for Top Ten    
sorted_favs = sorted(favs.items(), key=lambda x:x[1], reverse=True)
convert_favs = dict(sorted_favs)

## Sort Songs

sorted_songs = sorted(songs.items(), key=lambda x:x[1], reverse=True)
convert_songs = dict(sorted_songs)




counter = 0
print(f"Your Top Ten Artists are:")
print()
for artist in convert_favs:
    print(artist)
    search_for_artist_pic(token, artist)
    counter += 1
    if counter == 10:
        break 
print()

counter_songs = 0
print("Your Top Songs We're:")
print()
for song in convert_songs:
    print(f"{song[0]} by {song[1]}")
    counter_songs += 1
    if counter_songs == 10:
        break 
print()
print()
for artist, number in list(convert_favs.items())[:10]:
    print(f"You streamed {artist} this many times: {number}")
print()
for (song, artist), number in list(convert_songs.items())[:10]:
    print(f"You streamed {song} by {artist} this many times: {number}")

f.close()

'''