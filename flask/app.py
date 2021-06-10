import csv
from flask import Flask
from flask import abort
from flask import render_template
from flask import current_app
import pandas as pd
import os
import random

# 'mstat.py' contains function definitions written for use in this flask application.
import mstat

# Initialize Flask app
app = Flask(__name__)

# This is the path to the spotter output data files.  
path = '/Users/michaeljenkinson/Code/Projects/gitReps/spotter'

# Render home page. 
@app.route("/")
def index():
    link = 'index.html'

    # Get random page background from stored images.
    bg = getbg()
    return render_template(link, bg = bg)

# Summary readout page for listening history from Spotter app.
@app.route("/listening")
def listening():
    link  = 'listening.html'
    
    # Number of aggregated top tracks and artists to show.
    disp  = 10
  
    # Grab simple and detailed full play files.
    playsjson = getjson('plays.json','data')
    playscsv = getcsv('plays.csv','data', op = 1)

    # Get random page background.
    bg = getbg()

    # Get latest update time and playlist id (should not change until playlist is full) from log file. 
    log   = getcsv('log.csv','logs')[0]
    log['Time_Updated'] = splittime(log['Time_Updated'])
    logpl = log['Playlist_id'].split(':')[2]
    log['Playlist_id'] = "https://open.spotify.com/playlist/" + logpl

    # Fix page grammar if only one play was added.
    if( int(log['Plays_Added']) == 1 ):
        npl = ''

    # Only use the first artist id available if there are multiple artists.
    playscsv['artistid'] = playscsv['artistid'].apply(splitarts)

    # Get monthly and annual top artists and top tracks played.
    topartsm, toptracksm = mstat.getags(playscsv,  30)
    topartsy, toptracksy = mstat.getags(playscsv,  365) 

    # Get album art from detailed play history; change this to merge for speed.
    for i, row in playscsv.iterrows(): 
        if( (i <= len(playsjson) - 1) ):
            playscsv.loc[i]['uri'] = playsjson.loc[i,'track.album.images'][0]['url']

    # Format time played for tracks into date and time (smallest unit of minutes) - this is done after 'getags' since turning
    # 'Time_Played' into a series of lists makes aggregating by date impossible.
    playscsv['Time_Played'] = playscsv['Time_Played'].apply(splittime)

    # First ten and second ten recent tracks are displayed in separate style boxes and are passed separately for 
    # ease of use with iterator in Flask/Jinja. Check itertools later.
    playsr1 = playscsv.iloc[ 0:10,:]
    playsr2 = playscsv.iloc[10:20,:] 

    # Full play variable 'playscsv' not used in template (deprecated).
    return render_template(link, playscsv = playscsv, log = log, bg = bg, 
            topartsm = topartsm.head(disp), toptracksm = toptracksm.head(disp), 
            topartsy = topartsy.head(disp), toptracksy = toptracksy.head(disp),
            playsr1  = playsr1, playsr2 = playsr2)



###### The following page definitions are deprecated or for future construction. ######

# Page for information about website.
@app.route("/about")
def about():
    link  = 'about.html'
    bg = getbg()
    return render_template(link, bg = bg)

# Control panel for spotter app.
@app.route("/controlpanel")
def controlpanel():
    link  = 'controlpanel.html'
    bg = getbg()

    # Get update log file and track play files.
    logs = getcsv('log.csv','logs')
    playsjson = getjson('plays.json','data')
    playscsv = getcsv('plays.csv','data')

    return render_template(link, bg = bg, logs = logs)

# Listening statistics readout page.  
@app.route("/listening/fulltracks")
def fulltracks():
    link  = 'fulltracks.html'
    npl   = 's' 
    
    playsjson = getjson('plays.json','data')
    playscsv = getcsv('plays.csv','data') 

    bg = getbg()

    log   = getcsv('log.csv','logs')[0]
    logdt = log['Time_Updated'].split()
    logdt[1] = ':'.join(logdt[1].split(':')[0:2])
    log['Time_Updated'] = logdt
    logpl = log['Playlist_id'].split(':')[2]
    log['Playlist_id'] = "https://open.spotify.com/playlist/" + logpl

    if( int(log['Plays_Added']) == 1 ):
        npl = ''
    

    for i in range(len(playscsv) ):
        if( (i <= len(playsjson) - 1) ):
            playscsv[i]['uri'] = playsjson.loc[i,'track.album.images'][0]['url'] 

    return render_template(link, playscsv = playscsv, log = log, npl = npl, bg = bg)

@app.route('/listening/<trackid>/')
def track(trackid):
    link = 'playdetail.html'
    plays = getjson('plays.json','data')
    playscsv = getcsv('plays.csv','data')

    bg = getbg()

    for row in playscsv:
        if row['id'] == trackid:
            trackcsv = row
    for index, track in plays.iterrows(): 
        if int(index) == int(trackid):
            return render_template(link, track=track, trackcsv=trackcsv, bg = bg)

    abort(404)

# Static link.
@app.route("/static")
def watching():
    link  = 'static.html'
    bg = getbg()
    return render_template(link, bg = bg, films = films)


########################################
# Test server for debugging.
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
