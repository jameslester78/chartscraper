'''
todo:
multiple homes
exclude list
detect/alert new courses
automate downloading json
automate daily execution
'''


import json
import pandas as pd 
from pandas import json_normalize
from geopy.distance import distance


home = (52.6237742,-2.1985467)

with open('./parkrun/events.json') as f:
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

print(q.head(20))