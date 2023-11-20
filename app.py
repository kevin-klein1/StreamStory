from flask import Flask, render_template, session, request, redirect, url_for
import requests
import os
from werkzeug.utils import secure_filename
import json
import datetime
from dotenv import load_dotenv
import base64
import helpers


## Create the routing connection for uploading json files
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'json_files')
MAIN_FOLDER = os.path.join(os.getcwd(), 'json_files')

ALLOWED_EXT = {'json'}



## Set up flask app
app = Flask(__name__)
app.secret_key = '1234'




## Config upload path
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

Approved_years = ['2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023']
Filter = ['artist', 'songs', 'album']


## Function for allowed json (extra care)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

def upload_files(files):
    for file in files:
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


## Index route display
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        ## Delete all the json files in directory to start fresh each upload
        ##token = helpers.get_token()
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            try:
                os.unlink(file_path)
            except Exception as e:
                flash(f"Error deleting file: {e}", 'error')
                return redirect(request.url)
            
        if os.path.exists('merged_file.json'):
            os.remove('merged_file.json')

        return render_template("index.html")
    if request.method == "POST":
        ## Get files from the html form

        ## files from browse
        files = request.files.getlist('file')
        ## files from drag and drop
        files2 = request.files.getlist('file2')

        upload_files(files)
        upload_files(files2)

       
       
        return redirect("/years")
        
    
@app.route("/years", methods=["GET", "POST"])
def years():
    if request.method == "GET":

        input_files = []
        for filename in os.listdir(UPLOAD_FOLDER):
            input_files.append("json_files/" + filename)

        return render_template("years.html")

    if request.method == "POST":
        selected_years_unconverted = request.form.getlist('selectedYears')

        for year in selected_years_unconverted:
            session['selected_years'] = year.split(',')
    
        for year in session['selected_years']:
            if year not in Approved_years:
                return render_template("error.html")
        
    
        return redirect("/filter")


    
@app.route("/filter", methods=["GET", "POST"])
def filter():
    if request.method == "GET":
        return render_template("filter.html")

    if request.method == "POST":
        selected_option = request.form['selection']
        session['path'] = selected_option
        print(session['path'])
        return redirect("/results")
    else:
        return render_template ("error.html")
        
    

@app.route("/results")
def results():
    if request.method == "GET":
        favs = {}
        songs = {}
        albums = {}

        folder_path = os.path.join(app.root_path, 'json_files')
        input_files = os.listdir(folder_path)

        input_file_paths = [os.path.join(folder_path, file) for file in input_files]
     
        output_file = 'merged_file.json'
        helpers.merge_json(input_file_paths, output_file)


        f = open('merged_file.json')
        data = json.load(f)

        for i in data:
            time_string = i['ts']
            date_object = datetime.datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%SZ')
        

            date_object_str = str(date_object.year)


            counter_years = 0
            if date_object_str not in session['selected_years']:
                counter_years += 1
                if counter_years >= len(data):
                    message = "No data for these years"
                    return render_template("error.html", message=message)
                continue

            ## Set up json artist, song, album variables
            artist = i['master_metadata_album_artist_name']
            song = i['master_metadata_track_name']
            album = i['master_metadata_album_album_name']

            if artist == None or artist == "Valleyheart":
                continue

            if artist in favs:
                favs[artist] += 1
            else: 
                favs[artist] = 1

            ## Song Dict set up
            if (song, artist) in songs:
                songs[(song, artist)] += 1
            else:
                songs[(song, artist)] = 1

            ## Album Dict set up
            if (album, artist) in albums:
                albums[(album, artist)] += 1
            else:
                albums[(album, artist)] = 1

        if session['path'] == "artists":
            ##path variable for jinja
            path = "Artists"
            ## Sort Artists for Top Ten    
            sorted_favs = sorted(favs.items(), key=lambda x:x[1], reverse=True)
            convert_favs = dict(sorted_favs)

            counter = 0
            print(f"Your Top Ten Artists are:")
        
            print()
            for artist in convert_favs:
                print(artist)
                ##search_for_artist_pic(token, artist)
                counter += 1
                if counter == 10:
                    break 
            print()
            for artist, number in list(convert_favs.items())[:10]:
                print(f"You streamed {artist} this many times: {number}")
            data_final = convert_favs
        
        if session['path'] == "songs":
            path = "Songs"
            sorted_songs = sorted(songs.items(), key=lambda x:x[1], reverse=True)
            convert_songs = dict(sorted_songs)

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
            for (song, artist), number in list(convert_songs.items())[:10]:
                print(f"You streamed {song} by {artist} this many times: {number}")
            data_final = convert_songs


        if session['path'] == "albums":
            path = "Albums"
            sorted_albums = sorted(albums.items(), key=lambda x:x[1], reverse=True)
            convert_albums = dict(sorted_albums)

            counter_album = 0
            print("Your Top Albums Were:")
            print()
            for (album, artist) in convert_albums:
                print(f"{album} by {artist}")
                counter_album += 1
                if counter_album == 10:
                    break 
            print()
            
            print()
            for (album, artist), number in list(convert_albums.items())[:10]:
                print(f"You streamed {album} by {artist} this many times: {number}")
            data_final = convert_albums



        f.close()
        return render_template('results.html',path=path,years=session['selected_years'], data=data_final)
    

    

if __name__ == '__main__':
    app.run(debug=True, port=5005)

    
