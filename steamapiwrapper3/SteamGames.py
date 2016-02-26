"""
A small API wrapper intended to retrieve all available store information
for either a specific appid, or all appids.

Thanks for this SteamDB.info blog post for the idea on the best way to do this:
http://steamdb.info/blog/5/

"""

import urllib.request, urllib.parse, urllib.error
import json
from .SteamBase import SteamAPI


class Games(SteamAPI):
    """
    Retrieve either all Game objects, or specific ones given a list of appids.

    Example:
    games = Games()
    all_games = games.get_all('US') # Get a generator with all game info

    # Get a generator for just the appids you specify
    some_games = games.get_appids_info([123,1245])

    """

    def __init__(self, num=None):
        """
        args:
        num -- number of games to query per call. The default 150 should work in most cases.

        """
        self.num = 25 if num is None else num
        self.appids_to_names, self.names_to_appids = None, None

    def _create_url(self, appids, cc):
        """Given a list of appids, creates an API url to retrieve them"""
        appids = ','.join([str(x) for x in appids])
        data = {'appids': appids, 'cc': cc, 'l': 'english', 'v': '1'}
        return "http://store.steampowered.com/api/appdetails/?{}".format(urllib.parse.urlencode(data))

    def _get_urls(self, appids, cc):
        """Returns urls for all of appids"""
        list_of_ids = list(self._chunks(appids,self.num))
        return [self._create_url(x, cc) for x in list_of_ids]

    def get_all(self, cc):
        """
        Gets all games currently in the Steam store (as a generator)
        args:
        cc -- Country Code

        """
        if not (self.appids_to_names and self.names_to_appids):
            self.appids_to_names, self.names_to_appids = self.get_ids_and_names()
        
        urls = []
        for i in list(self.appids_to_names.keys()):
            urls += self._get_urls([i], cc)

        #urls = self._get_urls(self.appids_to_names.keys(), cc)
        for url in urls:
            for game in self._get_games_from(url):
                yield game

    def _get_games_from(self, url):
        """Generator to create the actual game objects"""
        print("Start self._open_url...")
        response = self._open_url(url)
        print("Response get. Loading json of response page...")
        page = json.loads(response.read().decode('utf-8'))
        #n = 0
        for appid in page:
            game = Game(page[appid], appid)
            #print("game object created successfully")
            if game.success:
                game._basicInfo()
                game._priceInfo()
                yield game
            else:
                print("game object created successfully but game.success is not true")

    def get_info_for(self, appids, cc):
        """Given a list of appids, returns their Game objects"""
        urls = self._get_urls(appids, cc)
        for url in urls:
            for game in self._get_games_from(url):
                yield game

    def get_ids_and_names(self):
        """
        Returns two dicts: one mapping appid->game name, and one game name->appid
        TODO: Refactor the code so we don't need to seperate dicts

        """
        # here
        url = self._open_url("http://api.steampowered.com/ISteamApps/GetAppList/v2")
        url_info = json.loads(url.read().decode('utf-8'))
        all_ids = {}
        all_names = {}
        for app in url_info['applist']['apps']:
            all_ids[app['appid']] = app['name']
            all_names[app['name']] = app['appid']
        return all_ids, all_names

    def get_id(self, game_name):
        """Given an appid, returns the game name"""
        if self.appids_to_names is None or self.names_to_appids is None:
            self.appids_to_names, self.names_to_appids = self.get_ids_and_names()
        if game_name in self.names_to_appids:
            return self.names_to_appids[game_name]

    def get_name(self, appid):
        """Given a game name returns its appid"""
        if self.appids_to_names is None or self.names_to_appids is None:
            self.appids_to_names, self.names_to_appids = self.get_ids_and_names()
        if appid in self.appids_to_names:
            return self.appids_to_names[appid]

    def _chunks(self, params, number):
        """Breaks a list into a set of equally sized chunked lists, with remaining entries in last list"""
        for i in range(0, len(params), number):
            yield params[i:i+number]


class Game(SteamAPI):
    """
    The actual Game() object -- really this is just a wrapper around the base
    json response from Steam, that makes it a bit easier to sift through the data.
    Rewritten by Spencer on Feb 22nd 2016.
    """
    def __init__(self, game_json:dict, appid:str):
        """
        Initialize Game object by mark appid, save json url and
        return game_json['data'] for further data extraction
        using other methods below if success state is True.
        """
        self.appid = appid
        self.success = game_json['success']
        if self.success:
            self.store_url = self._store_url(self.appid)
            self.data = game_json['data']
        else:
            print("Game object initialization failed...")


    def _basicInfo(self):
        """
        This method stores basic infomation of a game including 'name', 'type'
        'release_date' and 'platforms' to instance attributes when called.
        """
        self.name = self.data['name'] if 'name' in self.data.values() else None
        self.type = self.data['type'] if 'type' in self.data.values() else None
        self.required_age = self.data['required_age'] if 'required_age' in self.data.values() else None
        self.release_date = self.data['release_date']['date'] if 'date' in self.data['release_date'].values() else None
        self.platforms = self.data['platforms'] if 'platforms' in self.data.values() else None

    def _priceInfo(self):
        """
        This method creates price related attributes when called.
        """
        price_info = self.data['price_overview']
        self.discount_percent = price_info['discount_percent']
        self.final = price_info['final']
        self.currency = price_info['currency']
        self.is_free = self.data['is_free']

    def _imageURLs(self)->dict:
        """
        This method stores image resources of this game, for which
        might be useful for future UI designs.
        # TODO: better organization logic of urls, for now it is 
        just all squashed in a dictionary.
        """
        images = {'screenshot': self.data['screenshots'],
                  'background': self.data['background']}
        return images

    def _description(self, show=False):
        """
        Description text of the game. If show enabled the will print
        out the text. (Mainly for test purpose)
        """
        self.detailed_description = self.data['detailed_description']
        if show:
            print(self.detailed_description)

    def _packageInfo(self):
        """
        This method deal with package and DLC informations.
        """
        # To be done
        raise NotImplementedError


    def _calc_price(self, amount)->float:
        """Prices from the API are represented by cents -- convert to dollars"""
        return float(amount) / 100.0

    def _store_url(self, appid:str)->str:
        return "http://store.steampowered.com/app/{}".format(appid)
    
    # TODO: Some fields of json left unused. Add relevant methods on demand.
    def _unusedFields(self)->list:
        """
        A helper function that remind developer who might be working on
        this project that which fields of the json are not attatched as 
        attributes of Game object.
        """
        unused = []
        for attr in list(self.data.keys()):
            if attr not in list(self.__dict__.keys()):
                unused.append(attr)
        return unused