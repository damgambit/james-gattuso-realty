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

def get_iframe(self):

    headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',

                'Accept-Encoding':'gzip, deflate',

                'Accept-Language':'en-US,en;q=0.8',

                'Connection':'keep-alive',

                'Host':'www.tacheauctionsandsales.com',

                'Referer':'http://www.tacheauctionsandsales.com/current-auctions.html',

                'Upgrade-Insecure-Requests':'1',

                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}

    r = requests.get(self)

    return html.fromstring(r.text).xpath('//iframe/@src')



def parser(self,writer):

    headers = {'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',

                'accept-encoding':'gzip, deflate, br',

                'accept-language':'en-US,en;q=0.8',

                'referer':'http://www.tacheauctionsandsales.com/current-auctions.html',

                'upgrade-insecure-requests':'1',

                'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}

    r = requests.get(self)

    source = html.fromstring(r.text)

    sections = source.xpath("//tr[@style='height:24px;']")

    for section in sections:

        new_source = html.fromstring(html.tostring(section))

        new_tds = new_source.xpath('//td//text()')

        writer.writerow(new_tds[0:8])
        print(new_tds[0:8])

        t = TacheAuctionAndSales.objects.get_or_create(
                    date=datetime.datetime.strptime(new_tds[0], '%m/%d/%y'),
                    time=new_tds[1],
                    address=new_tds[2],
                    city=new_tds[3],
                    state=new_tds[4],
                    zipcode=new_tds[5],
                    status=new_tds[6],
                    deposit=new_tds[7],
                )


def main():       

    with open('./csv_file/tacheauctionsandsales.csv','w')as export:

        writer = csv.writer(export)

        writer.writerow(['Date','Time','Address','City','State','Zipcode','Status','Deposit'])

        iframe_link = get_iframe('http://www.tacheauctionsandsales.com/current-auctions.html')

        parser(iframe_link[0],writer)



if __name__ == "__main__":

    main()

