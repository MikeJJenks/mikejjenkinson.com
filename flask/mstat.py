import pandas as pd
import datetime

# plays = pd.read_csv('../data/plays.csv')

def getags(pin, nt):
    # Get top aggregated artists and tracks for given time period (in days)

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





