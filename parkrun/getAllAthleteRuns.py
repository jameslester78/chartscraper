import requests, pandas as pd

with open('c:\\temp\\eventsRun.txt','w') as f: ##initialise file
    f.write('')



with open('c:\\temp\\runners.txt') as file: #a containing each parkrun name on each line
    lines = file.readlines() #read the file into a variable

lineNum =1

for line in lines[:]:
    url = (line.rstrip()) #gets rid of new line char
    print (lineNum)

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    athleteNumber = str(url.replace("https://www.parkrun.org.uk/parkrunner/","").replace("/",""))

    html = requests.get(url,headers=headers).content
    df_list = pd.read_html(html)
    


    df = df_list[1][["Event","parkruns"]] #its the first df in the list that we want
    
    
    df.insert(0,"AthleteID",athleteNumber) #new col in position 0
    df = df.dropna(axis=0,subset=["Event"]) #get rid of the event is null rows
    df["Event"] = df["Event"].str.replace(' parkrun','' ) #get rid of text that will just bloat file
    df["Event"] = df["Event"].str.replace(',',';') #dont want commas

    with open('c:\\temp\\eventsRun.txt','ab') as f: #b - bytes - unicode

        f.write(df.to_csv(index=False,header=False, lineterminator='\n').encode('utf8')) #write it to a file, data contains unicode

    lineNum +=1

