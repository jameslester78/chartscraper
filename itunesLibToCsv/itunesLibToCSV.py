import pandas as pd
import xml.etree.ElementTree as ET

lib = 'C:\\temp\\Library.xml'


tree = ET.parse(lib)
root = tree.getroot()
main_dict=root.findall('dict')
for item in list(main_dict[0]):    
    if item.tag=="dict":
        tracks_dict=item
        break
tracklist=list(tracks_dict.findall('dict'))


output = [] #a soon to be list of dictionaries

for j in range(len(tracklist)):
    new ={}
    for i in range(200): #arbitrary number that is bigger than the number of columns
        try:
            if tracklist[j][i].tag == 'key':
                new[tracklist[j][i].text] = tracklist[j][i+1].text #add to dictionary header and value
        except:
            continue #go to the next track when we run out of columns
    output.append(new) #stick the final record into the output list          


df = pd.DataFrame(output)

df[df['Name']=='x'].to_csv('c:\\temp\\pandas_headers.txt',index=False,quoting=1)
df.to_csv('c:\\temp\\pandas.txt',index=False,quoting=1,header=False)