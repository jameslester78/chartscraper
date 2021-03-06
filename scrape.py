import requests,os,datetime,time,logging,traceback
from bs4 import BeautifulSoup
from datetime import datetime,timedelta

from requests.exceptions import SSLError

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

def parse_chart_html(url):
    '''take an url and spit out a csv file ready for importing to a db'''
    
    try:
        page = requests.get(url) #get the html
    except:
        with open('c:\\temp\log.txt',"a") as file: #if this works turn this into a parameter
            file.write(datetime.now().strftime("%d/%b/%Y %H:%M:%S") + ' - Error - '+url + '\n')
            print (datetime.now().strftime("%d/%b/%Y %H:%M:%S") + ' - Error - '+url)
            result = ''
            traceback.print_exc()
            return result

   
     
    soup = BeautifulSoup(page.content,'html.parser') #create a BS object
    
    position = soup.find_all(class_='position')
    lastweek = soup.find_all(class_='last-week')
    title = soup.find_all(class_='title')
    artist = soup.find_all(class_='artist')
    label = soup.find_all(class_='label-cat')
    tchartruns = [datetime.strptime(i.a['data-chartid'].split('-')[1],'%Y%m%d').date() for i in soup.find_all(class_='t-chart-runs')]

        #tchartruns contains the following, all we want to do is extract 20210624 from each list entry
        #
        #<td class="t-chart-runs">
        #    <a href="" data-productid="1198818-5I85O-USWBV2100581-SINGLE" data-chartid="7501-20210624" class="chart-runs-icon icon-circle-plus"></a>
        #</td>


    result_size= (len(position)) #how many records?

    result = ''

    for i in range(result_size):
        result += f'"{position[i].text.strip()}","{lastweek[i].text.strip()}","{title[i].text.strip()}","{artist[i].text.strip()}","{label[i].text.strip()}","{tchartruns[i]}"\n'

    
    logging.debug(f"{result.strip()}")

    return result#.strip() #remove the last new line charecter

def writefile(url,output_location):
    '''apends scraped data to output file'''
    with open(output_location,"ab") as file: #b, need to open in binary mode to allow saving in utf8
        file.write(parse_chart_html(url).encode('utf8')) #handle unicode

def generateurl(date):
    '''takes a date and spits out a url to scrape'''

    date_conv = datetime.strptime(date,'%Y%m%d') #convert date to datetime format
    date_new = (date_conv + timedelta(days = 6-date_conv.weekday())).date() #we want the first sunday from the input date, sunday = weekday:6

    return "https://www.officialcharts.com/charts/albums-chart/" + date_new.strftime("%Y%m%d")+'/7502/'

def geturls(start,end):
    '''outputs a list of urls to scrape, one page per sunday between start and end date'''

    start_conv = datetime.strptime(start,'%Y%m%d') -timedelta(days=7)   #minus 7 days as url date is the start date rather 
                                                                        #than end date for chart period, and convert to datetime format
    end_conv = datetime.strptime(end,'%Y%m%d') #convert end date

    output = []

    while start_conv+ timedelta(days=7) <= end_conv:
        output.append (generateurl(start_conv.strftime("%Y%m%d")))
        start_conv = start_conv + timedelta(days=7)

    return output


def process_load_file():
        '''after a lengthy scrape session, pull any failure urls (from the log) into a load file and process it here'''

        urllist = []
        
        with open('c:\\temp\load.txt',"r") as file:
            urls = file.readlines()
            for i in urls:
                urllist.append (i.strip())

        output_path = 'c:\\temp\output.txt' #\t = tab so escape the slash

        if os.path.isfile(output_path):
                os.remove(output_path) #delete the output file if it exists

        for i in urllist:
            writefile(i,output_path)
            time.sleep(3) #pause




if __name__ == '__main__':

    logging.disable(logging.CRITICAL)
    
    urllist = geturls('19600101','20210601')
    logging.debug(f"{urllist=}")

    output_path = 'c:\\temp\output.txt' #\t = tab so escape the slash

    if os.path.isfile(output_path):
        os.remove(output_path) #delete the output file if it exists

    for i in urllist:
        writefile(i,output_path)
        time.sleep(3) #pause