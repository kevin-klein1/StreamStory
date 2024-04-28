from flask import Flask, render_template, session, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import json
import datetime
from dotenv import load_dotenv
import helpers
import spotipy
from spotipy.oauth2 import SpotifyOAuth




## Create the routing connection for uploading json files
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'json_files')
ALLOWED_EXT = {'json'}



## Set up flask app
app = Flask(__name__)
app.secret_key = '1234'



## Config upload path
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

## Global lists for approved years & result path
Approved_years = ['2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023', '2024']
Filter = ['Artists', 'Songs', 'Albums']

## Function Defs

## Function for allowed json (extra care)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

# Uploads users json into project
def upload_files(files):
    for file in files:
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

# def create_spotify_oauth():
#     return SpotifyOAuth(
#         client_id=, 
#         client_secret=, 
#         redirect_uri=, 
#         scope=)

## load .env files (client id and sercet)
load_dotenv()
 
## Index route display
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        ## Create json folder upon each homepage visit if not exisiting already
        if not os.path.exists(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)

        ## Delete all the json files in directory to start fresh each upload
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            os.unlink(file_path)

        ## Delete old JSON from any previous search
        if os.path.exists('merged_file.json'):
            os.unlink('merged_file.json')
        return render_template("index.html")
    
    if request.method == "POST":

        ## Get files from browse button
        files = request.files.getlist('file')
        ## Get files from drag and drop
        files2 = request.files.getlist('file2')

        ## Upload files into project
        upload_files(files)
        upload_files(files2)

        return redirect("/years")
    

## Oauth Spotify redirection
@app.route('/login')
def login():
     ## create Oauth ojbject for user auth
        sp_oauth = SpotifyOAuth()
        auth_url = sp_oauth.get_authorize_url()
    
        return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    print("debug")
    return "yo"
    
        
    
@app.route("/years", methods=["GET", "POST"])
def years():
    if request.method == "GET":
        return render_template("years.html")

    if request.method == "POST":
        ## Get list of years user wants to filter
        selected_years_unconverted = request.form.getlist('selectedYears')

        ## Format years correctly for comparison & store in session variable
        for year in selected_years_unconverted:
            session['selected_years'] = year.split(',')
    
        ## Make sure years are approved years
        for year in session['selected_years']:
            if year not in Approved_years:
                message = "Years not valid!"
                return render_template("error.html", message=message,path=request.path.strip("/").title())
        return redirect("/filter")


    
@app.route("/filter", methods=["GET", "POST"])
def filter():
    if request.method == "GET":
        return render_template("filter.html")

    if request.method == "POST":
        ## Get results path selection into session variable
        selected_option = request.form['selection']
        if selected_option not in Filter:
            message= "Not a Valid Option!"
            return render_template("error.html",message=message, path=request.path.strip("/").title())
        session['path'] = selected_option
        return redirect("/results")
    else:
        return render_template ("error.html")
        
    

