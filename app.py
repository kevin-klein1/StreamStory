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
        if selected_option == "artists":
            print(selected_option)
            return redirect("/artists")
        elif selected_option == "songs":
            print(selected_option)
            return redirect("/songs")
        elif selected_option == "albums":
            print(selected_option)
            return redirect("/albums")
        else:
            return ("Error")
        
    

@app.route("/artists")
def artists():
    if request.method == "GET":
        favs = {}
        songs = {}
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
            print(type(date_object_str))
            print(session['selected_years'])

            if date_object_str not in session['selected_years']:
                print("wow")
                continue

            artist = i['master_metadata_album_artist_name']
            if artist == None or artist == "Valleyheart":
                continue

            if artist in favs:
                favs[artist] += 1
            else: 
                favs[artist] = 1

            
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

        counter_songs = 0

        for artist, number in list(convert_favs.items())[:10]:
            print(f"You streamed {artist} this many times: {number}")

        f.close()


        return render_template('artists.html')
    
@app.route("/songs")
def songs():
    return render_template('songs.html')
   
    
@app.route("/albums")
def albums():
    return render_template('albums.html')
   
    
    

if __name__ == '__main__':
    app.run(debug=True, port=5005)

    
