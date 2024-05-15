from flask import Flask, render_template, session, request, redirect, url_for, make_response
import os
from werkzeug.utils import secure_filename
import json
import datetime
from dotenv import load_dotenv
import helpers
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import debug




## Create the routing connection for uploading json files
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'json_files')
ALLOWED_EXT = {'json'}



## Set up flask app
app = Flask(__name__)


## Cookie config 
app.config['SESSION_COOKIE_NAME'] = 'User Cookie'
app.secret_key = '123g834#$9gsfg54'
TOKEN_INFO = "token_info"



## Config upload path
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

## Global lists for approved years & result path
Approved_years = ['2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023', '2024']
Filter = ['Artists', 'Songs', 'Albums']

SCOPES = "playlist-read-collaborative user-top-read user-read-email user-read-private"

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

## Index route display
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        
        ## checks if token session exists and redirects to user page if so
        if 'token_info' in session and session['token_info'] is not None:
            return redirect(url_for('userinfo'))
        
        session.clear()

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

        ## Init OAuth Object from Spotipy
        sp_oauth = SpotifyOAuth()

        ## Get Spotify login url from object 
        auth_url = sp_oauth.get_authorize_url()

        ## get access code from request params
        code = request.args.get('code')

        ## pass code as arguement to get access function to obtain token info
        token_info = sp_oauth.get_access_token(code)

        ## assign token info to session variable
        session[TOKEN_INFO] = token_info

        return redirect(auth_url)

## logout route
@app.route('/logout')
def logout():

    session.clear()  
    return redirect("/")


@app.route('/userinfo', methods=["GET", "POST"])
def userinfo():

    if request.method == "GET":

        ## check for cancel error 
        error = request.args.get('error')
        if error == 'access_denied':
            return redirect('/')
    
        ## checks if user is logged in
        if 'token_info' not in session:
            return redirect(url_for('index'))

        ## creates Spotify object that handles API calls and retrieval 
        sp = spotipy.Spotify(auth=session[TOKEN_INFO]['access_token'])

        ## gets info from current user
        user = sp.current_user()

        ## assign profile pic and external link to session variable for multi scoped use
        session['user_photo'] = user['images'][0]['url']
        session['user_link'] = user['external_urls']['spotify']


        ## response as a variable for cleaner output
        response = make_response(render_template("index2.html", profile_pic= session['user_photo'], profile_link=session['user_link']))

        # Add cache-control headers to prevent caching
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"

        return response
    
    if request.method == "POST":

            ## Get files from browse button
            files = request.files.getlist('file')
            ## Get files from drag and drop
            files2 = request.files.getlist('file2')

            ## Upload files into project
            upload_files(files)
            upload_files(files2)

            return redirect("/years")
        
    
@app.route("/years", methods=["GET", "POST"])
def years():
    if request.method == "GET":

        ## Creates login state. checks if user is logged in, if so renders login state
        logged_in = 'token_info' in session and session['token_info'] is not None
        if logged_in:
            profile_pic = session['user_photo']
            profile_link = session['user_link']
        else:
            profile_pic = None
            profile_link = None
        return render_template("years.html", logged_in=logged_in, profile_pic=profile_pic, profile_link=profile_link)


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

        
        logged_in = 'token_info' in session and session['token_info'] is not None
        if logged_in:
            profile_pic = session['user_photo']
            profile_link = session['user_link']
        else:
            profile_pic = None
            profile_link = None
        return render_template("filter.html",logged_in=logged_in, profile_pic=profile_pic, profile_link=profile_link)

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

        logged_in = 'token_info' in session and session['token_info'] is not None
        if logged_in:
            profile_pic = session['user_photo']
            profile_link = session['user_link']
        else:
            profile_pic = None
            profile_link = None

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
        return render_template('results.html',profile_pic=profile_pic, profile_link=profile_link, path=session['path'],years=session['selected_years'], results=results)
    



    

if __name__ == '__main__':
    app.run(debug=True, port=5005)

    