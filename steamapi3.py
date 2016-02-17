from steamapiwrapper3.SteamGames import *
from steamapiwrapper3.Users import SteamUser
import urllib.request, urllib.error, urllib.parse
import json
import csv

file = open(r'C:\Users\spencer\Desktop\games.csv',
                'w', newline='',
                encoding='utf8')

writer = csv.writer(file)
games = Games()
getall = games.get_all("CN")
counter = 1
for item in getall:
        print("#%d" % counter, " ", item.name, item.price)
        writer.writerow([item.name, item.price])
        counter += 1
        

