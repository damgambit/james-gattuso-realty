import requests, csv, sys, os, re, time, codecs
from datetime import date

from lxml import html

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
application = get_wsgi_application()


from development.models import *

from requests import Session



def parser(self):

    source = html.fromstring(self)

    both = source.xpath('//tr[@style="background-color:#DCDEDE;font-size:9pt;"]')+source.xpath('//tr[@style="background-color:White;font-size:9pt;"]')

    for bot in both:

        rise = html.fromstring(html.tostring(bot))

        texts = rise.xpath('//td//text()')#; print texts

        writer.writerow(texts[0:8]+[texts[-1]])
        print(texts[0:8]+[texts[-1]])

        

def get_page_response():

    s = requests.Session()

    s.get('http://www.towneauction.com/',

          headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'})

    r = s.get('http://www.towneauction.com/Auctions_NoNav.aspx',

      headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'})

    parser(r.text)
    
    print(re.findall('<td colspan="2">(.+?)</td>',r.text,re.DOTALL))
    
    last_page = re.findall('<td colspan="2">(.+?)</td>',r.text,re.DOTALL)[0].split('&nbsp; of &nbsp;')[1].strip().replace(' ','')

    __VIEWSTATE = (html.fromstring(r.text)).xpath('//input[@id="__VIEWSTATE"]//@value')[0]

    __VIEWSTATEGENERATOR = (html.fromstring(r.text)).xpath('//input[@id="__VIEWSTATEGENERATOR"]//@value')[0]

    i = 1

    while i < int(last_page):

        payload = {'__EVENTTARGET':'GridView1',

                    '__EVENTARGUMENT':'Page$Next',

                    '__LASTFOCUS':'',

                    '__VIEWSTATE':__VIEWSTATE,

                    '__VIEWSTATEGENERATOR':__VIEWSTATEGENERATOR,

                    'tbBeginDate':'',

                    'tbEndDate':'',

                    'TextBox1':'',

                    'CheckBoxActive':'on',

                    'CheckBoxPostponed':'on',

                    'CheckBoxCanceled':'on',

                    'inpSize':'testing',

                    'inpStartDate':'',

                    'inpEndDate':''}

        r1 = s.post('http://www.towneauction.com/Auctions_NoNav.aspx',headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'},

                    data=payload)

        try:
            parser(r1.text)
        except:
            print('error')

        __VIEWSTATE = (html.fromstring(r1.text)).xpath('//input[@id="__VIEWSTATE"]//@value')[0]

        __VIEWSTATEGENERATOR = (html.fromstring(r1.text)).xpath('//input[@id="__VIEWSTATEGENERATOR"]//@value')[0]

        i+=1



with codecs.open('./csv_file/towneauction.csv','w',encoding='utf-8')as export:

    writer = csv.writer(export)

    writer.writerow(['Auction Date','Time','Status','Address','City','State','Zip Code','County','Deposit'])

    get_page_response()

