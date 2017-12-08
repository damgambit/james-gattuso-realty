import requests, csv, sys, os

from lxml import html

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
application = get_wsgi_application()


from development.models import *
import csv






headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',

            'Accept-Encoding':'gzip, deflate',

            'Accept-Language':'en-US,en;q=0.8',

            'Connection':'keep-alive',

            'Host':'www.baystateauction.com',

            'Referer':'http://www.baystateauction.com/upcoming-auctions/',

            'Upgrade-Insecure-Requests':'1',

            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}



def cleaner(self):

    return [each.strip() for each in [each1.strip() for each1 in self] if each != '']



def parser(link):

    r = requests.get(link,headers=headers)

    if 'There are no upcoming auctions at this time.' in r.text:

        sys.exit()

    source = html.fromstring(r.text)

    sections = source.xpath('//tr')

    for section in sections[1:]:

        new_source = html.fromstring(html.tostring(section))

        Date_time = cleaner(new_source.xpath('//td[1]//text()'))[0]

        try:

            Status = cleaner(new_source.xpath('//td[1]//text()'))[1]

        except:

            Status = None

        Date = Date_time.split(" at ")[0].split(",")[1]; Time = Date_time.split(" at ")[1]; Day = Date_time.split(" at ")[0].split(",")[0]

        Address = cleaner(new_source.xpath('//td[2]//text()'))[:-1]

        City = cleaner(new_source.xpath('//td[2]//text()'))[-1]

        State = cleaner(new_source.xpath('//td[3]//text()'))[0]

        try:

            Deposit = new_source.xpath('//td[@style=""]//text()')[0]

        except:

            Deposit = None

        #writer.writerow([Status,Day,Date,Time,", ".join(Address),City,State,Deposit])

        row = [Status,Day,Date,Time,", ".join(Address),City,State,Deposit]
        print(row)
        if 'December' in row[2]:
            date_to_save = datetime.datetime.strptime(str(row[2][1:]) + ' 2017', '%B %d %Y')
        else: 
            date_to_save = datetime.datetime.strptime(str(row[2][1:]) + ' 2018', '%B %d %Y')
        if row[0] == None:
            row[0] = 'Continued'
        c = BayStateAuction.objects.get_or_create(date=date_to_save,
                                                  time=row[3],
                                                  status=row[0],
                                                  address=row[4],
                                                  city=row[5],
                                                  state=row[6],
                                                  deposit=row[7]
                                                  )



with open("./csv_file/baystateauction.csv","w")as export:

    writer = csv.writer(export)

    # writer.writerow(['Status','Day','Date','Time','Address','City','State','Deposit'])

    print("[*] Parsing")

    for i in range(1,100,1):
        parser('http://www.baystateauction.com/upcoming-auctions/'+str(i))

    

