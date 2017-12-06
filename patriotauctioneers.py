# -*- coding: cp1252 -*-
import requests, csv, re, sys
from lxml import html
from datetime import date

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
    try:
        raw_address = ", ".join(html.fromstring(re.findall('<h3 class="icon-location">Auction Location</h3>(.+?)</strong>',r.text,re.DOTALL)[0])\
                            .xpath('//strong//text()')).strip().encode('utf-8')
        if raw_address:
            try:
                Address = " ".join(raw_address.split(",")[:-2]).strip()
            except:
                Address = None
            try:
                City = raw_address.split(",")[-2].strip()
            except:
                City = None
            try:
                state = raw_address.split(",")[-1].split(" ")[1].strip()
            except:
                state = None
            try:
                Zipcode = raw_address.split(",")[-1].split(" ")[-1]
                if len(Zipcode) != 5:
                    Zipcode = None
            except:
                Zipcode = None
    except:
        pass
    try:
        Deposit = ", ".join(html.fromstring(r.text).xpath('//p[@class="auction-terms"]//text()')).strip().encode('utf-8')
    except:
        Deposit = None
    writer.writerow([Date,Time,each[1],Address,City,state,Zipcode,Deposit])
    
links = get_listings('https://patriotauctioneers.com/search/?date_1=&date_2=&city=&state=&county=&search=true')

with open("patriotauctioneers.csv","wb")as export:
    writer = csv.writer(export)
    writer.writerow(['Date','Time','Status','Address','City','State','Zipcode','Terms of sale'])
    for each in links:
        parser(each)