@app.route("/results")
def results():
    if request.method == "GET":
        ## Set up folder path to json files and get file names
        folder_path = os.path.join(app.root_path, 'json_files')
        input_files = os.listdir(folder_path)

        ## File paths for each json file 
        input_file_paths = [os.path.join(folder_path, file) for file in input_files]

        ## name output file and call merge to make one json file
        output_file = 'merged_file.json'
        helpers.merge_json(input_file_paths, output_file)

        ## load merged file
        f = open('merged_file.json')
        data = json.load(f)

        ## Set up empty dictionaries for results
        favs = {}
        songs = {}
        albums = {}

        ## Main for loop that goes through each object in JSON
        for stream in data:

            ## Get the year of stream from JSON
            time_string = stream['ts']
            date_object = datetime.datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%SZ')
            stream_year = str(date_object.year)

            ## Filter through years selected by user, abort loop if not found
            if stream_year not in session['selected_years']:
                continue

            ## Set up json artist, song, album variables
            artist = stream['master_metadata_album_artist_name']
            song = stream['master_metadata_track_name']
            album = stream['master_metadata_album_album_name']

            if artist == None:
                continue
        
            ## Artist Dictionary
            if artist in favs:
                favs[artist] += 1
            else: 
                favs[artist] = 1

        
            ## Song Dictionary
            if (song, artist,album) in songs:
                songs[(song, artist,album)] += 1
            else:
                songs[(song, artist,album)] = 1
   
            ## Album Dictionary
            if (album, artist) in albums:
                albums[(album, artist)] += 1
            else:
                albums[(album, artist)] = 1

        ## Make sure theres data in the dictionaries, if not - return error page
        if len(favs) == 0:
            return render_template("error.html", message="No Data for these years!", path=request.path)


        ## Set up Top Ten Dictionary
        results = {}

        ## Spotipy creds authorization library
        # spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

        ## play around with the OAuth Code Flow method
        # try:
        spotify = spotipy.Spotify(auth_manager=SpotifyOAuth())
        # except Exception:
        #     return render_template("error.html", message="Something went wrong :(", path=request.path)

        
        if session['path'] == "Artists":
            ## Sort Artists for Top Ten in sorted dict   
            sorted_favs = sorted(favs.items(), key=lambda x:x[1], reverse=True)
            convert_favs = dict(sorted_favs)

            counter = 0
            ## insert top ten for artists
            for artist, number in convert_favs.items():
                ## Get tuple of artist info with Spotify API call
                artist_info = helpers.search_for_artist_info(spotify, artist)

                artist_pic = artist_info[0]
                artist_uri = artist_info[2]

                ## Insert into results all info and picture
                results[artist, number, artist_uri] = artist_pic

                counter += 1
                if counter == 10:
                    break 
        
        if session['path'] == "Songs":
            ## Sort
            sorted_songs = sorted(songs.items(), key=lambda x:x[1], reverse=True)
            convert_songs = dict(sorted_songs)


            counter_songs = 0
            ## Insert
            for (song,artist,album), number in convert_songs.items():
                artist_info = helpers.search_for_artist_info(spotify, artist)

                artist_pic = artist_info[0]
                artist_id = artist_info[1]
                artist_uri = artist_info[2]

                ## Some artist_info comes back empty, if that's the case abort to avoid error
                if artist_info is None:
                    continue

                if artist_pic == None:
                    ## load a default image if artist picture is not found  
                    ## artist_pic = path to smile.png in static folder, load from there
                    artist_pic = "static/photos/smil.jpeg"
                    
                    
                    

                ## API call to get album information
                album_info = helpers.search_for_album(spotify, artist_id, album)


                ## Make sure this isn't Null + if it is: just display the artist picture. 
                if album_info != None:

                    # Get album info + Get Song uri link for href image link to spotify page 
                    album_pic = album_info[0]
                    album_id = album_info[2]
                    album_uri = album_info[1]
                    song_uri = helpers.search_song_uri(spotify, album_id, song)

                    ## Insert
                    results[(song,artist,number,song_uri)] = album_pic
                else:
                    results[(song,artist,number,artist_uri)] = artist_pic

                counter_songs += 1
                if counter_songs == 10:
                    break 


        if session['path'] == "Albums":

    
            sorted_albums = sorted(albums.items(), key=lambda x:x[1], reverse=True)
            convert_albums = dict(sorted_albums)

            counter_album = 0
            print("Your Top Albums Were:")
            print()
            for (album, artist), number in convert_albums.items():
                artist_info = helpers.search_for_artist_info(spotify, artist)

                artist_pic = artist_info[0]
                artist_id = artist_info[1]
                artist_uri = artist_info[2]

                album_info = helpers.search_for_album(spotify, artist_id, album)

                if album_info != None:

                    album_pic = album_info[0]
                    album_uri = album_info[1]
                    album_id = album_info[2]
                    results[(album,artist,number, album_uri)] = album_pic
                else:
                    results[(album,artist,number, artist_uri)] = artist_pic
                    print()
                counter_album += 1
                if counter_album == 10:
                    break

        f.close()
        return render_template('results.html',path=session['path'],years=session['selected_years'], results=results)
    



    

if __name__ == '__main__':
    app.run(debug=True, port=5005)

    