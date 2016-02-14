'''
This model is rewritten in order to be compatable with python 3
Model urllib is replaced by requests. Original doc string below:

A small API wrapper intended to retrieve all available store information
for either a specific appid, or all appids.

Thanks for this SteamDB.info blog post for the idea on the best way to do this:
http://steamdb.info/blog/5/
'''
import json, requests
from SteamBase import SteamAPI

class Games(SteamAPI):
    '''
    Retrieve either all game objects, or specific ones given a list of appids.
    Example:
    # Get information of all games:
    games = Games()
    all_games = games.get_all('US') # Get a generator with all game info

    # Get a generator for just the appids you specify
    some_games = games.get_appids_info([123,1245])
    '''
    def __init__(self, num = 25):
        '''
        num: number of games to query per call. The default 150 should work.
        '''
        self.num = num
        