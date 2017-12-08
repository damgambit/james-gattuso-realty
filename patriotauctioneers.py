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

                'Host':'patriotauctioneers.com',

                'Upgrade-Insecure-Requests':'1',

                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

    r = requests.get(link,headers=headers)

    source = html.fromstring(r.text)

    sections = source.xpath('//a[@class="auction-list"]')

    for section in sections:

        x = lambda x: html.fromstring(html.tostring(section)).xpath(x)

        try:

            listing_link = x('//a//@href')[0]

        except:

            listing_link = None

        try:

            Status = x('//div[@class="banner yellow"]//text()')[0].encode('utf-8')

        except:

            Status = None

        combined_list.append(('https://patriotauctioneers.com'+listing_link,Status))

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

                'Host':'patriotauctioneers.com',

                'Upgrade-Insecure-Requests':'1',

                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

    r = requests.get(each[0].strip(),headers=headers)

    try:

        Date_time = get_date(html.fromstring(r.text).xpath('//div[@class="auction-box"]')[0]).strip().replace('–','-')

        if Date_time != []:

            try:

                Date1 = Date_time.split(" ");Date = Date1[-6]+' '+Date1[-5]+' '+Date1[-4]

            except:

                Date = None

            try:

                Time = Date1[-2]+" "+Date1[-1]

            except:

                Time = None

    except:

        Date = None

        Time = None

    # try:

    raw_address = ", ".join(html.fromstring(re.findall('<h3 class="icon-location">Auction Location</h3>(.+?)</strong>',r.text,re.DOTALL)[0])\

                        .xpath('//strong//text()')).strip().encode('utf-8')

    if raw_address:

        try:

            Address = ' '.join(str(raw_address.split(b",")[:-2])).strip()

        except:

            Address = None

        try:

            City = raw_address.split(b",")[-2].strip()

        except:

            City = None

        try:

            state = raw_address.split(b",")[-1].split(b" ")[1]

        except:

            state = None

        try:

            Zipcode = raw_address.split(b",")[-1].split(b" ")[-1]

            if len(Zipcode) != 5:

                Zipcode = None

        except:

            Zipcode = None

    # except:

        pass

    try:

        Deposit = ", ".join(html.fromstring(r.text).xpath('//p[@class="auction-terms"]//text()')).strip().encode('utf-8')

    except:

        Deposit = None

    writer.writerow([Date,Time,each[1],Address,City,state,Zipcode,Deposit[:7]])

    status = each[1]

    if each[1] == None:
        status = 'On_Time'

    Date = encoding(Date)

    if b'- ' in Date:
        Date = Date.strip().replace(b'- ',b'')
        Date = Date.strip().replace(b',',b', ')
    if b'2017' not in Date and b'2018' not in Date:
        Date = Date + b'2018'

    if state == None:
        state = '##'
    if Zipcode == None:
        Zipcode = 0



    try:
        p = PatriotAuctioneer.objects.get_or_create(date=datetime.datetime.strptime(str(Date), "b'%B %d, %Y'"),
                                                    time=Time[:-1],
                                                    status=status,
                                                    address=Address[4:-3].replace('  ', '-').replace(' ','').replace('-',' '),
                                                    city=City,
                                                    state=state,
                                                    zipcode=Zipcode,
                                                    )
    except:
        print('Error saving {} to db'.format(each))
    

links = get_listings('https://patriotauctioneers.com/search/?date_1=&date_2=&city=&state=&county=&search=true')



with open("./csv_file/patriotauctioneers.csv","w")as export:

    writer = csv.writer(export)

    writer.writerow(['Date','Time','Status','Address','City','State','Zipcode','Terms of sale'])

    for each in links:

        print('[*] Parsing', each)
        parser(each)

