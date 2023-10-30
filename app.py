from flask import Flask, render_template, session

## Set up flask app
app = Flask(__name__)

## debugger output
##if __name__ == '__main__':
    ##app.run(debug=True, port=5001)
    


## Route display
@app.route("/")
def home():
    return ("again!")