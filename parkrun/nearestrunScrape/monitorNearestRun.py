from requests import get
from parsel import Selector
import ast
import datetime
import time


def getList(inputUrl):

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    url = inputUrl

    html = get(url,headers=headers).content

    sel = Selector(str(html))

    #2 methods to produce the same output via xpath and css selector
    #get html where div class = homerightinnerinner and return the text
    #for the link

    l1 = sel.xpath('//*/div[@class="homerightinnerinner"]/a/text()')
    #print (l1.extract())

    #l2 = sel.css('div.homerightinnerinner>a::text')
    #print (l2.extract())

    l3 = sel.xpath('//*/div[@class="homerightinnerinner"]/a/@href')
    #print (l3.extract())

    #print(*zip(l1.extract(),l3.extract()))
    returnValue = [ (l1.extract()[i],l3.extract()[i]) for i in range(len(l1))]
    return returnValue

def creatDicts():
    try:
        with open('c:\\temp\\runList.txt') as file: #a containing each parkrun name on each line
            lines = file.readlines() #read the file into a variable    
    except:
        with open('c:\\temp\\runList.txt','w') as f: ##initialise file
            writeSting = '{"Bushy Park":{"url":"https://www.parkrun.org.uk/bushy/"},"Pollok":{"url":"https://www.parkrun.org.uk/pollok/"}}'
            f.write(writeSting)   

    with open('c:\\temp\\runList.txt') as file: #a containing each parkrun name on each line
        lines = file.readlines() #read the file into a variable

    #print(lines)

    dict = ast.literal_eval(lines[0])
    dictCopy = dict.copy()

    for x,y in dict.items():
        visited = y.get("visited")
        delta = datetime.timedelta(0)
        
        #print (visited)
        if visited is not None:
            delta = datetime.datetime.now() - datetime.datetime.strptime(visited,"%Y-%m-%d %H:%M:%S.%f")   #2023-07-10 12:24:39.682658
            #print (delta.total_seconds())

        if delta.total_seconds() > 21600 or visited is None:
            runList = getList(y["url"])
            y["visited"] = str(datetime.datetime.now())

            for x in runList:
                #print (x[0],x[1],datetime.datetime.now())
                if x[0] not in dict:
                    dictVal = '{"url" : "' + x[1].replace("\\\'","") + '"}'
                    dictVal = (ast.literal_eval(dictVal))
                    dictCopy[x[0]] = dictVal
    
            time.sleep(0.25)        

    #print (dictCopy)
    dictLen = len(dict)
    dictCopyLen = len(dictCopy)

    #print (dictLen, dictCopyLen)


    x = set({})
    y = set({})

    if dictLen != dictCopyLen:
        x = {i for i in dict}
        y = {i for i in dictCopy}
        #print (sorted((y.difference(x)))) #new records
    

    with open('c:\\temp\\runList.txt','w') as file:
        file.write (str(dictCopy))

    #print (y)
    return sorted((y.difference(x))) #new records

if __name__ == '__main__':

    c = [1] #non empty list, initial value
    while len(c) !=0:
        #print (len(c))
        print (c)
        c= creatDicts()


#alert to new values
#apostrophy in names