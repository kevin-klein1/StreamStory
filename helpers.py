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
    result = json_result[0]['images'][0]['url']
    return result

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

