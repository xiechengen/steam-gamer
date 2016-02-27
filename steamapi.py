from steamapiwrapper.SteamGames import *
from steamapiwrapper.Users import SteamUser
import urllib2
import json
import csv
games = Games()

'''
url = games._get_urls(['65710'],'US')
#openurl = games._open_url(url)

print url

for i in url:
    a = urllib2.urlopen(i)
    page = json.loads(a.read())

#print page['65710']

target = Game(page['65710'],'65710')
print target.price
#print openurl

#print url
#b = games._get_games_from(url)

output = games.get_info_for(['65710'],'US')
for i in output:
    print i.price

data = {'appids': appids, 'cc': cc, 'l': 'english', 'v': '1'}
print "http://store.steampowered.com/api/appdetails/?{}".format(urllib.urlencode(data))

appids_to_names, names_to_appids = games.get_ids_and_names()

urls = []
for i in appids_to_names.keys():
    urls += games._get_urls([i], "CN")

print url
a = games._get_games_from(url)

for i in a:
    print i.name

for j in urls[:100]:
    a = games._get_games_from(j)
    for i in a:
        print i.name, i.price
'''

getall = games.get_all("CN")
counter = 0
with open("dino_output.csv", 'wb') as f:
        file_writer = csv.writer(f, delimiter=',')
        for i in getall:
            try:
                print "#%d" % counter, " ",i.name.encode('utf-8'), i.price
                file_writer.writerow([i.name , i.price])
            except:
                continue
            counter += 1

'''
def test():
    for i in range(3):
        if i == 5:
            yield i

b = test()
print b 

for i in b:
    print i


b =  games._get_urls([8930], "CN")
game = games._get_games_from(b[0])

for i in game:
    print i.price
'''

'''
for url in urls[:2]:
    print url
    game = games._get_games_from(url)
    #print type(game)

    for i in game:
        print i.price
     for game in games._get_games_from(url):
        print game.price()
'''
