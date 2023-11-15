from flask import Flask, render_template, session, request, redirect, url_for

import requests
import os
from werkzeug.utils import secure_filename
import seaborn as sea
import json
import datetime
from dotenv import load_dotenv
import base64
##import helpers


## Create the routing connection for uploading json files
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'json_files')
ALLOWED_EXT = {'json'}



## Set up flask app
app = Flask(__name__)




## Config upload path
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

## Function for allowed json (extra care)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT



## Route display
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
        return render_template("index.html")
    if request.method == "POST":
        ## Get files from the html form
        files = request.files.getlist('file')
       
        for file in files:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
              
        return redirect("/results")
        
    
@app.route("/results", methods=["GET", "POST"])
def results():
    if request.method == "GET":
        input_files = []
        for filename in os.listdir(UPLOAD_FOLDER):
            input_files.append("json_files/" + filename)

        output_file = 'merged_files.json'
        ##helpers.merge_json(input_files, output_file)

        f = open('merged_file.json')

        ##data = json.load(f)

        ##favs = {}
        if request.method == "POST":
            year_list = request.form.getlist('selectedYears')
            print(year_list)



        return render_template("results.html")

    if request.method == "POST":
        selected_years = request.form.getlist('selectedYear')
        print(selected_years)

        return redirect("/filter")


    
@app.route("/filter", methods=["GET", "POST"])
def filter():
    if request.method == "GET":
        return render_template("filter.html")

    if request.method == "POST":
        return render_template("lists.html")
    

if __name__ == '__main__':
    app.run(debug=True, port=5005)

    
