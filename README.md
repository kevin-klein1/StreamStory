

<h1 class="heading-element" dir="auto">StreamStory 🔮</h1>



StreamStory is an app built with Python/Flask that takes Extended Spotify Streaming Data (json) and parses it into a Spotify Wrapped-like visualization for your top artists, songs, and albums. 

<h2 class="heading-element" dir="auto">Features</h2>

* Extended History Parsing: The app allows you to aggregate and/or filter years of your streaming data. Think of Spotify-Wrapped but for any or all years of listening history.
* Artist, Song, or Album: Ability to choose one of these pages to see top 10 most streamed with number of times streamed. 

<h2 class="heading-element" dir="auto">Getting Started</h2>

1) Request your streaming history data from Spotify <a href="https://www.spotify.com/us/account/privacy/#_=" target="_blank">here</a>. Make sure you select "Extended Streaming History", not "Account Data".

2) Spotify will send you a zip file with your data within 5-7 days. You will recieve JSON files with all your data.

3) Upload json files into the homepage. 

4) See .env_sample file for instructions on API key setup for testing. Go to <a href="https://developer.spotify.com/" target="_bank">Spotify For Developers</a> to retrieve your keys. 

5) Enter command "flask run" or "flask run --debug" in terminal to get the server up and running. 

## Library Packages

* [Flask](https://flask.palletsprojects.com/en/3.0.x/)
* [Python-dotenv](https://pypi.org/project/python-dotenv/)
* [Spotipy!](https://spotipy.readthedocs.io/en/2.22.1/)

##

  
<br>
<br>
<img width="1549" alt="StreamStory photo" src="https://github.com/user-attachments/assets/fe1bba3c-6e0f-426b-a621-a7a98139ca18">









