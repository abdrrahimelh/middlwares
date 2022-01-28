from pymongo import MongoClient, errors
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime
import time
from datetime import datetime
import time
from pytz import timezone
tz = timezone('EST')
start_time = time.time()

# global variables for MongoDB host (default port is 27017)
DOMAIN = '15.236.141.54'
PORT = 27017
try:
 # try to instantiate a client instance
    client = MongoClient(
    host = [ str(DOMAIN) + ":" + str(PORT) ],
    serverSelectionTimeoutMS = 3000, # 3 second timeout
    username = "root",
    password = "1234",
    )

    # print the version of MongoDB server if connection successful
    print ("server version:", client.server_info()["version"])
    mydb = client.stocks
    mydb = client['stocktsla']
    mycol = mydb["TSLA"]
    print(mydb.list_collection_names())
    # get the database_names from the MongoClient()
    database_names = client.list_database_names()

except errors.ServerSelectionTimeoutError as err:
 # set the client and DB name list to 'None' and `[]` if exception
    client = None
    database_names = []
    # catch pymongo.errors.ServerSelectionTimeoutError
    print ("pymongo ERROR:", err)
        
print ("\ndatabases:", database_names)
while (True):
    now=datetime.now(tz) 
    #tester si on est dans le market est ouvert (between 9:30 and 16:00 "est")
    if (now.hour <=9) :
        if (now.minute <30):
            print("skipped")
            time.sleep(10)
            continue
    if (now.hour >=16):
        time.sleep(10)
        continue
    #si le market est fermé alors on execute pas le reste de la boucle
    start_time = time.time()
    #tester si la seconde est pair l'autre machine va tester si elle est impair
    if (int(time.time())%2 ==1):
        time.sleep(((100*int(time.time()))%100)/100)
    if (int(time.time())%2 ==0):
        try :
            data = yf.download(tickers='TSLA', period='5m', interval='1m')
            print(data.iloc[-1])
            print("--- %s seconds ---" % (time.time() - start_time))
        except: 
            print("error")
        mydata=data
        mydata.reset_index(inplace=True)
        data_dict = mydata.to_dict("records")
        print(data_dict)
        now = datetime.now()
        for s in data_dict :
            del s["Datetime"]
        mycol.insert_one({"day":3,"hour":now.hour-5,"minute":now.minute,"second":now.second,"data":data_dict[1]})
    print("--- %s seconds ---" % (time.time() - start_time))
    time.sleep(abs(1-float((time.time() - start_time))))   