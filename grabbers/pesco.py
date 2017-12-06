import requests, csv, re
from lxml import html

def get_response():
    headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'en-US,en;q=0.8,pt;q=0.6',
                'Connection':'keep-alive',
                'Host':'www.pesco.com',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}

    r = requests.get('http://www.pesco.com/realEstateAuctions.jsp',headers=headers)
    return r.text

def new_parser(x,each):
    try:
        to_work = x('//span[@class="offline"]//text()')
        if to_work != []:
            Date = to_work[0].split(",")[0].strip()+', '+to_work[0].split(",")[1].strip()
            Time = to_work[0].split(",")[-1].strip()
        else:
            Date = x('//span[@class="cancelled"]/text()')[0]
            Time = x('//span[@class="cancelled"]/text()')[0]
    except:
        pass
    try:
        Title = x('//div[@class="title"]//span/text()')[0]
    except:
        Title = None
    try:
        raw_Address = x('//div[@class="address"]//span/text()')[0].split(',')
    except:
        raw_Address = []
    if raw_Address != []:    
        try:
            Address = ", ".join(raw_Address[:-2])
        except:
            Address = None
        try:
            City = raw_Address[-2].strip()
        except:
            City = None
        try:
            State = raw_Address[-1].strip()
        except:
            State = None
    else:
        Address, City, State = None
    zipcode = None
    try:
        Terms = re.sub('<[^>]+>', '',re.findall('Terms of Sale:(.+?)</p>',html.tostring(each),re.DOTALL)[0].strip().replace('&amp;','&'))
    except:
        Terms = None
    return Date,Time,Title,Address, City, State, zipcode, Terms

def parser(response,writer):
    source = html.fromstring(response)
    for each in source.xpath('//div[@class="auction"]'):
        x = lambda x:html.fromstring(html.tostring(each)).xpath(x)
        Date,Time,Title,Address, City, State, zipcode, Terms = new_parser(x,each)
        writer.writerow([Date,Time,Title,Address, City, State, zipcode, Terms])
        
with open("pesco.csv","wb")as export:
    writer = csv.writer(export)
    writer.writerow(['Date','Time','Title','Address', 'City', 'State', 'zipcode', 'Terms'])
    response = get_response()
    parser(response,writer)
