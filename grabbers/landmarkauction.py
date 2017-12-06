import requests, csv, re, sys
from lxml import html

def get_listings(self):
    headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'en-US,en;q=0.8,pt;q=0.6',
                'Connection':'keep-alive',
                'Host':'www.landmarkauction.biz',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
    r = requests.get(self,headers=headers)
    return [self+each.strip() for each in html.fromstring(r.text).xpath('//a[@class="eventlist-column-thumbnail content-fill"]//@href')], headers

def encoding(self):
    try:
        self = self.encode('utf-8').strip().replace('\xc2','')
    except:
        self = self.strip()
    return self

def parser(self,headers,writer):
    r = requests.get(self,headers=headers)
    x = lambda x:html.fromstring(r.text).xpath(x)
    try:
        Status = x('//meta[@property="og:description"]//@content')[0].split('\r\n')[0]
    except:
        Status = None
    raw_address = x('//h1[@class="eventitem-title"]//text()')
    if raw_address != []:
        raw_address = raw_address[0].split(",")
        try:
            Address = ", ".join(raw_address[:-2])
        except:
            Address = None
        try:
            City = raw_address[-2]
        except:
            City = None
        try:
            State = " ".join(raw_address[-1].split(" ")[:-1]).strip()
        except:
            State = None
        try:
            Zipcode = raw_address[-1].split(" ")[-1]
        except:
            Zipcode = None
    try:
        Date = x('//time[@class="event-date"]/@datetime')[0]
    except:
        Date = None
    try:
        Time = " ".join(" - ".join(x('//span[@class="event-time-12hr"]//time//text()')).split())
    except:
        Time = None
    #print "%r\n%r\n%r\n%r\n%r\n%r\n%r\n%r\n" %(self,encoding(Status), encoding(Address),encoding(City), encoding(State), encoding(Zipcode), Date, Time)
    writer.writerow([Date,Time,encoding(Status),encoding(Address),encoding(City),encoding(State),encoding(Zipcode)])
    
with open('landmarkauction.csv','wb')as export:
    writer = csv.writer(export)
    writer.writerow(['Auction Date','Time','Status','Address','City','State','Zip Code'])
    Profile_links, headers = get_listings('http://www.landmarkauction.biz')
    for each in Profile_links:
        parser(each,headers,writer)
