'''
todo:

sqllite path parameter
move the email function, wait for internet function to a seperate utility file

DONE:
detect new courses
alert new courses
multiple homes
exclude list
automate downloading json
automate daily execution
back up json - dropbox
wait for internet connection
'''

import json
import pandas as pd 
from pandas import json_normalize
from geopy.distance import distance
import sqlite3,urllib.request,socket,time

#ONE OF THE FOLLOWING LOCATIONS SHOULD BE SELECTED AS HOME IN ORDER TO FIND THE CLOSEST AVAILABLE PARKRUN
#IF YOU ADD A NEW HOME ALSO ADD THE COORDINATES

#runfrom = 'codsall'
runfrom = 'borehamwood'

if runfrom == 'codsall':
    home = (52.6237742,-2.1985467)
elif runfrom == 'borehamwood':
    home = (51.659428688873305, -0.27137887684018747)


#MANUALLY ADD COMPLETED RUNS HERE
completed = ['aldenham','canonspark','sunnyhill','wolverhamptonNew','wolverhampton','eastpark','dudley','walsall','telford','chasewater','cannockchase','sandwellvalley','isabeltrail'\
            ,'severnvalleycountry','perryhall','woodgatevalleycountrypark','suttonpark','edgbastonreservoir','beacon','cannonhill','oaklands','babbsmill','kingsburywater','brueton','shrewsbury'
            ,'oakhill','allypally','cassiobury','southoxhey','stalbans','hampsteadheath']

def send_email(run_list):

    '''send the email, you'll need to create a pickle file with gmail account and password in it, code to create file down the bottom'''

    import smtplib, ssl
    import pickle


    with open('C:\\Users\\james\\Documents\\python\\vars.pkl','rb') as f: 
        password, email = pickle.load(f)

    print(email)     

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = email
    receiver_email = email
    password = password
    message = f"""Subject: New Parkrun

    There is a new Parkrun: {run_list}"""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

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

q=q[(q["properties.countrycode"]==97) & (q["properties.seriesid"]==1) ][["id","geometry.coordinates","properties.eventname"]] 
#filtering dataframe rows and specify cols
#countrycode 97 = uk, seriesid =1 - non junior parkrun

q[['c1','c2']] = pd.DataFrame(q["geometry.coordinates"].tolist(),index=q.index) #split out list column into seperate cols
q['dist']=q.apply(lambda row: distance((row['c2'],row['c1']),home).miles,axis=1) #create a new column
q=q.sort_values(by=['dist']) #sort dataframe
q=q.drop(['geometry.coordinates','c1','c2'],axis=1) #remove columns we dont care about
q=q.rename(columns={'dist':'distFromHome','properties.eventname':'eventName'}) #rename columns


conn = sqlite3.connect('C:\\Users\\james\\Dropbox\\temp\\parkrun.db')#create db
c=conn.cursor()#create connection
q.to_sql('stg_runs',conn, if_exists='replace')#upload data

#print(pd.read_sql('select * from stg_runs',conn))#view data

createTable ='\
CREATE TABLE IF NOT EXISTS runs (\
    id           INTEGER,\
    eventName    TEXT,\
    distFromHome REAL,\
    timestamp    DATETIME DEFAULT CURRENT_TIMESTAMP\
);'

c.execute(createTable)

#this view will tell me which is the closest unrun course to my home
createView = '\
CREATE VIEW IF NOT EXISTS newEvents \
AS \
\
select a.eventName,b.distFromHome from( \
select eventName from runs where timestamp = (select max(timestamp) from runs) \
except \
select eventName from runs where timestamp = (select max(timestamp) from runs where timestamp != (select max(timestamp) from runs))) a \
inner join (select * from runs where timestamp = (select max(timestamp) from runs)) b on a.eventname = b.eventname\
'

#print(createView)
c.execute(createView)

insertTable = '\
INSERT INTO runs ( id,eventname,distfromHome)\
SELECT id,eventname,distfromHome FROM stg_runs\
'

c.execute(insertTable) #insert the processed data into database
conn.commit()

c.execute('select * from newEvents') #I think this can be removed

newEventsDF = pd.read_sql('select * from newEvents',conn)

neweventCount = newEventsDF.shape[0] #shape function returns (number of rows, number of cols)

if neweventCount >0:
    run_list = ",".join(newEventsDF["eventName"].values.tolist())
    print (",".join(newEventsDF["eventName"].values.tolist()))
    send_email(run_list)



closestEvents=q[~q["eventName"].isin(completed)] # ~ means NOT
print(closestEvents.head(5)) #dump the 5 nearest to the screen


'''
create your password file

password = 'your email password'
email = 'your email address'

with open('vars.pkl','wb') as f:
    pickle.dump([password,email],f)
'''            