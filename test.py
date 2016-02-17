from steamapiwrapper.Users import SteamUser
from steamapiwrapper.SteamGames import Games

user = SteamUser('76561198053933752', 'FC65FE32E5732FC54BC70256CDA122BB')

games = user.get_games()

#for i in games:
	#print i['appid']

getgame = Games()
g = getgame.get_info_for(['260750','301520'],'CN')

for i in g:
	print i.price