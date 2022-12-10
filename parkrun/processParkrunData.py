import sys
sys.path.append(r'C:\Users\james\Documents\python') #location of sendEmail.py

import json
import pandas as pd 
from pandas import json_normalize
from geopy.distance import distance
import sqlite3,urllib.request,socket,time
from sendEmail import sendEmail

def isconnected():

    try:
        socket.create_connection(("1.1.1.1",53))
        return True

    except:
        print ('no internet connection')
        return False


while isconnected() == False:
    time.sleep(60) #loop every 60 seconds until there is an internet connection

jsonPath = 'C://Users//james//Dropbox//temp//events.json' #WE WILL DUMP THE JSON FILE HERE


urllib.request.urlretrieve('https://images.parkrun.com/events.json',jsonPath) #download the file


with open(jsonPath) as f:
    d = json.load(f)

q = json_normalize(d['events'],record_path = 'features')

q=q[(q["properties.countrycode"]==97) & (q["properties.seriesid"]==1) ][["id","properties.eventname"]] 
#filtering dataframe rows and specify cols
#countrycode 97 = uk, seriesid =1 - non junior parkrun

q=q.rename(columns={'properties.eventname':'eventName'}) #rename column


conn = sqlite3.connect('C:\\Users\\james\\Dropbox\\temp\\parkrun.db')#create db
c=conn.cursor()#create connection
q.to_sql('stg_runs',conn, if_exists='replace')#upload data

createTable ='\
CREATE TABLE IF NOT EXISTS runs (\
    id           INTEGER,\
    eventName    TEXT,\
    timestamp    DATETIME DEFAULT CURRENT_TIMESTAMP\
);'

c.execute(createTable)

createView = '\
CREATE VIEW IF NOT EXISTS newEvents \
AS \
\
select a.eventName from( \
select eventName from runs where timestamp = (select max(timestamp) from runs) \
except \
select eventName from runs where timestamp = (select max(timestamp) from runs where timestamp != (select max(timestamp) from runs))) a \
inner join (select * from runs where timestamp = (select max(timestamp) from runs)) b on a.eventname = b.eventname\
'

c.execute(createView)

insertTable = '\
INSERT INTO runs ( id,eventname)\
SELECT id,eventname FROM stg_runs\
'

c.execute(insertTable) #insert the processed data into database
conn.commit()

newEventsDF = pd.read_sql('select * from newEvents',conn)

neweventCount = newEventsDF.shape[0] #shape function returns (number of rows, number of cols)

if neweventCount >0:
    run_list = ",".join(newEventsDF["eventName"].values.tolist())
    print (",".join(newEventsDF["eventName"].values.tolist()))
    sendEmail('New parkrun',run_list)


print('parkrun scrape complete')
time.sleep(5) #delay to allow inspection for error messages