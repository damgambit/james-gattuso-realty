from development.models import *
import csv


def parcer():
    f = open('./csv_file/towneauction.csv', 'r')
    # Auction Date,Time,Status,Address,City,State,Zip Code,County,Page / Liber,Deposit
    reader = csv.reader(f)
    for row in reader:
        c = TownAuction.objects.get_or_create(date=datetime.datetime.strptime(str(row[0]), '%m/%d/%y'),
                                              time=row[1],
                                              status=row[2],
                                              address=row[3],
                                              city=row[4],
                                              state=row[5],
                                              zipcode=row[6],
                                              country=row[7],
                                              deposit=row[9]
                                              )
    f.close()
    f = open('./csv_file/baystateauction.csv', 'r')
    reader = csv.reader(f)
    # Status,Day,Date,Time,Address,City,State,Deposit
    for row in reader:
        c = BayStateAuction.objects.get_or_create(date=datetime.datetime.strptime(str(row[2]) + ' 2017', '%B %d %Y'),
                                                  time=row[3],
                                                  status=row[0],
                                                  address=row[4],
                                                  city=row[5],
                                                  state=row[6],
                                                  deposit=row[7]
                                                  )
    f.close()

    f = open('./csv_file/pesco.csv', 'r')
    #Date,Time,Title,Address,City,State,zipcode,Terms
    reader = csv.reader(f)
    for row in reader:
    	c = Pesco.objects.get_or_create(date=row[0],
    			time=row[1],
    			status=row[2],
    			address=row[3],
    			city=row[4],
    			state=row[5],
    			zipcode=row[6],
    			terms=row[7]
    		)
    f.close()
    
    f = open('./csv_file/landmarkauction.csv', 'r')
    # Auction Date,Time,Status,Address,City,State,Zip Code
    reader = csv.reader(f)
    for row in reader:
        c = LandMarkAuction.objects.get_or_create(date=row[0],
                                                  time=row[1],
                                                  status=row[2],
                                                  address=row[3],
                                                  city=row[4],
                                                  state=row[5],
                                                  zipcode=row[6],
                                                  )
    f.close()



    f = open('./csv_file/commonwealthauction.csv', 'r')
    # status,Auction_Date,Auction_time,Address,County,Deposit
    reader = csv.reader(f)
    for row in reader:
        c = CommonWealthAuction.objects.get_or_create(date=row[1],
                                                      time=row[2],
                                                      status=row[0],
                                                      address=row[3],
                                                      country=row[4],
                                                      deposit=row[5]
                                                      )
    f.close()
