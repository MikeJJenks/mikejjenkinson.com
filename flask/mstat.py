import pandas as pd
import datetime

# This file contains function definitions used in the main flask application file 'app.py'.

# Open a csv file as a dataframe, unless op = 0 which opens it as a list. 
def getcsv(fn,fl,op = 0):
    fn = os.path.join(path,fl,fn)
    if os.path.exists(fn):
        if( op == 0 ):
            f = open(fn, 'r')
            fdict = csv.DictReader(f)
            flist = list(fdict)
        else:
            flist = pd.read_csv(fn)
    else:
        flist = []
    return(flist)

# Open a json file as a dataframe.
def getjson(fn,fl):
    fn = os.path.join(path,fl,fn)
    if os.path.exists(fn):
        f = pd.read_json(fn)
    else:
        f = []
    return(f)

# Get top aggregated artists and tracks for given time period (in days)
def getags(pin, nt):

    # Get date cutoff for time period nt.
    cutoff = pd.Timestamp.utcnow() - pd.Timedelta(days=nt)
    # cutoff = cutoff.replace(hour=0, minute=0, second=0, microsecond = 0)
    pin['Time_Played'] = pd.to_datetime(pin['Time_Played'])
    pcur = pin[ pin['Time_Played'] >= cutoff ]

    # Aggregate top artists and top tracks after cutoff date.
    toparts   = pcur.groupby(    ['Artist', 'artistid']).id.count().sort_values(ascending = False)  
    toptracks = pcur.groupby(['Track_Name', 'Artist', 'Album', 'trackid']).id.count().sort_values(ascending = False)

    # Convert to data.frame
    toparts   = toparts.to_frame(name = 'count').reset_index()
    toptracks = toptracks.to_frame(name = 'count').reset_index()

    return toparts, toptracks

# Choose a random background from the appropriate folder.
def getbg():
    path2 = os.path.join(path,'flask','static','images')
    fns = os.listdir(path2)
    if 'DS_Store' in fns:
        fns.remove('DS_Store')
    bg = os.path.join('images',random.choice(fns))
    return(bg)

# Function 'splittime' splits a full UTC time object into date and time, with minutes as the smallest unit.
def splittime(x):
    xnew = str(x).split()
    if( len(xnew) == 1 ):
        xnew = str(x).split('T')
    xnew[1] = ':'.join(xnew[1].split(':')[0:2])
    return(xnew)

# Function 'splitarts' takes the first artist id from a series of artist id's separated by a semi-colon. 
def splitarts(x):
    xnew = str(x).split(';')
    xnew = xnew[0]
    return(xnew)



