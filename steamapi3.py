from steamapiwrapper3.SteamGames import *
from steamapiwrapper3.Users import SteamUser
import urllib.request, urllib.error, urllib.parse
import json
import csv
import time

start = time.clock()

file = open('api3_output_20160219.csv',
                'w', newline='',
                encoding='utf8')

writer = csv.writer(file)
games = Games()
getall = games.get_all("CN")
counter = 1
for item in getall:
        try:
            print("#%d" % counter, " ", item.name, item.price)
            writer.writerow([item.name, item.price])
        except UnicodeEncodeError as e:
            print(e)
            continue            
        counter += 1

end = time.clock()

timeConsumed = end - start

m , s = divmod(timeConsumed,60)
h , m = divmod(m, 60)

print("it takes ", h ,"hours ", m, "minutes and ", s, "seconds.")