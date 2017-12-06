import requests, csv, re

locations = ['http://www.commonwealthauction.com/auctions.asp?location=1',
             'http://www.commonwealthauction.com/auctions.asp?location=2',
             'http://www.commonwealthauction.com/auctions.asp?location=3']

headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'en-US,en;q=0.8',
            'Connection':'keep-alive',
            'Host':'www.commonwealthauction.com',
            'Referer':'http://www.commonwealthauction.com/',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

def parser(location):
    r = requests.get(location.strip(),headers=headers)
    sections = re.findall('<div class="AucH(.+?)<div class="aucbody">Notes',r.text,re.DOTALL)
    for section in sections:
        status = re.findall('ead">(.+?)</div>',section,re.DOTALL)[0]
        if status.startswith('</div>'):
            status = None
        else:
            status = status.encode('utf-8').strip()
        list_to_iterate = re.findall('<div class="aucbody">(.+?)</div>',section,re.DOTALL)
        Auction_Date = list_to_iterate[0].split("  ")[0].encode('utf-8').strip()
        Auction_time = list_to_iterate[0].split("  ")[1].encode('utf-8').strip()
        Address = list_to_iterate[1].encode('utf-8').strip()
        County = list_to_iterate[2].split('&nbsp;&nbsp;Book:&nbsp;')[0].replace('County:&nbsp;','').encode('utf-8').strip()
        Deposit = list_to_iterate[3].replace("Deposit: ","").encode('utf-8').strip()
        #print "%r\n%r\n%r\n%r\n%r\n%r\n" % (status, Auction_Date, Auction_time, Address, County, Deposit)
        writer.writerow([status, Auction_Date, Auction_time, Address, County, Deposit])

with open('commonwealthauction.csv','wb')as export:
    writer = csv.writer(export)
    writer.writerow(['status', 'Auction_Date', 'Auction_time', 'Address', 'County', 'Deposit'])
    for location in locations:
        parser(location)
    
