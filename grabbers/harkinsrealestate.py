import requests, csv, time, re
from lxml import html

def get_links(self):
    headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'en-US,en;q=0.8,pt;q=0.6',
                'Connection':'keep-alive',
                'Host':'www.harkinsrealestate.com',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
    r = requests.get(self.strip(),headers=headers)
    return html.fromstring(r.text).xpath('//h3[@class="title"]//a//@href')

def parser(link):
    headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'en-US,en;q=0.8,pt;q=0.6',
                'Connection':'keep-alive',
                'Host':'www.harkinsrealestate.com',
                'Referer':'http://www.harkinsrealestate.com/auction-schedule/',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
    r = requests.get(link.strip(),headers=headers)
    x = lambda x: html.fromstring(r.text).xpath(x)
    try:
        Date_time = x('//div[@class="sidebox info"]//li[2]//text()')[0]
        if Date_time:
            Date_time = Date_time.split("at")
            try:
                Date = " ".join(Date_time[0].split(" "))
            except:
                Date = None
            try:
                Time = Date_time[1].strip()
            except:
                Time = None
    except:
        Date, Time = None
    try:
        Status = x('//div[@class="sidebox info"]//li[1]//text()')[0].replace('Status:','').strip()
    except:
        Status = None
    try:
        Deposit = x('//div[@class="sidebox info"]//li[4]//text()')[0].replace('Required Deposit:','').strip()
    except:
        Deposit = None
    Raw_Address = x('//p[@class="address"]//text()')
    if Raw_Address != []:
        New_address = Raw_Address[0].split(",")
        try:
            Address = "".join(New_address[:-2])
        except:
            Address = None
        try:
            City = New_address[-2].strip()
        except:
            City = None
        try:
            State = New_address[-1].strip()
        except:
            State = None
    Zipcode = None
    #print "%r\n%r\n%r\n%r\n%r\n%r\n%r\n%r\n%r\n" % (link,Date,Time,Status,Deposit,Address,City,State,Zipcode)
    writer.writerow([Date,Time,Status,Address,City,State,Zipcode,Deposit])

with open('harkinsrealestate.csv','wb')as export:
    writer = csv.writer(export)
    writer.writerow(['Date','Time','Status','Address','City','State','Zipcode','Deposit'])
    links = get_links('http://www.harkinsrealestate.com/auction-schedule/')
    for link in links:
        parser(link)


