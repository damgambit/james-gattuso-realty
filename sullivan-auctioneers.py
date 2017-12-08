import requests, csv, sys, os, re, time
from datetime import date

from lxml import html

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
application = get_wsgi_application()


from development.models import *

def encoding(self):

    try:

        self = self.encode('utf-8').strip().replace(b'\\xc2',b'')
        self = self.strip().replace(b'\\xa0',b'')
        #self = self.strip().replace(b'- ',b'')

    except:

        self = self.strip()

    return self



def get_listings(link):

    combined_list = []

    headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',

                'Accept-Encoding':'gzip, deflate, br',

                'Accept-Language':'en-US,en;q=0.8,pt;q=0.6',

                'Connection':'keep-alive',

                'Host':'sullivan-auctioneers.com',

                'Upgrade-Insecure-Requests':'1',

                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

    r = requests.get(link,headers=headers)

    source = html.fromstring(r.text)

    sections = source.xpath('//div[@class="auction-list"]')

    for section in sections:

        new_source = html.fromstring(html.tostring(section))

        try:

            listing_link = new_source.xpath('//h1//@href')[0]

        except:

            listing_link = None

        try:

            Status = new_source.xpath('//span//text()')[0].encode('utf-8').replace('\xc2\xa0',' ').strip()

        except:

            Status = 'On_Time'

        combined_list.append(('https://sullivan-auctioneers.com'+listing_link,Status))

    return combined_list



def return_days():

    return ['wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'monday', 'tuesday']



def get_date(source):

    for datey in html.fromstring(html.tostring(source)).xpath('//p//text()'):

        datey = str(datey.encode('utf-8')).lower()

        if (str(date.today().year) in datey or str(date.today().year+1) in datey) and any(ext in datey for ext in return_days()):

            Date = datey

            break

        else:

            pass

    return Date





def parser(each):

    #print each[0]

    headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',

                'Accept-Encoding':'gzip, deflate, br',

                'Accept-Language':'en-US,en;q=0.8,pt;q=0.6',

                'Connection':'keep-alive',

                'Host':'sullivan-auctioneers.com',

                'Upgrade-Insecure-Requests':'1',

                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

    r = requests.get(each[0].strip(),headers=headers)

    try:

        Date = get_date(html.fromstring(r.text).xpath('//div[@class="auction-box"]')[0]).strip().replace('–','-')

    except:

        Date = None

    try:

        Address = ", ".join(html.fromstring(re.findall('<h3 class="icon-location">Property Address</h3>(.+?)</div>',r.text,re.DOTALL)[0])\

                            .xpath('//strong//text()')).strip().encode('utf-8')

    except:

        Address = []

    if Address == []:

        try:

            Address = ", ".join(html.fromstring(re.findall('<h3 class="icon-location">Auction Location</h3>(.+?)</div>',r.text,re.DOTALL)[0])\

                            .xpath('//strong//text()')).strip().encode('utf-8')

        except:

            Address = None

    try:

        Deposit = ", ".join(html.fromstring(r.text).xpath('//p[@class="auction-terms"]//text()')).strip().encode('utf-8')

    except:

        Deposit = None

    writer.writerow([each[0],each[1],Date,Address,Deposit])


    Time = ' '.join(Date.split(' ')[6:])[:-1]
    Date = ' '.join(Date.split(' ')[2:5])

    Zipcode = Address.split(b' ')[-1]
    State = Address.split(b' ')[-2]
    City = Address.split(b' ')[-3]

    try:
        s = SullivanAuctioneers.objects.get_or_create(
                                                date=datetime.datetime.strptime(str(encoding(Date)), "b'%B %d, %Y'"),
                                                time=Time,
                                                address=Address,
                                                zipcode=Zipcode,
                                                state=State,
                                                city=City,
                                                status=each[1]
                                                )
    except:
        print('Error')


    



links = get_listings('https://sullivan-auctioneers.com/search/?date_1=&date_2=&city=&state=&county=&search=true')

with open("./csv_file/sullivan-auctioneers.csv","w")as export:

    writer = csv.writer(export)

    writer.writerow(['Url','Status','Date','Address','Terms of sale'])

    for each in links:
        print('[*] Parsing', each)
        parser(each)
        
        

