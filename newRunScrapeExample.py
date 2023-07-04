from requests import get
from parsel import Selector

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
url = 'https://www.parkrun.org.uk/wolverhampton'

html = get(url,headers=headers).content

sel = Selector(str(html))


#2 methods to produce the same output via xpath and css selector
#get html where div class = homerightinnerinner and return the text
#for the link

l1 = sel.xpath('//*/div[@class="homerightinnerinner"]/a/text()')
print (l1.extract())

l2 = sel.css('div.homerightinnerinner>a::text')
print (l2.extract())
