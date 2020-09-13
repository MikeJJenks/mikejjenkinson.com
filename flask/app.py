import csv
from flask import Flask
from flask import abort
from flask import render_template
from flask import current_app
import pandas as pd
import os
import random

app = Flask(__name__)  # Note the double underscores on each side!

path = '/Users/michaeljenkinson/Code/Projects/gitReps/spotter'

def getcsv(fn,fl):
    fn = os.path.join(path,fl,fn) 
    if os.path.exists(fn):
        f = open(fn, 'r')
        fdict = csv.DictReader(f)
        flist = list(fdict)
    else:
        flist = []
    return(flist)

def getjson(fn,fl):
    fn = os.path.join(path,fl,fn)
    if os.path.exists(fn):
        f = pd.read_json(fn)
    else:
        f = []
    print(f)
    return(f)

def getbg():
    path2 = os.path.join(path,'flask','static','images')
    fns = os.listdir(path2)
    if 'DS_Store' in fns:
        fns.remove('DS_Store')
    bg = os.path.join('images',random.choice(fns)) 
    return(bg)

# Static test
@app.route("/")
def index():
    link = 'index.html'
    bg = getbg()
    return render_template(link, bg = bg)

@app.route("/about")
def about():
    link  = 'about.html'
    bg = getbg()
    return render_template(link, bg = bg)

# Static link test
@app.route("/listening")
def listening():
    link  = 'listening.html'
    npl   = 's' 
    
    playsjson = getjson('plays.json','data')
    playscsv = getcsv('plays.csv','data') 

    bg = getbg()
        
    # print(playsjson.columns)

    log   = getcsv('log.csv','logs')[0]
    logdt = log['Time_Updated'].split()
    logdt[1] = ':'.join(logdt[1].split(':')[0:2])
    log['Time_Updated'] = logdt
    logpl = log['Playlist_id'].split(':')[2]
    log['Playlist_id'] = "https://open.spotify.com/playlist/" + logpl

    if( int(log['Plays_Added']) == 1 ):
        npl = ''
    
    # print(playsjson.loc[0,'track.album.images'][0]['url'])
    # print(len(playscsv))
    # print(len(playsjson))
    print(playscsv)

    for i in range(len(playscsv) ):
        print(i)
        if( (i <= len(playsjson) - 1) ):
            playscsv[i]['uri'] = playsjson.loc[i,'track.album.images'][0]['url'] 

    return render_template(link, playscsv = playscsv, log = log, npl = npl, bg = bg)

@app.route('/listening/<trackid>/')
def track(trackid):
    link = 'playdetail.html'
    plays = getjson('plays.json','data')
    playscsv = getcsv('plays.csv','data')

    bg = getbg()


    print(plays)

    for row in playscsv:
        if row['id'] == trackid:
            trackcsv = row
            #print(trackcsv)
    for index, track in plays.iterrows(): 
        #print("here222")
        #print(index)
        #print(track)
        if int(index) == int(trackid):
            return render_template(link, track=track, trackcsv=trackcsv, bg = bg)

    # plays = getcsv('plays.csv','data')
    # for track in plays:
    #     if track['id'] == trackid:
    #         return render_template(link, track=track)
    abort(404)

# Static link test
@app.route("/watching")
def watching():
    link  = 'watching.html'
    bg = getbg()
    films = getcsv('films2.csv','data')
    print(films)
    return render_template(link, bg = bg, films = films)
 
if __name__ == '__main__':
    # Fire up the Flask test server

    app.run(debug=True, use_reloader=True)
