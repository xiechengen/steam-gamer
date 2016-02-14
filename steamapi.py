from steamapiwrapper.SteamGames import *
from steamapiwrapper.Users import SteamUser
import urllib2
import json

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
k = appids_to_names.keys()
print k[100]
urls = games._get_urls([k[100]], "CN")
print urls


for url in urls[:2]:
    print url
    game = games._get_games_from(url)
    #print type(game)

    for i in game:
        print i.price
     for game in games._get_games_from(url):
        print game.price()

appids = ['65710']
for game in games.get_info_for(appids,"CN"):
    print game.price


'''
all_games = games.get_all('US')
for i in all_games:

    print type(i)
