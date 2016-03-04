from steamapiwrapper.SteamGames import *
from steamapiwrapper.Users import SteamUser
import urllib2
import json
import csv
games = Games()



getall = games.get_all("CN")
counter = 0
with open("dino_output.csv", 'wb') as f:
        file_writer = csv.writer(f, delimiter=',')
        for i in getall:
            try:
                print "#%d" % counter, i.appid,i.name.encode('utf-8'), i.price, i.store_url 
                file_writer.writerow([i.appid, i.name , i.price, i.store_url])
            except:
                continue
            counter += 1




#user = SteamUser(userid, 'FC65FE32E5732FC54BC70256CDA122BB')